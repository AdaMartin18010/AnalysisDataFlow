{- ============================================================================
 - Haskell: 素数流 (Prime Number Stream)
 - ============================================================================
 -
 - 本示例演示使用筛法生成无限素数流。
 -
 - 经典算法:
 - 1. 埃拉托斯特尼筛法 (Sieve of Eratosthenes)
 - 2. 试除法
 - 3. 阿克曼筛法 (Akra-Bazzi)
 -
 - 惰性筛法定义:
 -   primes = sieve [2..]
 -   where sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]
 -
 - 数学性质:
 - - 素数定理: π(n) ~ n / ln(n)
 - - 第n个素数 p_n ~ n * ln(n)
 - - 素数间隙无界
 -
 - 参考:
 - - O'Neill, M. E. (2009). The Genuine Sieve of Eratosthenes
 - - Hutton, G. (2016). Programming in Haskell
 - ============================================================================ -}

module PrimesStream where

import Data.List (unfoldr)

-- ----------------------------------------------------------------------------
-- 基本素数筛
-- ----------------------------------------------------------------------------

-- | 简单的埃拉托斯特尼筛法
-- 注意: 这不是真正的埃氏筛, 而是试除法
-- 真正的埃氏筛使用优先队列
primesSimple :: [Integer]
primesSimple = sieve [2..]
  where
    sieve (p:xs) = p : sieve [x | x <- xs, x `mod` p /= 0]

-- | 优化的试除法: 只测试不超过 sqrt(n) 的素数
primes :: [Integer]
primes = 2 : filter isPrime [3,5..]
  where
    isPrime n = all (\p -> n `mod` p /= 0) 
                    (takeWhile (\p -> p*p <= n) primes)

-- | 获取前n个素数
takePrimes :: Int -> [Integer]
takePrimes n = take n primes

-- | 获取第n个素数 (1索引)
primeAt :: Int -> Integer
primeAt n = primes !! (n - 1)

-- ----------------------------------------------------------------------------
--  wheel 优化筛
-- ----------------------------------------------------------------------------

-- | 使用 wheel 因子分解优化的素数筛
-- 跳过能被 2,3,5 整除的数
wheelPrimes :: [Integer]
wheelPrimes = 2 : 3 : 5 : 7 : sieve (spin wheel2357 11)
  where
    wheel2357 = 2:4:2:4:6:2:6:4:2:4:6:6:2:6:4:2:6:4:6:8:4:2:4:2:[]
    spin (x:xs) n = n : spin xs (n + x)
    sieve (x:xs) = x : sieve [y | y <- xs, y `mod` x /= 0]

-- ----------------------------------------------------------------------------
-- 真正的埃拉托斯特尼筛 (使用优先队列)
-- ----------------------------------------------------------------------------

data PriorityQueue k v = PQ [(k, v)]

-- | 插入优先队列
insertPQ :: Ord k => k -> v -> PriorityQueue k v -> PriorityQueue k v
insertPQ k v (PQ xs) = PQ (insertSorted (k, v) xs)
  where
    insertSorted y [] = [y]
    insertSorted y (z:zs) 
        | fst y <= fst z = y : z : zs
        | otherwise      = z : insertSorted y zs

-- | 提取最小元素
minPQ :: PriorityQueue k v -> Maybe ((k, v), PriorityQueue k v)
minPQ (PQ []) = Nothing
minPQ (PQ (x:xs)) = Just (x, PQ xs)

-- | 真正的埃氏筛
genuineSieve :: [Integer]
genuineSieve = sieve [2..] PQEmpty
  where
    data Table = PQEmpty | Table Integer Integer Table  -- p -> p*p 的映射
    
    sieve [] _ = []
    sieve (x:xs) table = 
        case lookupTable x table of
            Nothing -> x : sieve xs (insertTable x table)
            Just _  -> sieve xs (adjustTable x table)
    
    lookupTable _ PQEmpty = Nothing
    lookupTable n (Table p pp rest)
        | n == pp   = Just p
        | otherwise = lookupTable n rest
    
    insertTable p PQEmpty = Table p (p*p) PQEmpty
    insertTable p (Table q qq rest)
        | p < q     = Table p (p*p) (Table q qq rest)
        | otherwise = Table q qq (insertTable p rest)
    
    adjustTable n (Table p pp rest)
        | n == pp   = insertTable p (adjustTable n rest)
        | otherwise = Table p pp (adjustTable n rest)

