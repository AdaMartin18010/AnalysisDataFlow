use criterion::{black_box, criterion_group, criterion_main, Criterion, Throughput};
use simd_benchmarks::data_generator::DataGenerator;
use simd_benchmarks::scalar_ops;

#[cfg(target_arch = "x86_64")]
use simd_benchmarks::simd_avx2;

fn bench_filter_i64(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    let threshold = 0i64;
    
    let mut group = c.benchmark_group("filter_i64_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    // 标量实现
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_filter(black_box(&data), black_box(threshold)))
    });
    
    // AVX2 实现
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2", |b| {
            b.iter(|| simd_avx2::safe_avx2_filter(black_box(&data), black_box(threshold)))
        });
    }
    
    group.finish();
}

fn bench_filter_with_selectivity(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("filter_selectivity");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    // 不同选择率
    for threshold in [i64::MIN + 100, -1000i64, 0i64, 1000i64] {
        let label = format!("scalar_threshold_{}", threshold);
        group.bench_function(&label, |b| {
            b.iter(|| scalar_ops::scalar_filter(black_box(&data), black_box(threshold)))
        });
        
        #[cfg(target_arch = "x86_64")]
        {
            let label = format!("avx2_threshold_{}", threshold);
            group.bench_function(&label, |b| {
                b.iter(|| simd_avx2::safe_avx2_filter(black_box(&data), black_box(threshold)))
            });
        }
    }
    
    group.finish();
}

fn bench_filter_different_sizes(c: &mut Criterion) {
    let mut group = c.benchmark_group("filter_sizes");
    
    for size in [10_000, 100_000, 1_000_000, 10_000_000] {
        let data = DataGenerator::new(size).generate_i64();
        group.throughput(Throughput::Elements(size as u64));
        
        group.bench_function(format!("scalar_{}", size), |b| {
            b.iter(|| scalar_ops::scalar_filter(black_box(&data), black_box(0i64)))
        });
        
        #[cfg(target_arch = "x86_64")]
        {
            group.bench_function(format!("avx2_{}", size), |b| {
                b.iter(|| simd_avx2::safe_avx2_filter(black_box(&data), black_box(0i64)))
            });
        }
    }
    
    group.finish();
}

criterion_group!(
    benches, 
    bench_filter_i64, 
    bench_filter_with_selectivity,
    bench_filter_different_sizes
);
criterion_main!(benches);
