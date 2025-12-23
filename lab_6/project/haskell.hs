module Main where

import Data.List

-- 1. БАЗОВЫЙ СИНТАКСИС И ФУНКЦИИ

square :: Int -> Int
square x = x * x

add :: Int -> Int -> Int
add x y = x + y

absolute :: Int -> Int
absolute x = if x >= 0 then x else -x

grade :: Int -> String
grade score
  | score >= 90 = "Excellent"
  | score >= 75 = "Good" 
  | score >= 60 = "Satisfactory"
  | otherwise   = "Fail"

-- 2. РЕКУРСИЯ И РАБОТА СО СПИСКАМИ

factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

sumList :: [Int] -> Int
sumList []     = 0
sumList (x:xs) = x + sumList xs

length' :: [a] -> Int
length' []     = 0
length' (_:xs) = 1 + length' xs

fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n-1) + fibonacci (n-2)

-- 3. PATTERN MATCHING И КОРТЕЖИ

addVectors :: (Double, Double) -> (Double, Double) -> (Double, Double)
addVectors (x1, y1) (x2, y2) = (x1 + x2, y1 + y2)

first :: (a, b, c) -> a
first (x, _, _) = x

second :: (a, b, c) -> b
second (_, y, _) = y

third :: (a, b, c) -> c
third (_, _, z) = z

describeList :: [a] -> String
describeList xs = case xs of
  []     -> "Empty list"
  [x]    -> "Singleton list"
  (_:_)  -> "Long list"

-- 4. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА

map' :: (a -> b) -> [a] -> [b]
map' _ []     = []
map' f (x:xs) = f x : map' f xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' _ []     = []
filter' p (x:xs)
  | p x     = x : filter' p xs
  | otherwise = filter' p xs

myFoldl :: (b -> a -> b) -> b -> [a] -> b
myFoldl _ acc []     = acc
myFoldl f acc (x:xs) = myFoldl f (f acc x) xs

compose :: (b -> c) -> (a -> b) -> a -> c
compose f g x = f (g x)

-- 5. АЛГЕБРАИЧЕСКИЕ ТИПЫ ДАННЫХ

data Day = Monday | Tuesday | Wednesday | Thursday | Friday | Saturday | Sunday
  deriving (Show, Eq)

isWeekend :: Day -> Bool
isWeekend Saturday = True
isWeekend Sunday   = True
isWeekend _        = False

data Point = Point Double Double
  deriving (Show)

distance :: Point -> Point -> Double
distance (Point x1 y1) (Point x2 y2) = sqrt ((x2 - x1)^2 + (y2 - y1)^2)

data List a = Empty | Cons a (List a)
  deriving (Show)

toStandardList :: List a -> [a]
toStandardList Empty      = []
toStandardList (Cons x xs) = x : toStandardList xs

-- 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ

countEven :: [Int] -> Int
countEven []     = 0
countEven (x:xs)
  | even x     = 1 + countEven xs
  | otherwise  = countEven xs

positiveSquares :: [Int] -> [Int]
positiveSquares []     = []
positiveSquares (x:xs)
  | x > 0     = x*x : positiveSquares xs
  | otherwise = positiveSquares xs

bubblePass :: [Int] -> [Int]
bubblePass []     = []
bubblePass [x]    = [x]
bubblePass (x:y:xs)
  | x > y     = y : bubblePass (x:xs)
  | otherwise = x : bubblePass (y:xs)

bubbleSort :: [Int] -> [Int]
bubbleSort xs =
  let xs' = bubblePass xs
  in if xs' == xs
     then xs'
     else bubbleSort xs'

-- 7. MAIN - ДЕМОНСТРАЦИЯ

main :: IO ()
main = do
  putStrLn "ЛАБОРАТОРНАЯ РАБОТА №6: ВВЕДЕНИЕ В HASKELL"

  -- 1. БАЗОВЫЙ СИНТАКСИС
  putStrLn "\n1. БАЗОВЫЙ СИНТАКСИС:"
  putStrLn $ "  square 5 = " ++ show (square 5)
  putStrLn $ "  add 3 4 = " ++ show (add 3 4)
  putStrLn $ "  absolute (-10) = " ++ show (absolute (-10))
  putStrLn $ "  grade 85 = " ++ grade 85

  -- 2. РЕКУРСИЯ
  putStrLn "\n2. РЕКУРСИЯ:"
  putStrLn $ "  factorial 5 = " ++ show (factorial 5)
  putStrLn $ "  sumList [1,2,3,4,5] = " ++ show (sumList [1,2,3,4,5])
  putStrLn $ "  length' [1,2,3,4,5] = " ++ show (length' [1,2,3,4,5])
  putStrLn $ "  fibonacci 7 = " ++ show (fibonacci 7)

  -- 3. PATTERN MATCHING
  putStrLn "\n3. PATTERN MATCHING:"
  putStrLn $ "  addVectors (1,2) (3,4) = " ++ show (addVectors (1.0,2.0) (3.0,4.0))
  putStrLn $ "  first (1,2,3) = " ++ show (first (1,2,3))
  putStrLn $ "  describeList [1,2,3] = " ++ describeList [1,2,3]

  -- 4. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА
  putStrLn "\n4. ФУНКЦИИ ВЫСШЕГО ПОРЯДКА:"
  putStrLn $ "  map' square [1,2,3,4] = " ++ show (map' square [1,2,3,4])
  putStrLn $ "  filter' even [1..6] = " ++ show (filter' even [1,2,3,4,5,6])
  putStrLn $ "  myFoldl (+) 0 [1..5] = " ++ show (myFoldl (+) 0 [1,2,3,4,5])

  -- 5. АЛГЕБРАИЧЕСКИЕ ТИПЫ
  putStrLn "\n5. АЛГЕБРАИЧЕСКИЕ ТИПЫ:"
  putStrLn $ "  distance (Point 0 0) (Point 3 4) = " ++ show (distance (Point 0 0) (Point 3 4))
  putStrLn $ "  isWeekend Saturday = " ++ show (isWeekend Saturday)

  -- 6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ
  putStrLn "\n6. ПРАКТИЧЕСКИЕ ЗАДАНИЯ:"
  putStrLn $ "  countEven [1..6] = " ++ show (countEven [1,2,3,4,5,6])
  putStrLn $ "  positiveSquares [-2..3] = " ++ show (positiveSquares [-2,-1,0,1,2,3])
  putStrLn $ "  bubbleSort [5,2,8,1,9] = " ++ show (bubbleSort [5,2,8,1,9])

  putStrLn "\n ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!"
