---
title: "OCS2 + ros-control：双足 NMPC / WBC 仿真上手"
description: "基于 OCS2 和 ros-control，用质心动力学 NMPC + WBC 控制双足机器人，在 Gazebo 里跑起来的完整命令顺序，以及 ROS launch 文件的基本写法。"
weight: 3
category: "模型预测控制"
tags: ["MPC", "WBC", "OCS2", "ROS", "Gazebo", "人形机器人"]
---

除了强化学习，我也试了模型的路线：OCS2 + ros-control，控制方法是非线性模型预测控制（NMPC），模型采用质心动力学，下层用全身控制（WBC）分配关节力矩。

代码在 [legged_control](https://github.com/qiayuanl/legged_control)、[hunter_bipedal_control](https://bridgedp.github.io/hunter_bipedal_control)、[livelybot_dynamic_control](https://github.com/HighTorque-Robotics/livelybot_dynamic_control) 的基础上做了一些改进，主要是修改了约束。

## 在 Gazebo 里跑起来

顺序很重要，按下面一步步来：

```bash
# 1. 启动 Gazebo 仿真
roslaunch legged_controllers one_start_gazebo.launch

# 2. 重置状态估计
rostopic pub --once /reset_estimation std_msgs/Float32 "data: 0.0"

# 3. 打开速度指令面板和调参界面
rosrun rqt_robot_steering rqt_robot_steering
rosrun legged_controllers tuning_view.py

# 4. 加载控制器，顺便打印关节力矩
roslaunch legged_controllers load_controller_sim.launch print_joint_torques:=true print_joint_torques_period:=0.2

# 5. 启动控制器，切换到行走
rostopic pub --once /load_controller std_msgs/Float32 "data: 0.0"
rostopic pub --once /set_walk std_msgs/Float32 "data: 0.0"
```

## 顺便：ROS launch 文件怎么读

launch 文件本质是 XML：以 `<?xml version="1.0" ?>` 开头，标签成对出现、可以嵌套。它的作用是批量启动多个相关节点、设置参数、管理节点之间的依赖，也用来控制仿真环境的启动和配置。

常用标签：

| 标签 | 作用 |
| --- | --- |
| `<launch>` | 根标签 |
| `<node>` | 启动一个 ROS 节点 |
| `<arg>` | 定义参数 |
| `<include>` | 包含其他 launch 文件 |
| `<group>` | 给节点分组 |

`<node>` 的常用属性：`pkg`（包名）、`type`（可执行文件）、`name`（节点名）、`args`（传给节点的参数）、`output`（比如 `screen` 表示输出到终端）。

和强化学习路线的对比，见 [足式机器人强化学习与 Sim2Real](../../projects/01-legged-rl-sim2real/index.md)。
