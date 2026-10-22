---
template: home.html
description: 个人网站：运动控制算法、足式机器人项目作品与技术笔记。
hide: [navigation, toc]
hero:
  image: assets/img/hero_bg.jpg
  eyebrow: 运动控制算法工程师
  title: 让足式机器人<br>从仿真走进现实
  lead: 从 LQR、VMC 的经典控制，到 PPO、AMP 强化学习与 Sim2Real 实机部署。RoboMaster 轮腿平衡步兵运动控制负责人，先后在两家人形机器人公司做运动控制算法实习。
  buttons:
    - label: 查看项目
      link: projects/
    - label: 技术笔记
      link: notes/
  badges:
    - label: GitHub
      value: Angst8
      link: https://github.com/Angst8
      color: "#5b6b7d"
---

<div class="zr-stats">
<div><b>2 次</b><span>全国赛二等奖</span><small>RoboMaster 机甲大师</small></div>
<div><b>2 次</b><span>区域赛一等奖</span><small>RoboMaster 机甲大师</small></div>
<div><b>3 项</b><span>发明专利申请</span><small>其中 1 项第一发明人</small></div>
<div><b>2 段</b><span>人形机器人实习</span><small>人形机器人 · 算法实习</small></div>
</div>

<figure class="zr-video">
  <video src="assets/video/showreel.mp4" autoplay loop muted playsinline preload="auto"></video>
  <figcaption><strong>作品合集</strong> · 人形强化学习、轮腿平衡机器人、RoboMaster 步兵与嵌入式小车</figcaption>
</figure>

## 我在做什么

<div class="grid cards zr-features" markdown>

-   :material-scale-balance: **运动控制**

    二级倒立摆建模、LQR、VMC 五连杆解算，以及单片机上的离线 MPC。

    [:octicons-arrow-right-24: 轮腿平衡机器人](projects/02-wheel-legged-balance/index.md)

-   :material-brain: **强化学习**

    Isaac Gym 大规模并行训练、AMP 动作模仿、Teacher-Student 蒸馏。

    [:octicons-arrow-right-24: 足式机器人 RL](projects/01-legged-rl-sim2real/index.md)

-   :material-chip: **嵌入式与部署**

    STM32 / FreeRTOS / CAN，Jetson Orin 上的 C++ 与 ONNX Runtime 推理。

    [:octicons-arrow-right-24: RoboMaster 步兵](projects/05-mecanum-infantry/index.md)

-   :material-tools: **工具与开源**

    浏览器端的 URDF 校验与自动修复，减少仿真「启动即爆炸」。

    [:octicons-arrow-right-24: URDF Validator](projects/08-urdf-validator/index.md)

</div>

## 项目作品

<!-- zr:projects -->

## 最近更新

<!-- zr:recent 6 -->

[全部笔记 :octicons-arrow-right-24:](notes/index.md){ .md-button }
