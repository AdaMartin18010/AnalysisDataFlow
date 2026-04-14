---
title: "RisingWave Rust UDF Source Code Deep Dive"
translation_status: ai_translated_reviewed
source_version: v4.1
last_sync: "2026-04-15"
---

# RisingWave Rust UDF Source Code Deep Dive

> **Stage**: Knowledge/Flink-Scala-Rust-Comprehensive | **Prerequisites**: [RisingWave Architecture Analysis] | **Formality Level**: L4

## 1. Project Structure

### 1.1 UDF Module Organization

RisingWave's UDF system adopts a layered architecture, supporting multiple languages and execution modes:

```
src/
├── expr/                      # Expression computation core
│   ├── core/                  # Expression trait definitions
│   ├── impl/src/              # Built-in function implementations
│   └── udf.rs                 # UDF entry point
├── frontend/src/expr/         # Frontend expression parsing
│   └── udf.rs                 # UDF registration and parsing
├── udf/                       # UDF runtime (standalone crate)
│   ├── src/
│   │   ├── lib.rs             # Public interfaces
│   │   ├── external.rs        # External UDF (Python/Java)
│   │   ├── wasm.rs            # WASM UDF runtime
│   │   └── javascript.rs      # JavaScript UDF
│   └── wasm/                  # WASM UDF dedicated implementation
├── arrow-udf/                 # Standalone project (arrow-udf)
│   ├── macros/                # #[function] proc macro
│   ├── wasm/                  # WASM runtime wrapper
│   └── flight/                # Arrow Flight RPC
```

### 1.2 Arrow-UDF Standalone Project

RisingWave extracted the UDF implementation into a standalone project arrow-udf for easier reuse:

```
arrow-udf/
├── arrow-udf-macros/          # Proc macro implementation
│   └── src/
│       ├── lib.rs             # #[function] macro
│       ├── gen.rs             # Code generation
│       └── sig.rs             # Signature parsing
├── arrow-udf-wasm/            # WASM runtime
│   └── src/
│       ├── lib.rs             # Runtime wrapper
│       ├── builder.rs         # WASM module builder
│       └── runtime.rs         # wasmtime wrapper
└── arrow-udf-flight/          # Arrow Flight RPC
    └── src/
        ├── client.rs          # Flight client
        └── server.rs          # Flight server
```

---

## 2. Core Module Analysis

### 2.1 UDF Registration and Parsing (src/expr/)

**Path**: `src/expr/core/src/expr/`

**Responsibilities**: UDF metadata management, type checking, and registration.

**Key trait/struct**:

```rust
// src/expr/core/src/expr/udf.rs
pub struct UdfExpression {
    pub function_name: String,
    pub arg_exprs: Vec<BoxedExpression>,
    pub return_type: DataType,
    pub udf_executor: Arc<dyn UdfExecutor>,
    pub span: Span,
}

#[async_trait]
pub trait UdfExecutor: Send + Sync {
    async fn eval(&self, input: &RecordBatch) -> Result<RecordBatch>;
    fn schema(&self) -> Schema;
}

// src/frontend/src/expr/udf.rs
pub struct UdfRegistry {
    functions: HashMap<FunctionId, UdfMetadata>,
    wasm_runtimes: Arc<WasmRuntimePool>,
}
```

**Source Analysis - UDF Registration Flow**:

```rust
// src/frontend/src/handler/create_function.rs
pub async fn handle_create_function(
    handler_args: HandlerArgs,
    stmt: CreateFunctionStatement,
) -> Result<RwPgResponse> {
    let metadata = parse_function_statement(&stmt)?;

    // Language-specific processing
    let compiled_body = match metadata.language {
        UdfLanguage::Rust => {
            compile_rust_to_wasm(&metadata.body.code).await?
        }
        UdfLanguage::JavaScript => {
            validate_javascript(&metadata.body.code)?;
            metadata.body.code.into_bytes()
        }
        _ => metadata.body.code.into_bytes(),
    };

    // Register to Meta Service
    handler_args.session.env()
        .meta_client()
        .create_function(function_catalog)
        .await?;

    Ok(RwPgResponse::empty_result(
        StatementType::CREATE_FUNCTION,
    ))
}
```

