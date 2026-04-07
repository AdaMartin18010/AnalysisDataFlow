use criterion::{black_box, criterion_group, criterion_main, Criterion, Throughput};
use simd_benchmarks::data_generator::DataGenerator;
use simd_benchmarks::scalar_ops;

#[cfg(target_arch = "x86_64")]
use simd_benchmarks::simd_avx2;

fn bench_sum_i64(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("sum_i64_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_sum(black_box(&data)))
    });
    
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2", |b| {
            b.iter(|| simd_avx2::safe_avx2_sum(black_box(&data)))
        });
    }
    
    group.finish();
}

fn bench_sum_filtered(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    let threshold = 0i64;
    
    let mut group = c.benchmark_group("sum_filtered_i64_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_sum_filtered(black_box(&data), black_box(threshold)))
    });
    
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2_masked", |b| {
            b.iter(|| unsafe {
                simd_avx2::avx2_sum_masked(black_box(&data), black_box(threshold))
            })
        });
    }
    
    group.finish();
}

fn bench_min_max(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("min_max_i64_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_min_max(black_box(&data)))
    });
    
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2", |b| {
            b.iter(|| simd_avx2::safe_avx2_min_max(black_box(&data)))
        });
    }
    
    group.finish();
}

fn bench_average(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("average_i64_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_average(black_box(&data)))
    });
    
    // SIMD average = SIMD sum / count
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2", |b| {
            b.iter(|| {
                let sum = simd_avx2::safe_avx2_sum(black_box(&data));
                sum as f64 / data.len() as f64
            })
        });
    }
    
    group.finish();
}

criterion_group!(
    benches,
    bench_sum_i64,
    bench_sum_filtered,
    bench_min_max,
    bench_average
);
criterion_main!(benches);
