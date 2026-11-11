# 文献阅读笔记（UWB 定位与惯性融合）

前六篇来自已经整理的全文阅读材料；随后是研究过程中查阅的数学、惯性与鲁棒估计资料，并补充了本次核验的论文配套项目。每条保留问题、方法和个人阅读判断。阅读笔记不等同于完成作者实验复现。

## 1. A Learning-Enhanced Robust Adaptive Fading Extended/Error-State Kalman Filter for Integrated IMU-UWB Indoor Localization Under NLOS Reception

- **作者/年份/出处：** He M.、Chan S. C.；2026；*IEEE Transactions on Vehicular Technology* 75(6), 9462–9478。
- **链接：** <https://doi.org/10.1109/TVT.2025.3648547>
- **问题：** NLOS 量测会让 IMU–UWB 融合滤波出现偏差和不一致，固定噪声模型难以适应环境变化。
- **核心方法：** 以学习模块辅助鲁棒自适应渐消 EKF/ESKF，在 NLOS 条件下调节滤波增益与噪声假设。
- **实用启发：** 把“异常检测”和“滤波器自适应”连起来读，注意自适应量是否由可在线获得的残差驱动。
- **限制/追问：** 学习部分依赖训练分布；需看跨环境表现、协方差一致性和与同输入基线的比较。
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 2. Robust indoor localization via spatiotemporal graph modeling and adaptive error state Kalman filtering using ultra-wideband and inertial measurement unit

- **作者/年份/出处：** Li X. 等；2026；*Measurement* 284, 122246。
- **链接：** <https://doi.org/10.1016/j.measurement.2026.122246>
- **问题：** 室内 NLOS、锚点几何和 IMU 漂移共同导致定位不稳，单一时刻的测量处理不足。
- **核心方法：** 用时空图刻画测量与节点关系，再把自适应 ESKF 用于 UWB–IMU 状态更新。
- **实用启发：** 图结构可以组织历史与邻域信息；阅读时区分图学习本身与滤波增益调整各自贡献。
- **限制/追问：** 图的构建是否依赖已知布局？跨房间迁移和计算开销如何？
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 3. An adaptive Kalman filter loosely coupled indoor fusion positioning system based on inertial navigation system and ultra-wide band

- **作者/年份/出处：** Cheng L.、Fu Z.；2025；*Measurement* 244, 116412。
- **链接：** <https://doi.org/10.1016/j.measurement.2024.116412>
- **问题：** INS 单独积分会漂移，UWB 位置又受 NLOS 与跳变影响，松组合需要在线调节可信度。
- **核心方法：** INS 机械编排提供预测，UWB 位置作量测，并用自适应 Kalman 滤波调整噪声或增益。
- **实用启发：** 适合建立离散滤波的工程直觉：预测、量测、更新、异常处理和初始化分别做什么。
- **限制/追问：** 松组合丢弃了部分距离几何信息；需看 UWB 位置跳变时如何检测，以及参数迁移性。
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 4. A decoupled backend optimizer for UWB localization in NLOS environments

- **作者/年份/出处：** Lu C.等；2026；*Measurement* 276, 121494。
- **链接：** <https://doi.org/10.1016/j.measurement.2026.121494>
- **问题：** NLOS 异常量测会污染整体后端优化，联合求解时一处错误可能拖累全部状态。
- **核心方法：** 以虚拟前后向迭代过程构造解耦后端优化器，并分析误差传播与收敛。
- **实用启发：** 解耦是一种计算与稳健性取舍；应检查拆分后是否仍保留足够的锚点几何约束。
- **限制/追问：** 解耦假设何时失效？初始化、异常比例和锚点布局变化时是否稳定？
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 5. A novel credibility evaluation and mitigation for ranging measurement in UWB localization

