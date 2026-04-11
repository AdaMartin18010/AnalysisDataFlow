#[cfg(target_arch = "x86_64")]
use std::arch::x86_64::*;

/// AVX2 过滤操作 - 返回匹配元素的索引
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_filter_indices(data: &[i64], threshold: i64) -> Vec<usize> {
    let len = data.len();
    let mut result = Vec::with_capacity(len / 4);
    
    let threshold_vec = _mm256_set1_epi64x(threshold);
    let data_ptr = data.as_ptr();
    
    let chunk_size = 4;
    let chunks = len / chunk_size;
    
    for i in 0..chunks {
        let offset = i * chunk_size;
        let vec = _mm256_loadu_si256(data_ptr.add(offset) as *const __m256i);
        let mask = _mm256_cmpgt_epi64(vec, threshold_vec);
        let mask_bits = _mm256_movemask_pd(_mm256_castsi256_pd(mask));
        
        for j in 0..chunk_size {
            if (mask_bits >> j) & 1 == 1 {
                result.push(offset + j);
            }
        }
    }
    
    let remainder_start = chunks * chunk_size;
    for i in remainder_start..len {
        if data[i] > threshold {
            result.push(i);
        }
    }
    
    result
}

/// AVX2 过滤操作 - 直接返回匹配值
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_filter(data: &[i64], threshold: i64) -> Vec<i64> {
    let indices = avx2_filter_indices(data, threshold);
    indices.iter().map(|&i| data[i]).collect()
}

/// AVX2 求和聚合
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_sum(data: &[i64]) -> i64 {
    let len = data.len();
    let mut sum_vec = _mm256_setzero_si256();
    let data_ptr = data.as_ptr();
    
    let chunk_size = 4;
    let chunks = len / chunk_size;
    
    for i in 0..chunks {
        let vec = _mm256_loadu_si256(data_ptr.add(i * chunk_size) as *const __m256i);
        sum_vec = _mm256_add_epi64(sum_vec, vec);
    }
    
    let sum_array: [i64; 4] = std::mem::transmute(sum_vec);
    let mut total: i64 = sum_array.iter().sum();
    
    let remainder_start = chunks * chunk_size;
    for i in remainder_start..len {
        total += data[i];
    }
    
    total
}

/// AVX2 带掩码的求和（条件聚合）
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_sum_masked(data: &[i64], threshold: i64) -> i64 {
    let len = data.len();
    let mut sum_vec = _mm256_setzero_si256();
    let threshold_vec = _mm256_set1_epi64x(threshold);
    let data_ptr = data.as_ptr();
    
    let chunk_size = 4;
    let chunks = len / chunk_size;
    
    for i in 0..chunks {
        let vec = _mm256_loadu_si256(data_ptr.add(i * chunk_size) as *const __m256i);
        let mask = _mm256_cmpgt_epi64(vec, threshold_vec);
        let masked = _mm256_and_si256(vec, mask);
        sum_vec = _mm256_add_epi64(sum_vec, masked);
    }
    
    let sum_array: [i64; 4] = std::mem::transmute(sum_vec);
    let mut total: i64 = sum_array.iter().sum();
    
    let remainder_start = chunks * chunk_size;
    for i in remainder_start..len {
        if data[i] > threshold {
            total += data[i];
        }
    }
    
    total
}

/// AVX2 Min/Max
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_min_max(data: &[i64]) -> (i64, i64) {
    let len = data.len();
    if len == 0 {
        return (0, 0);
    }
    
    let mut min_vec = _mm256_set1_epi64x(i64::MAX);
    let mut max_vec = _mm256_set1_epi64x(i64::MIN);
    let data_ptr = data.as_ptr();
    
    let chunk_size = 4;
    let chunks = len / chunk_size;
    
    for i in 0..chunks {
        let vec = _mm256_loadu_si256(data_ptr.add(i * chunk_size) as *const __m256i);
        min_vec = _mm256_min_epi64(min_vec, vec);
        max_vec = _mm256_max_epi64(max_vec, vec);
    }
    
    let min_array: [i64; 4] = std::mem::transmute(min_vec);
    let max_array: [i64; 4] = std::mem::transmute(max_vec);
    
    let mut global_min = *min_array.iter().min().unwrap();
    let mut global_max = *max_array.iter().max().unwrap();
    
    let remainder_start = chunks * chunk_size;
    for i in remainder_start..len {
        if data[i] < global_min { global_min = data[i]; }
        if data[i] > global_max { global_max = data[i]; }
    }
    
    (global_min, global_max)
}

