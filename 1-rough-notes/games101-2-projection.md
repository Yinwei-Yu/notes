Time:2025-09-20

Status: 

- [x] **working** 👨‍💻
- [ ] *done*    💻

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

  y轴的cos角相反?->z叉乘x得到y,而不是x叉乘z,所以要取反.

能否把任意旋转->三个轴旋转?

Euler angle

旋转公式

四元数-万向锁

## view/camera transformation

what?

taking a photo
  arrange people - model
  a good angle to put the camera - view
  Cheese! - projection - 3d to 2d
MVP transformation

how to put the camera?

position $\vec e$
look at/gaze $\hat g$
up direction(相机的向上方向) $\hat t$

相机标准位置:
相机固定位置(0,0,0),往-z看,y为向上方向
然后移动物体

把相机的原位置移到标准位置:
$\vec e$ to origin
g to -z
t to y

the matrix?->基变换矩阵 

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

then how to squish the frustum? $M_{persp->ortho}$?

similar triangle

any point on the near plane will not change
any point's z on the far plane will not change 

so we can get the matrix
## Reference
