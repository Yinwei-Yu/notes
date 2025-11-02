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

# AI Summarize

## 3D变换 (3D Transformation)

### 3D变换矩阵基础

与2D变换类似，3D变换使用4×4矩阵进行仿射变换，在齐次坐标下统一表示：

$$
\begin{pmatrix}
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
\end{pmatrix}
$$

其中：
- 左上角3×3子矩阵表示线性变换（旋转、缩放、切变）
- 右侧3×1列向量表示平移变换
- 底部行固定为(0,0,0,1)

### 3D旋转变换

**绕坐标轴旋转矩阵：**

绕x轴旋转：
$$\begin{gathered}
\mathbf{R}_x(\alpha)=
\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & \cos\alpha & -\sin\alpha & 0 \\
0 & \sin\alpha & \cos\alpha & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
\end{gathered}$$

绕y轴旋转：
$$\begin{gathered}
\mathbf{R}_y(\alpha)=
\begin{pmatrix}
\cos\alpha & 0 & \sin\alpha & 0 \\
0 & 1 & 0 & 0 \\
-\sin\alpha & 0 & \cos\alpha & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
\end{gathered}$$

绕z轴旋转：
$$\begin{gathered}
\mathbf{R}_z(\alpha)=
\begin{pmatrix}
\cos\alpha & -\sin\alpha & 0 & 0 \\
\sin\alpha & \cos\alpha & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}
\end{gathered}$$

**y轴旋转矩阵的特殊性：**
y轴旋转矩阵中sin项的符号与其他两个旋转矩阵相反。这是因为在右手坐标系中：
- x轴：y × z = x
- z轴：x × y = z  
- y轴：z × x = y（不是x × z）

因此绕y轴旋转的矩阵形式与其他两个轴不同。

### 欧拉角 (Euler Angles)

**定义：** 用绕三个坐标轴的旋转角度来表示任意三维旋转。

**旋转顺序表示：**
$$
R_{xyz}(\alpha,\beta,\gamma)=R_x(\alpha)R_y(\beta)R_z(\gamma)
$$

其中α、β、γ分别是绕x、y、z轴的旋转角度。

**万向锁问题 (Gimbal Lock)：**
当第二个旋转角度β = ±90°时，第一个旋转轴和第三个旋转轴重合，导致失去一个旋转自由度。

**示例：**
当β = 90°时，R_x(α)R_y(90°)R_z(γ) = R_x(α+γ)R_y(90°)，无法区分α和γ的单独贡献。

### 绕任意轴旋转

