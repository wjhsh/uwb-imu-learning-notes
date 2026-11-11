# 经典方法的具体代码入口

这里直接链接源文件，不搬运第三方实现。所有文件已通过上游Git树核对存在（2026-11-11）；未在本轮声称编译或运行。库的默认分支可能变化，核验快照见[资源记录](../resources/classic_source_paths.json)。

| 方法 | 源码 | 建议先看什么 |
|---|---|---|
| EKF核心更新 | [rlabbe/filterpy / EKF.py](https://github.com/rlabbe/filterpy/blob/master/filterpy/kalman/EKF.py) | 对照predict/update、HJacobian和测量函数的职责 |
| UKF | [rlabbe/filterpy / UKF.py](https://github.com/rlabbe/filterpy/blob/master/filterpy/kalman/UKF.py) | 看sigma点传播；仍需自己定义过程和观测 |
| IMM | [rlabbe/filterpy / IMM.py](https://github.com/rlabbe/filterpy/blob/master/filterpy/kalman/IMM.py) | 看模型混合、似然与概率更新；标准IMM本身不是UWB专属方法 |
| 可视化EKF示例 | [AtsushiSakai/PythonRobotics / extended_kalman_filter.py](https://github.com/AtsushiSakai/PythonRobotics/blob/master/Localization/extended_kalman_filter/extended_kalman_filter.py) | 先读运动模型，再看观测与误差曲线 |
| UKF示例 | [AtsushiSakai/PythonRobotics / unscented_kalman_filter.py](https://github.com/AtsushiSakai/PythonRobotics/blob/master/Localization/unscented_kalman_filter/unscented_kalman_filter.py) | 与同库EKF示例比较非线性传播 |
| 粒子滤波 | [AtsushiSakai/PythonRobotics / particle_filter.py](https://github.com/AtsushiSakai/PythonRobotics/blob/master/Localization/particle_filter/particle_filter.py) | 理解采样、观测权重和重采样 |
| IMU预积分 | [borglab/gtsam / ImuFactorExample.py](https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/ImuFactorExample.py) | 先看预积分量、偏置与IMU因子的连接 |
| IMU与iSAM2 | [borglab/gtsam / ImuFactorISAM2Example.py](https://github.com/borglab/gtsam/blob/develop/python/gtsam/examples/ImuFactorISAM2Example.py) | 看增量求解器如何处理高频IMU和新因子 |
| Huber等鲁棒模型 | [borglab/gtsam / NoiseModel.cpp](https://github.com/borglab/gtsam/blob/develop/gtsam/linear/NoiseModel.cpp) | 先白化残差，再使用鲁棒核；阈值单位不能混用 |
| IMU机械编排 | [gavngao/imu_x_fusion / imu.hpp](https://github.com/gavngao/imu_x_fusion/blob/master/include/sensor/imu.hpp) | 核对旋转、重力、加计和陀螺偏置的传播 |
| NLOS分类训练 | [ewine-project/UWB-localization / build_classification_model.py](https://github.com/ewine-project/UWB-localization/blob/master/NLOSClassificationModel/build_classification_model.py) | 与下一项误差回归分开；老TensorFlow接口需原环境 |
| CIR测距误差回归 | [ewine-project/UWB-localization / build_regression_model.py](https://github.com/ewine-project/UWB-localization/blob/master/RangingErrorModel/build_regression_model.py) | 看输入、标签与误差定义，不只复制网络层数 |
| 测距回归训练 | [KlemenBr/uwb_positioning / train_ranging_error.py](https://github.com/KlemenBr/uwb_positioning/blob/main/technical_validation/train_ranging_error.py) | 2023作者实现，按其数据格式运行 |
| 定位验证 | [KlemenBr/uwb_positioning / positioning.py](https://github.com/KlemenBr/uwb_positioning/blob/main/technical_validation/positioning.py) | 观察测距纠偏如何进入位置求解 |
| 连续时间滑窗 | [KIT-ISAS/SFUISE / SplineFusion.cpp](https://github.com/KIT-ISAS/SFUISE/blob/main/sfuise/src/SplineFusion.cpp) | 配合RA-L 2023论文看样条与窗口更新 |
| 学习惯导滤波 | [CathIAS/TLIO / scekf.py](https://github.com/CathIAS/TLIO/blob/master/src/tracker/scekf.py) | 看相对位移约束与协方差处理，不当作UWB更新 |
| TLIO入口 | [CathIAS/TLIO / main_filter.py](https://github.com/CathIAS/TLIO/blob/master/src/main_filter.py) | 先按作者说明准备数据、训练模型和配置 |
| Student-t滤波参考 | [wmkouw/bayes-filters / kalman_filters.jl](https://github.com/wmkouw/bayes-filters/blob/master/kalman_filters.jl) | 第三方Julia实现；对照其引用的Roth 2013原文，不能冒充作者代码 |

## 鲁棒估计再补两个原理入口

- [Roth等2017 Student-t滤波与平滑](https://arxiv.org/abs/1703.02428)：重点看尺度、协方差与递归近似。
- [SciPy least_squares](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html)：官方接口提供linear、soft_l1、Huber和Cauchy等损失；它是优化器，不是完整的鲁棒UWB–IMU滤波器。

Huber核、Student-t测量分布、Student-t状态滤波是不同层次，不能只替换一个权重就声称复现了同一篇论文。学习时建议先用原始源码的小例子理解，再接自己的传感器观测模型。
