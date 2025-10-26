Time:2025-09-20

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/cg|cg]]

## 3d transformation

like in the 2d transformation

use 4x4 matrices for affine transformations

$$\begin{pmatrix}
x^{\prime} \\
y^{\prime} \\
z^{\prime} \\
1
\end{pmatrix}=
\begin{pmatrix}
a & b & c & t_x \\
d & e & f & t_y \\
g & h & i & t_z \\
0 & 0 & 0 & 1
\end{pmatrix}\cdot
\begin{pmatrix}
x \\
y \\
z \\
1
\end{pmatrix}$$

---

about rotate?

$$\begin{gathered}
\mathbf{R}_x(\alpha)=
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & \cos\alpha & -\sin\alpha & 0 \\
0 & \sin\alpha & \cos\alpha & 0 \\
0 & 0 & 0 & 1
\end{pmatrix} \\
\mathbf{R}_y(\alpha)=
\begin{pmatrix}
\cos\alpha & 0 & \sin\alpha & 0 \\
0 & 1 & 0 & 0 \\
-\sin\alpha & 0 & \cos\alpha & 0 \\
0 & 0 & 0 & 1
\end{pmatrix} \\
\mathbf{R}_z(\alpha)=
\begin{pmatrix}
\cos\alpha & -\sin\alpha & 0 & 0 \\
\sin\alpha & \cos\alpha & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
\end{gathered}$$
  
  y轴的cos角相反?->z叉乘x得到y,而不是x叉乘z,所以要取反.

能否把任意旋转转换为三个轴旋转?即用绕xyz三个轴的旋转来模拟任意的三维旋转?

这种绕某个坐标轴旋转的角度叫做Euler angle

这种旋转可以写作:

$$
R_{xyz}(\alpha,\beta,\gamma)=R_x(\alpha)R_y(\beta)R_z(\gamma)
$$

但是这种旋转有一个问题:万向锁

绕任意轴$n$旋转$\alpha$公式:

$$
\mathbf{R}(\mathbf{n}, \alpha) 
= \cos(\alpha)\mathbf{I} 
+ (1 - \cos(\alpha)) \mathbf{n}\mathbf{n}^T 
+ \sin(\alpha) 
\underbrace{\begin{pmatrix}
0 & -n_z & n_y \\
n_z & 0 & -n_x \\
-n_y & n_x & 0
\end{pmatrix}}_{\mathbf{N}}
$$

## view/camera transformation

what?

taking a photo
  arrange people - model
  a good angle to put the camera - view
  Cheese! - projection - 3d to 2d
MVP transformation

---

how to put the camera?

position $\vec e$
look at/gaze $\hat g$
up direction(相机的向上方向) $\hat t$

观察到:*如果所有物体都随相机的移动一起移动,那么相机中的画面不变,所以我们可以把相机从egj放到一个**标准位置***

相机标准位置:
相机固定位置(0,0,0),往-z看,y为向上方向
然后移动物体

把相机的原位置移到标准位置:
$\vec e$ to origin
g to -z
t to y

the matrix $M_{view}$?->基变换矩阵 

$M_{view}=R_{view}T_{view}$

即:先平移把相机移动到世界坐标原点,然后再把三个轴对齐

$$
T_{view} = \begin{bmatrix}
1&0&0&-x_e\\
0&1&0&-y_e\\
0&0&1&-z_e\\
0&0&0&1
\end{bmatrix}
$$

next rotate g to -z , t to Y, (g x t) to  X
how?
consider the **inverse** rotation:X to (g x t),Y to t,Z to -g:

$$ R_{view}^{-1} = \begin{bmatrix} x_{\hat{g} \times \hat{t}} & x_{t} & x_{-g} & 0 \\ y_{\hat{g} \times \hat{t}} & y_{t} & y_{-g} & 0 \\ z_{\hat{g} \times \hat{t}} & z_{t} & z_{-g} & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

we can calculate $R^{-1}_{view}[1,0,0,1]^T$ to verify it

because $R_{view}$ is a orthographic matrix , so it's inverse matrix equals to it's transposition matrix

$$ R_{view} = \begin{bmatrix} x_{\hat{g} \times \hat{t}} & y_{\hat{g} \times \hat{t}} & z_{\hat{g} \times \hat{t}} & 0 \\ x_{t} & y_{t} & z_{t} & 0 \\ x_{-g} & y_{-g} & z_{-g} & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} $$

## Orthographic projection(正交投影)

透视投影->近大远小
正交投影->保持原有平行关系

![[2-source-material/images/Pasted image 20250920162706.png]]

---
a simple way:
1. camera at origin looking at -z ,up at y
2. drop z coordinate(front and back?)
3. translate and scale the resulting rectangle to $[-1,1]^2$

In general:
把空间中的立方体A描述一下:上下左右前后的坐标
把A映射到canonical cube

1. 中心移到原点
2. xyz轴拉伸

matrix?

$$
M_{ortho} = 
\begin{bmatrix}
\frac{2}{r-l} & 0 & 0 & 0 \\
0 & \frac{2}{t-b} & 0 & 0 \\
0 & 0 & \frac{2}{n-f} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
1 & 0 & 0 & -\frac{r+l}{2} \\
0 & 1 & 0 & -\frac{t+b}{2} \\
0 & 0 & 1 & -\frac{n+f}{2} \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

需要注意,因为我们是向-z方向看的,所以near平面的坐标更大

## Perspective Projection

most common
faster are smaller
parallel lines not parallel

first:
(x,y,z,1),(kx,ky,kz,k!=0)->all the same point

---

how?

1. first squish the frustum into a cuboid
2. do orthographic projection

near plane keep all the same
far plane's z keep the same , the central point of far plane keep the same

---

then how to squish the frustum? $M_{persp->ortho}$?

**similar triangle**

![[2-source-material/images/Pasted image 20250926144948.png]]

so are the x and z:

![[2-source-material/images/Pasted image 20250926145029.png]]

then we can write this:

![[2-source-material/images/Pasted image 20250926145054.png]]

next, what's the value of "?"

use extra information:
  any point on the near plane will not change
  any point's z on the far plane will not change 

![[2-source-material/images/Pasted image 20250926145320.png]]

so is the far plane , then we can have the formula:

![[2-source-material/images/Pasted image 20250926145401.png]]

so we can get the matrix:

$$
M_{presp\rightarrow ortho} = 
\begin{pmatrix}
n&0&0&0\\
0&n&0&0\\
0&0&n+f&-nf\\
0&0&1&0
\end{pmatrix}
$$

and finally the persp matrix:

$$M_{persp}=M_{ortho}M_{persp\rightarrow ortho}$$

## Reference

[slide](https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_04.pdf)