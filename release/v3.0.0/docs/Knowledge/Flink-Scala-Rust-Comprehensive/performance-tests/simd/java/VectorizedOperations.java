package simd;

import jdk.incubator.vector.*;

public class VectorizedOperations {
    private static final VectorSpecies<Long> LONG_SPECIES = LongVector.SPECIES_PREFERRED;
    private static final VectorSpecies<Integer> INT_SPECIES = IntVector.SPECIES_PREFERRED;
    private static final VectorSpecies<Double> DOUBLE_SPECIES = DoubleVector.SPECIES_PREFERRED;
    
    // 标量过滤
    public static long[] scalarFilter(long[] data, long threshold) {
        java.util.ArrayList<Long> result = new java.util.ArrayList<>();
        for (long x : data) {
            if (x > threshold) {
                result.add(x);
            }
        }
        return result.stream().mapToLong(Long::longValue).toArray();
    }
    
    // 向量化过滤
    public static long[] vectorFilter(long[] data, long threshold) {
        int i = 0;
        int bound = LONG_SPECIES.loopBound(data.length);
        java.util.ArrayList<Long> result = new java.util.ArrayList<>();
        
        LongVector thresholdVec = LongVector.broadcast(LONG_SPECIES, threshold);
        
        for (; i < bound; i += LONG_SPECIES.length()) {
            LongVector vec = LongVector.fromArray(LONG_SPECIES, data, i);
            VectorMask<Long> mask = vec.compare(VectorOperators.GT, thresholdVec);
            
            for (int j = 0; j < LONG_SPECIES.length(); j++) {
                if (mask.laneIsSet(j)) {
                    result.add(vec.lane(j));
                }
            }
        }
        
        // 处理剩余
        for (; i < data.length; i++) {
            if (data[i] > threshold) result.add(data[i]);
        }
        
        return result.stream().mapToLong(Long::longValue).toArray();
    }
    
    // 标量求和
    public static long scalarSum(long[] data) {
        long sum = 0;
        for (long x : data) {
            sum += x;
        }
        return sum;
    }
    
    // 向量化求和
    public static long vectorSum(long[] data) {
        int i = 0;
        int bound = LONG_SPECIES.loopBound(data.length);
        LongVector sumVec = LongVector.zero(LONG_SPECIES);
        
        for (; i < bound; i += LONG_SPECIES.length()) {
            LongVector vec = LongVector.fromArray(LONG_SPECIES, data, i);
            sumVec = sumVec.add(vec);
        }
        
        long sum = sumVec.reduceLanes(VectorOperators.ADD);
        
        // 处理剩余
        for (; i < data.length; i++) {
            sum += data[i];
        }
        
        return sum;
    }
    
    // 标量求平均
    public static double scalarAverage(long[] data) {
        if (data.length == 0) return 0.0;
        return (double) scalarSum(data) / data.length;
    }
    
    // 向量化求平均
    public static double vectorAverage(long[] data) {
        if (data.length == 0) return 0.0;
        return (double) vectorSum(data) / data.length;
    }
    
    // 标量 Min/Max
    public static long[] scalarMinMax(long[] data) {
        if (data.length == 0) return new long[]{0, 0};
        
        long min = data[0];
        long max = data[0];
        
        for (int i = 1; i < data.length; i++) {
            if (data[i] < min) min = data[i];
            if (data[i] > max) max = data[i];
        }
        
        return new long[]{min, max};
    }
    
    // 向量化 Min/Max
    public static long[] vectorMinMax(long[] data) {
        if (data.length == 0) return new long[]{0, 0};
        
        int i = 0;
        int bound = LONG_SPECIES.loopBound(data.length);
        
        LongVector minVec = LongVector.broadcast(LONG_SPECIES, Long.MAX_VALUE);
        LongVector maxVec = LongVector.broadcast(LONG_SPECIES, Long.MIN_VALUE);
        
        for (; i < bound; i += LONG_SPECIES.length()) {
            LongVector vec = LongVector.fromArray(LONG_SPECIES, data, i);
            minVec = vec.min(minVec);
            maxVec = vec.max(maxVec);
        }
        
        long min = minVec.reduceLanes(VectorOperators.MIN);
        long max = maxVec.reduceLanes(VectorOperators.MAX);
        
        // 处理剩余
        for (; i < data.length; i++) {
            if (data[i] < min) min = data[i];
            if (data[i] > max) max = data[i];
        }
        
        return new long[]{min, max};
    }
    
    // 标量货币转换
    public static long[] scalarCurrencyConvert(long[] prices) {
        long[] result = new long[prices.length];
        for (int i = 0; i < prices.length; i++) {
            result[i] = (long) (prices[i] * 0.908);
        }
        return result;
    }
    
    // 向量化货币转换 (使用定点数)
    public static long[] vectorCurrencyConvert(long[] prices) {
        final long MULTIPLIER = 908;
        final long DIVISOR = 1000;
        
        int i = 0;
        int bound = LONG_SPECIES.loopBound(prices.length);
        long[] result = new long[prices.length];
        
        LongVector mulVec = LongVector.broadcast(LONG_SPECIES, MULTIPLIER);
        
        for (; i < bound; i += LONG_SPECIES.length()) {
            LongVector vec = LongVector.fromArray(LONG_SPECIES, prices, i);
            LongVector prod = vec.mul(mulVec);
            // 需要逐个除以 DIVISOR
            for (int j = 0; j < LONG_SPECIES.length(); j++) {
                result[i + j] = prod.lane(j) / DIVISOR;
            }
        }
        
        // 处理剩余
        for (; i < prices.length; i++) {
            result[i] = (prices[i] * MULTIPLIER) / DIVISOR;
        }
        
        return result;
    }
    
    // 测试主函数
    public static void main(String[] args) {
        int size = 10_000_000;
        long[] data = new long[size];
        java.util.Random random = new java.util.Random();
        for (int i = 0; i < size; i++) {
            data[i] = random.nextLong() % 10000;
        }
        
        System.out.println("Data size: " + size);
        
        // 测试 Sum
        long start = System.nanoTime();
        long scalarSum = scalarSum(data);
        long scalarTime = System.nanoTime() - start;
        
        start = System.nanoTime();
        long vectorSum = vectorSum(data);
        long vectorTime = System.nanoTime() - start;
        
        System.out.println("Sum - Scalar: " + scalarSum + " (" + scalarTime / 1_000_000 + "ms)");
        System.out.println("Sum - Vector: " + vectorSum + " (" + vectorTime / 1_000_000 + "ms)");
        System.out.println("Speedup: " + (double) scalarTime / vectorTime + "x");
        
        // 验证结果
        if (scalarSum != vectorSum) {
            System.err.println("ERROR: Results don't match!");
        }
    }
}
