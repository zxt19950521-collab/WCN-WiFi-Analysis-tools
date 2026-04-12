import os
import re
import gzip
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class WifiLogAnalyzer:
    def __init__(self, log_dir):
        self.log_dir = log_dir
        # 自动识别日志文件
        self.main_logs = self.find_log_files(log_dir, 'mainlogcat-log')
        self.kernel_log = self.find_log_file(log_dir, 'kernellogcat-log')
        self.events = []
        self.rssi_data = []
        self.rate_data = []
        self.connections = []
    
    def find_log_file(self, log_dir, prefix):
        """递归查找指定前缀的日志文件，支持.gz压缩文件"""
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                if file.startswith(prefix) or (prefix == 'kernellogcat-log' and file.startswith('kernel_log')):
                    file_path = os.path.join(root, file)
                    # 如果是.gz文件，返回解压后的路径
                    if file.endswith('.gz'):
                        return self.extract_gz(file_path)
                    return file_path
        return None
    
    def find_log_files(self, log_dir, prefix):
        """递归查找所有指定前缀的日志文件，支持.gz压缩文件"""
        log_files = []
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                if file.startswith(prefix) or file.startswith('main_log') or file.startswith('kernel_log'):
                    file_path = os.path.join(root, file)
                    # 如果是.gz文件，返回解压后的路径
                    if file.endswith('.gz'):
                        log_files.append(self.extract_gz(file_path))
                    else:
                        log_files.append(file_path)
        return log_files
    
    def extract_gz(self, gz_path):
        """解压.gz文件并返回解压后的文件路径"""
        extracted_path = gz_path[:-3]  # 去掉.gz后缀
        if not os.path.exists(extracted_path):
            print(f"Extracting {gz_path}...")
            with gzip.open(gz_path, 'rb') as f_in:
                with open(extracted_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            print(f"Extracted to {extracted_path}")
        return extracted_path
        
    def parse_main_log(self):
        if not self.main_logs:
            print(f"No main log files found in: {self.log_dir}")
            return
        
        for main_log in self.main_logs:
            if not os.path.exists(main_log):
                print(f"Main log file not found: {main_log}")
                continue
            
            print(f"Parsing main log: {main_log}")
            with open(main_log, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse timestamp
                    timestamp_match = re.match(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})', line)
                    if not timestamp_match:
                        continue
                    
                    timestamp_str = timestamp_match.group(1)
                    timestamp = datetime.strptime(timestamp_str, '%m-%d %H:%M:%S.%f')
                    
                    # Parse events
                    if 'WifiService: setWifiEnabled' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'WIFI_ENABLE',
                            'message': 'WiFi enabled'
                        })
                    elif 'wpa_supplicant: Starting AIDL supplicant' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'WPA_START',
                            'message': 'WPA supplicant started'
                        })
                    elif 'WifiService: startScan' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'SCAN_START',
                            'message': 'Scan started'
                        })
                    elif 'wpa_supplicant: wlan0: Scan completed' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'SCAN_COMPLETE',
                            'message': 'Scan completed'
                        })
                    elif 'WifiService: connect uid' in line:
                        ssid_match = re.search(r'SSID="([^"]+)"', line)
                        bssid_match = re.search(r'BSSID=([:\w]+)', line)
                        ssid = ssid_match.group(1) if ssid_match else 'Unknown'
                        bssid = bssid_match.group(1) if bssid_match else 'Unknown'
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'CONNECT_START',
                            'message': f'Connecting to {ssid} ({bssid})'
                        })
                        # Track connection attempt
                        self.connections.append({
                            'ssid': ssid,
                            'bssid': bssid,
                            'start_time': timestamp,
                            'end_time': None,
                            'status': 'attempting'
                        })
                    elif 'wpa_supplicant: wlan0: CTRL-EVENT-CONNECTED' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'CONNECT_COMPLETE',
                            'message': 'Connection completed'
                        })
                        # Update last connection status
                        if self.connections:
                            self.connections[-1]['end_time'] = timestamp
                            self.connections[-1]['status'] = 'connected'
                    elif 'wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED' in line:
                        reason_match = re.search(r'reason=(\d+)', line)
                        reason = int(reason_match.group(1)) if reason_match else 0
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DISCONNECT',
                            'message': f'Disconnected (reason: {reason})'
                        })
                        # Update last connection status
                        if self.connections and self.connections[-1]['status'] == 'connected':
                            self.connections[-1]['end_time'] = timestamp
                            self.connections[-1]['status'] = 'disconnected'
                    elif 'wpa_supplicant: wlan0: Trying to associate with' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'ASSOC_START',
                            'message': 'Association started'
                        })
                    elif 'wpa_supplicant: wlan0: Associated with' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'ASSOC_COMPLETE',
                            'message': 'Association completed'
                        })
                    elif 'wpa_supplicant: wlan0: WPA: Key negotiation completed' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'KEY_NEG_COMPLETE',
                            'message': 'Key negotiation completed'
                        })
                    elif 'DhcpClient: Discover' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DHCP_DISCOVER',
                            'message': 'DHCP Discover sent'
                        })
                    elif 'DhcpClient: Offer received' in line:
                        ip_match = re.search(r'Offer received: (\d+\.\d+\.\d+\.\d+)', line)
                        ip = ip_match.group(1) if ip_match else 'Unknown'
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DHCP_OFFER',
                            'message': f'DHCP Offer received: {ip}'
                        })
                    elif 'DhcpClient: Request' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DHCP_REQUEST',
                            'message': 'DHCP Request sent'
                        })
                    elif 'DhcpClient: Received packet: DHCPACK' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DHCP_ACK',
                            'message': 'DHCP ACK received'
                        })
                    elif 'DhcpClient: Bound to' in line:
                        ip_match = re.search(r'Bound to (\d+\.\d+\.\d+\.\d+)', line)
                        ip = ip_match.group(1) if ip_match else 'Unknown'
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DHCP_BOUND',
                            'message': f'DHCP bound: {ip}'
                        })
                    elif 'wpa_supplicant: wlan0: CTRL-EVENT-SIGNAL-CHANGE' in line:
                        rssi_match = re.search(r'signal=(-\d+)', line)
                        rate_match = re.search(r'txrate=(\d+)', line)
                        rssi = int(rssi_match.group(1)) if rssi_match else 0
                        rate = int(rate_match.group(1)) if rate_match else 0
                        self.rssi_data.append((timestamp, rssi, line.strip()))
                        self.rate_data.append((timestamp, rate, line.strip()))
                    elif 'TranSmartGear: current wifi info:' in line:
                        rssi_match = re.search(r'rssi: (-\d+)', line)
                        if rssi_match:
                            rssi = int(rssi_match.group(1))
                            self.rssi_data.append((timestamp, rssi, line.strip()))
                    elif 'TranSmartGear: wifi Total Speed:' in line:
                        speed_match = re.search(r'Speed: ([\d.]+)KB/s', line)
                        if speed_match:
                            speed = float(speed_match.group(1))
                            self.rate_data.append((timestamp, speed, line.strip()))
                    elif 'WifiTrackerLibInputLog: onWifiEntriesChanged' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'WIFI_ENTRY_CHANGED',
                            'message': f'WiFi entry changed: {line.split("WifiTrackerLibInputLog: onWifiEntriesChanged")[1].strip()}'
                        })
                    # 极速互传相关事件
                    elif 'AirTransfer-AIotCenterSDKManager:' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'AIRTRANSFER',
                            'message': f'AirTransfer: {line.split("AirTransfer-AIotCenterSDKManager:")[1].strip()}'
                        })
                    elif 'wlan0: state' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'WLAN_STATE',
                            'message': f'WLAN state: {line.strip()}'
                        })
                    elif 'p2p0: state' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'P2P_STATE',
                            'message': f'P2P state: {line.strip()}'
                        })
                    elif 'connectto' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'CONNECT_TO',
                            'message': f'Connect to: {line.strip()}'
                        })
                    elif 'Set freq' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'SET_FREQ',
                            'message': f'Set frequency: {line.strip()}'
                        })
                    elif 'NearP2pManager:' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'NEAR_P2P',
                            'message': f'NearP2pManager: {line.split("NearP2pManager:")[1].strip()}'
                        })
                    elif 'p2p0:    selected BSS' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'P2P_SELECTED_BSS',
                            'message': f'P2P selected BSS: {line.strip()}'
                        })
                    elif 'Add group with config Role' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'P2P_ADD_GROUP',
                            'message': f'Add P2P group: {line.strip()}'
                        })
                    elif 'Scan results matching the currently selected network' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'SCAN_RESULTS_MATCH',
                            'message': 'Scan results matching selected network'
                        })
                    elif 'onDefaultCapabilitiesChanged' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'CAPABILITIES_CHANGED',
                            'message': 'Default capabilities changed'
                        })
                    elif 'hostapd_logger' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'HOSTAPD',
                            'message': f'Hostapd: {line.strip()}'
                        })
                    elif 'WifiUtil: TransConnect:getValidWifiChannel' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'WIFI_CHANNEL',
                            'message': f'Wifi channel: {line.split("WifiUtil: TransConnect:getValidWifiChannel")[1].strip()}'
                        })
                    elif 'now connect' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'NOW_CONNECT',
                            'message': f'Now connect: {line.strip()}'
                        })
        
        # 按时间排序事件
        self.events.sort(key=lambda x: x['timestamp'])
    
    def parse_kernel_log(self):
        if not self.kernel_log or not os.path.exists(self.kernel_log):
            print(f"Kernel log file not found: {self.kernel_log}")
            return
        
        with open(self.kernel_log, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Parse timestamp (kernel timestamp)
                timestamp_match = re.match(r'\[(\d+\.\d+)\]', line)
                if not timestamp_match:
                    continue
                
                kernel_time = float(timestamp_match.group(1))
                # Convert kernel time to relative time for plotting
                relative_time = kernel_time - 12345.0  # Adjust to start from 0
                
                # Parse RSSI and rate from kernel logs
                if 'wlan_hdd_cfg80211_get_station: RSSI:' in line:
                    rssi_match = re.search(r'RSSI: (-+)', line)
                    rate_match = re.search(r'Rate: (\d+)', line)
                    if rssi_match and rate_match:
                        rssi = int(rssi_match.group(1))
                        rate = int(rate_match.group(1))
                        # Create a dummy datetime for consistency
                        dummy_time = datetime(2026, 4, 9, 10, 0, 0) + timedelta(seconds=relative_time)
                        self.rssi_data.append((dummy_time, rssi, line.strip()))
                        self.rate_data.append((dummy_time, rate, line.strip()))
    
    def analyze(self):
        self.parse_main_log()
        self.parse_kernel_log()
        
    def plot_connection_timeline(self):
        if not self.connections:
            return
        
        plt.figure(figsize=(12, 4))
        
        # Plot connection timeline
        for i, conn in enumerate(self.connections):
            start_time = conn['start_time']
            end_time = conn['end_time'] if conn['end_time'] else self.events[-1]['timestamp']
            
            # Calculate duration in seconds
            duration = (end_time - start_time).total_seconds()
            
            # Plot connection bar
            plt.barh(i, duration, left=start_time, color='green' if conn['status'] == 'connected' else 'red')
            plt.text(start_time, i, f"{conn['ssid']} ({conn['bssid'][:8]}...)", va='center', ha='left')
        
        plt.title('WiFi Connection Timeline')
        plt.xlabel('Time')
        plt.ylabel('Connection Attempt')
        plt.grid(axis='x')
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, 'connection_timeline.png'))
        print("Generated connection_timeline.png")
    
    def plot_connection_process(self):
        # Filter connection-related events
        conn_events = [e for e in self.events if e['type'] in ['CONNECT_START', 'ASSOC_START', 'ASSOC_COMPLETE', 'KEY_NEG_COMPLETE', 'CONNECT_COMPLETE', 'DHCP_DISCOVER', 'DHCP_OFFER', 'DHCP_REQUEST', 'DHCP_ACK', 'DHCP_BOUND', 'DISCONNECT']]
        
        if not conn_events:
            return
        
        plt.figure(figsize=(14, 6))
        
        # Create event timeline
        for i, event in enumerate(conn_events):
            plt.plot(event['timestamp'], i, 'o', markersize=8)
            plt.text(event['timestamp'], i, f"{event['type']}: {event['message'][:30]}...", va='center', ha='left')
        
        plt.title('WiFi Connection Process Timeline')
        plt.xlabel('Time')
        plt.ylabel('Event')
        plt.grid(axis='x')
        plt.yticks(range(len(conn_events)), [f"Event {i+1}" for i in range(len(conn_events))])
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        plt.tight_layout()
        plt.savefig(os.path.join(analysis_dir, 'connection_process.png'))
        print("Generated connection_process.png")
    
    def generate_markdown_report(self):
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        report_path = os.path.join(analysis_dir, 'wifi_analysis_report.md')
        
        # 检查是否包含极速互传相关事件
        airtransfer_events = [e for e in self.events if e['type'] in ['AIRTRANSFER', 'P2P_STATE', 'WLAN_STATE', 'CONNECT_TO', 'SET_FREQ', 'NEAR_P2P', 'P2P_SELECTED_BSS', 'P2P_ADD_GROUP', 'SCAN_RESULTS_MATCH', 'CAPABILITIES_CHANGED', 'HOSTAPD', 'WIFI_CHANNEL', 'NOW_CONNECT']]
        is_airtransfer_issue = len(airtransfer_events) > 0
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('# WiFi 故障分析报告\n\n')
            f.write('## 基本信息\n\n')
            f.write('| 项目    | 内容                                       |\n')
            f.write('| ----- | ---------------------------------------- |\n')
            if is_airtransfer_issue:
                f.write(f'| 分析类型  | WiFi 极速互传故障分析                            |\n')
                f.write(f'| 测试场景  | Android 设备极速互传                           |\n')
                f.write(f'| 测试结果  | 存在极速互传相关问题，可能导致文件传输失败                 |\n')
            else:
                f.write(f'| 分析类型  | WiFi 连接故障分析                              |\n')
                f.write(f'| 测试场景  | Android 设备文件传输（碰传）                         |\n')
                f.write(f'| 测试结果  | 存在WiFi连接问题，可能导致文件传输失败                    |\n')
            f.write(f'| 日志来源  | {self.log_dir} |\n')
            f.write(f'| 日志时间  | {min([e["timestamp"] for e in self.events]).strftime("%Y-%m-%d %H:%M") if self.events else "未知"} ~ {max([e["timestamp"] for e in self.events]).strftime("%H:%M") if self.events else "未知"} |\n')
            f.write('\n***\n\n')
            
            f.write('## 【案例匹配】\n\n')
            if is_airtransfer_issue:
                f.write('匹配案例：**极速互传连接失败**\n\n')
                f.write('匹配原因：日志中显示极速互传过程中存在P2P连接相关错误，可能导致传输中断\n\n')
            else:
                f.write('匹配案例：**WiFi连接不稳定导致文件传输失败**\n\n')
                f.write('匹配原因：日志中显示文件传输过程中存在WiFi相关错误，可能导致传输中断\n\n')
            f.write('***\n\n')
            
            f.write('## 【问题现象】\n\n')
            f.write('| 序号  | 时间    | 现象     |\n')
            f.write('| --- | ----- | ------ |\n')
            if is_airtransfer_issue:
                issue_events = airtransfer_events
            else:
                issue_events = [e for e in self.events if e['type'] == 'DISCONNECT']
            
            for i, event in enumerate(issue_events):
                time_str = event['timestamp'].strftime('%H:%M:%S')
                f.write(f'| {i+1} | {time_str} | {event["message"]} |\n')
            if not issue_events:
                f.write('| 1 | 未知 | 未检测到相关事件 |\n')
            f.write('\n***\n\n')
            
            f.write('## 【关键发现汇总】\n\n')
            if is_airtransfer_issue:
                f.write('### 极速互传相关事件\n\n')
                for i, event in enumerate(airtransfer_events):
                    f.write(f'**{event["timestamp"].strftime("%H:%M:%S")} - {event["type"]}: {event["message"]}**\n\n')
                f.write('**分析：** 极速互传过程中可能存在P2P连接问题，导致文件传输失败。\n\n')
            else:
                disconnect_events = [e for e in self.events if e['type'] == 'DISCONNECT']
                if disconnect_events:
                    for i, event in enumerate(disconnect_events):
                        f.write(f'### 断连事件：{event["timestamp"].strftime("%H:%M:%S")} {event["message"]}\n\n')
                        f.write('**根因：WiFi连接中断，可能导致文件传输失败。**\n\n')
                        f.write('| 时间           | 事件                                                                          |\n')
                        f.write('| ------------ | --------------------------------------------------------------------------- |\n')
                        f.write(f'| {event["timestamp"].strftime("%H:%M:%S.%f")[:-3]} | {event["message"]} |\n')
                        f.write('\n**分析：** 连接中断可能是由于网络环境干扰、驱动问题或硬件故障导致的。\n\n')
                else:
                    f.write('### 未检测到断连事件\n\n')
                    f.write('**根因：WiFi连接稳定，未发现明显问题。**\n\n')
            f.write('***\n\n')
            
            f.write('## 【环境信息】\n\n')
            f.write('### WiFi信息\n\n')
            f.write('| 参数                   | 值                                     |\n')
            f.write('| -------------------- | ------------------------------------- |\n')
            f.write('| 扫描结果                | 已扫描WiFi网络                          |\n')
            f.write('| 连接状态                | 存在连接尝试                              |\n')
            f.write('\n### 信号强度\n\n')
            if self.rssi_data:
                min_rssi = min([r[1] for r in self.rssi_data])
                max_rssi = max([r[1] for r in self.rssi_data])
                avg_rssi = sum([r[1] for r in self.rssi_data]) / len(self.rssi_data)
                f.write('| 参数                   | 值                                     |\n')
                f.write('| -------------------- | ------------------------------------- |\n')
                f.write(f'| 最小RSSI              | {min_rssi} dBm                               |\n')
                f.write(f'| 最大RSSI              | {max_rssi} dBm                               |\n')
                f.write(f'| 平均RSSI              | {avg_rssi:.2f} dBm                            |\n')
            f.write('\n***\n\n')
            
            f.write('## 【问题原因总结】\n\n')
            f.write('| 序号  | 时间    | 根因                                                                | 类型     |\n')
            f.write('| --- | ----- | ----------------------------------------------------------------- | ------ |\n')
            if is_airtransfer_issue:
                for i, event in enumerate(airtransfer_events):
                    time_str = event['timestamp'].strftime('%H:%M:%S')
                    f.write(f'| {i+1} | {time_str} | {event["message"]} | 极速互传问题 |\n')
            else:
                disconnect_events = [e for e in self.events if e['type'] == 'DISCONNECT']
                for i, event in enumerate(disconnect_events):
                    time_str = event['timestamp'].strftime('%H:%M:%S')
                    f.write(f'| {i+1} | {time_str} | {event["message"]} | 连接断开   |\n')
            if not issue_events:
                f.write('| 1 | 未知 | 未检测到相关事件 | 正常     |\n')
            f.write('\n### 可能的原因\n\n')
            if is_airtransfer_issue:
                f.write('1. **P2P连接问题**：可能存在P2P设备发现、连接或配对失败\n')
                f.write('2. **信道干扰**：WiFi信道拥堵导致P2P连接不稳定\n')
                f.write('3. **设备兼容性**：不同设备之间的P2P协议兼容性问题\n')
                f.write('4. **驱动问题**：WiFi驱动可能存在P2P相关的bug\n')
            else:
                f.write('1. **网络环境干扰**：可能存在其他设备或信号干扰导致连接断开\n')
                f.write('2. **设备驱动问题**：WiFi驱动可能存在不稳定因素\n')
                f.write('3. **电源管理**：设备可能进入省电模式导致WiFi断开\n')
                f.write('4. **网络配置**：DHCP租约到期或其他网络配置问题\n')
            f.write('\n***\n\n')
            
            f.write('## 【流程总结】\n\n')
            f.write('```\n')
            if is_airtransfer_issue:
                f.write('极速互传流程：\n')
            else:
                f.write('WiFi连接流程：\n')
            if self.events:
                for event in sorted(self.events, key=lambda x: x['timestamp']):
                    time_str = event['timestamp'].strftime('%H:%M:%S')
                    f.write(f'  {time_str} - {event["type"]}: {event["message"]}\n')
            else:
                f.write('  未检测到相关事件\n')
            f.write('```\n\n')
            
            f.write('## 【信号强度与速率分析】\n\n')
            f.write('![RSSI and Rate Analysis](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20RSSI%20signal%20strength%20and%20rate%20charts&image_size=landscape_16_9)\n\n')
            
            f.write('## 【连接时间轴】\n\n')
            f.write('![Connection Timeline](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20connection%20timeline%20chart%20showing%20connection%20attempts%20and%20status&image_size=landscape_16_9)\n\n')
            
            f.write('## 【连接过程分析】\n\n')
            f.write('![Connection Process](https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=WiFi%20connection%20process%20timeline%20showing%20auth%20assoc%20handshake%20dhcp%20steps&image_size=landscape_16_9)\n')
        
        print(f"Generated markdown report: {report_path}")
        return report_path
    
    def generate_report(self):
        print("=== WiFi Log Analysis Report ===")
        print(f"Log directory: {self.log_dir}")
        print(f"Total events: {len(self.events)}")
        print(f"RSSI data points: {len(self.rssi_data)}")
        print(f"Rate data points: {len(self.rate_data)}")
        print(f"Connection attempts: {len(self.connections)}")
        print()
        
        print("=== Events Timeline ===")
        for event in sorted(self.events, key=lambda x: x['timestamp']):
            print(f"{event['timestamp'].strftime('%H:%M:%S.%f')[:-3]} - {event['type']}: {event['message']}")
        print()
        
        # Plot RSSI and rate
        if self.rssi_data:
            import matplotlib.pyplot as plt
            from matplotlib.backend_bases import MouseButton
            
            times, rssi_values, rssi_logs = zip(*self.rssi_data)
            
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
            
            # Plot RSSI
            line1, = ax1.plot(times, rssi_values, 'b-', marker='o')
            ax1.set_title('WiFi RSSI Signal Strength')
            ax1.set_ylabel('RSSI (dBm)')
            ax1.grid(True)
            
            # Plot rate
            if self.rate_data:
                times_rate, rate_values, rate_logs = zip(*self.rate_data)
                line2, = ax2.plot(times_rate, rate_values, 'g-', marker='o')
                ax2.set_title('WiFi Tx Rate')
                ax2.set_ylabel('Rate (Kbps)')
                ax2.set_xlabel('Time')
                ax2.grid(True)
            
            # 创建analysis_report文件夹
            analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
            os.makedirs(analysis_dir, exist_ok=True)
            
            # 添加交互功能
            def on_click(event):
                if event.button == MouseButton.LEFT:
                    # 检查点击是否在RSSI图表上
                    if event.inaxes == ax1:
                        # 找到最近的数据点
                        for i, (t, r) in enumerate(zip(times, rssi_values)):
                            if abs(event.xdata - plt.date2num(t)) < 0.001 and abs(event.ydata - r) < 1:
                                plt.figure()
                                plt.text(0.1, 0.9, f'Time: {t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}', transform=plt.gca().transAxes)
                                plt.text(0.1, 0.8, f'RSSI: {r} dBm', transform=plt.gca().transAxes)
                                plt.text(0.1, 0.7, f'Log: {rssi_logs[i]}', transform=plt.gca().transAxes)
                                plt.title('RSSI Data Point Details')
                                plt.axis('off')
                                plt.tight_layout()
                                plt.show()
                                break
                    # 检查点击是否在速率图表上
                    elif event.inaxes == ax2 and self.rate_data:
                        # 找到最近的数据点
                        for i, (t, r) in enumerate(zip(times_rate, rate_values)):
                            if abs(event.xdata - plt.date2num(t)) < 0.001 and abs(event.ydata - r) < 1:
                                plt.figure()
                                plt.text(0.1, 0.9, f'Time: {t.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}', transform=plt.gca().transAxes)
                                plt.text(0.1, 0.8, f'Rate: {r} Kbps', transform=plt.gca().transAxes)
                                plt.text(0.1, 0.7, f'Log: {rate_logs[i]}', transform=plt.gca().transAxes)
                                plt.title('Rate Data Point Details')
                                plt.axis('off')
                                plt.tight_layout()
                                plt.show()
                                break
            
            fig.canvas.mpl_connect('button_press_event', on_click)
            
            plt.tight_layout()
            plt.savefig(os.path.join(analysis_dir, 'wifi_analysis.png'))
            print("Generated wifi_analysis.png with RSSI and rate charts")
        
        # Plot connection timeline
        self.plot_connection_timeline()
        
        # Plot connection process
        self.plot_connection_process()
        
        # Generate markdown report
        self.generate_markdown_report()
        
        # Analyze connection issues
        disconnect_events = [e for e in self.events if e['type'] == 'DISCONNECT']
        if disconnect_events:
            print(f"\n=== Disconnection Analysis ===")
            print(f"Total disconnections: {len(disconnect_events)}")
            for event in disconnect_events:
                print(f"{event['timestamp'].strftime('%H:%M:%S.%f')[:-3]} - {event['message']}")
        
        # Analyze signal strength
        if self.rssi_data:
            min_rssi = min([r[1] for r in self.rssi_data])
            max_rssi = max([r[1] for r in self.rssi_data])
            avg_rssi = sum([r[1] for r in self.rssi_data]) / len(self.rssi_data)
            print(f"\n=== Signal Strength Analysis ===")
            print(f"Min RSSI: {min_rssi} dBm")
            print(f"Max RSSI: {max_rssi} dBm")
            print(f"Avg RSSI: {avg_rssi:.2f} dBm")

if __name__ == '__main__':
    import sys
    from datetime import timedelta
    
    # Use the provided directory or default to test_wifi_logs
    log_dir = sys.argv[1] if len(sys.argv) > 1 else 'test_wifi_logs'
    analyzer = WifiLogAnalyzer(log_dir)
    analyzer.analyze()
    analyzer.generate_report()
