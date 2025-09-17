import random
import time

X = 365
NUM = 1_000

def normal_normal(x,a)->int:
  length = len(a)
  sum = 0
  for i in range(length):
    temp = power1(x,i)*a[length-i-1]
    sum+=temp
  return sum

def normal_fast(x,a)->int:
  length = len(a)
  sum = 0
  for i in range(length):
    temp = power2(x,i)*a[length-i-1]
    sum+=temp
  return sum

def horner(x,a)->int:
  n = len(a)
  p = a[0]
  for i in range(1,n):
    p = p*x+a[i]
  return p

# recursive horner
# P(i) = a[i] if i == 0
# P(i) = P(i-1)*x + a[n-i]
def recur_horner(x,a,n)->int:
  if n==1:return a[0]
  return x*recur_horner(x,a,n-1)+a[n-1]

def power1(x,n)->int:
  ans = 1
  for i in range(0,n):
    ans*=x
  return ans

def power2(x,n)->int:
  ans = 1
  while n>0:
    if n%2==1:
      ans = ans*x
    x = x*x
    n = n//2
  return ans

def main():
  #x = int(input())
  x = X
  a = [random.randint(-1000,1000)for _ in range(NUM)]

  t1 = time.perf_counter()
  ans1 = normal_normal(x,a)
  t2 = time.perf_counter()

  t3 = time.perf_counter()
  ans2 = normal_fast(x,a)
  t4 = time.perf_counter()

  t5 = time.perf_counter()
  ans3 = horner(x,a)
  t6 = time.perf_counter()
  
  if NUM<200:
    t7 = time.perf_counter()
    ans4 = recur_horner(x,a,len(a))
    t8 = time.perf_counter()
    assert(ans1==ans2 and ans2==ans3 and ans3==ans4)
    print("ans4 takes ",(t8-t7)*1_000_000," us")

  else:
    assert(ans1==ans2 and ans2==ans3)
  print("ans1 takes ",(t2-t1)*1_000_000," us")
  print("ans2 takes ",(t4-t3)*1_000_000," us")
  print("ans3 takes ",(t6-t5)*1_000_000," us")
  

if __name__ == "__main__":
  main()