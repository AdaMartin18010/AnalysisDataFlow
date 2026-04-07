// 原生实现，用于性能对比基准

pub fn native_empty() {}

pub fn native_identity(x: i64) -> i64 {
    x
}

pub fn native_add(a: i64, b: i64) -> i64 {
    a + b
}

pub fn native_filter_gt(x: i64, threshold: i64) -> bool {
    x > threshold
}

pub fn native_sum_array(arr: &[i64]) -> i64 {
    arr.iter().sum()
}

pub fn native_currency_convert(prices: &[i64]) -> Vec<i64> {
    prices.iter().map(|&p| (p as f64 * 0.908) as i64).collect()
}

pub fn native_fibonacci(n: i32) -> i64 {
    if n <= 1 {
        n as i64
    } else {
        native_fibonacci(n - 1) + native_fibonacci(n - 2)
    }
}

// 迭代版斐波那契 (更高效)
pub fn native_fibonacci_iter(n: i32) -> i64 {
    if n <= 1 {
        return n as i64;
    }
    
    let mut a = 0i64;
    let mut b = 1i64;
    
    for _ in 2..=n {
        let temp = a + b;
        a = b;
        b = temp;
    }
    
    b
}

// 带缓存的斐波那契
use std::collections::HashMap;
use std::cell::RefCell;

thread_local! {
    static FIB_CACHE: RefCell<HashMap<i32, i64>> = RefCell::new(HashMap::new());
}

pub fn native_fibonacci_memoized(n: i32) -> i64 {
    FIB_CACHE.with(|cache| {
        let mut cache = cache.borrow_mut();
        
        if let Some(&result) = cache.get(&n) {
            return result;
        }
        
        let result = if n <= 1 {
            n as i64
        } else {
            native_fibonacci_memoized(n - 1) + native_fibonacci_memoized(n - 2)
        };
        
        cache.insert(n, result);
        result
    })
}

// 批量操作 - 批处理优化
pub fn native_batch_sum(arrays: &[&[i64]]) -> Vec<i64> {
    arrays.iter().map(|arr| arr.iter().sum()).collect()
}

pub fn native_batch_filter(data: &[i64], threshold: i64) -> Vec<i64> {
    data.iter().filter(|&&x| x > threshold).cloned().collect()
}

// 统计函数
pub fn native_statistics(data: &[i64]) -> (i64, i64, f64) {
    if data.is_empty() {
        return (0, 0, 0.0);
    }
    
    let sum: i64 = data.iter().sum();
    let min = *data.iter().min().unwrap();
    let max = *data.iter().max().unwrap();
    let avg = sum as f64 / data.len() as f64;
    
    (min, max, avg)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_native_identity() {
        assert_eq!(native_identity(42), 42);
    }
    
    #[test]
    fn test_native_fibonacci() {
        assert_eq!(native_fibonacci(10), 55);
        assert_eq!(native_fibonacci_iter(10), 55);
        assert_eq!(native_fibonacci_memoized(10), 55);
    }
    
    #[test]
    fn test_native_statistics() {
        let data = vec![1, 2, 3, 4, 5];
        let (min, max, avg) = native_statistics(&data);
        assert_eq!(min, 1);
        assert_eq!(max, 5);
        assert!((avg - 3.0).abs() < 0.001);
    }
}
