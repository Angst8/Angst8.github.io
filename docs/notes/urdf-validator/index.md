---
title: "开源了一个浏览器里的 URDF 体检工具"
description: "仿真一启动机器人就爆炸，十有八九是 URDF 的问题。于是写了 URDF Validator：25+ 条校验规则、8 个自动修复，全部在浏览器里跑。"
weight: 1
category: "开源工具"
tags: ["开源", "URDF", "Isaac Sim", "MuJoCo", "Pyodide"]
---

做强化学习时最烦的一类问题：模型导进 Isaac Sim 或 MuJoCo，一启动机器人就抖、飞、爆炸。查到最后，往往是 URDF 里某个惯量矩阵不正定、关节上下限写反，或者 SolidWorks 导出时单位用了 kg·mm²。

于是写了 [URDF Validator](https://github.com/Angst8/urdf-validator)：拖进一个 URDF，几秒钟告诉你哪里有问题，能修的直接修好。

<div class="zr-repo" markdown>

[:fontawesome-brands-github: Angst8/urdf-validator](https://github.com/Angst8/urdf-validator){ .zr-repo__name }

浏览器端的 URDF 校验与自动修复：25+ 条规则、8 个自动修复，Python 规则引擎经 Pyodide 在本地运行，零后端。

</div>

## 它会检查什么

25 条以上的规则，分 6 类：

- **Structure**：XML 是否合法、必填字段、运动学树是否连通。
- **Inertia**：质量正负、惯量矩阵正定、三角不等式、单位是否合理、质心是否落在 mesh 包围盒内。
- **Joint**：上下限反转、轴向量未归一化、类型非法、缺失 dynamics。
- **Mesh**：STL 能否解析、面数过高、碰撞体是否凸、visual 是否直接复用 collision。
- **Collision**：零姿态下非相邻 link 的包围盒相交——这是仿真启动即爆炸的常见原因。
- **Material**：未定义的材质引用、缺 color / texture。

## 能自动修什么

8 个修复器里，最有用的是这几个：

- `inertia_units`：把 kg·mm² 换算成 kg·m²（×1e-6），专治 SolidWorks 导出。
- `inertia_pd`：对惯量矩阵做特征分解，钳制负特征值，再按三角不等式重建；修不好就逐级放宽安全因子，最后用各向同性惯量兜底。
- `swap_limits` / `axis_normalize`：交换反转的上下限、归一化关节轴。
- `inject_dynamics` / `inject_materials`：补默认阻尼摩擦、注入 14 种常见工业材质。

## 为什么放在浏览器里

校验引擎是纯 Python，用 Pyodide 跑在 WebWorker 里，不需要后端，也不用装环境。前端用 Three.js 画运动学树并按问题严重程度着色，能渲染 ZIP 包里的真实 STL；Monaco Editor 显示 XML，问题直接高亮到行。最后一键「自动修复并下载」。

也可以在命令行里用：

```bash
cd packages/core
python -m urdf_validator.cli robot.urdf                             # 校验
python -m urdf_validator.cli robot.urdf --fix --output fixed.urdf   # 修复
```

核心引擎有 40 个单元测试，MIT 协议开源。欢迎提 issue。
