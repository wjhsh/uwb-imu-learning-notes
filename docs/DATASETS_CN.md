# 数据集选择指南

数据集是否有用，取决于它是否提供当前实验需要的输入和参考，不取决于名称里是否同时出现UWB和定位。

| 资源 | 已核对的信息 | 适合什么 | 先确认什么 |
|---|---|---|---|
| [eWINE LOS/NLOS](https://github.com/ewine-project/UWB-LOS-NLOS-Data-Set) | LOS/NLOS信道测量与CIR相关字段 | 传播识别、特征和测距误差分析 | CIR归一化、设备字段、环境划分，不默认有动态IMU |
| [Bregar定位与跟踪](https://github.com/KlemenBr/uwb_positioning) / [Zenodo](https://zenodo.org/record/7629141) | Scientific Data 2023，作者给预处理和定位验证 | CIR测距回归与定位关系 | 先看数据字段、文件体积和原有评价，不与2018集合混名 |
| [IDLab官方数据入口](https://idlab.ugent.be/resources/uwb-positioning-datasets) | ADS-TWR、TDoA、PHY三类资料；TWR为移动机器人工业记录 | 测距修正、时间迁移、动态研究的数据筛选 | 官方入口下有多种数据；逐份核验IMU、姿态、GT同步，不能仅凭IDLab名称认定同一录制 |
| [工业23位置CIR](https://github.com/JaronFontaine/Industrial-UWB-localization-CIR-dataset) | TWR与CIR，23个位置、21个锚点 | 链路误差/信号分析 | 静态位置集合不等于完整动态融合轨迹 |
| [IDLab多环境](https://github.com/JaronFontaine/UWB-dataset-from-an-office-industrial-and-university-environment) | meta/features/CIR，2025 V2修正样本对齐及反归一化 | 分类、误差回归、跨环境泛化 | 版本、索引与波形归一化；保留作者的使用说明 |
| [UTIL](https://utiasdsl.github.io/util-uwb-dataset/) / [解析代码](https://github.com/learnsyslab/util-uwb-dataset) | TDoA室内定位，配套惯性/轨迹与基线资源 | TDoA–IMU融合及锚点几何 | 量测是距离差；锚点对、单位和同步规则与TWR不同 |
| [ISAS-Walk](https://github.com/KIT-ISAS/SFUISE) | SFUISE README提供ToA–inertial运行示例 | 连续时间融合与步行轨迹 | 原版ROS bag、配置和初始化，不与UTIL配置直接互换 |
| [MILUV](https://github.com/decargroup/miluv) | 多无人机UWB与视觉数据devkit | 数据加载、多平台/多传感器研究 | 逐项确认CIR/IMU/姿态/GT和基线使用的视觉、高度信息；测量级结果不能直接外推完整三维定位 |

没有在本轮重新下载或完整回放这些数据集。分享的是公开来源和项目中形成的数据适配经验，不是额外动态轨迹已经验证成功的声明。
