package wasm;

/**
 * JNI UDF 接口 - 用于性能对比
 */
public class JniUdf {
    static {
        System.loadLibrary("native_udf");
    }
    
    // 空函数
    public static native void emptyNative();
    
    // 恒等函数
    public static native long identityNative(long x);
    
    // 加法
    public static native long addNative(long a, long b);
    
    // 过滤
    public static native boolean filterGtNative(long x, long threshold);
    
    // 数组求和
    public static native long sumArrayNative(long[] arr);
    
    // 货币转换 - 返回新数组
    public static native long[] currencyConvertNative(long[] prices);
    
    // 斐波那契
    public static native long fibonacciNative(int n);
}
