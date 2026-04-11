{- ============================================================================
 - Haskell: 斐波那契流 (Fibonacci Stream)
 - ============================================================================
 -
 - 本示例演示 Haskell 中无限流的定义和操作。
 -
 - 核心概念:
 - - 惰性求值: 只在需要时计算元素
 - - 无限数据结构: 可以表示无限的序列
 - - 流变换: map, filter, zipWith 等高阶函数
 -
 - 斐波那契数列定义:
 -   fib(0) = 0
 -   fib(1) = 1
 -   fib(n) = fib(n-1) + fib(n-2) for n >= 2
 -
 - 流式定义:
 -   fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
 -
 - 这个定义利用了 Haskell 的惰性求值, 在常数空间生成无限斐波那契流。
 -
 - 参考:
 - - Bird, R. (2015). Thinking Functionally with Haskell
 - - Hutton, G. (2016). Programming in Haskell
 - ============================================================================ -}

module FibonacciStream where

-- ----------------------------------------------------------------------------
-- 基本斐波那契流定义
-- ----------------------------------------------------------------------------

-- | 无限斐波那契流
-- 使用 zipWith 将流与自身的尾部相加
-- 这是一个典型的循环定义 (knot-tying), 在惰性语言中工作良好
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- | 前n个斐波那契数
-- take 5 fibs = [0, 1, 1, 2, 3]
takeFibs :: Int -> [Integer]
takeFibs n = take n fibs

-- | 获取第n个斐波那契数 (0索引)
-- fibAt 10 = 55
fibAt :: Int -> Integer
fibAt n = fibs !! n

-- ----------------------------------------------------------------------------
-- 斐波那契流的性质
-- ----------------------------------------------------------------------------

-- | 验证性质: fib(n) == fib(n-1) + fib(n-2)
-- 这个函数用于测试流的正确性
verifyFib :: Int -> Bool
verifyFib n 
    | n < 2     = True
    | otherwise = fibs !! n == fibs !! (n-1) + fibs !! (n-2)

-- | 批量验证前n个性质
verifyFibs :: Int -> Bool
verifyFibs n = all verifyFib [0..n]

-- ----------------------------------------------------------------------------
-- 斐波那契数列的数学性质
-- ----------------------------------------------------------------------------

-- | 黄金比例近似: fib(n+1) / fib(n) -> φ (当 n -> ∞)
-- φ = (1 + sqrt 5) / 2 ≈ 1.6180339887...
goldenRatioApprox :: Int -> Double
goldenRatioApprox n = fromInteger (fibs !! (n+1)) / fromInteger (fibs !! n)

-- | 黄金比例的真值
phi :: Double
phi = (1 + sqrt 5) / 2

-- | 计算近似误差
approximationError :: Int -> Double
approximationError n = abs (goldenRatioApprox n - phi)

-- ----------------------------------------------------------------------------
-- 斐波那契矩阵快速幂
-- ----------------------------------------------------------------------------

-- | 2x2 矩阵乘法 (用于快速计算斐波那契数)
type Matrix2x2 = ((Integer, Integer), (Integer, Integer))

-- | 矩阵乘法
matrixMult :: Matrix2x2 -> Matrix2x2 -> Matrix2x2
matrixMult ((a,b),(c,d)) ((e,f),(g,h)) = 
    ((a*e + b*g, a*f + b*h),
     (c*e + d*g, c*f + d*h))

-- | 矩阵快速幂
matrixPow :: Matrix2x2 -> Int -> Matrix2x2
matrixPow _ 0 = ((1,0),(0,1))  -- 单位矩阵
matrixPow m n
    | even n    = let half = matrixPow m (n `div` 2) in matrixMult half half
    | otherwise = matrixMult m (matrixPow m (n-1))

-- | 使用矩阵快速幂计算第n个斐波那契数
-- 时间复杂度: O(log n)
fibFast :: Int -> Integer
fibFast n = let ((_, _), (fibN, _)) = matrixPow ((1,1),(1,0)) n in fibN

-- ----------------------------------------------------------------------------
-- 斐波那契流的变换
-- ----------------------------------------------------------------------------

-- | 斐波那契偶数流
evenFibs :: [Integer]
evenFibs = filter even fibs

-- | 斐波那契奇数流
oddFibs :: [Integer]
oddFibs = filter odd fibs

-- | 斐波那契倍数流 (能被k整除的斐波那契数)
divisibleFibs :: Integer -> [Integer]
divisibleFibs k = filter (\x -> x `mod` k == 0) fibs

-- | 累积和流
-- partialSums fibs = [0, 0+1, 0+1+1, 0+1+1+2, ...] = [0, 1, 2, 4, 7, ...]
partialSums :: [Integer] -> [Integer]
partialSums = scanl (+) 0

fibPartialSums :: [Integer]
fibPartialSums = partialSums fibs

-- | 相邻斐波那契数比率流
fibRatios :: [Double]
fibRatios = zipWith (/) (map fromInteger (tail fibs)) (map fromInteger fibs)

-- ----------------------------------------------------------------------------
-- 广义斐波那契序列
-- ----------------------------------------------------------------------------

-- | Tribonacci 流: T(n) = T(n-1) + T(n-2) + T(n-3)
-- 初始值: 0, 0, 1
tribonacci :: [Integer]
tribonacci = 0 : 0 : 1 : zipWith3 add3 tribonacci (tail tribonacci) (tail (tail tribonacci))
  where
    add3 a b c = a + b + c

