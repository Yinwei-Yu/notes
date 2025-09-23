## 1

相对于数组,使用链表作为$L_0..L_9$的数据结构时:

时间复杂度不变,仍然是 $\Theta(n)$  

因为在k轮循环中,每次对n个元素做分发,总的时间时间复杂度为$\Theta(kn)=\Theta(n)$

空间复杂度降低为$O(1)$,因为对于链表而言,可以直接把原来在$L$中的node直接改变指向,链到Li的头节点之后,这样不要额外的空间存储中间结果

## 2

(1)

```
average(arr,n) //求数组arr的前n个数的平均值
	if n==1
		return 1
	return ((n-1)*average(arr,n-1)+arr[n])/n //返回前n-1个数的平均值和第n个数的平均值的平均值
```

(2)

可以写出递推式:

$$
f(n)=
\begin{cases}
1 &\text{if } n=1 \\
f(n-1)+1 &\text{if } n>0
\end{cases}
$$
其中$f(n)=f(n-1)+1$的常数1的原因是:只需要对$f(n-1)$的结果和$arr[n]$做一次平均运算

展开可得:
$$
\begin{aligned}
f(n) &= f(n-1)+1\\
&= f(n-2)+1+1 \\
&= f(1)+1+1+\cdot\cdot\cdot+1\\
& = n
\end{aligned}
$$
所以算法的时间复杂度为$\Theta(n)$

## 3

基本情况:

当只有一个人时,他一定是VIP

其余情况:

随机从房间里抽取两个人:A,B

问A是否认识B:

1. A认识B,因为VIP不认识任何人,所以A不是VIP,从房间中踢出A,在剩下n-1个人中继续
2. A不认识B,因为任何人都认识VIP,所以B不是VIP,从房间里踢出B,在剩下n-1个人中继续

伪代码:

```
find_vip(arr)
	if len(arr)==1
		return arr[0]
	randomly pick A and B from arr
	know = ask(A,B)
	if know
		remove(arr,A)
		find_vip(arr)
	else
		remove(arr,B)
		find_vip
```

## 4

(1)

因为P\[i]为0代表P\[i]这个位置可以成为我们挑选的数可以被放置的位置

如果不置0,那么在下一轮递归中,这个位置被m-1占据了,就会漏掉可能的组合

(2)

初始时,P中包含n个0

每调用一次$Perm2(P,m)$,P中减少一个0

在调用到$Perm2(P,m)$时,之前已经调用过了n-m次,则P中还包含$n-(n-m)=m$个0

$Perm2(P,m)$的语义是:在数组P中,将m置于P中为0的位置上后,生成其余数字组成的排列.

在调用到$Perm(P,m-1)$时,P中有m个0,因此$Perm(P,m-1)$会恰好执行m次