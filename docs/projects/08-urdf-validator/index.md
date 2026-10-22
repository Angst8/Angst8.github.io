---
title: "URDF Validator"
description: "开源 · 浏览器端 URDF 校验与自动修复 · Pyodide + Three.js"
category: "开源工具"
weight: 8
tags: ["开源", "URDF", "Python", "Pyodide", "Three.js", "Isaac Sim", "MuJoCo"]
---

<div class="zr-repo" markdown>

[:fontawesome-brands-github: Angst8/urdf-validator](https://github.com/Angst8/urdf-validator){ .zr-repo__name }

浏览器端的 URDF 校验与自动修复：25+ 条规则、8 个自动修复，Python 规则引擎经 Pyodide 在本地运行，零后端。

</div>

| 角色 | 关键技术 |
| --- | --- |
| 作者 | Python · Pyodide · WebWorker · React · Three.js · Monaco Editor |

为 Isaac Sim / ROS2 / MuJoCo 强化学习工作流写的 URDF 校验 + 自动修复工具。浏览器原生运行（Pyodide + WebWorker），零后端；拖入 `.urdf` 或带 mesh 的 `.zip`，就能看到问题列表、3D 运动学树和高亮到行的 XML。

## 校验：25+ 规则，6 类

| 类别 | 检查内容 |
| --- | --- |
| Structure | XML 合法性、必填字段、运动学树连通性 |
| Inertia | 质量正负、惯量矩阵正定、三角不等式、单位合理性、质心在 mesh 包围盒内 |
| Joint | limit 反转、axis 归一化、type 合法性、缺失 dynamics |
| Mesh | STL 可解析性、面数过高、碰撞体凸包性、visual 与 collision 是否相同 |
| Collision | 零姿态下非相邻 link 包围盒相交（防止仿真一启动就爆炸） |
| Material | 未定义引用、缺少 color / texture |

## 自动修复：8 个 fixer

- `axis_normalize`：关节轴向量归一化
- `swap_limits`：交换反转的上下限
- `inertia_units`：kg·mm² → kg·m² 换算（×1e-6）
- `inject_dynamics`：给转动 / 平移关节注入默认阻尼和摩擦
- `inertia_pd`：特征分解 → 钳制负特征值 → 按三角不等式重建（五级安全因子降级 + 各向同性兜底）
- `mass_abs`：负质量取绝对值
- `inject_materials`：注入 14 种工业材质（钢、铝、塑料、橡胶、碳纤维等）

## 架构

```text
packages/
├── core/   Python 校验 / 修复引擎（engine · rules · fixer · materials · cli，40 个单元测试）
└── web/    React + Three.js + Monaco，Pyodide 在 WebWorker 内运行 Python 引擎
```

开发背景和设计思路写在了博客里：[浏览器里的 URDF 体检工具](../../notes/urdf-validator/index.md)。
