# UWB–IMU 论文与开源代码资料库

整理UWB测距、CIR/NLOS、惯性导航与融合定位研究过程中积累的公开资料。重点是**这篇论文解决什么问题、哪份代码值得看、数据是否适合自己的任务**，而不只是收集链接。

## 从这里开始

| 想找什么 | 入口 | 能得到什么 |
|---|---|---|
| 不清楚有哪些研究方向 | [研究方向指南](docs/RESEARCH_DIRECTIONS_CN.md) | CIR纠偏、可靠性、EKF/ESKF、滑窗、学习惯导和验证设计 |
| 想看已有阅读积累 | [13篇论文笔记](docs/READING_NOTES_CN.md) | 问题、核心思路、实用启发、局限和代码状态 |
| 想直接打开经典方法源码 | [经典代码索引](docs/CLASSIC_CODE_INDEX_CN.md) | EKF、UKF、PF、IMM、Huber、Student-t、预积分的具体文件 |
| 想选一个公开项目复现 | [17个项目的用途比较](docs/OPEN_SOURCE_PROJECTS_CN.md) | 作者代码/第三方实现、依赖、适配成本与阅读顺序 |
| 想找能用的数据 | [数据集指南](docs/DATASETS_CN.md) | 测距级/动态轨迹、TWR/TDoA、CIR和IMU的区别 |
| 复现时结果对不上 | [问题速查](docs/REPRODUCTION_PITFALLS_CN.md) | 项目中积累的坐标、时间、波形、观测类型和鲁棒参数检查方法 |

## 按问题选资料

- **CIR、NLOS与测距误差回归：** Bregar 2018及2023作者代码；Wei的时频识别；Yang的可信度与测距抑制。
- **鲁棒更新和不确定性：** He–Chan的学习增强鲁棒滤波，Roth的Student-t滤波讨论；搭配GTSAM鲁棒模型和第三方实现阅读。
- **UWB–IMU递归融合：** Li的图模型加ESKF，Cheng–Fu的松组合，以及可对照阅读的紧组合项目。
- **滑窗和连续时间：** SFUISE作者代码；Forster预积分与GTSAM IMU示例。它们相关，但不是同一种建模方法。
- **学习式惯性里程计：** TLIO论文与作者代码；它是IMU学习里程计，不是可直接替换的UWB融合系统。

## 推荐的实际入口

1. 刚入门：先看FilterPy配套书，再对照PythonRobotics的EKF源码。
2. 做CIR前端：从Bregar作者仓库的数据说明、分类与回归脚本开始。
3. 做融合后端：先统一Solà的旋转/误差状态约定，再看imu_x_fusion或UWB紧组合代码。
4. 做连续时间或优化：先看SFUISE的观测模型与数据要求，再读窗口求解代码；预积分单独看Forster与GTSAM。

## 这些资料核验到哪一步

- 六篇Measurement/TVT论文已有全文阅读整理；其他条目是相关原理、项目资料或新增推荐，详见笔记。
- 17个外部仓库已核对公开页面/README；经典代码索引中的具体文件通过上游Git树核验存在。**没有把“链接能打开”写成“已复现作者结果”。**
- 自带的[基础合成示例](examples/basic_ekf/README.md)仅作为可选练习，已运行自检和一次演示，不是资料库的主要内容。
- 代码和数据版本会变；部分旧账号已重定向，目录保留现用地址。最后核验：2026-11-11。机器可读记录见[resources](resources/)中的JSON。

## 阅读和复现实用模板

- [论文阅读记录](reading_template.md)
- [小实验记录](experiment_log_template.md)
- [公开范围与第三方许可](OPEN_SOURCE_SCOPE.md)
- 本地目录自检：`python scripts/check_internal_links.py`（不发网络请求）

本仓库不放核心科研实现、训练权重或未发表结果，也不搬运出版社全文和第三方代码。上游论文、代码和数据请分别遵守原作者的引用与许可要求。
