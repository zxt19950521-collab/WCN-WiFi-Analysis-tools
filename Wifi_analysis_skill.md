# WiFi 故障分析技能文档

## 概述

此技能用于分析 Android 设备的 WiFi 故障，通过解析特定文件夹下的日志文件（如 main log 和 kernel log），提供全面的 WiFi 故障分析功能。递归查找提供目录下的所有`main_log_*`, `sys_log_*`, 或者`logcat 文件`

## 功能特性

### 1. 日志解析与脱水

- 提取 WiFi 相关的关键日志信息
- 去除冗余内容，保留关键事件

### 2. 连接流程分析

以时间为轴绘制 WiFi 连接流程，包括：

- **Auth（认证）**
- **Assoc（关联）**
- **握手过程**：显示1/4、2/4、3/4、4/4握手状态
- **DHCP 流程**

### 3. 断链流程分析

- 识别并可视化 WiFi 断链事件及其原因
- 显示详细的SSID、MAC地址和reason code

### 4. 异常连接检测

- 自动检测异常连接过程
- 用红色标记异常事件

### 5. 时间轴交互

- 使用Plotly库生成可交互的HTML图表
- 支持缩放时间轴
- 查看具体时间点的详细信息和整体连接断链的时间分布

### 6. 信号强度分析

- 绘制 WiFi RSSI 信号强度变化图
- 显示最小、最大、平均RSSI值

### 7. 速率分析

- 绘制实时吞吐速率和协商速率图

### 8. 极速互传分析

- 分析 P2P 连接相关事件
- 识别极速互传失败的原因

### 9. TAG分类分析

- 基于《WIFI问题分析红宝书》的TAG分类
- 自动为事件添加TAG标签
- 生成TAG统计分析

### 10. 多格式报告生成

- 自动生成Markdown格式的分析报告
- 自动生成HTML格式的分析报告
- 将图表嵌入到HTML报告中

***

## TAG分类体系

基于《WIFI问题分析红宝书》，WiFi故障分析使用以下TAG分类：

| TAG           | 描述         | 关键日志特征                                                  |
| ------------- | ---------- | ------------------------------------------------------- |
| `开关`          | WiFi开关相关事件 | `setWifiEnabled`, `Starting AIDL supplicant`            |
| `扫描`          | WiFi扫描相关事件 | `startScan`, `Scan completed`                           |
| `连接`          | WiFi连接相关事件 | `connect uid`, `Trying to associate`, `Associated with` |
| `DHCP`        | DHCP流程相关事件 | `DhcpClient`, `DHCPACK`, `DHCP Discover`                |
| `热点`          | 热点/SAP相关事件 | `SoftAp`, `hostapd`                                     |
| `P2P`         | P2P连接相关事件  | `p2p0`, `P2P-GROUP`                                     |
| `极速互传`        | 极速互传相关事件   | `AirTransfer`, `NearP2pManager`                         |
| `功耗`          | 功耗相关事件     | `Power Save`, 电源管理相关                                    |
| `上网`          | 网络连接质量相关   | `mtk_cfg80211_get_station`, `rssi`, `frequency`         |
| `自动回连&WIFI切换` | 自动回连和切换相关  | `WifiNetworkSelector`, `WifiConnectivityManager`        |

***

## 关键日志分析

### 开关

```
WifiService: setWifiEnabled package=com.android.settings
wpa_supplicant: Starting AIDL supplicant
wpa_supplicant: Successfully initialized wpa_supplicant
wpa_supplicant: Initializing interface 'wlan0'
```

### 扫描

- 包含扫描管控逻辑的相关日志

### 连接

```
WifiService: connect uid=
wpa_supplicant: wlan0: Trying to associate with
mtk_cfg80211_connect
wpa_supplicant: nl80211: BSS Event 127 (NL80211_BSS_EVENT_ASSOCIATED)
wpa_supplicant: wlan0: Associated with
```

### DHCP

```
D/DhcpClient: Discover (xid=0x12345678)
D/DhcpClient: Renewing address 192.168.1.1
setprop log.tag.DhcpClient VERBOSE
D/DhcpClient: Received packet: DHCPACK
```

### 热点

```
wifiservices
WifiNative: Failed to start softAp Hal
SoftApManager
SoftApManager[unknown]: Soft AP is stopped
```

### P2P

```
P2P-GROUP-STARTED p2p0 GO
p2p0: CTRL-EVENT-CONNECTED
P2P-GROUP-REMOVED p2p0 GO
p2p0: AP-STA-DISCONNECTED
onWifiStateChanged: State:
TransConnect:startP2p: start p2p go
TransConnect:onCreateGroupSuccess
TransConnect:WIFI_P2P_PEERS_CHANGED_ACTION:
TransConnect:Group Client IP address
wpa_supplicant: wlan0:
wpa_supplicant: p2p0:
TransConnect:disconnectP2p:
```

### 极速互传

```
AirTransfer-AIotCenterSDKManager:
wlan0: state
p2p0: state
connectto
Set freq
NearP2pManager:
p2p0:    selected BSS
Add group with config Role
Scan results matching the currently selected network
onDefaultCapabilitiesChanged
DhcpClient:
hostapd_logger
WifiUtil: TransConnect:getValidWifiChannel
now connect
```

### 功耗

- 包含Power Save过程分析的相关日志

### 上网

