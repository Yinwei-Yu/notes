Time:2025-09-17

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/cg|cg]]

## Why transformation?

camera->move
direction
rotation
scale
3d to 2d projection

## Scale

![[2-source-material/images/Pasted image 20250917205930.png]]

$$
\begin{aligned}
x' = sx \\
y' = sy
\end{aligned}
$$

we can write this as:

$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}s & 0 \\0 & s\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

if we use non-uniform scale? like this:

![[2-source-material/images/Pasted image 20250917210715.png]]

its ok we only use to change s in the matrix

## reflection
$$
x' = -x ,\ y' = y
$$

$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}-1&0 \\0 &1\end{bmatrix} 
\begin{bmatrix}x\\y\end{bmatrix}
$$

## Shear(切变)

![[2-source-material/images/Pasted image 20250917210945.png]]

for every point, vertical shift is always 0
if y = 0, horizontal shift is 0
if y = 1, horizontal shift is a

so we can figure it out:

$$x'=x+ay$$

let's use matrix:

$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}1 & a \\ 0 & 1\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

## Rotate

![[2-source-material/images/Pasted image 20250917211344.png]]

**Always centering around the origin**

prove:use two points (0,1) and (0,1)

---

==conclusion==

$$
\begin{aligned}
x'&=\ ax+by\\
y'&=\ cx+dy\\
\begin{bmatrix}x' \\ y'\end{bmatrix}&=
\begin{bmatrix}a&b\\c&d\end{bmatrix}\ 
\begin{bmatrix}x\\y\end{bmatrix}
\end{aligned}
$$

## Homogeneous coordinates(齐次坐标)

![[2-source-material/images/Pasted image 20250917212456.png]]

seems like we can not write it like $A\mathbf{v}$ 

$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}a&b\\c&d\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}+
\begin{bmatrix}t_x\\t_y\end{bmatrix}
$$

translation is NOT linear transform!

can we use a uniform way to represent all transformations?

---

*add a third dimension*
$$
\begin{aligned}
2d point  = (x,y,\mathbf1)^T \\
2d vector = (x,y,\mathbf0)^T
\end{aligned}
$$

$$
\begin{bmatrix}x'\\y'\\w'\end{bmatrix}=
\begin{bmatrix}
1&0&t_x \\
0&1&t_y \\
0&0&1
\end{bmatrix} \cdot
\begin{bmatrix}x\\y\\1\end{bmatrix} = 
\begin{bmatrix}x+t_x\\y+t_y\\1\end{bmatrix}
$$

why we treat point and vector differently?

vector represent direction-->keep same after translation

v+v->v  
p-p->v  
v-v->v  
p+p->? $\begin{pmatrix}x\\y\\w\end{pmatrix}$ is $\begin{pmatrix}x/w \\ y/w \\1\end{pmatrix},w\neq0$->p1+p2 is the middle point of p1 and p2

## Affine transformations(仿射变换)

affine map = linear map + translation

$$
\begin{pmatrix}x'\\y'\end{pmatrix} = 
\begin{pmatrix}a&b\\c&d\end{pmatrix}\cdot
\begin{pmatrix}x\\y\end{pmatrix}+
\begin{pmatrix}t_x\\t_y\end{pmatrix}
$$

using homogenous coordinates:

$$
\begin{pmatrix}x'\\y'\\1\end{pmatrix}=
\begin{pmatrix}
a&b&t_x\\
c&d&t_y\\
0&0&1\end{pmatrix} \cdot 
\begin{pmatrix}x\\y\\1\end{pmatrix}
$$

*scale*

$$
\mathbf{S}(s_x,s_y) = 
\begin{pmatrix}
s_x&0&0\\
0&s_y&0\\
0&0&1
\end{pmatrix}
$$

*rotation*

$$
\mathbf{R}(\alpha) = 
\begin{pmatrix}
cos\alpha & -sin\alpha & 0 \\
sin\alpha & cos\alpha & 0 \\
0 & 0 &1
\end{pmatrix}
$$

*translation*

$$
\mathbf{T}(t_x,t_y) = 
\begin{pmatrix}
1&0&t_x\\
0&1&t_y\\
0&0&1\\
\end{pmatrix}
$$

affine->the bottom of the matrix is always $(0,0,1)$

## Composing transform

transform ordering maters!

![[2-source-material/images/Pasted image 20250917214459.png]]

because matrix multiple is not commutative

---

$$
A_n(...A_2(A_1(x))) = \mathbf{A_n}\cdot\cdot\cdot\mathbf{A_2}\cdot\mathbf{A_1}\cdot\begin{pmatrix}x\\y\\1\end{pmatrix}
$$

we can pre-multiply n matrices first->improve performance

## Decomposing Transforms

Eigenvalue decomposition

Singular value decomposition

## 3D Transformations