- **作者/年份/出处：** Yang H.等；2025；*Measurement* 256, 117721。
- **链接：** <https://doi.org/10.1016/j.measurement.2025.117721>
- **问题：** 仅凭 LOS/NLOS 标签不足以描述测距质量，错误量测需要可量化的可信度和抑制策略。
- **核心方法：** 细分测距传播状态，结合学习方法进行可信度评价与测距误差抑制。
- **实用启发：** 可信度应能预测误差而非只复述标签；可用于加权、门限或后端鲁棒核。
- **限制/追问：** 可信度是否概率校准？阈值跨场景是否稳定？与“只做分类”相比增益来自哪里？
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 6. NLOS identification using parallel deep learning model and time-frequency information in UWB-based positioning system

- **作者/年份/出处：** Wei J.等；2022；*Measurement* 195, 111191。
- **链接：** <https://doi.org/10.1016/j.measurement.2022.111191>
- **问题：** UWB 在遮挡下接收波形变化复杂，单一时域或人工特征难以稳定判别 NLOS。
- **核心方法：** 用并行深度学习模型融合时频与 CIR 信息，输出 LOS/NLOS 识别结果。
- **实用启发：** 是理解“波形特征如何服务分类”的入口；分类之后仍需单独的误差改正或加权环节。
- **限制/追问：** 分类准确率不等于定位精度；需看类别不平衡、跨环境泛化和误删 LOS 的代价。
- **阅读与代码状态：** 已整理全文阅读笔记；尚未核验作者配套实现。

## 7. Quaternion kinematics for the error-state Kalman filter

- **作者/年份/出处：** Joan Solà；2017；作者公开稿（arXiv）。
- **链接：** <https://arxiv.org/abs/1711.02508>
- **问题：** 姿态与旋转误差不满足普通向量加法，直接线性化容易产生公式和实现错误。
- **核心方法：** 系统整理四元数运动学、误差状态定义、雅可比与扰动更新，作为 ESKF 推导参考。
- **实用启发：** 实现前先统一旋转约定、误差定义和左右扰动，能避免大多数符号与坐标系错误。
- **限制/追问：** 它是数学教程，不含 UWB 实验；需自行补观测模型、噪声标定与一致性检验。
- **阅读与代码状态：** 已查阅的理论/相关方法资料，未完成整套作者实验复现。

## 8. On-Manifold Preintegration for Real-Time Visual–Inertial Odometry

- **作者/年份/出处：** Christian Forster, Luca Carlone, Frank Dellaert, Davide Scaramuzza；2017；*IEEE Transactions on Robotics* 33(1), 1–21。
- **链接：** <https://doi.org/10.1109/TRO.2016.2597321>
- **问题：** 视觉–惯性优化中反复积分高频 IMU 代价高，bias 更新还会使已有积分失效。
- **核心方法：** 在流形上预积分 IMU 相对运动，并提供 bias 一阶修正与协方差传播。
- **实用启发：** 预积分把“高频积分”变成可复用的相对因子，是滑窗/因子图实现的数学基础。
- **限制/追问：** 这是视觉–惯性工作，不是 UWB 论文；用于 UWB 时仍需设计测距因子与异常处理。
- **阅读与代码状态：** 已查阅的理论/相关方法资料，未完成整套作者实验复现。

## 9. TLIO: Tight Learned Inertial Odometry

- **作者/年份/出处：** Liu W. 等；2020；*IEEE Robotics and Automation Letters* 5(4), 5653–5660。
- **链接：** <https://doi.org/10.1109/LRA.2020.3007421>；项目页: <https://cathias.github.io/TLIO/>；[作者GitHub](https://github.com/CathIAS/TLIO)；[作者GitHub](https://github.com/CathIAS/TLIO)
- **问题：** 传统惯性里程计会漂移，希望网络从 IMU 序列学习运动增量并提供可用不确定性。
- **核心方法：** 用学习模型从 IMU 序列回归短窗相对位移及其不确定性，并用滤波框架约束长期轨迹。
- **实用启发：** 可把学习式惯性模块视为相对运动来源；融合前要检查输出不确定性和坐标系约定。
- **限制/追问：** 它是 IMU-only，不是 UWB 融合；设备、步态和采样率变化会带来域偏移。
- **阅读与代码状态：** 已查阅的理论/相关方法资料，未完成整套作者实验复现。

