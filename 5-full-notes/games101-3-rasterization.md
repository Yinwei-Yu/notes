Time:2025-10-11

Status: 

- [ ] **working** 👨‍💻
- [x] *done*    💻

Tags:[[3-tags/cg|cg]]

## Finishing up viewing

透视投影->正交投影

aspect ratio = width/height

field-of-view 视角

t = |n|tan(fovY/2)
aspect = r/t

after mvp?

物体在\[-1,1]^3
接下来要画到屏幕上

## Canonical Cube to Screen

array of pixels
resolution

raster=drawing onto the screen

pixel is a little square with uniform color

**screen space**

(0,0) to (width-1,height-1)

pixel(x,y) is centered at (x+0.5,y+0.5)

忽略z,\[-1,1]^2 to \[0,width],\[0,height]

![[2-source-material/images/Pasted image 20251011081639.png]]

上面的矩阵称为视口变换,注意屏幕中心要变

## drawing machine

cathode ray tube->示波器,阴极射线管 CRT
逐行扫描-隔行扫描

frame buffer:memory for a raster display

LCD display->液晶,光的偏转

LED 发光二极管

electrophoretic 墨水屏

## drawing to screen

triangle meshes

why triangles?
most basic
  break up other polygons
unique properties
  guaranteed to be planar
  well-defined interior
  Well-defined method for interpolating values at
vertices over triangle (barycentric interpolation)

a simple approach - sampling

discretize a function by sampling

sample if each pixel's center is inside the triangle
inside(tri,x,y)
how to implented?
三个叉积,判断点是否在三条边的同一侧(同负,同正)

on the edge? 没规定

减少光栅化像素数?
取三角形的bounding box,减少光栅化数量
每行取最左最上

## Raster on real screen

bayer pattern--more green because human eye more sense to green light

how about jaggies(aliasing)?

## Antialiasing

sampling artifacts(error/mistake/inaccuracies)
  aliasing
  moirem pattern
  wagon wheel effect
-> all because signal changing too fast but sampled too slowly

---

blurring before sampling->why can?

frequencies cos2πfx

fourier transform 时域->频域

滤波->去掉一些频率

高通滤波,低通滤波

filtering = convolution

冲激函数

aliasing = 频谱重叠

解决?
  提高采样率
  反走样,模糊->采样

## Z-buffering

用一个z-buffer来存储像素点的"深度"信息
z值小的离我们近,反之远(和向-z观察正好相反,这里是为了简化)
离我们近的绘制在屏幕上,反之不绘制,代码流程为:

```c
for (each triangle T)

    for (each sample (x,y,z) in T)

        if (2 < zbuffer[x,y]) //closest sample so far

            framebuffer[x,y] = rgb; //update color

            zbuffer[x,y] = z; //update depth

        else
            ; //do nothing, this sample is occluded
```
## Reference
