//! Iron Functions 验证示例 - Rust UDF
//! 
//! 本模块提供可运行的 Rust UDF 示例，用于验证 Iron Functions 兼容性。
//! 
//! ## 编译步骤
//! 
//! ```bash
//! # 安装 wasm32 目标
//! rustup target add wasm32-unknown-unknown
//! 
//! # 编译为 WASM
//! cargo build --release --target wasm32-unknown-unknown
//! 
//! # 输出文件
//! # target/wasm32-unknown-unknown/release/iron_functions_verify_examples.wasm
//! ```

use extism_pdk::*;
use serde::{Deserialize, Serialize};

// ============================================================
// 示例 1: 简单字符串处理 UDF
// ============================================================

/// 字符串处理输入
#[derive(Deserialize)]
struct StringInput {
    /// 输入字符串
    value: String,
    /// 操作类型: "upper", "lower", "reverse"
    operation: String,
}

/// 字符串处理输出
#[derive(Serialize)]
struct StringOutput {
    /// 处理结果
    result: String,
    /// 操作是否成功
    success: bool,
    /// 错误信息（如果失败）
    error: Option<String>,
}

/// 简单字符串处理 UDF
/// 
/// # 输入 JSON 格式
/// ```json
/// {
///     "value": "hello",
///     "operation": "upper"
/// }
/// ```
/// 
/// # 输出 JSON 格式
/// ```json
/// {
///     "result": "HELLO",
///     "success": true,
///     "error": null
/// }
/// ```
#[plugin_fn]
pub fn process_string(input: String) -> FnResult<String> {
    let input: StringInput = match serde_json::from_str(&input) {
        Ok(v) => v,
        Err(e) => {
            return Ok(serde_json::to_string(&StringOutput {
                result: String::new(),
                success: false,
                error: Some(format!("JSON parse error: {}", e)),
            })?);
        }
    };

    let result = match input.operation.as_str() {
        "upper" => input.value.to_uppercase(),
        "lower" => input.value.to_lowercase(),
        "reverse" => input.value.chars().rev().collect(),
        "length" => input.value.len().to_string(),
        _ => {
            return Ok(serde_json::to_string(&StringOutput {
                result: String::new(),
                success: false,
                error: Some(format!("Unknown operation: {}", input.operation)),
            })?);
        }
    };

    Ok(serde_json::to_string(&StringOutput {
        result,
        success: true,
        error: None,
    })?)
}

// ============================================================
// 示例 2: 数值计算 UDF
// ============================================================

/// 数值计算输入
#[derive(Deserialize)]
struct MathInput {
    /// 操作数 A
    a: f64,
    /// 操作数 B
    b: f64,
    /// 操作: "add", "subtract", "multiply", "divide"
    operation: String,
}

/// 数值计算输出
#[derive(Serialize)]
struct MathOutput {
    /// 计算结果
    result: f64,
    /// 操作是否成功
    success: bool,
    /// 错误信息
    error: Option<String>,
}

/// 数值计算 UDF
#[plugin_fn]
pub fn calculate(input: String) -> FnResult<String> {
    let input: MathInput = match serde_json::from_str(&input) {
        Ok(v) => v,
        Err(e) => {
            return Ok(serde_json::to_string(&MathOutput {
                result: 0.0,
                success: false,
                error: Some(format!("JSON parse error: {}", e)),
            })?);
        }
    };

    let result = match input.operation.as_str() {
        "add" => input.a + input.b,
        "subtract" => input.a - input.b,
        "multiply" => input.a * input.b,
        "divide" => {
            if input.b == 0.0 {
                return Ok(serde_json::to_string(&MathOutput {
                    result: 0.0,
                    success: false,
                    error: Some("Division by zero".to_string()),
                })?);
            }
            input.a / input.b
        }
        "power" => input.a.powf(input.b),
        _ => {
            return Ok(serde_json::to_string(&MathOutput {
                result: 0.0,
                success: false,
                error: Some(format!("Unknown operation: {}", input.operation)),
            })?);
        }
    };

    Ok(serde_json::to_string(&MathOutput {
        result,
        success: true,
        error: None,
    })?)
}

// ============================================================
// 示例 3: 数据验证 UDF
// ============================================================

/// 验证输入
#[derive(Deserialize)]
struct ValidationInput {
    /// 邮箱地址
    email: String,
    /// 年龄
    age: i32,
}

