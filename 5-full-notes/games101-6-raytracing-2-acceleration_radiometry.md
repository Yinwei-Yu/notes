Time:2025-11-11

Tags:[cg](3-tags/cg.md)

# 使用AABB加速光线求交集

## Uniform grids

预处理:

得到一个包围盒
把盒子分成很多小格子
标注和物体相交的格子

先看光线和格子有没有交点,有再和物体进行判断

类似二次索引

格子的数量选取?
C\* 物体数
C约为27

在物体密集场景好用
但是
体育场茶杯问题->物体分布不均匀

# 空间划分

稀疏的地方用不着小的格子

![](2-source-material/images/Pasted%20image%2020251111204958.png)

八叉树:把一个场景切成八份,递归切->不同的停止标准(足够少)
随纬度提升而增加划分数->提出KD树

KD树:一个空间一次沿一个方向分割

BSP树:空间二分,在每个空间选一个方向划分


# KD树

## 数据结构

一个节点:

1. 划分轴
2. 划分方向
3. 孩子
4. 中间节点不存储obj,obj只存储在叶子节点处

## 遍历KD树

![](2-source-material/images/Pasted%20image%2020251111210432.png)

kd树的问题:

1. 难以判断一个物体和盒子相不相交
2. 一个物体和多个盒子相交(重复存储)
# obj partition & BVH(bounding volume hierarchy)

不划分空间而是划分物体

把物体组织成不同部分,重新计算包围盒,递归,直到停止条件,obj只存储在leaf中

问题:bounding box相交->划分需要让重叠部分尽可能小

如何划分node?

1. 选择最长的轴
2. 在中间obj位置处划分(两边物体数量差不多)

数据结构:

算法:

```cpp
Intersect (Ray ray, BVH node) 1

if (ray misses node.bbox) return;

if (node is a leaf node)

test intersection with all objs;
return closest intersection;

hit1 = Intersect (ray, node.child1); hit2 = Intersect (ray, node.child2);

return the closer of hitl, hitz;
```

# 空间划分 vs 物体划分

表格对比here

# 辐射度量学 radiometry

光强为10,10什么?

---

基于几何光学

描述光照
基于光的空间属性

Radiant flux, intensity, irradiance, radiance

## radian energy and flux

rafian energy:电磁辐射能量

Q / J

flux:per unit time

$\phi$ = dQ/dt W/lm(lumen)

others:

![](2-source-material/images/Pasted%20image%2020251111213238.png)

## radian intensity

power per unit solid angle(立体角)

W/sr lm/sr=cd(candela)

---

立体角

θ = l/r

Ω = A/r^2

![](2-source-material/images/Pasted%20image%2020251111213455.png)

---

intensity

光源在某个方向上的亮度

# AI summarize

# 使用AABB加速光线求交集

## Uniform grids 均匀网格法

**预处理流程：**
1. **构建包围盒**：计算整个场景的轴对齐包围盒(AABB)
2. **网格划分**：将包围盒均匀划分为N×N×N个小格子
3. **格子标注**：标记每个与物体相交的格子

**算法执行：**
- 光线首先与网格系统进行求交测试
- 仅在与物体相交的格子中进行光线-物体求交计算
- 类似数据库的二级索引结构，先粗筛后精查

**网格数量优化：**
- 经验公式：格子数量 = C × 物体数量
- 推荐C值约为27（3×3×3）
- 实际应用中需要根据场景复杂度调整

**优缺点分析：**
- **优点**：在物体分布均匀的密集场景中效率很高
- **缺点**：
  - "体育场茶杯问题"：大场景中稀疏分布的小物体导致大量空网格
  - 内存消耗与网格数量成正比
  - 不适合动态场景（网格需要重新构建）

## 空间划分 Spatial Partitioning

针对均匀网格法的缺陷，提出自适应空间划分方法：

![[2-source-material/images/Pasted image 20251111204958.png]]

**八叉树(Octree)：**
- 每次将空间沿三个坐标轴同时分割，产生8个子空间
- 递归分割直到满足停止条件：
  - 空间内物体数量少于阈值（如5个）
  - 空间尺寸小于预设值
  - 达到最大递归深度

**KD树(KD-Tree)：**
- 每次沿单一坐标轴方向分割空间
- 交替选择分割轴（x→y→z循环）
- 分割面为轴对齐平面
- 比八叉树更灵活，适合各向异性场景

**BSP树(Binary Space Partitioning)：**
- 每次用任意方向的平面分割空间
- 理论上最优但实现复杂
- 在2D游戏中广泛应用（如Doom）

# KD树详细解析

## 数据结构