### 2.2 WASM UDF Runtime (arrow-udf-wasm)

**Path**: `arrow-udf/arrow-udf-wasm/src/`

**Responsibilities**: WebAssembly UDF execution engine based on wasmtime, providing isolation and security.

**Key trait/struct**:

```rust
// arrow-udf-wasm/src/lib.rs
pub struct WasmRuntime {
    engine: Engine,
    module: Module,
    linker: Linker<StoreData>,
}

pub struct WasmInstance {
    store: Store<StoreData>,
    instance: Instance,
    functions: HashMap<String, WasmFunction>,
}

pub struct WasmFunction {
    name: String,
    input_schema: Schema,
    output_schema: Schema,
    caller: TypedFunc<(i32, i32, i32, i32), i32>,
}
```

**Source Analysis - WASM Module Loading and Execution**:

```rust
// arrow-udf-wasm/src/runtime.rs
impl WasmRuntime {
    /// Create runtime from WASM bytecode
    pub fn new(wasm_bytes: &[u8]) -> Result<Self> {
        // 1. Create wasmtime engine
        let mut config = Config::new();
        config.wasm_backtrace_details(WasmBacktraceDetails::Enable);
        config.async_support(false);

        let engine = Engine::new(&config)?;

        // 2. Compile WASM module
        let module = Module::new(&engine, wasm_bytes)?;

        // 3. Create Linker and add host functions
        let mut linker = Linker::new(&engine);
        Self::link_host_functions(&mut linker)?;

        Ok(WasmRuntime {
            engine,
            module,
            linker,
        })
    }

    /// Instantiate WASM module
    pub fn instantiate(&self) -> Result<WasmInstance> {
        // 1. Create Store
        let mut store = Store::new(
            &self.engine,
            StoreData {
                memory: None,
                arrow_buffer: Vec::new(),
            },
        );

        // 2. Instantiate module
        let instance = self.linker.instantiate(&mut store, &self.module)?;

        // 3. Get memory export
        let memory = instance
            .get_memory(&mut store, "memory")
            .ok_or(Error::MissingMemory)?;
        store.data_mut().memory = Some(memory);

        // 4. Scan symbol table for all UDFs
        let mut functions = HashMap::new();
        for export in instance.exports(&mut store) {
            if let Some(func) = export.into_func() {
                let name = export.name().to_string();

                // Parse function signature (extracted from symbol name)
                if let Some(sig) = parse_function_signature(&name) {
                    let typed_func = func.typed::<(i32, i32, i32, i32), i32>(&store)?;
                    functions.insert(
                        sig.name.clone(),
                        WasmFunction {
                            name: sig.name,
                            input_schema: sig.input_schema,
                            output_schema: sig.output_schema,
                            caller: typed_func,
                        },
                    );
                }
            }
        }

        Ok(WasmInstance {
            store,
            instance,
            functions,
        })
    }
}

impl WasmInstance {
    /// Execute WASM UDF
    pub fn call(
        &mut self,
        function_name: &str,
        input: RecordBatch,
    ) -> Result<RecordBatch> {
        let func = self.functions.get(function_name)
            .ok_or(Error::FunctionNotFound)?;

        // 1. Serialize input to Arrow IPC format
        let input_bytes = serialize_record_batch(&input)?;

        // 2. Allocate WASM memory
        let input_ptr = self.malloc(input_bytes.len() as i32)?;

        // 3. Write input data to WASM memory
        self.store.data().memory
            .unwrap()
            .write(&mut self.store, input_ptr as usize, &input_bytes)?;

        // 4. Call WASM function
        let output_ptr = func.caller.call(
            &mut self.store,
            (input_ptr, input_bytes.len() as i32, 0, 0),
        )?;

        // 5. Read output data
        let output_len = self.read_output_len(output_ptr)?;
        let output_bytes = self.read_bytes(output_ptr, output_len)?;

        // 6. Deserialize to RecordBatch
        let output = deserialize_record_batch(&output_bytes)?;

        // 7. Free WASM memory
        self.free(input_ptr)?;
        self.free(output_ptr)?;

        Ok(output)
    }

    fn malloc(&mut self, size: i32) -> Result<i32> {
        let malloc_func = self.instance
            .get_typed_func::<i32, i32>(&mut self.store, "malloc")?;
        Ok(malloc_func.call(&mut self.store, size)?)
    }

    fn free(&mut self, ptr: i32) -> Result<()> {
        let free_func = self.instance
            .get_typed_func::<i32, ()>(&mut self.store, "free")?;
        free_func.call(&mut self.store, ptr)?;
        Ok(())
    }
}
```

