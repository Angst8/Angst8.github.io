---
title: "从 Isaac Gym 到 Isaac Sim 5.1：强化学习环境搭建记录"
description: "Isaac Gym Preview 的 conda 安装、humanoid-gym 的训练 / 回放 / Sim2Sim 命令，以及用 pip 安装 Isaac Sim 5.1 和 Isaac Lab。"
weight: 2
category: "环境搭建"
tags: ["Isaac Gym", "Isaac Sim", "Isaac Lab", "强化学习", "Ubuntu"]
---

足式机器人强化学习的主力平台已经从 Isaac Gym 转到 Isaac Sim / Isaac Lab。两套环境的安装与验证步骤都在下面，可以直接复用。

## Isaac Gym（Preview）

我的环境：Ubuntu 20.04、Python 3.8、CUDA 12.9。

```bash
conda create -n isaac python=3.8
conda activate isaac
```

从 [NVIDIA 官网](https://developer.nvidia.com/isaac-gym) 下载 `IsaacGym_Preview_Package.tar.gz`，解压后安装 Python 包：

```bash
tar -xzvf IsaacGym_Preview_Package.tar.gz -C ~/
cd ~/IsaacGym/python
pip install -e .
```

<figure markdown="span">
  ![Isaac Gym 训练界面](i03_isaacgym.jpg){ loading=lazy }
  <figcaption>Isaac Gym 训练界面</figcaption>
</figure>

## humanoid-gym 常用命令

基于开源的 humanoid-gym 训练人形机器人时，常用的就这几条：

```bash
# 训练（无界面，4096 个并行环境）
python scripts/train.py --task=humanoid_ppo --run_name v1 --headless --num_envs 4096

# 回放训练好的策略
python humanoid/scripts/play.py --task=humanoid_ppo --run_name v1

# Sim2Sim：把导出的策略放进 MuJoCo 里验证
python humanoid/scripts/sim2sim.py --load_model logs/XBot_ppo/exported/policies/policy_example.pt

# 看训练曲线
tensorboard --logdir logs --port 6006
```

本地的任务包用 `pip install -e .` 装进当前 conda 环境，改代码不用重装。训练曲线怎么读，见 [TensorBoard 曲线怎么读、PPO 怎么调](../tensorboard-ppo/index.md)。

## Isaac Sim 5.1 + Isaac Lab（pip 安装）

Isaac Sim 5.1 可以直接用 pip 装，不需要再下 Omniverse Launcher。参考 [Isaac Lab 官方安装文档](https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/pip_installation.html)：

```bash
conda create -n env_isaaclab python=3.11
conda activate env_isaaclab
pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com
pip install -U torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
isaacsim   # 第一次启动，确认能打开
```

然后克隆 Isaac Lab，安装依赖和 RL 框架：

```bash
sudo apt install cmake build-essential
./isaaclab.sh --install            # 或 ./isaaclab.sh -i
./isaaclab.sh --install rl_games   # 按需安装 rl_games
```