-- | 通用线性递推流
-- recurrence coeffs initials 生成满足递推关系的流
-- 例如: fibs = recurrence [1,1] [0,1]
recurrence :: [Integer] -> [Integer] -> [Integer]
recurrence coeffs initials = initials ++ go (length initials)
  where
    go n = let next = sum $ zipWith (*) coeffs (take (length coeffs) $ drop (n - length coeffs) result)
               result = initials ++ go (n + 1)
           in next : go (n + 1)

-- | 使用 recurrence 重新定义斐波那契流
fibs' :: [Integer]
fibs' = recurrence [1, 1] [0, 1]

-- ----------------------------------------------------------------------------
-- 斐波那契数列的组合解释
-- ----------------------------------------------------------------------------

-- | 卡特兰数流 (与斐波那契相关)
catalan :: [Integer]
catalan = 1 : zipWith div (zipWith (*) [2,4..] catalan) [2..]

-- | 斐波那契数列的生成函数
-- F(x) = sum_{n>=0} fib(n) * x^n = x / (1 - x - x^2)
-- 这个函数计算生成函数的近似值
genFuncFib :: Double -> Double
genFuncFib x = x / (1 - x - x*x)

-- ----------------------------------------------------------------------------
-- 实用函数
-- ----------------------------------------------------------------------------

-- | 查找满足条件的斐波那契数
findFib :: (Integer -> Bool) -> Maybe Integer
findFib p = find p fibs

-- | 判断一个数是否是斐波那契数
-- 利用性质: n 是斐波那契数当且仅当 5*n^2+4 或 5*n^2-4 是完全平方数
isFibonacci :: Integer -> Bool
isFibonacci n = isPerfectSquare (5*n*n + 4) || isPerfectSquare (5*n*n - 4)
  where
    isPerfectSquare m = let r = floor (sqrt (fromInteger m)) in r*r == m

-- | 找出最接近给定数的斐波那契数
nearestFib :: Integer -> Integer
nearestFib n = head $ dropWhile (\f -> abs (f - n) > abs (head (tail fibs) - n)) fibs

-- ----------------------------------------------------------------------------
-- 示例和测试
-- ----------------------------------------------------------------------------

-- | 示例输出
examples :: IO ()
examples = do
    putStrLn "=== Fibonacci Stream Examples ==="
    
    putStrLn "\n1. First 20 Fibonacci numbers:"
    print $ takeFibs 20
    -- [0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181]
    
    putStrLn "\n2. Fibonacci at position 50:"
    print $ fibAt 50
    -- 12586269025
    
    putStrLn "\n3. First 10 even Fibonacci numbers:"
    print $ take 10 evenFibs
    -- [0,2,8,34,144,610,2584,10946,46368,196418]
    
    putStrLn "\n4. Golden ratio approximation:"
    putStrLn $ "  n=10: " ++ show (goldenRatioApprox 10)
    putStrLn $ "  n=20: " ++ show (goldenRatioApprox 20)
    putStrLn $ "  True φ: " ++ show phi
    
    putStrLn "\n5. Fibonacci ratios converging to φ:"
    print $ take 10 fibRatios
    
    putStrLn "\n6. First 15 Tribonacci numbers:"
    print $ take 15 tribonacci
    -- [0,0,1,1,2,4,7,13,24,44,81,149,274,504,927]
    
    putStrLn "\n7. First 10 partial sums of Fibonacci:"
    print $ take 10 fibPartialSums
    -- [0,1,2,4,7,12,20,33,54,88]
    
    putStrLn "\n8. Verify Fibonacci property for first 100:"
    print $ verifyFibs 100
    -- True
    
    putStrLn "\n9. Is 987 a Fibonacci number?"
    print $ isFibonacci 987
    -- True
    
    putStrLn "\n10. Nearest Fibonacci to 1000:"
    print $ nearestFib 1000
    -- 987

-- ----------------------------------------------------------------------------
-- 高级: 斐波那契与惰性求值原理
-- ----------------------------------------------------------------------------

{- 
斐波那契流的求值过程:

fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

展开求值:
  fibs = 0 : 1 : zipWith (+) (0:1:...) (1:...)
       = 0 : 1 : (0+1) : zipWith (+) (1:...) (1:...)
       = 0 : 1 : 1 : (1+1) : zipWith (+) (1:...) (2:...)
       = 0 : 1 : 1 : 2 : (1+2) : ...
       = 0 : 1 : 1 : 2 : 3 : ...

关键观察:
1. 定义是循环的 (fibs 出现在等式两边)
2. 每次只计算需要的部分 (thunk)
3. 已计算的值被缓存 (memoization)
4. 空间复杂度是 O(1) (常数空间)
-}

-- | 使用 iterate 的替代定义
fibsIterate :: [Integer]
fibsIterate = map fst $ iterate (\(a,b) -> (b, a+b)) (0, 1)

-- | 使用 unfoldr 的定义
fibsUnfoldr :: [Integer]
fibsUnfoldr = unfoldr (\(a,b) -> Just (a, (b, a+b))) (0, 1)

-- | 显式 thunk 定义 (展示底层原理)
data Stream a = Cons a (Stream a)

fibStream :: Stream Integer
fibStream = fibStream' 0 1
  where
    fibStream' a b = Cons a (fibStream' b (a+b))

-- | Stream 转列表 (有限)
streamToList :: Stream a -> [a]
streamToList (Cons x xs) = x : streamToList xs

-- 主函数
main :: IO ()
main = examples