**WASM UDF Call Flow Diagram**:

```mermaid
sequenceDiagram
    participant RW as RisingWave
    participant WR as WasmRuntime
    participant WT as wasmtime
    participant WM as WASM Module

    RW->>WR: call(function_name, input_batch)
    WR->>WR: serialize to Arrow IPC
    WR->>WT: malloc(size)
    WT->>WM: allocate memory
    WT-->>WR: ptr
    WR->>WT: write_memory(ptr, data)
    WR->>WT: call_udf(ptr, len)
    WT->>WM: execute function
    WM->>WM: process arrow data
    WM-->>WT: return output_ptr
    WT-->>WR: output_ptr
    WR->>WT: read_memory(output_ptr)
    WT-->>WR: output_bytes
    WR->>WR: deserialize RecordBatch
    WR->>WT: free(ptr)
    WR->>WT: free(output_ptr)
    WR-->>RW: RecordBatch
```

### 2.3 Dynamic Library Loading (UDF FFI)

**Path**: `src/expr/udfs/src/native.rs`

**Responsibilities**: Supports loading native UDFs via dynamic libraries (.so/.dll) for scenarios requiring extreme performance.

**Key trait/struct**:

```rust
// src/expr/udfs/src/native.rs
pub struct NativeUdfLibrary {
    library: Library,
    functions: HashMap<String, NativeFunction>,
}

pub struct NativeFunction {
    name: String,
    func_ptr: Symbol<'static, extern "C" fn(
        *const u8,  // input arrow data
        usize,      // input len
        *mut u8,    // output buffer
        usize,      // output capacity
    ) -> i32>,
    input_schema: Schema,
    output_schema: Schema,
}

unsafe impl Send for NativeUdfLibrary {}
unsafe impl Sync for NativeUdfLibrary {}
```

**Source Analysis - Dynamic Library Loading**:

```rust
// src/expr/udfs/src/native.rs
impl NativeUdfLibrary {
    /// Load dynamic library
    pub unsafe fn load(path: &str) -> Result<Self> {
        // 1. Open dynamic library
        let library = Library::new(path)?;

        // 2. Get exported function table
        let func_table: Symbol<extern "C" fn() -> *const UdfDescriptor> =
            library.get(b"udf_descriptor_table\0")?;

        let descriptors = func_table();

        // 3. Iterate and register functions
        let mut functions = HashMap::new();
        let mut ptr = descriptors;
        while !(*ptr).name.is_null() {
            let name = CStr::from_ptr((*ptr).name).to_string_lossy();
            let func_ptr: Symbol<_> = library.get(
                format!("{}\0", name).as_bytes()
            )?;

            functions.insert(
                name.to_string(),
                NativeFunction {
                    name: name.to_string(),
                    func_ptr: std::mem::transmute(func_ptr),
                    input_schema: parse_schema(&(*ptr).input_schema)?,
                    output_schema: parse_schema(&(*ptr).output_schema)?,
                },
            );
            ptr = ptr.add(1);
        }

        Ok(NativeUdfLibrary {
            library,
            functions,
        })
    }

    /// Execute native UDF
    pub fn call(
        &self,
        name: &str,
        input: &RecordBatch,
    ) -> Result<RecordBatch> {
        let func = self.functions.get(name)
            .ok_or(Error::FunctionNotFound)?;

        // 1. Serialize input
        let input_bytes = serialize_record_batch(input)?;

        // 2. Prepare output buffer
        let mut output_buffer = vec![0u8; 65536];

        // 3. Call native function
        let result_len = (func.func_ptr)(
            input_bytes.as_ptr(),
            input_bytes.len(),
            output_buffer.as_mut_ptr(),
            output_buffer.capacity(),
        );

        if result_len < 0 {
            return Err(Error::UdfExecutionError(result_len));
        }

        // 4. Deserialize output
        output_buffer.truncate(result_len as usize);
        let output = deserialize_record_batch(&output_buffer)?;

        Ok(output)
    }
}
```

