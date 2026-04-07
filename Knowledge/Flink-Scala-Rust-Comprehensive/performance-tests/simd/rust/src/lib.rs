pub mod data_generator;
pub mod scalar_ops;

#[cfg(target_arch = "x86_64")]
pub mod simd_avx2;

#[cfg(all(target_arch = "x86_64", target_feature = "avx512f"))]
pub mod simd_avx512;

#[cfg(target_arch = "aarch64")]
pub mod simd_neon;