/// AVX2 货币转换
#[cfg(target_arch = "x86_64")]
pub unsafe fn avx2_currency_convert(prices: &[i64]) -> Vec<i64> {
    let len = prices.len();
    let mut result = vec![0i64; len];
    
    const MULTIPLIER: i64 = 908;
    const DIVISOR: i64 = 1000;
    
    let mul_vec = _mm256_set1_epi64x(MULTIPLIER);
    let data_ptr = prices.as_ptr();
    let result_ptr = result.as_mut_ptr();
    
    let chunk_size = 4;
    let chunks = len / chunk_size;
    
    for i in 0..chunks {
        let vec = _mm256_loadu_si256(data_ptr.add(i * chunk_size) as *const __m256i);
        let prod = _mm256_mul_epu32(vec, mul_vec);
        let prod_array: [i64; 4] = std::mem::transmute(prod);
        for j in 0..4 {
            result[i * chunk_size + j] = prod_array[j] / DIVISOR;
        }
    }
    
    let remainder_start = chunks * chunk_size;
    for i in remainder_start..len {
        result[i] = (prices[i] * MULTIPLIER) / DIVISOR;
    }
    
    result
}

// 安全包装函数
#[cfg(target_arch = "x86_64")]
pub fn safe_avx2_filter(data: &[i64], threshold: i64) -> Vec<i64> {
    unsafe { avx2_filter(data, threshold) }
}

#[cfg(target_arch = "x86_64")]
pub fn safe_avx2_sum(data: &[i64]) -> i64 {
    unsafe { avx2_sum(data) }
}

#[cfg(target_arch = "x86_64")]
pub fn safe_avx2_min_max(data: &[i64]) -> (i64, i64) {
    unsafe { avx2_min_max(data) }
}

#[cfg(not(target_arch = "x86_64"))]
pub fn safe_avx2_filter(data: &[i64], threshold: i64) -> Vec<i64> {
    crate::scalar_ops::scalar_filter(data, threshold)
}

#[cfg(not(target_arch = "x86_64"))]
pub fn safe_avx2_sum(data: &[i64]) -> i64 {
    crate::scalar_ops::scalar_sum(data)
}

#[cfg(not(target_arch = "x86_64"))]
pub fn safe_avx2_min_max(data: &[i64]) -> (i64, i64) {
    let (min, max) = crate::scalar_ops::scalar_min_max(data);
    (min.unwrap_or(0), max.unwrap_or(0))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::data_generator::{DataGenerator, DataDistribution};
    
    #[test]
    fn test_avx2_filter() {
        let data = vec![1i64, 5, 10, 3, 8, 2, 7, 4];
        let result = safe_avx2_filter(&data, 4);
        assert_eq!(result, vec![5, 10, 8, 7]);
    }
    
    #[test]
    fn test_avx2_sum() {
        let data = vec![1i64, 2, 3, 4, 5, 6, 7, 8];
        assert_eq!(safe_avx2_sum(&data), 36);
    }
    
    #[test]
    fn test_avx2_large_array() {
        let gen = DataGenerator::new(10000);
        let data = gen.generate_i64();
        
        let scalar_sum = crate::scalar_ops::scalar_sum(&data);
        let simd_sum = safe_avx2_sum(&data);
        
        assert_eq!(scalar_sum, simd_sum);
    }
}
