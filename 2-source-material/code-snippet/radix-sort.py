from typing import List
import random

def radix_sort(arr:List[int])->List[int]:
  if not arr:
    return []
  if any(n<0 for n in arr):
    raise ValueError("radix sort only support non negative number!")
  output = arr[:]
  # 找到最高位数
  k = len(str(max(output)))
  # radix sort 
  for i in range(k):
    buckets=[[] for _ in range(10)]
    place = 10**i
    for n in output:
      digit = (n//place)%10
      buckets[digit].append(n)
    output = [x for bucket in buckets for x in bucket]
  return output


v = [random.randint(0,100) for _ in range(20)]
print("the v is:\n",v)
v=radix_sort(v)
print("after sort:\n",v)


