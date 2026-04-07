use rand::prelude::*;
use rand_distr::{Distribution, Normal, Uniform};

#[derive(Clone, Copy, Debug)]
pub enum DataDistribution {
    Uniform,
    Normal { mean: f64, std_dev: f64 },
    Sequential,
}

pub struct DataGenerator {
    size: usize,
    distribution: DataDistribution,
}

impl DataGenerator {
    pub fn new(size: usize) -> Self {
        Self {
            size,
            distribution: DataDistribution::Uniform,
        }
    }
    
    pub fn with_distribution(mut self, dist: DataDistribution) -> Self {
        self.distribution = dist;
        self
    }
    
    pub fn generate_i64(&self) -> Vec<i64> {
        let mut rng = thread_rng();
        let mut data = vec![0i64; self.size];
        
        match self.distribution {
            DataDistribution::Uniform => {
                let dist = Uniform::new(i64::MIN / 2, i64::MAX / 2);
                for i in 0..self.size {
                    data[i] = dist.sample(&mut rng);
                }
            }
            DataDistribution::Normal { mean, std_dev } => {
                let dist = Normal::new(mean, std_dev).unwrap();
                for i in 0..self.size {
                    data[i] = dist.sample(&mut rng) as i64;
                }
            }
            DataDistribution::Sequential => {
                for i in 0..self.size {
                    data[i] = i as i64;
                }
            }
        }
        
        data
    }
    
    pub fn generate_f64(&self) -> Vec<f64> {
        let mut rng = thread_rng();
        let mut data = vec![0.0f64; self.size];
        
        match self.distribution {
            DataDistribution::Uniform => {
                let dist = Uniform::new(-1e6, 1e6);
                for i in 0..self.size {
                    data[i] = dist.sample(&mut rng);
                }
            }
            DataDistribution::Normal { mean, std_dev } => {
                let dist = Normal::new(mean, std_dev).unwrap();
                for i in 0..self.size {
                    data[i] = dist.sample(&mut rng);
                }
            }
            _ => panic!("Distribution not supported for f64"),
        }
        
        data
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_uniform_generation() {
        let gen = DataGenerator::new(1000);
        let data = gen.generate_i64();
        assert_eq!(data.len(), 1000);
    }
    
    #[test]
    fn test_sequential_generation() {
        let gen = DataGenerator::new(100)
            .with_distribution(DataDistribution::Sequential);
        let data = gen.generate_i64();
        assert_eq!(data[0], 0);
        assert_eq!(data[99], 99);
    }
}