### 2.4 Memory Safety and Isolation Mechanisms

**Path**: `arrow-udf-wasm/src/sandbox.rs`

**Responsibilities**: The WASM sandbox provides memory isolation, execution time limits, and resource quota control.

**Source Analysis - Resource Limit Configuration**:

```rust
// arrow-udf-wasm/src/sandbox.rs
pub struct SandboxConfig {
    /// Maximum memory limit (MB)
    pub max_memory_mb: u32,
    /// Maximum execution time (ms)
    pub max_execution_time_ms: u32,
    /// Whether filesystem access is allowed
    pub allow_fs: bool,
    /// Whether network access is allowed
    pub allow_network: bool,
    /// Maximum output data size (MB)
    pub max_output_size_mb: u32,
}

impl Default for SandboxConfig {
    fn default() -> Self {
        SandboxConfig {
            max_memory_mb: 128,
            max_execution_time_ms: 5000,
            allow_fs: false,
            allow_network: false,
            max_output_size_mb: 64,
        }
    }
}

pub fn create_sandboxed_config(config: &SandboxConfig) -> Config {
    let mut wasm_config = Config::new();

    // 1. Limit linear memory size
    wasm_config.static_memory_maximum_size(
        (config.max_memory_mb as u64) * 1024 * 1024
    );

    // 2. Disable SIMD (potential security risk)
    wasm_config.wasm_simd(false);

    // 3. Enable WebAssembly multi-memory (isolation)
    wasm_config.wasm_multi_memory(true);

    // 4. Configure fuel metering (prevent infinite loops)
    wasm_config.consume_fuel(true);

    wasm_config
}

// arrow-udf-wasm/src/runtime.rs
impl WasmInstance {
    /// Secure execution with timeout
    pub fn call_with_timeout(
        &mut self,
        func_name: &str,
        input: RecordBatch,
        timeout: Duration,
    ) -> Result<RecordBatch> {
        // 1. Set fuel quota
        self.store.add_fuel(10_000_000_000)?;

        // 2. Use signal for timeout
        let result = catch_unwind(AssertUnwindSafe(|| {
            self.call(func_name, input)
        }));

        match result {
            Ok(Ok(batch)) => Ok(batch),
            Ok(Err(e)) => Err(e),
            Err(_) => Err(Error::UdfPanicked),
        }
    }
}
```

---

## 3. Data Flow Analysis

### 3.1 UDF Execution Pipeline

```mermaid
graph TB
    subgraph "Frontend"
        SQL["SQL: SELECT my_udf(col) FROM t"]
        Parser["SQL Parser"]
        Binder["Binder<br/>(Type Checking)"]
        Planner["Planner"]
    end

    subgraph "Compute Node"
        Executor["Project Executor"]
        UdfExpr["UdfExpression"]

        subgraph "UDF Runtime"
            WasmRT["WasmRuntime"]
            WasmInst["WasmInstance"]
            Wasmtime["wasmtime"]
        end

        ArrowConv["Arrow -> Native"]
        ArrowConv2["Native -> Arrow"]
    end

    subgraph "WASM Module"
        UserFunc["User-defined Function"]
    end

    SQL --> Parser
    Parser --> Binder
    Binder --> Planner
    Planner --> Executor
    Executor --> UdfExpr
    UdfExpr --> WasmRT
    WasmRT --> WasmInst
    WasmInst --> ArrowConv
    ArrowConv --> Wasmtime
    Wasmtime --> UserFunc
    UserFunc --> Wasmtime
    Wasmtime --> ArrowConv2
    ArrowConv2 --> WasmInst
    WasmInst --> UdfExpr
    UdfExpr --> Executor
```

