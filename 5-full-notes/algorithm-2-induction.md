Time:2025-09-15

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/algorithm|algorithm]]

## 典型的例子

斐波那契序列

递归->栈溢出?速度?
通项公式->数值溢出?

## 选择排序

```python
def sort(i)
	if i<n:
		k=i
		for j in range(i+1,n):
			if A[j]<A[k]:k=j
		if k!=i:
			swap(A[i],A[k])
		sort(i+1)
```

time complexity?

$$
C(n) = \begin{cases}
0 & \text{if } n = 1 \\
C(n-1) + (n-1) & \text{if } n \ge 2
\end{cases}
$$

$O(n^2)$

## 插入排序

类似

但是选择排序稳定$O(n^2)$
插入排序最好$O(n)$

## 证明

数学归纳法证明insertsort:

![[2-source-material/images/Pasted image 20250915145900.png]]

循环不变式:sort(n)执行后,A\[0..n]是已经排好序的

## example

*求幂问题*

直观:x自乘n次 $O(n)$

more efficient method?

just use half:if we know $x^{[m/2]}$->we know $x^m$

```python
def power(x,m):
	if m==0 return 1
	y = power(x,m//2)
	y = y*y
	if m%2 == 1:
		y=x*y
	return y
```

can we expand Recursion?

a simple way:

```python
def power(x,m)->int:
	ans=1
	while m>0:
		if m%2 == 1:
			ans = ans*x
		x = x*x
		m = m//2
	return ans
```


![[2-source-material/images/Pasted image 20250915152242.png]]

n=2,x=3:

n=b10
j:1->0
j=1:dj=1->y=xy=3
j=0:dj=0->y=y\*y=9

another way:

![[2-source-material/images/Pasted image 20250915152833.png]]

$O(logn)$

code snippet [[2-source-material/code-snippet/fast-power.py|fast-power]]

![[2-source-material/images/Pasted image 20250915193639.png]]

---

*多项式求值*

分别求值:$O(n^2)$
用上面的快速幂:$O(nlogn)$

**Horner's rule(Horner规则)**

![[2-source-material/images/Pasted image 20250915153411.png]]

```python
def horner(n)->int:
	p = a[n]
	for j in range(1,n):
		p = xp+a[n-j]
	return p
```

can we use a recursion way?

```python
# recursive horner
# P(i) = a[i] if i == 0
# P(i) = P(i-1)*x + a[n-i]
def recur_horner(x,a,n)->int:
  if n==1:return a[0]
  return x*recur_horner(x,a,n-1)+a[n-1]
```

code snippet [[2-source-material/code-snippet/horner-rule.py|horner-rule]]

![[2-source-material/images/Pasted image 20250915193744.png]]

## 生成排列

input:n
output:1..n的所有可能排列

假设可以生成n-1个数的排列
将一个元素放到第一个,然后生成后面的排列,把第一个元素插到后面的排列里

- 生成2..n的所有排列,然后在每个排列前加一个1
- 对于1,3..n做上述操作
- 重复直到最后生成1..n-1的排列

```python
def perm1(arr,m):# 对于arr,生成从m开始的所有排列(前m-1个元素已经生成过了排列不要动)
    if m==len(arr):
        print(arr)
    for j in range(m,len(arr)):
        arr[j],arr[m] = arr[m],arr[j] # 为了生成m后的元素的排列,需要依次把后面的每一个元素拿到第一位,然后生成后面的排列
        perm1(arr,m+1) # 递归调用
        arr[j],arr[m] = arr[m],arr[j] # 恢复原状
```

---

取一个数字,放到结果的某一个位置,加上剩下的n-1个数字在结果中剩余的位置的排列

```python
def perm2(arr,m):
    if m==0:
      print(arr)
    for j in range(len(arr)):
        if arr[j]==0:
            arr[j]=m
            perm2(arr,m-1)
            arr[j]=0
```
## 基数排序

一个数组中的数字,都恰好有k位数字
先按照最高位的数字大小,把数字分发到不同的10个桶中

then?

1. 对每个桶中的数字用一个排序算法,最坏退化到$O(logn)$
2. 对每个桶递归调用桶排序->太多桶了 $10^k$

more efficient way?

use the least important number

基数排序的一个重要性质是稳定排序,eg:

1234,1235两个数字按照第2位数字3排序后,其顺序仍然是1234,1235

这个性质保证了基数排序的正确性

算法的时间复杂度为$O(n)$,空间复杂度为$O(n)$

```python
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
```

有没有办法降低空间复杂度?->链表

如果原本的数据以链表的形式呈现,那么可以采用仅改变节点指向的方式来做到$O(1)$的复杂度

## 多数元素

背景:找出一个在数组中出现次数>n/2的数字

方法一:暴力搜索
方法二:排序后取中间数字
方法三:

```python
def max_number(arr):
  ans,hp = 0,0
  for n in arr:
    if hp == 0 :
      ans,hp =n,1
    else: hp+=1 if ans == n else -1
  print(ans)
```

证明:
设多数元素出现的次数为a,其余元素的个数为b,有a>=b

我们从第一个数开始,认为他是多数元素,其hp为1.往后每出现一个相同元素,它的hp+1,否则-1.

如果有一个数A\[i]的hp变为0,那么我们可以证明:在剩余的A\[i+1..n]
中,多数元素x的a'仍然大于剩余元素的数量b':

首先:要理解到A\[i]的hp变为0,那么A\[i]一定不是多数元素.

所以,在A\[0..i]中,多数元素x的出现次数x'和其余元素的数量关系y'满足:$x'<y'$,否则不会出现A\[i]的hp降为0.

那么在A\[i+1..n]中有:

a-x' > b-y'

因此在最后,hp不为0的数绝对是多数元素.
## Reference

[[2-source-material/code-snippet/fast-power.py|fast-power]]

[[2-source-material/code-snippet/horner-rule.py|horner-rule]]

[[2-source-material/code-snippet/permutation.py|permutation]]

[[2-source-material/code-snippet/radix-sort.py|radix-sort]]

[[2-source-material/code-snippet/max-number.py|max-number]]

[多数元素证明](https://leetcode.cn/problems/majority-element/solutions/3744717/on-mo-er-tou-piao-fa-yan-jin-zheng-ming-ww1zv/)
