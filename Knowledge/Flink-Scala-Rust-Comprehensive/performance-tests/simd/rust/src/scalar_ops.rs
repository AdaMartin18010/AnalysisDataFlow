/// 标量过滤操作
pub fn scalar_filter(data: &[i64], threshold: i64) -> Vec<i64> {
    data.iter()
        .filter(|&&x| x > threshold)
        .cloned()
        .collect()
}

/// 带选择率统计的标量过滤
pub fn scalar_filter_with_selectivity(data: &[i64], threshold: i64) -> (Vec<i64>, f64) {
    let result: Vec<i64> = data.iter()
        .filter(|&&x| x > threshold)
        .cloned()
        .collect();
    
    let selectivity = result.len() as f64 / data.len() as f64;
    (result, selectivity)
}

/// 标量求和聚合
pub fn scalar_sum(data: &[i64]) -> i64 {
    data.iter().sum()
}

/// 带条件的标量聚合
pub fn scalar_sum_filtered(data: &[i64], threshold: i64) -> i64 {
    data.iter()
        .filter(|&&x| x > threshold)
        .sum()
}

/// 标量求平均
pub fn scalar_average(data: &[i64]) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    data.iter().sum::<i64>() as f64 / data.len() as f64
}

/// 标量 Min/Max
pub fn scalar_min_max(data: &[i64]) -> (Option<i64>, Option<i64>) {
    if data.is_empty() {
        return (None, None);
    }
    
    let mut min = data[0];
    let mut max = data[0];
    
    for &x in &data[1..] {
        if x < min { min = x; }
        if x > max { max = x; }
    }
    
    (Some(min), Some(max))
}

/// 标量 Map 操作
pub fn scalar_map<F>(data: &[i64], f: F) -> Vec<i64>
where
    F: Fn(i64) -> i64,
{
    data.iter().map(|&x| f(x)).collect()
}

/// 标量复杂表达式: price * 0.908 (模拟货币转换)
pub fn scalar_currency_convert(prices: &[i64]) -> Vec<i64> {
    const MULTIPLIER: i64 = 908;
    const DIVISOR: i64 = 1000;
    prices.iter()
        .map(|&p| (p * MULTIPLIER) / DIVISOR)
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_scalar_filter() {
        let data = vec![1, 5, 10, 3, 8, 2];
        let result = scalar_filter(&data, 4);
        assert_eq!(result, vec![5, 10, 8]);
    }
    
    #[test]
    fn test_scalar_sum() {
        let data = vec![1, 2, 3, 4, 5];
        assert_eq!(scalar_sum(&data), 15);
    }
    
    #[test]
    fn test_scalar_min_max() {
        let data = vec![3, 1, 4, 1, 5, 9, 2, 6];
        let (min, max) = scalar_min_max(&data);
        assert_eq!(min, Some(1));
        assert_eq!(max, Some(9));
    }
    
    #[test]
    fn test_scalar_currency_convert() {
        let prices = vec![1000, 2000, 5000];
        let result = scalar_currency_convert(&prices);
        assert_eq!(result, vec![908, 1816, 4540]);
    }
}