**罗德里格斯旋转公式 (Rodrigues' Rotation Formula)：**
绕单位向量轴$\mathbf{n}$旋转角度$\alpha$的矩阵：

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

其中：
- $\mathbf{I}$是3×3单位矩阵
- $\mathbf{n}\mathbf{n}^T$是外积矩阵
- $\mathbf{N}$是叉乘矩阵，满足$\mathbf{N}\mathbf{v} = \mathbf{n} \times \mathbf{v}$

## 视图/相机变换 (View/Camera Transformation)

### MVP变换概念

类比拍照过程：
- **模型变换 (Model)：** 安排人物位置 → 物体在世界坐标系中的位置
- **视图变换 (View)：** 寻找好的拍摄角度 → 相机位置和方向
- **投影变换 (Projection)：** 按下快门 → 3D到2D投影

### 相机参数定义

- **位置 (Position)：** $\vec e = (x_e, y_e, z_e)$
- **观察方向 (Gaze Direction)：** $\hat g$（单位向量）
- **向上方向 (Up Direction)：** $\hat t$（单位向量）

### 标准相机位置

**关键观察：** 如果所有物体都随相机一起移动，相机看到的画面不变。

**标准位置：**
- 相机位置：(0, 0, 0)
- 观察方向：-z轴
- 向上方向：y轴

### 视图变换矩阵推导

视图变换矩阵：$M_{view} = R_{view}T_{view}$

**平移矩阵：**
将相机从$\vec e$平移到原点：
$$
T_{view} = \begin{bmatrix}
1&0&0&-x_e\\
0&1&0&-y_e\\
0&0&1&-z_e\\
0&0&0&1
\end{bmatrix}
$$

**旋转矩阵推导：**
目标：将相机坐标系对齐到标准坐标系
- $\hat{g} \times \hat{t}$ → X轴
- $\hat{t}$ → Y轴  
- $-\hat{g}$ → Z轴

考虑逆变换：将标准坐标系的基向量旋转到相机坐标系：
$$
R_{view}^{-1} = \begin{bmatrix} 
x_{\hat{g} \times \hat{t}} & x_{t} & x_{-g} & 0 \\ 
y_{\hat{g} \times \hat{t}} & y_{t} & y_{-g} & 0 \\ 
z_{\hat{g} \times \hat{t}} & z_{t} & z_{-g} & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

由于旋转矩阵是正交矩阵，$R_{view}^{-1} = R_{view}^T$，因此：
$$
R_{view} = \begin{bmatrix} 
x_{\hat{g} \times \hat{t}} & y_{\hat{g} \times \hat{t}} & z_{\hat{g} \times \hat{t}} & 0 \\ 
x_{t} & y_{t} & z_{t} & 0 \\ 
x_{-g} & y_{-g} & z_{-g} & 0 \\ 
0 & 0 & 0 & 1 
\end{bmatrix}
$$

**验证：** 计算$R^{-1}_{view}[1,0,0,1]^T$应该得到$(x_{\hat{g} \times \hat{t}}, y_{\hat{g} \times \hat{t}}, z_{\hat{g} \times \hat{t}}, 1)^T$

## 正交投影 (Orthographic Projection)

### 基本概念

**正交投影特性：**
- 保持平行关系不变
- 无近大远小效果
- 投影线互相平行

**透视投影特性：**
- 近大远小
- 平行线在投影中可能相交

### 正交投影实现方法

**简单方法：**
1. 相机位于原点，看向-z方向，向上为y方向
2. 丢弃z坐标（但保留用于深度测试）
3. 将结果矩形平移缩放至$[-1,1]^2$

**通用方法：**
将任意视景体映射到规范立方体$[-1,1]^3$

**视景体参数：**
- 左/右：l, r
- 下/上：b, t  
- 近/远：n, f

**注意：** 由于相机看向-z方向，近平面z坐标值更大（n > f）

### 正交投影矩阵

**步骤：**
1. 平移视景体中心到原点
2. 缩放为规范立方体

**平移矩阵：**
$$
T_{ortho} = \begin{bmatrix}
1 & 0 & 0 & -\frac{r+l}{2} \\
0 & 1 & 0 & -\frac{t+b}{2} \\
0 & 0 & 1 & -\frac{n+f}{2} \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**缩放矩阵：**
$$
S_{ortho} = \begin{bmatrix}
\frac{2}{r-l} & 0 & 0 & 0 \\
0 & \frac{2}{t-b} & 0 & 0 \\
0 & 0 & \frac{2}{n-f} & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
$$

**完整正交投影矩阵：**
$$
M_{ortho} = S_{ortho}T_{ortho} = 
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

## 透视投影 (Perspective Projection)

### 基本概念

**透视投影特性：**
- 最常见投影方式
- 近大远小效果
- 平行线在投影中不再平行

**齐次坐标性质：**
$(x,y,z,1)$和$(kx,ky,kz,k)$（$k \neq 0$）表示同一点

### 透视投影实现方法

**两步法：**
1. 将视锥体挤压成立方体：$M_{persp→ortho}$
2. 进行正交投影：$M_{ortho}$

**约束条件：**
- 近平面上的点保持不变
- 远平面z坐标不变，中心点保持不变

### 相似三角形原理

![[2-source-material/images/Pasted image 20250926144948.png]]

根据相似三角形：
$$
\frac{y'}{y} = \frac{n}{z} \Rightarrow y' = \frac{n}{z}y
$$

同理：
$$
x' = \frac{n}{z}x
$$

### 透视投影矩阵推导

**目标矩阵形式：**
寻找矩阵$M_{persp→ortho}$使得：
$$
\begin{pmatrix}
x' \\ y' \\ z' \\ w'
\end{pmatrix}
= M_{persp→ortho} \cdot
\begin{pmatrix}
x \\ y \\ z \\ 1
\end{pmatrix}
= 
\begin{pmatrix}
nx \\ ny \\ ? \\ z
\end{pmatrix}
$$

**z坐标约束：**
利用近平面和远平面的约束条件：

近平面(z=n)：任意点(x,y,n,1)变换后z坐标应为n
远平面(z=f)：中心点(0,0,f,1)变换后z坐标应为f

设第三行为(A,B,C,D)，则：
$$
z' = Ax + By + Cz + D
$$

**近平面约束：**
对于(x,y,n,1)，变换后：
$$
\frac{Ax + By + Cn + D}{n} = n
\Rightarrow Ax + By + Cn + D = n^2
$$

由于x,y任意，A=0, B=0，得：
$$
Cn + D = n^2
$$

**远平面约束：**
对于(0,0,f,1)，变换后：
$$
\frac{Cf + D}{f} = f
\Rightarrow Cf + D = f^2
$$

**解方程组：**
$$
\begin{cases}
Cn + D = n^2 \\
Cf + D = f^2
\end{cases}
\Rightarrow
\begin{cases}
C = n + f \\
D = -nf
\end{cases}
$$

**透视到正交变换矩阵：**
$$
M_{persp\rightarrow ortho} = 
\begin{pmatrix}
n & 0 & 0 & 0 \\
0 & n & 0 & 0 \\
0 & 0 & n+f & -nf \\
0 & 0 & 1 & 0
\end{pmatrix}
$$

**完整透视投影矩阵：**
$$
M_{persp} = M_{ortho}M_{persp\rightarrow ortho}
$$

### 矩阵验证

**近平面点验证：**
对于近平面点(x,y,n,1)：
$$
M_{persp→ortho} \cdot \begin{pmatrix}x\\y\\n\\1\end{pmatrix} = \begin{pmatrix}nx\\ny\\n^2\\n\end{pmatrix} \Rightarrow \begin{pmatrix}x\\y\\n\\1\end{pmatrix}
$$

**远平面中心点验证：**
对于远平面中心点(0,0,f,1)：
$$
M_{persp→ortho} \cdot \begin{pmatrix}0\\0\\f\\1\end{pmatrix} = \begin{pmatrix}0\\0\\f^2\\f\end{pmatrix} \Rightarrow \begin{pmatrix}0\\0\\f\\1\end{pmatrix}
$$

## 应用与扩展

### 深度值非线性分布
透视投影后的深度值在规范化设备坐标中呈非线性分布，近处精度高，远处精度低。

### 视锥体裁剪
在透视除法之前进行裁剪，可以避免除以零和数值不稳定问题。

### 投影矩阵的实际应用
在OpenGL和DirectX等图形API中，都提供了构建投影矩阵的函数，如：
- `glm::perspective()`（GLM库）
- `XMMatrixPerspectiveFovLH()`（DirectX Math）
# Reference

[slide](https://sites.cs.ucsb.edu/~lingqi/teaching/resources/GAMES101_Lecture_04.pdf)