```
mtk_cfg80211_get_station
rssi
frequency
kalPerMonUpdate
wlanLinkQualityMonitor
```

### 自动回连 & WIFI切换

```
WifiNetworkSelector
WifiConnectivityManager
wifiservice
wpa_supplicant
tranwifismartassistant
```

***

## 使用方法

### 基本使用

```python
from wifi_analysis_with_tags import WifiLogAnalyzerWithTags

# 创建分析器实例
analyzer = WifiLogAnalyzerWithTags("/path/to/log/directory")

# 执行分析
analyzer.analyze()

# 生成图表
analyzer.plot_connection_timeline()
analyzer.plot_connection_process()

# 生成报告
analyzer.generate_markdown_report()
analyzer.generate_html_report()
```

### 日志文件支持

技能会自动识别并处理以下格式的日志文件：

- `mainlogcat-log.xxx` - 主日志文件
- `kernellogcat-log.xxx` - 内核日志文件
- `main_log_*` - 主日志文件（替代格式）
- `kernel_log_*` - 内核日志文件（替代格式）
- 支持 `.gz` 压缩格式的日志文件，会自动解压后分析

***

## 输出结果

### 1. 连接/断链事件时间线

- 可视化展示所有连接和断链事件
- 按时间顺序排列
- 显示事件类型和详细信息

### 2. RSSI 信号强度变化图

- 实时信号强度变化曲线
- 显示最小、最大、平均RSSI值
- 支持交互式查看

### 3. 速率变化图

- 实时吞吐速率变化
- 协商速率变化
- 支持交互式查看

### 4. 关键事件详细信息

- 每个事件的详细描述
- 时间戳、事件类型、消息内容
- TAG分类信息

### 5. TAG统计分析

- 各TAG的事件数量统计
- TAG分布图表
- 帮助快速定位问题类型

### 6. 故障原因分析

- 基于红宝书经验的故障定位
- 可能的原因列表
- 建议的解决方案

***

## 适用场景

- WiFi 连接不稳定
- 频繁断网
- 连接速度慢
- 认证失败
- 漫游问题
- 极速互传失败
- 其他 WiFi 相关故障排查

***

## 分析流程

1. **日志收集**：获取Android设备的main log和kernel log
2. **日志过滤**：使用关键日志进行过滤，提取WiFi相关信息
3. **TAG分类**：根据日志内容为每个事件添加TAG标签
4. **时间轴构建**：以时间为轴整理连接、认证、关联、握手、DHCP等流程
5. **故障识别**：根据关键日志和时间轴分析，识别可能的故障原因
6. **可视化分析**：生成信号强度、速率等变化图表
7. **故障定位**：结合红宝书中的经验，定位具体故障点

***

## 平台支持

- 通用平台
- MTK平台
- SPRD平台

***

## 配置文件

### TAG配置文件 (tag\_config.json)

```json
{
  "tags": [
    "开关",
    "扫描",
    "连接",
    "DHCP",
    "热点",
    "P2P",
    "极速互传",
    "功耗",
    "上网",
    "自动回连&WIFI切换"
  ],
  "version": "1.0",
  "description": "WiFi故障分析TAG配置"
}
```

***

## 技术实现

### 核心类：WifiLogAnalyzerWithTags

#### 主要方法

| 方法                           | 功能             |
| ---------------------------- | -------------- |
| `load_tags()`                | 加载TAG配置文件      |
| `find_log_files()`           | 递归查找日志文件       |
| `extract_gz()`               | 解压.gz压缩文件      |
| `parse_main_log()`           | 解析主日志文件        |
| `parse_kernel_log()`         | 解析内核日志文件       |
| `get_event_tags()`           | 根据日志内容为事件添加TAG |
| `analyze()`                  | 执行完整分析流程       |
| `plot_connection_timeline()` | 生成连接时间轴图表      |
| `plot_connection_process()`  | 生成连接过程图表       |
| `generate_markdown_report()` | 生成Markdown格式报告 |
| `generate_html_report()`     | 生成HTML格式报告     |

***

## 依赖库

- `plotly` - 用于生成交互式图表
- `pandas` - 用于数据处理
- `gzip` - 用于解压压缩文件
- `re` - 用于正则表达式匹配
- `datetime` - 用于时间处理
- `json` - 用于配置文件处理

***

## 报告示例

### Markdown报告结构

```markdown
# WiFi 故障分析报告

## 基本信息
- 分析类型
- 测试场景
- 测试结果
- 日志来源
- 日志时间

## TAG分析
- 各TAG事件数量统计

## 【案例匹配】
- 匹配的案例类型
- 匹配原因

## 【问题现象】
- 时间、现象、TAG

## 【关键发现汇总】
- 详细的事件分析

## 【环境信息】
- WiFi信息
- 信号强度统计

## 【问题原因总结】
- 根因分析
- 可能的原因列表

## 【流程总结】
- 完整的流程时间线

## 【图表】
- 信号强度与速率分析
- 连接时间轴
- 连接过程分析
```

***

## 更新日志

### v1.0

- 初始版本发布
- 支持基本的WiFi日志分析
- 实现TAG分类功能
- 支持Markdown和HTML报告生成

***

## 参考资料

- 《WIFI问题分析红宝书》
- Android WiFi框架文档
- wpa\_supplicant文档
- MTK/SPRD平台WiFi驱动文档

