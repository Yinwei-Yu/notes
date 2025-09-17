Time:2025-09-15

Status: 

- [x] **working** 👨‍💻
- [ ] *done*    💻

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

---

取一个数字,放到结果的某一个位置,加上剩下的n-1个数字在结果中剩余的位置的排列

## 基数排序

一个数组中的数字,都恰好有k位数字
先按照最高位的数字大小,把数字分发到不同的10个桶中

then?

1. 对每个桶中的数字用一个排序算法,最坏退化到$O(logn)$
2. 对每个桶递归调用桶排序->太多桶了 $10^k$

more efficient way?

use the least important number

## 多数元素


## Reference
