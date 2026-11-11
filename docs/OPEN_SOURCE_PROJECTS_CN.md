# 开源项目怎么选

核验日期2026-11-11。以下均核对了README；未在本轮安装、编译或训练。作者配套项目与第三方实现分开标明。完整元数据见[repositories.json](../resources/repositories.json)。

## 先学经典估计方法

| 项目 | 最值得看什么 | 使用边界 |
|---|---|---|
| [FilterPy](https://github.com/rlabbe/filterpy) | KF/EKF/UKF/IMM的可读Python实现 | 通用估计库，需要自己定义UWB观测、输入和数据协议 |
| [Kalman and Bayesian Filters in Python](https://github.com/rlabbe/Kalman-and-Bayesian-Filters-in-Python) | 从直觉到代码的Notebook教材 | 配套FilterPy，适合补基础；书与代码许可应分别看原库 |
| [PythonRobotics](https://github.com/AtsushiSakai/PythonRobotics) | EKF、UKF、粒子滤波等小型示例 | 教学示例，不是现成UWB科研基线 |
| [GTSAM](https://github.com/borglab/gtsam) | 因子图、IMU预积分、iSAM2和鲁棒噪声 | C++/Python接口与版本需匹配，需自行构造UWB因子 |
| [bayes-filters](https://github.com/wmkouw/bayes-filters) | Julia版KF、Student-t与变分滤波 | 第三方个人实现；不是Roth作者官方完整代码 |

## 直接关联测距与CIR

| 项目 | 和论文的关系 | 建议入口及成本 |
|---|---|---|
| [eWINE UWB-localization](https://github.com/ewine-project/UWB-localization) | Bregar与Mohorčič 2018论文作者项目 | 分类、测距回归、定位评价分别看；旧TensorFlow环境需隔离，检查子目录许可 |
| [uwb_positioning](https://github.com/KlemenBr/uwb_positioning) | Bregar 2023数据论文作者项目 | 先看technical_validation/positioning.py，再看训练脚本；README有Docker和数据空间要求 |
| [UWB-LOS-NLOS-Data-Set](https://github.com/ewine-project/UWB-LOS-NLOS-Data-Set) | 作者公开的LOS/NLOS测量数据与解析资料 | 适合识别/CIR特征；不默认包含动态IMU轨迹 |
| [IDLab工业CIR](https://github.com/JaronFontaine/Industrial-UWB-localization-CIR-dataset) | README关联2020测距误差纠正论文 | 23个位置的测量集合；适合信号与误差研究，不能直接称动态UWB–IMU数据 |
| [IDLab多环境CIR](https://github.com/JaronFontaine/UWB-dataset-from-an-office-industrial-and-university-environment) | README关联迁移学习论文 | 核对2025 CIR V2修订与样本对齐，适合跨环境测距研究 |

## 融合后端和学习惯导

| 项目 | 类型与技术 | 适合借鉴什么 |
|---|---|---|
| [SFUISE](https://github.com/KIT-ISAS/SFUISE) | RA-L 2023作者代码，连续时间UWB–IMU样条滑窗 | 原版README是ROS Noetic/Ubuntu20.04，含UTIL和ISAS-Walk入口；不要混用其他组织的重写版本 |
| [Tightly Coupled UWB–IMU Fusion](https://github.com/i-ASL/Tightly_Coupled_UWB-IMU_Fusion) | 公开参考实现，README列EKF/ESKF/UKF/LIEKF | 对照多种姿态/误差状态更新；未核验为某篇论文的官方实现，许可证元数据未给出 |
| [imu_x_fusion](https://github.com/gavngao/imu_x_fusion) | 社区通用融合项目，含ESKF/IEKF/UKF/MAP | 从IMU传播和误差定义入手；原cggos地址已重定向。主接口是GNSS/里程计，不是原生UWB距离 |
| [robot_localization](https://github.com/cra-ros-pkg/robot_localization) | ROS通用非线性估计节点 | 学ROS消息、配置与坐标系；原始UWB距离不能默认直接当Pose输入，需观测适配 |
| [TLIO](https://github.com/CathIAS/TLIO) | RA-L 2020作者补充代码，学习式惯性里程计 | 看网络相对运动、协方差和滤波接口；README要求数据格式与训练，不是下载即可输出UWB位置 |
| [UTIL devkit](https://github.com/learnsyslab/util-uwb-dataset) | UWB TDoA数据解析与基线资源 | 原utiasDSL地址已重定向；TDoA需要锚点对差分观测模型 |
| [MILUV devkit](https://github.com/decargroup/miluv) | 多无人机UWB与视觉数据配套工具 | 先看数据加载和传感器字段，完整基线使用哪些传感器要逐项核对 |

## 使用前只核对最重要的几项

先确认量测类型和单位、传感器输入、初始化与坐标约定，再确认原环境和许可证。GitHub API的NOASSERTION或空license并不等于可以任意复制，需看原仓库文件。此处只提供索引，不把第三方代码重新发布为本仓库MIT代码。
