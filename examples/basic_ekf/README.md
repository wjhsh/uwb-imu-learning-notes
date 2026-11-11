# 可选基础仿真

这个独立合成示例用于练习EKF，与目录中的上游科研项目无关。自检和一次演示已实际运行。假定外部提供偏航、已去除重力、已知起点；不是完整惯导或NLOS基线。

在仓库根目录执行：

```bash
python examples/basic_ekf/demo_uwb_imu_ekf.py --self-check
python examples/basic_ekf/demo_uwb_imu_ekf.py --out demo_output
```

依赖见根目录requirements.txt；数学说明见[math_notes.md](math_notes.md)。输出目录必须未存在。