### 3.2 Arrow Data Conversion Flow

```rust
// arrow-udf-wasm/src/arrow_conv.rs
use arrow::ipc::writer::StreamWriter;
use arrow::ipc::reader::StreamReader;

/// Serialize RecordBatch to Arrow IPC format
pub fn serialize_record_batch(batch: &RecordBatch) -> Result<Vec<u8>> {
    let mut buffer = Vec::new();
    {
        let mut writer = StreamWriter::try_new(&mut buffer, batch.schema())?;
        writer.write(batch)?;
        writer.finish()?;
    }
    Ok(buffer)
}

/// Deserialize RecordBatch from Arrow IPC
pub fn deserialize_record_batch(bytes: &[u8]) -> Result<RecordBatch> {
    let reader = StreamReader::try_new(bytes)?;
    let mut batches = Vec::new();

    for batch in reader {
        batches.push(batch?);
    }

    // Merge multiple batches
    concat_batches(&batches)
}

// arrow-udf-macros/src/gen.rs
/// Generate Arrow type conversion code
fn generate_type_conversion(field: &Field) -> TokenStream {
    match field.data_type() {
        DataType::Int32 => quote! { arrow::datatypes::Int32Type },
        DataType::Int64 => quote! { arrow::datatypes::Int64Type },
        DataType::Float32 => quote! { arrow::datatypes::Float32Type },
        DataType::Float64 => quote! { arrow::datatypes::Float64Type },
        DataType::Utf8 => quote! { arrow::datatypes::Utf8Type },
        DataType::Struct(fields) => generate_struct_type(fields),
        _ => unimplemented!(),
    }
}
```

---

## 4. Key Algorithms

### 4.1 #[function] Proc Macro Implementation

**Pseudocode**:

```
Algorithm: Function Attribute Macro

Input: Function definition with #[function("name(args) -> ret")]
Output: Generated FFI adapter code

1. Parse function signature
   - Extract function name
   - Parse parameter types (SQL types)
   - Parse return type

2. Generate Arrow type mapping
   - Map SQL types to Arrow DataType
   - Generate Schema definition

3. Generate FFI entry function
   - Define C-ABI interface function
   - Implement Arrow IPC serialization/deserialization
   - Wrap user function call

4. Register in symbol table
   - Generate init function
   - Register function metadata
```

**Rust Implementation** (arrow-udf-macros/src/lib.rs):

```rust
/// #[function] proc macro
#[proc_macro_attribute]
pub function(attr: TokenStream, item: TokenStream) -> TokenStream {
    // 1. Parse attribute
    let sig = parse_function_signature(attr);

    // 2. Parse function definition
    let input_fn = parse::<ItemFn>(item).expect("expected function");
    let fn_name = &input_fn.sig.ident;

    // 3. Generate FFI function name (includes type info for runtime parsing)
    let ffi_name = format!(
        "arrow_udf_{}_{}",
        sig.name,
        sig.signature_hash()
    );
    let ffi_ident = Ident::new(&ffi_name, Span::call_site());

    // 4. Generate type conversion code
    let arg_conversions: Vec<_> = sig.args.iter().enumerate()
        .map(|(i, ty)| generate_arg_conversion(i, ty))
        .collect();

    let ret_conversion = generate_return_conversion(&sig.ret);

    // 5. Generate complete code
    let expanded = quote! {
        // Original user function
        #input_fn

        // FFI entry function
        #[no_mangle]
        pub extern "C" fn #ffi_ident(
            input_ptr: *const u8,
            input_len: usize,
            output_ptr: *mut u8,
            output_capacity: usize,
        ) -> i32 {
            // Deserialize input
            let input_batch = unsafe {
                deserialize_from_ptr(input_ptr, input_len)
            };

            // Extract parameter columns
            let columns: Vec<_> = (0..input_batch.num_columns())
                .map(|i| input_batch.column(i))
                .collect();

            // Call user function
            #(#arg_conversions)*
            let result = #fn_name(#(arg#i),*);

            // Serialize output
            #ret_conversion

            output_len as i32
        }

        // Register function metadata
        #[no_mangle]
        pub static ARROW_UDF_METADATA: &[u8] =
            include_bytes!(concat!(env!("OUT_DIR"), "/udf_metadata.bin"));
    };

    expanded.into()
}
```

