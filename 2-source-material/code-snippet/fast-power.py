import time

def algorithm1(x,n)->int:
  ans = 1
  for i in range(0,n):
    ans*=x
  return ans

def algorithm2(x,n)->int:
  ans =1
  if n==0: return 1
  ans=algorithm2(x,n//2)
  ans=ans*ans
  if n % 2 == 1:
    ans=x*ans
  return ans

def algorithm3(x,n)->int:
  ans =1
  while n>0:
    if n%2 ==1:
      ans = ans*x
    x = x*x
    n =n//2
  return ans

def main():
  x = 25
  n = 100
  t1 = time.perf_counter_ns()
  ans1 = algorithm1(x,n)
  t2 = time.perf_counter_ns()

  t3 = time.perf_counter_ns()
  ans2 = algorithm2(x,n)
  t4 = time.perf_counter_ns()

  t5 = time.perf_counter_ns()
  ans3 = algorithm3(x,n)
  t6 = time.perf_counter_ns()

  assert(ans1 == ans2 and ans2==ans3)
  print("algo1 takes ",t2-t1," ns")
  print("algo2 takes ",t4-t3," ns")
  print("algo3 takes ",t6-t5," ns")

if __name__ == "__main__":
  main()