$$
\begin{aligned}
3d\ point  = (x,y,z,0)^T \\
3d\ vector = (x,y,z,1)^T
\end{aligned}
$$

# AI Summarize

## 为什么需要变换？

变换是计算机图形学中的基础概念，应用场景包括：

1. **相机移动：** 在3D场景中移动观察视角
2. **物体方向调整：** 改变物体的朝向和位置
3. **旋转操作：** 使物体绕特定轴旋转
4. **缩放控制：** 调整物体大小比例
5. **3D到2D投影：** 将三维场景映射到二维显示平面

## 2D基本变换

### 缩放变换 (Scale Transformation)

缩放变换通过乘法因子改变物体的大小。

**均匀缩放：**
![[2-source-material/images/Pasted image 20250917205930.png]]

数学表示：
$$
\begin{aligned}
x' = s \cdot x \\
y' = s \cdot y
\end{aligned}
$$

矩阵形式：
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}s & 0 \\0 & s\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

**非均匀缩放：**
![[2-source-material/images/Pasted image 20250917210715.png]]

矩阵形式：
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}s_x & 0 \\0 & s_y\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

其中 $s_x$ 和 $s_y$ 分别是 x 和 y 方向的缩放因子。

### 反射变换 (Reflection Transformation)

反射变换产生物体的镜像效果。

**关于y轴的反射：**
$$
x' = -x ,\ y' = y
$$

矩阵形式：
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}-1&0 \\0 &1\end{bmatrix} 
\begin{bmatrix}x\\y\end{bmatrix}
$$

**其他反射变换：**
- 关于x轴反射：$\begin{bmatrix}1&0\\0&-1\end{bmatrix}$
- 关于原点反射：$\begin{bmatrix}-1&0\\0&-1\end{bmatrix}$

### 切变变换 (Shear Transformation)

切变变换使物体在某一方向上发生倾斜变形。

**水平切变：**
![[2-source-material/images/Pasted image 20250917210945.png]]

数学推导：
- 当 y = 0 时，水平位移为 0
- 当 y = 1 时，水平位移为 a
- 因此：$x' = x + a \cdot y$

矩阵形式：
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}1 & a \\ 0 & 1\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

**垂直切变：**
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}1 & 0 \\ b & 1\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
$$

### 旋转变换 (Rotation Transformation)

旋转变换使物体绕原点旋转特定角度。

**绕原点旋转：**
![[2-source-material/images/Pasted image 20250917211344.png]]

**证明过程：**
考虑点 (1,0) 和 (0,1) 旋转 θ 角度：
- (1,0) → (cosθ, sinθ)
- (0,1) → (-sinθ, cosθ)

因此旋转矩阵为：
$$
\mathbf{R}(\theta) = 
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
$$

**旋转性质：**
- 旋转矩阵是正交矩阵：$\mathbf{R}^{-1} = \mathbf{R}^T$
- 旋转矩阵的行列式为 1
- 保持向量长度和角度不变

## 线性变换的一般形式

$$
\begin{aligned}
x'&=\ ax+by\\
y'&=\ cx+dy\\
\begin{bmatrix}x' \\ y'\end{bmatrix}&=
\begin{bmatrix}a&b\\c&d\end{bmatrix}\ 
\begin{bmatrix}x\\y\end{bmatrix}
\end{aligned}
$$

## 齐次坐标 (Homogeneous Coordinates)

### 问题引入：平移不是线性变换

![[2-source-material/images/Pasted image 20250917212456.png]]

平移变换无法用标准的 2×2 矩阵表示：
$$
\begin{bmatrix}x'\\y'\end{bmatrix} = 
\begin{bmatrix}a&b\\c&d\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}+
\begin{bmatrix}t_x\\t_y\end{bmatrix}
$$

### 齐次坐标的引入

通过增加第三个维度来统一表示所有变换：

**定义：**
- 2D 点：$(x, y, 1)^T$
- 2D 向量：$(x, y, 0)^T$

**平移变换的齐次坐标表示：**
$$
\begin{bmatrix}x'\\y'\\w'\end{bmatrix}=
\begin{bmatrix}
1&0&t_x \\
0&1&t_y \\
0&0&1
\end{bmatrix} \cdot
\begin{bmatrix}x\\y\\1\end{bmatrix} = 
\begin{bmatrix}x+t_x\\y+t_y\\1\end{bmatrix}
$$

### 点和向量的区别

**为什么区分点和向量？**
- 向量表示方向，平移后应该保持不变
- 点表示位置，平移后位置改变

**运算规则：**
- 向量 + 向量 = 向量
- 点 - 点 = 向量
- 点 + 向量 = 点
- 点 + 点 = 中点（通过齐次坐标归一化）