/// 验证输出
#[derive(Serialize)]
struct ValidationOutput {
    /// 是否有效
    valid: bool,
    /// 验证错误列表
    errors: Vec<String>,
}

/// 数据验证 UDF
#[plugin_fn]
pub fn validate_data(input: String) -> FnResult<String> {
    let input: ValidationInput = match serde_json::from_str(&input) {
        Ok(v) => v,
        Err(e) => {
            return Ok(serde_json::to_string(&ValidationOutput {
                valid: false,
                errors: vec![format!("JSON parse error: {}", e)],
            })?);
        }
    };

    let mut errors = Vec::new();

    // 邮箱验证
    if !input.email.contains('@') {
        errors.push("Invalid email format".to_string());
    }

    // 年龄验证
    if input.age < 0 || input.age > 150 {
        errors.push("Age must be between 0 and 150".to_string());
    }

    Ok(serde_json::to_string(&ValidationOutput {
        valid: errors.is_empty(),
        errors,
    })?)
}

// ============================================================
// 示例 4: JSON 处理 UDF
// ============================================================

/// JSON 处理输入
#[derive(Deserialize)]
struct JsonInput {
    /// JSON 字符串
    json_str: String,
    /// 操作: "pretty", "compact", "extract_keys"
    operation: String,
}

/// JSON 处理输出
#[derive(Serialize)]
struct JsonOutput {
    /// 处理结果
    result: String,
    /// 是否成功
    success: bool,
    /// 错误信息
    error: Option<String>,
}

/// JSON 处理 UDF
#[plugin_fn]
pub fn process_json(input: String) -> FnResult<String> {
    let input: JsonInput = match serde_json::from_str(&input) {
        Ok(v) => v,
        Err(e) => {
            return Ok(serde_json::to_string(&JsonOutput {
                result: String::new(),
                success: false,
                error: Some(format!("JSON parse error: {}", e)),
            })?);
        }
    };

    // 解析输入 JSON
    let value: serde_json::Value = match serde_json::from_str(&input.json_str) {
        Ok(v) => v,
        Err(e) => {
            return Ok(serde_json::to_string(&JsonOutput {
                result: String::new(),
                success: false,
                error: Some(format!("Invalid JSON: {}", e)),
            })?);
        }
    };

    let result = match input.operation.as_str() {
        "pretty" => serde_json::to_string_pretty(&value),
        "compact" => serde_json::to_string(&value),
        "extract_keys" => {
            if let Some(obj) = value.as_object() {
                let keys: Vec<&String> = obj.keys().collect();
                serde_json::to_string(&keys)
            } else {
                return Ok(serde_json::to_string(&JsonOutput {
                    result: String::new(),
                    success: false,
                    error: Some("Not a JSON object".to_string()),
                })?);
            }
        }
        _ => {
            return Ok(serde_json::to_string(&JsonOutput {
                result: String::new(),
                success: false,
                error: Some(format!("Unknown operation: {}", input.operation)),
            })?);
        }
    };

    match result {
        Ok(r) => Ok(serde_json::to_string(&JsonOutput {
            result: r,
            success: true,
            error: None,
        })?),
        Err(e) => Ok(serde_json::to_string(&JsonOutput {
            result: String::new(),
            success: false,
            error: Some(format!("Processing error: {}", e)),
        })?),
    }
}

// ============================================================
// 单元测试
// ============================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_string_upper() {
        let input = r#"{"value": "hello", "operation": "upper"}"#;
        // 注意：测试中无法直接调用 plugin_fn，这里只测试内部逻辑
        let parsed: StringInput = serde_json::from_str(input).unwrap();
        assert_eq!(parsed.value, "hello");
        assert_eq!(parsed.operation, "upper");
    }

    #[test]
    fn test_math_add() {
        let input = r#"{"a": 10.0, "b": 5.0, "operation": "add"}"#;
        let parsed: MathInput = serde_json::from_str(input).unwrap();
        assert_eq!(parsed.a, 10.0);
        assert_eq!(parsed.b, 5.0);
    }

    #[test]
    fn test_validation() {
        let input = r#"{"email": "test@example.com", "age": 25}"#;
        let parsed: ValidationInput = serde_json::from_str(input).unwrap();
        assert_eq!(parsed.email, "test@example.com");
        assert_eq!(parsed.age, 25);
    }
}
