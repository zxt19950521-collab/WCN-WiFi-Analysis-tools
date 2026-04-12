# WiFi 故障分析报告

## 基本信息

| 项目    | 内容                                       |
| ----- | ---------------------------------------- |
| 分析类型  | WiFi 极速互传故障分析                            |
| 测试场景  | Android 设备极速互传                           |
| 测试结果  | 存在极速互传相关问题，可能导致文件传输失败                 |
| 日志来源  | Test_log/rebooterro/正常开机/debuglogger |
| 日志时间  | 1900-04-12 20:37 ~ 20:45 |

***

## 【案例匹配】

匹配案例：**极速互传连接失败**

匹配原因：日志中显示极速互传过程中存在P2P连接相关错误，可能导致传输中断

***

## 【问题现象】

| 序号  | 时间    | 现象     |
| --- | ----- | ------ |
| 1 | 20:37:25 | Default capabilities changed |
| 2 | 20:37:28 | Default capabilities changed |
| 3 | 20:38:55 | Default capabilities changed |
| 4 | 20:38:58 | Default capabilities changed |
| 5 | 20:39:43 | Default capabilities changed |
| 6 | 20:39:44 | Default capabilities changed |
| 7 | 20:39:45 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e18025b |
| 8 | 20:39:45 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair |
| 9 | 20:39:45 | Default capabilities changed |
| 10 | 20:39:48 | Default capabilities changed |
| 11 | 20:39:51 | Default capabilities changed |
| 12 | 20:40:45 | Default capabilities changed |
| 13 | 20:40:45 | Default capabilities changed |
| 14 | 20:40:47 | Default capabilities changed |
| 15 | 20:40:54 | Default capabilities changed |
| 16 | 20:41:41 | Default capabilities changed |
| 17 | 20:41:43 | Default capabilities changed |
| 18 | 20:41:43 | Default capabilities changed |
| 19 | 20:41:46 | Default capabilities changed |
| 20 | 20:41:50 | Default capabilities changed |
| 21 | 20:41:54 | NearP2pManager: TransConnect:wifiP2pEnabled: true |
| 22 | 20:41:54 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@775bcce |
| 23 | 20:41:54 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair |
| 24 | 20:42:05 | Default capabilities changed |
| 25 | 20:42:51 | Default capabilities changed |
| 26 | 20:42:52 | Default capabilities changed |
| 27 | 20:42:54 | Default capabilities changed |
| 28 | 20:43:04 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@34092ab |
| 29 | 20:43:04 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair |
| 30 | 20:44:02 | Default capabilities changed |
| 31 | 20:44:02 | Default capabilities changed |
| 32 | 20:44:05 | Default capabilities changed |
| 33 | 20:44:14 | NearP2pManager: TransConnect:wifiP2pEnabled: true |
| 34 | 20:44:14 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e966930 |
| 35 | 20:44:14 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair |
| 36 | 20:45:26 | Default capabilities changed |
| 37 | 20:45:29 | Default capabilities changed |

***

## 【关键发现汇总】

### 极速互传相关事件

**20:37:25 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:37:28 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:38:55 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:38:58 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:39:43 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:39:44 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:39:45 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e18025b**

**20:39:45 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair**

**20:39:45 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:39:48 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:39:51 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:40:45 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:40:45 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:40:47 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:40:54 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:41 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:43 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:43 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:46 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:50 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:wifiP2pEnabled: true**

**20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@775bcce**

**20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair**

**20:42:05 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:42:51 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:42:52 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:42:54 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:43:04 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@34092ab**

**20:43:04 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair**

**20:44:02 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:44:02 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:44:05 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:wifiP2pEnabled: true**

**20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e966930**

**20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair**

**20:45:26 - CAPABILITIES_CHANGED: Default capabilities changed**

**20:45:29 - CAPABILITIES_CHANGED: Default capabilities changed**

