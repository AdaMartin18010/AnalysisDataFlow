use criterion::{black_box, criterion_group, criterion_main, Criterion, Throughput};
use simd_benchmarks::data_generator::DataGenerator;
use simd_benchmarks::scalar_ops;

#[cfg(target_arch = "x86_64")]
use simd_benchmarks::simd_avx2;

fn bench_currency_convert(c: &mut Criterion) {
    let prices = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("currency_convert_1M");
    group.throughput(Throughput::Elements(prices.len() as u64));
    
    group.bench_function("scalar", |b| {
        b.iter(|| scalar_ops::scalar_currency_convert(black_box(&prices)))
    });
    
    #[cfg(target_arch = "x86_64")]
    {
        group.bench_function("avx2", |b| {
            b.iter(|| unsafe {
                simd_avx2::avx2_currency_convert(black_box(&prices))
            })
        });
    }
    
    group.finish();
}

fn bench_simple_map(c: &mut Criterion) {
    let data = DataGenerator::new(1_000_000).generate_i64();
    
    let mut group = c.benchmark_group("simple_map_1M");
    group.throughput(Throughput::Elements(data.len() as u64));
    
    group.bench_function("scalar_add_100", |b| {
        b.iter(|| scalar_ops::scalar_map(black_box(&data), |x| x + 100))
    });
    
    group.bench_function("scalar_mul_2", |b| {
        b.iter(|| scalar_ops::scalar_map(black_box(&data), |x| x * 2))
    });
    
    group.finish();
}

criterion_group!(benches, bench_currency_convert, bench_simple_map);
criterion_main!(benches);
