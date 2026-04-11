use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};

// 原生函数直接调用
fn bench_native_empty(c: &mut Criterion) {
    c.bench_function("native_empty", |b| {
        b.iter(|| {
            for _ in 0..1000 {
                wasm_udf::native::native_empty()
            }
        })
    });
}

fn bench_native_identity(c: &mut Criterion) {
    let input = 42i64;
    c.bench_function("native_identity", |b| {
        b.iter(|| {
            for _ in 0..1000 {
                wasm_udf::native::native_identity(black_box(input));
            }
        })
    });
}

fn bench_native_add(c: &mut Criterion) {
    c.bench_function("native_add", |b| {
        b.iter(|| {
            for i in 0..1000i64 {
                wasm_udf::native::native_add(black_box(i), black_box(i + 1));
            }
        })
    });
}

fn bench_native_fibonacci(c: &mut Criterion) {
    let mut group = c.benchmark_group("native_fibonacci");
    
    for n in [10, 20].iter() {
        group.bench_with_input(BenchmarkId::new("recursive", n), n, |b, n| {
            b.iter(|| wasm_udf::native::native_fibonacci(black_box(*n)))
        });
        
        group.bench_with_input(BenchmarkId::new("iterative", n), n, |b, n| {
            b.iter(|| wasm_udf::native::native_fibonacci_iter(black_box(*n)))
        });
    }
    
    group.finish();
}

fn bench_native_sum_array(c: &mut Criterion) {
    let sizes = [100, 1000, 10000];
    let mut group = c.benchmark_group("native_sum_array");
    
    for size in sizes.iter() {
        let data: Vec<i64> = (0..*size).map(|i| i as i64).collect();
        group.throughput(criterion::Throughput::Elements(*size as u64));
        
        group.bench_with_input(BenchmarkId::from_parameter(size), size, |b, _| {
            b.iter(|| wasm_udf::native::native_sum_array(black_box(&data)))
        });
    }
    
    group.finish();
}

fn bench_native_currency_convert(c: &mut Criterion) {
    let sizes = [100, 1000, 10000];
    let mut group = c.benchmark_group("native_currency_convert");
    
    for size in sizes.iter() {
        let data: Vec<i64> = (0..*size).map(|i| (i * 100) as i64).collect();
        group.throughput(criterion::Throughput::Elements(*size as u64));
        
        group.bench_with_input(BenchmarkId::from_parameter(size), size, |b, _| {
            b.iter(|| wasm_udf::native::native_currency_convert(black_box(&data)))
        });
    }
    
    group.finish();
}

criterion_group!(
    benches,
    bench_native_empty,
    bench_native_identity,
    bench_native_add,
    bench_native_fibonacci,
    bench_native_sum_array,
    bench_native_currency_convert
);
criterion_main!(benches);
