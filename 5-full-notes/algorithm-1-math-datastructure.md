Time:2025-09-08

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[algorithm|algorithm]]

## 复杂度

大 O 记法
渐进符号

---
空间复杂度
## 常用阶

![[2-source-material/images/Pasted image 20250910095800.png]]
## others

最优算法->时间
正确性->证明->数学归纳法等

**循环不变式**:
example:sequential search

```
for i=1;i<n;i++ do
  if a[i]==k then
    return i
return 0
```

*在第 i 轮循环前,a[0..i-1]中,不包含 k*

只需证明上式正确,则此顺序查找算法正确

## math

递推式:
常系数线性齐次递推式->特征方程,特征根
非齐次递推式:展开
![[2-source-material/images/Pasted image 20250910102458.png]]

## 递推关系-分治展开

![[2-source-material/images/Pasted image 20250910102911.png]]

---

代入展开
  bad..

---

## master theorem

![[2-source-material/images/Pasted image 20250910104240.png]]

why?
  递推树,汇总子节点计算代价$f(n)$,叶节点计算代价$a^{log{_b}n}$
how?
  ![[2-source-material/images/Pasted image 20250910110933.png]]

---
*self explain*

[a nice video](https://www.youtube.com/watch?v=SLsHKh_OUEM)

[simple prove](https://www.luogu.com.cn/article/w3avh1ku)

a->分解为子问题的规模
b->分解后每个子问题的复杂度减少多少
f(n)->非递归部分的问题求解所需时间

T(n)其实可以写成:
  $T(n) = \Theta(n^{\log_b a}) + \sum_{j=0}^{\log_b n-1} a^j f(\frac{n}{b^j})$
  后面的部分可以暂时简化,得到:
  $T(n) = \Theta(n^{\log_b a}) + p*f(n)$

$n^{log_b a}$ 代表什么?
  有递归树:![[2-source-material/images/Pasted image 20250911001421.png]]
  它其实是 $a^{log_b n}$ 换底之后的结果,代表所有叶节点的工作量,也就是说,算法中递归的部分所需的时间

$p*f(n)$ 代表什么?
  所有非叶节点的开销

那么求T(n),实际上就是在求,所有叶节点的工作量和非叶节点工作量哪个大
因此有了三种情况:
1. f(n)小于非叶节点工作量,则以非叶节点为主
2. f(n)和叶节点工作量差不多,则,每层的工作量都近似为f(n),那么总工作量近似为 $f(n)*log{n}$,**注意**,这里的f(n)是可以带个logn的,因为logn的增长速度介于多项式和n之间(其实这里有详细的证明,可以见上文提到链接)
3. f(n)大于叶节点,则以f(n)为主,但是这里有个额外的正则条件限制:$af(\frac{n}{b})\leq \lambda f(n) ,\lambda \leq 1$,是在限制每一层中,分治后的子问题的消耗小于原问题的消耗.
## Reference

[a nice video](https://www.youtube.com/watch?v=SLsHKh_OUEM)

[simple prove luogu](https://www.luogu.com.cn/article/w3avh1ku)

[blog](https://blog.restkhz.com/post/how-master-theorem-works)