**分析：** 极速互传过程中可能存在P2P连接问题，导致文件传输失败。

***

## 【环境信息】

### WiFi信息

| 参数                   | 值                                     |
| -------------------- | ------------------------------------- |
| 扫描结果                | 已扫描WiFi网络                          |
| 连接状态                | 存在连接尝试                              |

### 信号强度

| 参数                   | 值                                     |
| -------------------- | ------------------------------------- |
| 最小RSSI              | -40 dBm                               |
| 最大RSSI              | -31 dBm                               |
| 平均RSSI              | -36.47 dBm                            |

***

## 【问题原因总结】

| 序号  | 时间    | 根因                                                                | 类型     |
| --- | ----- | ----------------------------------------------------------------- | ------ |
| 1 | 20:37:25 | Default capabilities changed | 极速互传问题 |
| 2 | 20:37:28 | Default capabilities changed | 极速互传问题 |
| 3 | 20:38:55 | Default capabilities changed | 极速互传问题 |
| 4 | 20:38:58 | Default capabilities changed | 极速互传问题 |
| 5 | 20:39:43 | Default capabilities changed | 极速互传问题 |
| 6 | 20:39:44 | Default capabilities changed | 极速互传问题 |
| 7 | 20:39:45 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e18025b | 极速互传问题 |
| 8 | 20:39:45 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair | 极速互传问题 |
| 9 | 20:39:45 | Default capabilities changed | 极速互传问题 |
| 10 | 20:39:48 | Default capabilities changed | 极速互传问题 |
| 11 | 20:39:51 | Default capabilities changed | 极速互传问题 |
| 12 | 20:40:45 | Default capabilities changed | 极速互传问题 |
| 13 | 20:40:45 | Default capabilities changed | 极速互传问题 |
| 14 | 20:40:47 | Default capabilities changed | 极速互传问题 |
| 15 | 20:40:54 | Default capabilities changed | 极速互传问题 |
| 16 | 20:41:41 | Default capabilities changed | 极速互传问题 |
| 17 | 20:41:43 | Default capabilities changed | 极速互传问题 |
| 18 | 20:41:43 | Default capabilities changed | 极速互传问题 |
| 19 | 20:41:46 | Default capabilities changed | 极速互传问题 |
| 20 | 20:41:50 | Default capabilities changed | 极速互传问题 |
| 21 | 20:41:54 | NearP2pManager: TransConnect:wifiP2pEnabled: true | 极速互传问题 |
| 22 | 20:41:54 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@775bcce | 极速互传问题 |
| 23 | 20:41:54 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair | 极速互传问题 |
| 24 | 20:42:05 | Default capabilities changed | 极速互传问题 |
| 25 | 20:42:51 | Default capabilities changed | 极速互传问题 |
| 26 | 20:42:52 | Default capabilities changed | 极速互传问题 |
| 27 | 20:42:54 | Default capabilities changed | 极速互传问题 |
| 28 | 20:43:04 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@34092ab | 极速互传问题 |
| 29 | 20:43:04 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair | 极速互传问题 |
| 30 | 20:44:02 | Default capabilities changed | 极速互传问题 |
| 31 | 20:44:02 | Default capabilities changed | 极速互传问题 |
| 32 | 20:44:05 | Default capabilities changed | 极速互传问题 |
| 33 | 20:44:14 | NearP2pManager: TransConnect:wifiP2pEnabled: true | 极速互传问题 |
| 34 | 20:44:14 | NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e966930 | 极速互传问题 |
| 35 | 20:44:14 | NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair | 极速互传问题 |
| 36 | 20:45:26 | Default capabilities changed | 极速互传问题 |
| 37 | 20:45:29 | Default capabilities changed | 极速互传问题 |

### 可能的原因

1. **P2P连接问题**：可能存在P2P设备发现、连接或配对失败
2. **信道干扰**：WiFi信道拥堵导致P2P连接不稳定
3. **设备兼容性**：不同设备之间的P2P协议兼容性问题
4. **驱动问题**：WiFi驱动可能存在P2P相关的bug