-- 简化版本
primesGenuine :: [Integer]
primesGenuine = 2 : sieve [3,5..] []
  where
    sieve [] _ = []
    sieve (x:xs) composites
        | x `elem` composites = sieve xs (delete x composites)
        | otherwise           = x : sieve xs (composites ++ [x*x, x*(x+2) ..])

-- ----------------------------------------------------------------------------
-- 素数性质和函数
-- ----------------------------------------------------------------------------

-- | 判断是否为素数
isPrime :: Integer -> Bool
isPrime n 
    | n < 2     = False
    | n == 2    = True
    | even n    = False
    | otherwise = all (\p -> n `mod` p /= 0) 
                      (takeWhile (\p -> p*p <= n) primes)

-- | 质因数分解
primeFactors :: Integer -> [Integer]
primeFactors n = factor n primes
  where
    factor 1 _ = []
    factor m (p:ps)
        | p*p > m    = [m]
        | m `mod` p == 0 = p : factor (m `div` p) (p:ps)
        | otherwise  = factor m ps

-- | 唯一质因数
uniquePrimeFactors :: Integer -> [Integer]
uniquePrimeFactors = map head . group . primeFactors
  where
    group [] = []
    group (x:xs) = (x : takeWhile (==x) xs) : group (dropWhile (==x) xs)

-- | 除数函数: d(n) = 能整除n的正整数个数
divisorCount :: Integer -> Int
divisorCount n = product [e + 1 | (_, e) <- factorization]
  where
    factorization = [(p, length ps) | ps@(p:_) <- group $ primeFactors n]

-- | 除数之和函数: σ(n)
divisorSum :: Integer -> Integer
divisorSum n = product [sum [p^e | e <- [0..k]] | (p, k) <- factorization]
  where
    factorization = [(p, length ps) | ps@(p:_) <- group $ primeFactors n]

-- | 欧拉 totient 函数: φ(n) = 小于n且与n互质的正整数个数
totient :: Integer -> Integer
totient n = n * product [1 - 1/p | p <- uniquePrimeFactors n]

-- ----------------------------------------------------------------------------
-- 素数分布
-- ----------------------------------------------------------------------------

-- | 素数计数函数 π(n): 小于等于n的素数个数
primeCount :: Integer -> Int
primeCount n = length $ takeWhile (<= n) primes

-- | 素数定理近似: π(n) ≈ n / ln(n)
primeCountApprox :: Double -> Double
primeCountApprox n = n / log n

-- | 第n个素数近似: p_n ≈ n * ln(n)
nthPrimeApprox :: Integer -> Double
nthPrimeApprox n = fromInteger n * log (fromInteger n)

-- | 素数间隙: 相邻素数之差
twinGaps :: [(Integer, Integer, Integer)]
twinGaps = zipWith3 (\p1 p2 -> (p1, p2, p2 - p1)) primes (tail primes)

-- | 孪生素数 (间隔为2的素数对)
twinPrimes :: [(Integer, Integer)]
twinPrimes = [(p, p+2) | (p, q, _) <- take 1000 twinGaps, q == p + 2]

-- ----------------------------------------------------------------------------
-- 素数相关的数列
-- ----------------------------------------------------------------------------

-- | 素数阶乘 (primorial): p# = 所有小于等于p的素数的乘积
primorial :: [Integer]
primorial = scanl (*) 1 primes

-- | 梅森数: M_n = 2^n - 1
mersenneNumbers :: [Integer]
mersenneNumbers = [2^n - 1 | n <- [1..]]

-- | 已知的梅森素数指数 (截至2024年)
knownMersenneExponents :: [Int]
knownMersenneExponents = 
    [2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 
     2203, 2281, 3217, 4253, 4423, 9689, 9941, 11213, 19937, 21701,
     23209, 44497, 86243, 110503, 132049, 216091, 756839, 859433,
     1257787, 1398269, 2976221, 3021377, 6972593, 13466917, 20996011,
     24036583, 25964951, 30402457, 32582657, 37156667, 42643801,
     43112609, 57885161, 74207281, 77232917, 82589933]

-- | 已知的梅森素数
knownMersennePrimes :: [Integer]
knownMersennePrimes = map (\n -> 2^n - 1) knownMersenneExponents

-- ----------------------------------------------------------------------------
-- 流变换
-- ----------------------------------------------------------------------------

-- | 素数间隔流
primeGaps :: [Integer]
primeGaps = zipWith (-) (tail primes) primes

