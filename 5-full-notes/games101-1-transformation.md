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

## Reference

[slides](https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_03.pdf)

[video](https://www.bilibili.com/video/BV1X7411F744?spm_id_from=333.788.videopod.episodes&vd_source=50767b15cd83989de95f6de6e35f510c&p=3)