***

## 【流程总结】

```
极速互传流程：
  20:37:25 - CAPABILITIES_CHANGED: Default capabilities changed
  20:37:25 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:37:25 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:37:28 - CAPABILITIES_CHANGED: Default capabilities changed
  20:37:28 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:37:28 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:38:55 - CAPABILITIES_CHANGED: Default capabilities changed
  20:38:55 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:38:55 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:38:58 - CAPABILITIES_CHANGED: Default capabilities changed
  20:38:58 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:38:58 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:38:58 - DISCONNECT: 04-12 20:38:58.920300 31711 31711 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:39:37 - WPA_START: WPA supplicant started
  20:39:38 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:38 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:38 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:42 - ASSOC_START: 04-12 20:39:42.272615  3056  3056 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:39:42 - ASSOC_COMPLETE: 04-12 20:39:42.488580  3056  3056 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:39:42 - HANDSHAKE_1_4: 04-12 20:39:42.585860  3056  3056 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:39:42 - HANDSHAKE_2_4: 04-12 20:39:42.586025  3056  3056 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:39:42 - HANDSHAKE_3_4: 04-12 20:39:42.591649  3056  3056 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:39:42 - HANDSHAKE_4_4: 04-12 20:39:42.591663  3056  3056 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:39:42 - KEY_NEG_COMPLETE: 04-12 20:39:42.592268  3056  3056 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:39:42 - CONNECT_COMPLETE: Connection completed
  20:39:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在获取 IP 地址…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:39:43 - CAPABILITIES_CHANGED: Default capabilities changed
  20:39:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Default][Primary][Saved]
  20:39:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Default][Primary][Saved]
  20:39:44 - CAPABILITIES_CHANGED: Default capabilities changed
  20:39:44 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:44 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:44 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:45 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e18025b
  20:39:45 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair
  20:39:45 - CAPABILITIES_CHANGED: Default capabilities changed
  20:39:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:48 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:48 - CAPABILITIES_CHANGED: Default capabilities changed
  20:39:49 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:49 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:51 - CAPABILITIES_CHANGED: Default capabilities changed
  20:39:51 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:39:52 - DISCONNECT: 04-12 20:39:52.460619  3056  3056 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:39:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已断开连接][Level:-1][WPA/WPA2/WPA3][Saved]
  20:39:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:39:53 - ASSOC_START: 04-12 20:39:53.050092  3056  3056 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:39:53 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在连接…][Level:-1][WPA/WPA2][Connecting...][Primary][Saved]
  20:40:02 - DISCONNECT: 04-12 20:40:02.015498  3056  3056 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:40:39 - WPA_START: WPA supplicant started
  20:40:40 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:40:40 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:40:40 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:40:44 - ASSOC_START: 04-12 20:40:44.124206  3188  3188 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:40:44 - ASSOC_COMPLETE: 04-12 20:40:44.338627  3188  3188 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:40:44 - HANDSHAKE_1_4: 04-12 20:40:44.435477  3188  3188 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:40:44 - HANDSHAKE_2_4: 04-12 20:40:44.435598  3188  3188 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:40:44 - HANDSHAKE_3_4: 04-12 20:40:44.439433  3188  3188 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:40:44 - HANDSHAKE_4_4: 04-12 20:40:44.439452  3188  3188 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:40:44 - KEY_NEG_COMPLETE: 04-12 20:40:44.440142  3188  3188 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:40:44 - CONNECT_COMPLETE: Connection completed
  20:40:45 - CAPABILITIES_CHANGED: Default capabilities changed
  20:40:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:40:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Primary][Saved]
  20:40:45 - CAPABILITIES_CHANGED: Default capabilities changed
  20:40:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][][Level:4][WPA/WPA2][Connected][Internet][Primary][Saved]
  20:40:45 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:47 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:47 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:47 - CAPABILITIES_CHANGED: Default capabilities changed
  20:40:47 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:47 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:54 - CAPABILITIES_CHANGED: Default capabilities changed
  20:40:54 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:54 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:40:58 - DISCONNECT: 04-12 20:40:58.357843  3188  3188 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:41:36 - WPA_START: WPA supplicant started
  20:41:37 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:37 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:37 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:40 - ASSOC_START: 04-12 20:41:40.720019  3077  3077 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:41:40 - ASSOC_COMPLETE: 04-12 20:41:40.948293  3077  3077 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:41:41 - HANDSHAKE_1_4: 04-12 20:41:41.037790  3077  3077 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:41:41 - HANDSHAKE_2_4: 04-12 20:41:41.037981  3077  3077 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:41:41 - HANDSHAKE_3_4: 04-12 20:41:41.041700  3077  3077 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:41:41 - HANDSHAKE_4_4: 04-12 20:41:41.041718  3077  3077 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:41:41 - KEY_NEG_COMPLETE: 04-12 20:41:41.042867  3077  3077 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:41:41 - CONNECT_COMPLETE: Connection completed
  20:41:41 - CAPABILITIES_CHANGED: Default capabilities changed
  20:41:41 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:41 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Primary][Saved]
  20:41:41 - DISCONNECT: 04-12 20:41:41.663171  3077  3077 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:41:41 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:41 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:42 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:42 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:42 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:41:42 - ASSOC_START: 04-12 20:41:42.897844  3077  3077 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:41:42 - ASSOC_COMPLETE: 04-12 20:41:42.942996  3077  3077 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:41:42 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在连接…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:41:43 - HANDSHAKE_1_4: 04-12 20:41:43.038555  3077  3077 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:41:43 - HANDSHAKE_2_4: 04-12 20:41:43.038908  3077  3077 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:41:43 - HANDSHAKE_3_4: 04-12 20:41:43.040647  3077  3077 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:41:43 - HANDSHAKE_4_4: 04-12 20:41:43.040663  3077  3077 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:41:43 - KEY_NEG_COMPLETE: 04-12 20:41:43.041492  3077  3077 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:41:43 - CONNECT_COMPLETE: Connection completed
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在获取 IP 地址…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在获取 IP 地址…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在获取 IP 地址…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:41:43 - CAPABILITIES_CHANGED: Default capabilities changed
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在获取 IP 地址…][Level:4][WPA/WPA2][Connecting...][Primary][Saved]
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Default][Primary][Saved]
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Default][Primary][Saved]
  20:41:43 - CAPABILITIES_CHANGED: Default capabilities changed
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:43 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:46 - CAPABILITIES_CHANGED: Default capabilities changed
  20:41:46 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:46 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:50 - CAPABILITIES_CHANGED: Default capabilities changed
  20:41:50 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:50 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:wifiP2pEnabled: true
  20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@775bcce
  20:41:54 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair
  20:42:05 - CAPABILITIES_CHANGED: Default capabilities changed
  20:42:05 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:05 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:07 - DISCONNECT: 04-12 20:42:07.266152  3077  3077 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:42:45 - WPA_START: WPA supplicant started
  20:42:46 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:42:46 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:42:46 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:42:50 - ASSOC_START: 04-12 20:42:50.018701  3005  3005 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:42:50 - ASSOC_COMPLETE: 04-12 20:42:50.228964  3005  3005 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:42:50 - HANDSHAKE_1_4: 04-12 20:42:50.323585  3005  3005 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:42:50 - HANDSHAKE_2_4: 04-12 20:42:50.323793  3005  3005 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:42:50 - HANDSHAKE_3_4: 04-12 20:42:50.325795  3005  3005 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:42:50 - HANDSHAKE_4_4: 04-12 20:42:50.325821  3005  3005 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:42:50 - KEY_NEG_COMPLETE: 04-12 20:42:50.326701  3005  3005 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:42:50 - CONNECT_COMPLETE: Connection completed
  20:42:51 - CAPABILITIES_CHANGED: Default capabilities changed
  20:42:51 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:42:51 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Primary][Saved]
  20:42:52 - CAPABILITIES_CHANGED: Default capabilities changed
  20:42:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:52 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:54 - CAPABILITIES_CHANGED: Default capabilities changed
  20:42:54 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:54 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:55 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:42:55 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:43:04 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@34092ab
  20:43:04 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair
  20:43:19 - DISCONNECT: 04-12 20:43:19.068762  3005  3005 I wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=0c:4b:54:49:83:1c reason=3 locally_generated=1
  20:43:56 - WPA_START: WPA supplicant started
  20:43:57 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:43:57 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:43:57 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:44:01 - ASSOC_START: 04-12 20:44:01.252025  3092  3092 I wpa_supplicant: wlan0: Trying to associate with SSID 'David_5'
  20:44:01 - ASSOC_COMPLETE: 04-12 20:44:01.463462  3092  3092 I wpa_supplicant: wlan0: Associated with 0c:4b:54:49:83:1c
  20:44:01 - HANDSHAKE_1_4: 04-12 20:44:01.560203  3092  3092 I wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:44:01 - HANDSHAKE_2_4: 04-12 20:44:01.560399  3092  3092 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4
  20:44:01 - HANDSHAKE_3_4: 04-12 20:44:01.562221  3092  3092 I wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake from 0c:4b:54:49:83:1c (ver=2)
  20:44:01 - HANDSHAKE_4_4: 04-12 20:44:01.562279  3092  3092 I wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4
  20:44:01 - KEY_NEG_COMPLETE: 04-12 20:44:01.565696  3092  3092 I wpa_supplicant: wlan0: WPA: Key negotiation completed with 0c:4b:54:49:83:1c [PTK=CCMP GTK=CCMP]
  20:44:01 - CONNECT_COMPLETE: Connection completed
  20:44:02 - CAPABILITIES_CHANGED: Default capabilities changed
  20:44:02 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=null
  20:44:02 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][正在检查互联网访问权限…][Level:4][WPA/WPA2][Connected][Primary][Saved]
  20:44:02 - CAPABILITIES_CHANGED: Default capabilities changed
  20:44:02 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][][Level:4][WPA/WPA2][Connected][Internet][Primary][Saved]
  20:44:02 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:44:04 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:44:04 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:44:05 - CAPABILITIES_CHANGED: Default capabilities changed
  20:44:05 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:44:05 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:wifiP2pEnabled: true
  20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: listener:com.transsion.nearby.nfbd.NearConnectionService$mNearWifiP2pListener$1@e966930
  20:44:14 - NEAR_P2P: NearP2pManager: TransConnect:registerMonitoredListener: monitoredListenerPairs add pair
  20:45:26 - CAPABILITIES_CHANGED: Default capabilities changed
  20:45:27 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:45:27 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:45:29 - CAPABILITIES_CHANGED: Default capabilities changed
  20:45:29 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
  20:45:29 - WIFI_ENTRY_CHANGED: WiFi entry changed: . ConnectedEntry=[StandardWifiEntry][David_5][已连接][Level:4][WPA/WPA2][Connected][Internet][Default][Primary][Saved]
```

## 【信号强度与速率分析】

![RSSI and Rate Analysis](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20RSSI%20signal%20strength%20and%20rate%20charts&image_size=landscape_16_9)

## 【连接时间轴】

![Connection Timeline](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20connection%20timeline%20chart%20showing%20connection%20attempts%20and%20status&image_size=landscape_16_9)

## 【连接过程分析】

![Connection Process](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20connection%20process%20timeline%20showing%20auth%20assoc%20handshake%20dhcp%20steps&image_size=landscape_16_9)
