// WASMI 运行时集成 - 用于测试 WASM 性能
use wasmi::{Engine, Linker, Module, Store, Instance, Value, Func};

pub struct WasmRuntime {
    store: Store<()>,
    instance: Instance,
}

impl WasmRuntime {
    pub fn new(wasm_bytes: &[u8]) -> Self {
        let engine = Engine::default();
        let module = Module::new(&engine, wasm_bytes).unwrap();
        
        let linker = Linker::new(&engine);
        let mut store = Store::new(&engine, ());
        let instance = linker.instantiate(&mut store, &module).unwrap().start(&mut store).unwrap();
        
        Self { store, instance }
    }
    
    pub fn call_empty(&mut self) {
        let empty_fn = self.instance.get_export(&self.store, "empty")
            .and_then(|e| e.into_func())
            .unwrap();
        empty_fn.call(&mut self.store, &[], &mut []).unwrap();
    }
    
    pub fn call_identity(&mut self, x: i64) -> i64 {
        let identity_fn = self.instance.get_export(&self.store, "identity")
            .and_then(|e| e.into_func())
            .unwrap();
        let mut result = [Value::I64(0)];
        identity_fn.call(&mut self.store, &[Value::I64(x)], &mut result).unwrap();
        result[0].i64().unwrap()
    }
    
    pub fn call_add(&mut self, a: i64, b: i64) -> i64 {
        let add_fn = self.instance.get_export(&self.store, "add")
            .and_then(|e| e.into_func())
            .unwrap();
        let mut result = [Value::I64(0)];
        add_fn.call(&mut self.store, &[Value::I64(a), Value::I64(b)], &mut result).unwrap();
        result[0].i64().unwrap()
    }
    
    pub fn call_fibonacci(&mut self, n: i32) -> i64 {
        let fib_fn = self.instance.get_export(&self.store, "fibonacci")
            .and_then(|e| e.into_func())
            .unwrap();
        let mut result = [Value::I64(0)];
        fib_fn.call(&mut self.store, &[Value::I32(n)], &mut result).unwrap();
        result[0].i64().unwrap()
    }
    
    pub fn call_sum_array(&mut self, arr: &[i64]) -> i64 {
        let sum_fn = self.instance.get_export(&self.store, "sum_array")
            .and_then(|e| e.into_func())
            .unwrap();
        
        // 获取内存并写入数据
        let memory = self.instance.get_export(&self.store, "memory")
            .and_then(|e| e.into_memory())
            .unwrap();
        
        // 写入数组数据
        for (i, &value) in arr.iter().enumerate() {
            let bytes = value.to_le_bytes();
            memory.write(&mut self.store, i * 8, &bytes).unwrap();
        }
        
        let mut result = [Value::I64(0)];
        sum_fn.call(&mut self.store, &[Value::I32(0), Value::I32(arr.len() as i32)], &mut result).unwrap();
        result[0].i64().unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    // 注意: 这里需要编译好的 WASM 文件
    // 测试需要 wasm 文件存在
    
    #[test]
    #[ignore] // 需要 WASM 文件
    fn test_wasm_identity() {
        let wasm_bytes = include_bytes!("../target/wasm32-unknown-unknown/release/wasm_udf.wasm");
        let mut runtime = WasmRuntime::new(wasm_bytes);
        assert_eq!(runtime.call_identity(42), 42);
    }
}