**节点结构：**
```cpp
struct KDNode {
    int split_axis;        // 分割轴：0(x), 1(y), 2(z)
    float split_position;  // 分割位置
    KDNode* left_child;    // 左子树
    KDNode* right_child;   // 右子树
    vector<Object*> objects; // 仅叶子节点存储物体
    AABB bounding_box;     // 节点包围盒
};
```

**构建算法复杂度：**
- 最佳情况：O(n log n)
- 最坏情况：O(n²)
- 平均性能良好

## 遍历KD树

![[2-source-material/images/Pasted image 20251111210432.png]]

**遍历算法伪代码：**
```cpp
Intersection traverse_KDTree(Ray ray, KDNode node) {
    if (!ray.intersect(node.bounding_box)) 
        return null;
    
    if (node.is_leaf) {
        // 叶子节点：与所有物体求交
        return find_closest_intersection(ray, node.objects);
    }
    
    // 决定遍历顺序：先近后远
    float t_split = (node.split_position - ray.origin[node.split_axis]) / ray.direction[node.split_axis];
    KDNode* near_child = (ray.origin[node.split_axis] < node.split_position) ? node.left : node.right;
    KDNode* far_child = (near_child == node.left) ? node.right : node.left;
    
    Intersection near_hit = traverse_KDTree(ray, near_child);
    if (near_hit && near_hit.t < t_split)
        return near_hit;
    
    Intersection far_hit = traverse_KDTree(ray, far_child);
    return choose_closer(near_hit, far_hit);
}
```

## KD树的问题与局限

1. **三角形-包围盒相交判断复杂**：
   - 需要精确判断三角形是否与分割平面相交
   - 一个三角形可能跨越多个叶子节点

2. **存储冗余问题**：
   - 跨越分割平面的物体会被多个叶子节点引用
   - 内存使用效率较低
   - 构建时间较长

3. **动态场景适应性差**：
   - 场景变化需要重建整棵树
   - 不适合实时渲染中的动态物体

# 物体划分与BVH(Bounding Volume Hierarchy)

## 核心思想

不划分空间，而是直接划分物体集合：
1. 将场景物体递归分组
2. 为每个组计算包围盒
3. 形成层次化的包围盒树结构

## 构建算法

**划分策略选择：**
1. **选择分割轴**：选取包围盒最长的维度
2. **分割位置**：选择中位数物体位置，保证左右子树物体数量平衡

**具体实现：**
```cpp
BVHNode* build_BVH(vector<Object*> objects, int depth = 0) {
    if (objects.size() <= LEAF_THRESHOLD) {
        return new BVHLeaf(objects);
    }
    
    // 选择分割轴
    int axis = choose_split_axis(objects);
    
    // 按中位数分割
    sort(objects.begin(), objects.end(), [axis](Object* a, Object* b) {
        return a->centroid[axis] < b->centroid[axis];
    });
    
    auto mid = objects.begin() + objects.size() / 2;
    vector<Object*> left_objs(objects.begin(), mid);
    vector<Object*> right_objs(mid, objects.end());
    
    BVHNode* left = build_BVH(left_objs, depth + 1);
    BVHNode* right = build_BVH(right_objs, depth + 1);
    
    return new BVHInternal(union_AABB(left->bbox, right->bbox), left, right);
}
```

## 遍历算法

```cpp
Intersection Intersect(Ray ray, BVH node) {
    // 快速排除：光线与节点包围盒不相交
    if (ray misses node.bbox) return null;
    
    // 叶子节点：与所有物体求交
    if (node is a leaf node) {
        test intersection with all objs;
        return closest intersection;
    }
    
    // 递归遍历子树
    hit1 = Intersect(ray, node.child1);
    hit2 = Intersect(ray, node.child2);
    
    return the closer of hit1, hit2;
}
```

## BVH的优势

- **无存储冗余**：每个物体只出现在一个叶子节点中
- **构建速度快**：相比KD树构建更高效
- **内存友好**：节点结构简单紧凑
- **适合动态场景**：局部更新相对容易

# 空间划分 vs 物体划分对比

| 特性 | 空间划分(KD树) | 物体划分(BVH) |
|------|----------------|---------------|
| 划分对象 | 空间区域 | 物体集合 |
| 存储效率 | 物体可能重复存储 | 每个物体只存一次 |
| 构建时间 | 相对较慢 | 相对较快 |
| 遍历效率 | 优秀 | 优秀 |
| 动态场景 | 不适合 | 相对适合 |
| 实现复杂度 | 中等 | 简单 |
| 内存占用 | 较高 | 较低 |
| 三角形相交测试 | 复杂 | 简单 |

# 辐射度量学 Radiometry

## 基础概念

