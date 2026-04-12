---
name: "wifi-fault-analysis"
description: "解析特定文件夹下的android log，如main log和kernel log，进行log脱水，绘制以时间为轴的连接 auth assoc 握手 dhcp流程和断链流程，缩放时间轴查看具体时间和整体连接断链的时间分布，绘制wifi rssi的信号强度变化图和实时吞吐速率和协商速率图。在用户需要解析log的时候触发。"
---

# WiFi 故障分析工具

## 功能描述

此技能用于分析 Android 设备的 WiFi 故障，通过解析特定文件夹下的日志文件（如 main log 和 kernel log），提供以下功能：

1. **日志解析与脱水**：提取 WiFi 相关的关键日志信息，去除冗余内容
2. **连接流程分析**：以时间为轴绘制 WiFi 连接流程，包括：
   - Auth（认证）
   - Assoc（关联）
   - 握手过程（显示1/4、2/4、3/4、4/4握手状态）
   - DHCP 流程
3. **断链流程分析**：识别并可视化 WiFi 断链事件及其原因，显示详细的SSID、MAC地址和reason code
4. **异常连接检测**：自动检测异常连接过程，用红色标记异常事件
5. **时间轴交互**：使用Plotly库生成可交互的HTML图表，支持缩放时间轴，查看具体时间点的详细信息和整体连接断链的时间分布
6. **信号强度分析**：绘制 WiFi RSSI 信号强度变化图
7. **速率分析**：绘制实时吞吐速率和协商速率图
8. **极速互传分析**：分析 P2P 连接相关事件，识别极速互传失败的原因
9. **多格式报告生成**：自动生成Markdown和HTML格式的分析报告，将图表嵌入到HTML报告中

## 使用方法

当用户需要分析 WiFi 相关的故障时，调用此技能。用户需要提供：

1. 包含 Android 日志文件的文件夹路径
2. 感兴趣的时间范围（可选）
3. 特定的 WiFi SSID（可选）

### 日志文件支持

技能会自动识别并处理以下格式的日志文件：
- `mainlogcat-log.xxx` - 主日志文件
- `kernellogcat-log.xxx` - 内核日志文件
- 支持 `.gz` 压缩格式的日志文件，会自动解压后分析

技能将处理日志文件，生成分析报告和可视化图表，帮助用户快速定位 WiFi 故障原因。

## 输出结果

- 连接/断链事件时间线
- RSSI 信号强度变化图
- 速率变化图
- 关键事件详细信息
- 可能的故障原因分析

## 适用场景

- WiFi 连接不稳定
- 频繁断网
- 连接速度慢
- 认证失败
- 漫游问题
- 极速互传失败
- 其他 WiFi 相关故障排查

## 关键日志分析

根据《WIFI问题分析红宝书》，以下是各分类的关键日志信息：

### 开关
- `WifiService: setWifiEnabled package=com.android.settings`
- `wpa_supplicant: Starting AIDL supplicant`
- `wpa_supplicant: Successfully initialized wpa_supplicant`
- `wpa_supplicant: Initializing interface 'wlan0'`

### 扫描
- 包含扫描管控逻辑的相关日志

### 连接
- `WifiService: connect uid=`
- `wpa_supplicant: wlan0: Trying to associate with`
- `mtk_cfg80211_connect`
- `wpa_supplicant: nl80211: BSS Event 127 (NL80211_BSS_EVENT_ASSOCIATED)`
- `wpa_supplicant: wlan0: Associated with`

### DHCP
- `D/DhcpClient: Discover (xid=0x12345678)`
- `D/DhcpClient: Renewing address 192.168.1.1`
- `setprop log.tag.DhcpClient VERBOSE`
- `D/DhcpClient: Received packet: DHCPACK`

### 热点
- `wifiservices`
- `WifiNative: Failed to start softAp Hal`
- `SoftApManager`
- `SoftApManager[unknown]: Soft AP is stopped`

### P2P
- `P2P-GROUP-STARTED p2p0 GO`
- `p2p0: CTRL-EVENT-CONNECTED`
- `P2P-GROUP-REMOVED p2p0 GO`
- `p2p0: AP-STA-DISCONNECTED`
- `onWifiStateChanged: State:`
- `TransConnect:startP2p: start p2p go`
- `TransConnect:onCreateGroupSuccess`
- `TransConnect:WIFI_P2P_PEERS_CHANGED_ACTION:`
- `TransConnect:Group Client IP address`
- `wpa_supplicant: wlan0:`
- `wpa_supplicant: p2p0:`
- `TransConnect:disconnectP2p:`

### 极速互传
- `AirTransfer-AIotCenterSDKManager:`
- `wlan0: state`
- `p2p0: state`
- `connectto`
- `Set freq`
- `NearP2pManager:`
- `p2p0:    selected BSS`
- `Add group with config Role`
- `Scan results matching the currently selected network`
- `onDefaultCapabilitiesChanged`
- `DhcpClient:`
- `hostapd_logger`
- `WifiUtil: TransConnect:getValidWifiChannel`
- `now connect`

### 功耗
- 包含Power Save过程分析的相关日志

### 上网
- `mtk_cfg80211_get_station`
- `rssi`
- `frequency`
- `kalPerMonUpdate`
- `wlanLinkQualityMonitor`

### 自动回连 & WIFI切换
- `WifiNetworkSelector`
- `WifiConnectivityManager`
- `wifiservice`
- `wpa_supplicant`
- `tranwifismartassistant`

## 分析流程

1. **日志收集**：获取Android设备的main log和kernel log
2. **日志过滤**：使用关键日志进行过滤，提取WiFi相关信息
3. **时间轴构建**：以时间为轴整理连接、认证、关联、握手、DHCP等流程
4. **故障识别**：根据关键日志和时间轴分析，识别可能的故障原因
5. **可视化分析**：生成信号强度、速率等变化图表
6. **故障定位**：结合红宝书中的经验，定位具体故障点

## 平台支持

- 通用平台
- MTK平台
- SPRD平台

## 测试与分析流程

### 测试步骤
1. **准备测试日志**：创建包含模拟WiFi日志的测试目录
2. **运行分析脚本**：执行测试脚本分析日志文件
3. **生成报告**：自动生成包含图表和详细分析的Markdown报告

### 分析输出
- **连接时间轴**：展示何时连接到哪个WiFi网络
- **连接过程分析**：详细的连接步骤（认证、关联、握手、DHCP等）
- **信号强度与速率分析**：RSSI和传输速率变化图表
- **事件时间线**：所有WiFi相关事件的详细列表
- **连接分析**：每个连接的详细信息（SSID、BSSID、时间、状态）
- **断连分析**：断连事件和原因
- **信号强度分析**：最小、最大、平均RSSI值
- **结论**：基于分析结果的总结

### 示例命令
```bash
# 运行测试分析
python3 test_wifi_analysis.py

# 查看生成的报告
open test_wifi_logs/wifi_analysis_report.md
```

## 技能集成

此技能已集成以下功能：
1. **日志解析**：自动解析main log和kernel log中的WiFi相关信息
2. **数据提取**：提取连接、认证、关联、握手、DHCP等关键事件
3. **可视化分析**：生成连接时间轴、连接过程、信号强度和速率变化图表
4. **报告生成**：自动生成包含详细分析的Markdown报告
5. **故障定位**：基于红宝书中的经验，定位具体故障点

当用户提供WiFi日志目录时，技能将自动执行上述分析步骤，生成完整的故障分析报告。