**齐次坐标归一化：**
对于 $\begin{pmatrix}x\\y\\w\end{pmatrix}$，当 $w \neq 0$ 时，对应笛卡尔坐标为 $\begin{pmatrix}x/w \\ y/w \\1\end{pmatrix}$

## 仿射变换 (Affine Transformations)

### 定义

仿射变换 = 线性变换 + 平移变换

标准形式：
$$
\begin{pmatrix}x'\\y'\end{pmatrix} = 
\begin{pmatrix}a&b\\c&d\end{pmatrix}\cdot
\begin{pmatrix}x\\y\end{pmatrix}+
\begin{pmatrix}t_x\\t_y\end{pmatrix}
$$

齐次坐标形式：
$$
\begin{pmatrix}x'\\y'\\1\end{pmatrix}=
\begin{pmatrix}
a&b&t_x\\
c&d&t_y\\
0&0&1\end{pmatrix} \cdot 
\begin{pmatrix}x\\y\\1\end{pmatrix}
$$

### 常见仿射变换的齐次坐标矩阵

**缩放变换：**
$$
\mathbf{S}(s_x,s_y) = 
\begin{pmatrix}
s_x&0&0\\
0&s_y&0\\
0&0&1
\end{pmatrix}
$$

**旋转变换：**
$$
\mathbf{R}(\alpha) = 
\begin{pmatrix}
\cos\alpha & -\sin\alpha & 0 \\
\sin\alpha & \cos\alpha & 0 \\
0 & 0 &1
\end{pmatrix}
$$

**平移变换：**
$$
\mathbf{T}(t_x,t_y) = 
\begin{pmatrix}
1&0&t_x\\
0&1&t_y\\
0&0&1\\
\end{pmatrix}
$$

**仿射变换矩阵的特征：** 底部总是 $(0,0,1)$

## 变换的组合 (Composing Transform)

### 变换顺序的重要性

![[2-source-material/images/Pasted image 20250917214459.png]]

**矩阵乘法不可交换：**
- 先旋转后平移：$\mathbf{T} \cdot \mathbf{R} \cdot \mathbf{v}$
- 先平移后旋转：$\mathbf{R} \cdot \mathbf{T} \cdot \mathbf{v}$

**示例：绕任意点旋转**
要绕点 $P$ 旋转角度 $\theta$，需要：
1. 平移使 $P$ 到原点：$\mathbf{T}(-P_x, -P_y)$
2. 旋转角度 $\theta$：$\mathbf{R}(\theta)$
3. 平移回原位置：$\mathbf{T}(P_x, P_y)$

组合矩阵：$\mathbf{T}(P_x, P_y) \cdot \mathbf{R}(\theta) \cdot \mathbf{T}(-P_x, -P_y)$

### 矩阵预乘优化

$$
A_n(...A_2(A_1(x))) = \mathbf{A_n}\cdot\cdot\cdot\mathbf{A_2}\cdot\mathbf{A_1}\cdot\begin{pmatrix}x\\y\\1\end{pmatrix}
$$

可以预先计算组合矩阵 $\mathbf{M} = \mathbf{A_n}\cdot\cdot\cdot\mathbf{A_2}\cdot\mathbf{A_1}$，然后应用于多个点，提高性能。

## 变换的分解 (Decomposing Transforms)

### 特征值分解 (Eigenvalue Decomposition)

对于方阵 $\mathbf{A}$，可以分解为：
$$
\mathbf{A} = \mathbf{Q}\mathbf{\Lambda}\mathbf{Q}^{-1}
$$

其中：
- $\mathbf{\Lambda}$ 是对角矩阵，包含特征值
- $\mathbf{Q}$ 的列是对应的特征向量

**在图形学中的应用：**
- 特征值表示缩放因子
- 特征向量表示缩放方向
- 用于分析变换的几何特性

### 奇异值分解 (Singular Value Decomposition)

对于任意矩阵 $\mathbf{A}$，可以分解为：
$$
\mathbf{A} = \mathbf{U}\mathbf{\Sigma}\mathbf{V}^T
$$

其中：
- $\mathbf{U}$ 和 $\mathbf{V}$ 是正交矩阵
- $\mathbf{\Sigma}$ 是对角矩阵，包含奇异值

**在图形学中的应用：**
- 将任意线性变换分解为旋转-缩放-旋转
- 用于纹理映射、法线变换等
- 在物理模拟中分析变形

## 3D变换 (3D Transformations)

### 3D齐次坐标

- 3D 点：$(x, y, z, 1)^T$
- 3D 向量：$(x, y, z, 0)^T$

### 3D基本变换矩阵

**3D缩放：**
$$
\mathbf{S}(s_x, s_y, s_z) = 
\begin{pmatrix}
s_x & 0 & 0 & 0 \\
0 & s_y & 0 & 0 \\
0 & 0 & s_z & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