-- | 素数平方流
primeSquares :: [Integer]
primeSquares = map (^2) primes

-- | 素数和的流
primeCumulativeSum :: [Integer]
primeCumulativeSum = scanl (+) 0 primes

-- | 素数倒数和 (发散, 但非常缓慢)
primeReciprocals :: [Double]
primeReciprocals = scanl (+) 0 [1 / fromInteger p | p <- primes]

-- | 哥德巴赫分解: 将偶数分解为两个素数之和
goldbachPairs :: Integer -> [(Integer, Integer)]
goldbachPairs n
    | odd n     = []
    | otherwise = [(p, n-p) | p <- takeWhile (<= n `div` 2) primes, 
                              isPrime (n - p)]

-- ----------------------------------------------------------------------------
-- 实用函数
-- ----------------------------------------------------------------------------

-- | 查找大于n的最小素数
nextPrime :: Integer -> Integer
nextPrime n = head $ dropWhile (<= n) primes

-- | 查找小于n的最大素数
prevPrime :: Integer -> Integer
prevPrime n = last $ takeWhile (< n) primes

-- | 素数间隙函数: 从n到下一个素数的距离
primeGapFrom :: Integer -> Integer
primeGapFrom n = nextPrime n - n

-- | 素数密度: n附近的素数密度约为 1 / ln(n)
primeDensity :: Double -> Double
primeDensity n = 1 / log n

-- ----------------------------------------------------------------------------
-- 示例和测试
-- ----------------------------------------------------------------------------

examples :: IO ()
examples = do
    putStrLn "=== Prime Stream Examples ==="
    
    putStrLn "\n1. First 30 primes:"
    print $ takePrimes 30
    -- [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113]
    
    putStrLn "\n2. 100th prime:"
    print $ primeAt 100
    -- 541
    
    putStrLn "\n3. Prime factors of 360:"
    print $ primeFactors 360
    -- [2,2,2,3,3,5]
    
    putStrLn "\n4. Unique prime factors of 360:"
    print $ uniquePrimeFactors 360
    -- [2,3,5]
    
    putStrLn "\n5. Euler's totient of 100:"
    print $ totient 100
    -- 40
    
    putStrLn "\n6. Number of primes <= 1000:"
    print $ primeCount 1000
    -- 168
    
    putStrLn "\n7. Prime theorem approximation for n=1000:"
    putStrLn $ "  Actual: " ++ show (primeCount 1000)
    putStrLn $ "  Approx: " ++ show (primeCountApprox 1000.0)
    
    putStrLn "\n8. First 20 twin prime pairs:"
    print $ take 20 twinPrimes
    
    putStrLn "\n9. First 10 primorials:"
    print $ take 10 primorial
    -- [1,2,6,30,210,2310,30030,510510,9699690,223092870]
    
    putStrLn "\n10. First 10 Mersenne numbers:"
    print $ take 10 mersenneNumbers
    
    putStrLn "\n11. First 20 prime gaps:"
    print $ take 20 primeGaps
    
    putStrLn "\n12. Goldbach pairs for 100:"
    print $ goldbachPairs 100
    
    putStrLn "\n13. Is 104729 a prime?"
    print $ isPrime 104729
    -- True (10000th prime)

-- ----------------------------------------------------------------------------
-- 高级: 素数筛的数学原理
-- ----------------------------------------------------------------------------

{- 
埃拉托斯特尼筛法的复杂度分析:

时间复杂度: O(n log log n)
- 每个合数被其最小质因数筛除
- 调和级数求和得到 log log n

空间复杂度: O(n)
- 需要存储到 n 的所有数

素数定理:
π(n) ~ n / ln(n)
p_n ~ n * ln(n)

其中 π(n) 是素数计数函数, p_n 是第n个素数。
-}

-- | 素数密度实验
primeDensityExperiment :: IO ()
primeDensityExperiment = do
    let ranges = [10, 100, 1000, 10000, 100000, 1000000]
    putStrLn "\n=== Prime Density Experiment ==="
    putStrLn "n\t\tπ(n)\t\tn/ln(n)\t\tratio"
    mapM_ (\n -> do
        let actual = fromIntegral $ primeCount n
            approx = n / log n
            ratio = actual / approx
        putStrLn $ show n ++ "\t\t" ++ show (round actual) ++ 
                   "\t\t" ++ show approx ++ "\t" ++ show ratio
        ) ranges

-- 主函数
main :: IO ()
main = do
    examples
    primeDensityExperiment