**基于几何光学的精确光照描述**：
- 提供物理准确的光照计算框架
- 建立光照传播的数学模型
- 为渲染方程提供理论基础

## 基本物理量

### 辐射能量与辐射通量

**辐射能量(Radiant Energy)**：
- 定义：电磁辐射的能量
- 符号：Q
- 单位：焦耳(J)

**辐射通量(Radiant Flux)**：
- 定义：单位时间内通过某表面的辐射能量
- 符号：Φ = dQ/dt
- 单位：瓦特(W) 或 流明(lm)
- 物理意义：光源的总发射功率

### 辐射强度(Radiant Intensity)

**定义**：单位立体角内的辐射通量
**公式**：$I = \frac{d\Phi}{d\omega}$
**单位**：瓦特/球面度(W/sr) 或 坎德拉(cd, lm/sr)

**物理意义**：描述点光源在特定方向上的发光强度

## 立体角(Solid Angle)详解

### 基本概念

**平面角**：
- 定义：θ = 弧长/半径
- 单位：弧度(rad)

**立体角**：
- 定义：Ω = 投影面积/半径²
- 单位：球面度(sr)

![[2-source-material/images/Pasted image 20251111213455.png]]

### 立体角计算

**微分立体角**：
$d\omega = \frac{dA}{r^2} = \sin\theta d\theta d\phi$

**整个球面的立体角**：
$\Omega_{sphere} = \oint d\omega = 4\pi$ sr

**圆锥立体角**：
$\Omega = 2\pi(1 - \cos\theta_{max})$ sr

## 辐射强度的深入理解

**点光源模型**：
- 假设光源尺寸远小于观察距离
- 在各个方向上可能具有不同的强度
- 常用IES文件描述真实光源的强度分布

**各向同性光源**：
- 在所有方向上强度相等：I(ω) = constant
- 总通量：Φ = 4πI

**方向性光源**：
- 强度随方向变化：I = I(θ, φ)
- 需要定义强度分布函数

---

# 术语表

## AABB (Axis-Aligned Bounding Box)
- **定义**：边与坐标轴平行的长方体包围盒
- **应用领域**：计算机图形学、碰撞检测、光线追踪加速
- **相关概念**：OBB(有向包围盒)、包围球
- **优势**：相交测试计算简单快速

## Uniform Grids (均匀网格)
- **定义**：将空间均匀划分为相同大小的立方体网格
- **应用领域**：空间索引、碰撞检测、流体模拟
- **优缺点**：实现简单但内存效率低，适合均匀分布场景

## Octree (八叉树)
- **定义**：每个节点有8个子节点的空间分割树结构
- **应用领域**：3D图形、医学成像、地理信息系统
- **停止条件**：物体数量阈值、空间尺寸、递归深度

## KD-Tree (k维树)
- **定义**：在k维空间中对数据进行划分的二叉树
- **应用领域**：光线追踪、最近邻搜索、范围查询
- **特点**：交替选择分割维度，适合高维数据

## BSP Tree (二叉空间分割树)
- **定义**：用任意平面递归分割空间的二叉树
- **应用领域**：游戏引擎、隐藏面消除、碰撞检测
- **变体**：轴对齐BSP、多边形对齐BSP

## BVH (Bounding Volume Hierarchy)
- **定义**：基于物体包围盒的层次化树结构
- **应用领域**：光线追踪、碰撞检测、视锥裁剪
- **优势**：无存储冗余、构建快速、内存友好

## Radiometry (辐射度量学)
- **定义**：研究电磁辐射测量的物理学分支
- **应用领域**：计算机图形学、遥感、光学工程
- **核心量**：通量、强度、辐照度、辐射度

## Radiant Flux (辐射通量)
- **定义**：单位时间内通过某表面的辐射能量
- **单位**：瓦特(W)、流明(lm)
- **物理意义**：光源的总发射功率

## Radiant Intensity (辐射强度)
- **定义**：点光源在单位立体角内发射的辐射通量
- **单位**：瓦特/球面度(W/sr)、坎德拉(cd)
- **特点**：描述光源的方向性分布

## Solid Angle (立体角)
- **定义**：锥体所夹的球面面积与半径平方的比值
- **单位**：球面度(sr)
- **计算**：用于量化三维空间中的角度范围

## Candela (坎德拉)
- **定义**：国际单位制中的发光强度单位
- **关系**：1 cd = 1 lm/sr
- **历史**：基于标准蜡烛的光强定义

## Lumen (流明)
- **定义**：光通量单位，描述人眼感知的光功率
- **关系**：1 lm = 1 cd·sr
- **应用**：照明工程中的光通量测量
# Reference