**3D平移：**
$$
\mathbf{T}(t_x, t_y, t_z) = 
\begin{pmatrix}
1 & 0 & 0 & t_x \\
0 & 1 & 0 & t_y \\
0 & 0 & 1 & t_z \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

**3D旋转（绕坐标轴）：**

绕x轴旋转：
$$
\mathbf{R}_x(\theta) = 
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & \cos\theta & -\sin\theta & 0 \\
0 & \sin\theta & \cos\theta & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

绕y轴旋转：
$$
\mathbf{R}_y(\theta) = 
\begin{pmatrix}
\cos\theta & 0 & \sin\theta & 0 \\
0 & 1 & 0 & 0 \\
-\sin\theta & 0 & \cos\theta & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

绕z轴旋转：
$$
\mathbf{R}_z(\theta) = 
\begin{pmatrix}
\cos\theta & -\sin\theta & 0 & 0 \\
\sin\theta & \cos\theta & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
$$

**绕任意轴旋转：**
使用罗德里格斯旋转公式或四元数表示。

## 变换的应用实例

### 视图变换 (Viewing Transformation)
- 模型变换：物体从模型空间到世界空间
- 视图变换：从世界空间到相机空间
- 投影变换：从3D空间到2D投影平面

### 法线变换
法线向量不能直接用模型变换矩阵，需要使用变换矩阵的逆转置：
$$
\mathbf{n}' = (\mathbf{M}^{-1})^T \cdot \mathbf{n}
$$

## 术语表

| 术语 | 英文 | 定义 | 应用/解释 |
|------|------|------|-----------|
| **变换** | Transformation | 改变几何对象位置、方向、形状或大小的数学操作 | 计算机图形学中用于物体移动、旋转、缩放等 |
| **缩放变换** | Scale Transformation | 通过乘法因子改变物体大小的变换 | 均匀缩放保持比例，非均匀缩放在不同方向使用不同因子 |
| **反射变换** | Reflection Transformation | 产生物体镜像的变换，也称为镜像变换 | 关于坐标轴或平面进行反射 |
| **切变变换** | Shear Transformation | 使物体在某一方向上发生倾斜变形的变换 | 保持面积不变，改变形状 |
| **旋转变换** | Rotation Transformation | 绕某点或某轴旋转物体的变换 | 保持距离和角度不变，改变方向 |
| **齐次坐标** | Homogeneous Coordinates | 用n+1维坐标表示n维点的方法 | 统一表示线性变换和平移变换，便于矩阵运算 |
| **仿射变换** | Affine Transformation | 保持直线性和平行性的变换，包括线性变换和平移 | 在计算机图形学中广泛应用，保持几何关系 |
| **线性变换** | Linear Transformation | 满足加法和数乘性质的变换 | 包括缩放、旋转、反射、切变等 |
| **平移变换** | Translation Transformation | 将物体沿特定方向移动固定距离的变换 | 不是线性变换，需要用齐次坐标表示 |
| **特征值分解** | Eigenvalue Decomposition | 将方阵分解为特征向量和特征值的方法 | 分析变换的几何特性，找出主方向 |
| **奇异值分解** | SVD | 将任意矩阵分解为三个矩阵乘积的方法 | 将变换分解为旋转-缩放-旋转，用于各种图形算法 |
| **组合变换** | Composite Transformation | 多个变换按顺序组合形成的复杂变换 | 通过矩阵乘法实现，顺序很重要 |
| **正交矩阵** | Orthogonal Matrix | 满足 $\mathbf{A}^T\mathbf{A} = \mathbf{I}$ 的矩阵 | 旋转变换矩阵是正交矩阵，保持向量长度 |
| **行列式** | Determinant | 方阵的一个标量值，表示线性变换的缩放因子 | 行列式为负表示包含反射，为零表示降维 |
| **视图变换** | Viewing Transformation | 将3D场景变换到2D显示平面的过程 | 包括模型变换、视图变换和投影变换 |
| **法线变换** | Normal Transformation | 变换法线向量的特殊方法 | 使用模型变换矩阵的逆转置，保持法线与表面的垂直关系 |
| **罗德里格斯公式** | Rodrigues' Formula | 计算绕任意轴旋转的公式 | 用于3D旋转的数学表示 |
| **四元数** | Quaternion | 用四个数表示3D旋转的数学对象 | 避免万向节锁，便于旋转插值 |

这份完整的笔记详细展开了原笔记中简略提到的概念，特别是对变换的数学原理、齐次坐标的重要性、变换组合的顺序影响以及高级分解技术进行了深入说明，并提供了全面的术语解释。

# Reference

[slides](https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_03.pdf)

[video](https://www.bilibili.com/video/BV1X7411F744?spm_id_from=333.788.videopod.episodes&vd_source=50767b15cd83989de95f6de6e35f510c&p=3)
