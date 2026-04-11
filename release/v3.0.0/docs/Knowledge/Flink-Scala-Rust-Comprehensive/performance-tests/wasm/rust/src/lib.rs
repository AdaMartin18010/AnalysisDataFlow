pub mod native;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

// 空函数基准
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn empty() {}

#[cfg(not(feature = "wasm"))]
pub fn empty() {}

// 恒等函数
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn identity(x: i64) -> i64 {
    x
}

#[cfg(not(feature = "wasm"))]
pub fn identity(x: i64) -> i64 {
    x
}

// 简单加法
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

#[cfg(not(feature = "wasm"))]
pub fn add(a: i64, b: i64) -> i64 {
    a + b
}

// 过滤条件
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn filter_gt(x: i64, threshold: i64) -> bool {
    x > threshold
}

#[cfg(not(feature = "wasm"))]
pub fn filter_gt(x: i64, threshold: i64) -> bool {
    x > threshold
}

// 数组求和
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn sum_array(ptr: *const i64, len: usize) -> i64 {
    let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
    slice.iter().sum()
}

#[cfg(not(feature = "wasm"))]
pub fn sum_array(arr: &[i64]) -> i64 {
    arr.iter().sum()
}

// 数组映射 - 货币转换
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn currency_convert(ptr: *const i64, len: usize) -> *mut i64 {
    let input = unsafe { std::slice::from_raw_parts(ptr, len) };
    let result: Vec<i64> = input.iter().map(|&p| (p as f64 * 0.908) as i64).collect();
    let mut boxed = result.into_boxed_slice();
    let ptr = boxed.as_mut_ptr();
    std::mem::forget(boxed);
    ptr
}

#[cfg(not(feature = "wasm"))]
pub fn currency_convert(prices: &[i64]) -> Vec<i64> {
    prices.iter().map(|&p| (p as f64 * 0.908) as i64).collect()
}

// 斐波那契数列 (递归)
#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn fibonacci(n: i32) -> i64 {
    if n <= 1 {
        n as i64
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

#[cfg(not(feature = "wasm"))]
pub fn fibonacci(n: i32) -> i64 {
    if n <= 1 {
        n as i64
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

#[cfg(feature = "wasm")]
mod wasm_transaction {
    use wasm_bindgen::prelude::*;
    use serde::{Serialize, Deserialize};
    
    #[derive(Serialize, Deserialize)]
    pub struct Transaction {
        pub id: i64,
        pub amount: f64,
        pub currency: String,
        pub timestamp: i64,
    }
    
    #[derive(Serialize)]
    struct TaxResult {
        id: i64,
        tax_amount: f64,
        total: f64,
    }
    
    #[wasm_bindgen]
    pub fn calculate_tax(json_input: &str) -> String {
        let tx: Transaction = serde_json::from_str(json_input).unwrap();
        let tax_rate = match tx.currency.as_str() {
            "USD" => 0.08,
            "EUR" => 0.19,
            "GBP" => 0.20,
            _ => 0.10,
        };
        let tax = tx.amount * tax_rate;
        
        let result = TaxResult {
            id: tx.id,
            tax_amount: tax,
            total: tx.amount + tax,
        };
        
        serde_json::to_string(&result).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_identity() {
        assert_eq!(identity(42), 42);
    }
    
    #[test]
    fn test_add() {
        assert_eq!(add(10, 20), 30);
    }
    
    #[test]
    fn test_filter_gt() {
        assert!(filter_gt(10, 5));
        assert!(!filter_gt(3, 5));
    }
    
    #[test]
    fn test_sum_array() {
        let data = vec![1, 2, 3, 4, 5];
        assert_eq!(sum_array(&data), 15);
    }
    
    #[test]
    fn test_fibonacci() {
        assert_eq!(fibonacci(0), 0);
        assert_eq!(fibonacci(1), 1);
        assert_eq!(fibonacci(10), 55);
    }
}