### 4.2 WASM Module Optimization Strategy

```rust
// arrow-udf-wasm/src/optimize.rs

/// WASM module optimization pipeline
pub fn optimize_wasm(module: &mut [u8]) -> Result<()> {
    // 1. Use wasm-strip to remove debug symbols
    wasm_strip(module)?;

    // 2. Use wasm-opt for binary optimization
    wasm_opt(module, OptimizationLevel::Size)?;

    // 3. Compression (gzip/brotli)
    compress(module)?;

    Ok(())
}

/// Remove unused exports
pub fn prune_exports(module: &mut walrus::Module) {
    // Only keep necessary exported functions
    let necessary_exports: HashSet<&str> = [
        "arrow_udf_",
        "malloc",
        "free",
        "memory",
    ].into();

    module.exports.retain(|export| {
        necessary_exports.iter().any(|&prefix| {
            export.name.starts_with(prefix)
        })
    });
}

/// Inline small functions
pub fn inline_small_functions(module: &mut walrus::Module, threshold: usize) {
    for func in module.functions.iter_mut() {
        if func.size() < threshold {
            // Inline optimization
            inline_function(module, func.id());
        }
    }
}
```

---

## 5. Comparison with Flink

| Dimension | RisingWave UDF | Apache Flink UDF |
|-----------|----------------|------------------|
| **Supported Languages** | SQL, Python, Java, Rust, JavaScript | Java, Scala, Python |
| **Rust UDF** | WASM (built-in) | Not supported |
| **Python UDF** | External process (Arrow Flight) | External process (Py4J) |
| **Execution Mode** | Embedded WASM / External process | JVM Embedded / External RPC |
| **Isolation** | WASM sandbox / Process isolation | JVM isolation / Process isolation |
| **Performance** | Near-native (WASM JIT) | JVM JIT optimized |
| **Memory Safety** | WASM memory isolation | JVM GC |
| **Deployment** | SQL-embedded / External service | JAR package / External service |

### 5.1 UDF Architecture Comparison

```mermaid
graph TB
    subgraph "RisingWave UDF"
        RW_SQL["CREATE FUNCTION ... LANGUAGE rust"]
        RW_Compile["Frontend compiles to WASM"]
        RW_Catalog["Catalog storage"]
        RW_Exec["WASM Runtime (wasmtime)"]
        RW_Sandbox["WASM Sandbox"]
    end

    subgraph "Flink UDF"
        FL_SQL["CREATE FUNCTION ... LANGUAGE java"]
        FL_Jar["Upload JAR"]
        FL_ClassLoader["URLClassLoader"]
        FL_JVM["JVM Execution"]
        FL_GC["JVM GC"]
    end
```

### 5.2 Performance Comparison Analysis

| Scenario | RisingWave (WASM) | Flink (JVM) | Note |
|----------|-------------------|-------------|------|
| Simple numeric computation | ~0.9x | 1.0x (baseline) | WASM near-native |
| String processing | ~0.85x | 1.0x | JVM string optimization is better |
| Complex aggregation | ~0.95x | 1.0x | No GC pauses in WASM |
| Cold start latency | ~10ms | ~100ms+ | WASM instantiation is faster |
| Memory isolation | Strong (sandbox) | Medium (JVM) | WASM is safer |

---

## 6. References