## 使用说明

这些笔记用于建立共同术语和阅读路线，不是这些工作的完整复现记录。需要引用方法或数字时回到论文原文；需要代码时参见[经典代码索引](CLASSIC_CODE_INDEX_CN.md)与[开源项目比较](OPEN_SOURCE_PROJECTS_CN.md)。若后续补充公开数据集或作者代码，应同时记录版本、许可证和实际运行结果。

## 10. Continuous-Time Ultra-Wideband-Inertial Fusion

- **作者与出处：** Kailai Li、Ziyu Cao、Uwe D. Hanebeck；IEEE RA-L 8(7), 4338–4345，2023。DOI [10.1109/LRA.2023.3281932](https://doi.org/10.1109/LRA.2023.3281932)。
- **论文与代码：** [作者稿](https://arxiv.org/abs/2301.09033)；[SFUISE](https://github.com/KIT-ISAS/SFUISE)。
- **问题与方法：** 用连续时间样条表示运动，以滑窗拟合处理异步UWB与IMU观测。
- **值得借鉴：** 观察时间连续表示、异步测距残差和窗口求解如何连接。不要把样条滑窗、预积分和普通递归EKF当成同一种实现。
- **状态：** 本次核验论文与README对应关系、原版ROS Noetic依赖及UTIL/ISAS-Walk示例；未编译复现。

## 11. Improving Indoor Localization Using Convolutional Neural Networks on Computationally Restricted Devices

- **作者与出处：** Klemen Bregar、Mihael Mohorčič；IEEE Access 6, 17429–17441，2018。DOI [10.1109/ACCESS.2018.2817800](https://doi.org/10.1109/ACCESS.2018.2817800)。
- **作者代码：** [UWB-localization](https://github.com/ewine-project/UWB-localization)。
- **问题与方法：** 使用原始CIR学习NLOS类别及测距误差，研究信号信息如何减少定位误差。
- **值得借鉴：** 同时查看分类脚本和误差回归脚本，区分两种监督目标；比较环境划分与输入归一化，不能把分类准确率当成纠偏效果。
- **状态：** 与项目所用CIR研究资料相关；本次核验作者README、论文引用与实际源文件入口，未在本次重跑旧TensorFlow训练。

## 12. Indoor UWB Positioning and Position Tracking Data Set

- **作者与出处：** Klemen Bregar；Scientific Data 10, 744，2023。DOI [10.1038/s41597-023-02639-5](https://doi.org/10.1038/s41597-023-02639-5)。
- **作者代码：** [uwb_positioning](https://github.com/KlemenBr/uwb_positioning)；[数据](https://zenodo.org/record/7629141)。
- **问题与方法：** 发布UWB定位/跟踪数据，并给出预处理、CNN误差估计与定位验证程序。
- **值得借鉴：** 从数据格式和technical_validation目录入手，把测距预测、定位求解和评价分开。数据论文中的验证代码可以作为入口，但不能据此假定任意IMU融合所需字段齐全。
- **状态：** 本次核验README、数据论文与训练/定位脚本路径；未重新下载或执行全套实验。

## 13. Robust Bayesian Filtering and Smoothing Using Student's t Distribution

- **作者与出处：** Michael Roth、Tohid Ardeshiri、Emre Özkan、Fredrik Gustafsson；2017作者稿。[arXiv:1703.02428](https://arxiv.org/abs/1703.02428)。
- **问题与方法：** 讨论重尾过程/测量噪声下的Student-t滤波和平滑，以及使递归计算可行所需的近似。
- **值得借鉴：** 看清Student-t尺度矩阵和协方差的区别，以及矩匹配可能产生的行为；“采用Student-t”不等于实现了同一个滤波器。
- **相关代码：** [bayes-filters](https://github.com/wmkouw/bayes-filters)提供第三方Julia实现，并引用Roth等2013年的Student-t滤波论文；它不是该2017稿的作者官方完整复现。
- **状态：** 新补充的原文/实现入口，核验摘要及仓库说明，未运行第三方实现。
