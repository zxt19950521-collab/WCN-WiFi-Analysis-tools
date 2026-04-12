import os
import re
import gzip
import plotly.express as px
import plotly.graph_objects as go
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
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'DISCONNECT',
                            'message': line  # 保留原始日志消息
                        })
                        # Update last connection status
                        if self.connections and self.connections[-1]['status'] == 'connected':
                            self.connections[-1]['end_time'] = timestamp
                            self.connections[-1]['status'] = 'disconnected'
                    elif 'wpa_supplicant: wlan0: Trying to associate with' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'ASSOC_START',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: Associated with' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'ASSOC_COMPLETE',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: WPA: Key negotiation completed' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'KEY_NEG_COMPLETE',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: WPA: RX message 1 of 4-Way Handshake' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'HANDSHAKE_1_4',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 2/4' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'HANDSHAKE_2_4',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: RSN: RX message 3 of 4-Way Handshake' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'HANDSHAKE_3_4',
                            'message': line  # 保留原始日志消息
                        })
                    elif 'wpa_supplicant: wlan0: WPA: Sending EAPOL-Key 4/4' in line:
                        self.events.append({
                            'timestamp': timestamp,
                            'type': 'HANDSHAKE_4_4',
                            'message': line  # 保留原始日志消息
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
        
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        
        # 准备数据
        data = []
        for i, conn in enumerate(self.connections):
            start_time = conn['start_time']
            end_time = conn['end_time'] if conn['end_time'] else self.events[-1]['timestamp']
            duration = (end_time - start_time).total_seconds()
            data.append({
                'timestamp': start_time,
                'connection_id': i,
                'ssid': conn['ssid'],
                'bssid': conn['bssid'],
                'status': conn['status'],
                'duration': duration,
                'end_time': end_time
            })
        
        # 创建散点图
        fig = go.Figure()
        
        # 添加散点
        for conn in data:
            color = 'green' if conn['status'] == 'connected' else 'red'
            fig.add_trace(go.Scatter(
                x=[conn['timestamp']],
                y=[conn['connection_id']],
                mode='markers',
                marker=dict(color=color, size=10),
                hovertemplate=
                    '<b>时间</b>: %{x|%Y-%m-%d %H:%M:%S.%f}<br>'+
                    '<b>SSID</b>: '+conn['ssid']+'<br>'+
                    '<b>BSSID</b>: '+conn['bssid']+'<br>'+
                    '<b>状态</b>: '+'已连接' if conn['status'] == 'connected' else '未连接'+'<br>'+
                    '<b>持续时间</b>: '+f"{conn['duration']:.2f}秒"+'<br>'+
                    '<b>结束时间</b>: '+conn['end_time'].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+'<br>',
                name=f"Connection {conn['connection_id']+1}"
            ))
        
        # 布局设置
        fig.update_layout(
            title='WiFi Connection Timeline',
            xaxis=dict(title='时间'),
            yaxis=dict(
                title='连接尝试',
                tickvals=[conn['connection_id'] for conn in data],
                ticktext=[f"连接 {conn['connection_id']+1}" for conn in data]
            ),
            hovermode='closest',
            showlegend=False
        )
        
        # 保存为HTML
        html_path = os.path.join(analysis_dir, 'connection_timeline.html')
        fig.write_html(html_path)
        print(f"Generated connection_timeline.html")
    
    def plot_connection_process(self):
        # Filter connection-related events - only keep specific states
        conn_events = []
        current_ssid = "Unknown"
        current_mac = "Unknown"
        
        for event in self.events:
            # Extract SSID from connect events and association events
            if event['type'] == 'CONNECT_START' or event['type'] == 'ASSOC_START':
                # Try to extract SSID from different formats
                ssid_match = re.search(r'SSID=[\'"]([^\'"]+)[\'"]', event['message'])
                if not ssid_match:
                    ssid_match = re.search(r'SSID \'([^\']+)\'', event['message'])
                if not ssid_match:
                    ssid_match = re.search(r'associate with SSID \'([^\']+)\'', event['message'])
                if ssid_match:
                    current_ssid = ssid_match.group(1)
            
            # Extract MAC address from association complete events and disconnect events
            if event['type'] == 'ASSOC_COMPLETE' or 'Associated with' in event['message'] or event['type'] == 'DISCONNECT':
                mac_match = re.search(r'[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}', event['message'])
                if mac_match:
                    current_mac = mac_match.group(0)
            
            # Only include specific event types
            if event['type'] in ['CONNECT_START', 'ASSOC_START', 'ASSOC_COMPLETE', 'HANDSHAKE_1_4', 'HANDSHAKE_2_4', 'HANDSHAKE_3_4', 'HANDSHAKE_4_4', 'CONNECT_COMPLETE', 'DISCONNECT']:
                # Determine node type from message
                node_type = 'Unknown'
                if 'wlan0' in event['message']:
                    node_type = 'wlan0'
                elif 'p2p0' in event['message']:
                    node_type = 'P2P'
                elif 'P2P' in event['type']:
                    node_type = 'P2P'
                
                # Extract reason code from disconnect events
                reason_code = "Unknown"
                if event['type'] == 'DISCONNECT':
                    reason_match = re.search(r'reason=(\d+)', event['message'])
                    if reason_match:
                        reason_code = reason_match.group(1)
                
                # Add event with SSID, MAC, node type, and reason code
                conn_events.append({
                    'timestamp': event['timestamp'],
                    'type': event['type'],
                    'message': event['message'],
                    'node_type': node_type,
                    'ssid': current_ssid,
                    'mac': current_mac,
                    'reason_code': reason_code
                })
        
        if not conn_events:
            return
        
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        
        # 准备数据
        data = []
        for i, event in enumerate(conn_events):
            data.append({
                'timestamp': event['timestamp'],
                'event_id': i,
                'type': event['type'],
                'message': event['message'],
                'node_type': event['node_type'],
                'ssid': event['ssid'],
                'mac': event['mac'],
                'reason_code': event['reason_code']
            })
        
        # 创建散点图
        # 分析连接过程，检测异常
        # 构建连接事件序列
        connection_sequences = []
        current_sequence = []
        
        for event in data:
            if event['type'] == 'CONNECT_START':
                if current_sequence:
                    connection_sequences.append(current_sequence)
                current_sequence = [event]
            elif current_sequence:
                current_sequence.append(event)
                if event['type'] == 'DISCONNECT':
                    connection_sequences.append(current_sequence)
                    current_sequence = []
        
        if current_sequence:
            connection_sequences.append(current_sequence)
        
        # 检测异常连接
        event_is_abnormal = {}
        for sequence in connection_sequences:
            # 检查序列是否以CONNECT_START开始，以DISCONNECT结束
            if not (sequence and sequence[0]['type'] == 'CONNECT_START' and sequence[-1]['type'] == 'DISCONNECT'):
                # 标记异常事件
                for event in sequence:
                    event_is_abnormal[event['event_id']] = True
        
        fig = go.Figure()
        
        # 添加散点
        for event in data:
            # 根据事件类型和节点类型设置不同的颜色
            color_map = {
                'CONNECT_START': 'blue',
                'ASSOC_START': 'cyan',
                'ASSOC_COMPLETE': 'green',
                'HANDSHAKE_1_4': 'yellow',
                'HANDSHAKE_2_4': 'orange',
                'HANDSHAKE_3_4': 'pink',
                'HANDSHAKE_4_4': 'purple',
                'CONNECT_COMPLETE': 'darkgreen',
                'DISCONNECT': 'red'
            }
            
            # 检查是否为异常事件
            if event['event_id'] in event_is_abnormal:
                color = 'red'  # 异常事件用红色标记
            else:
                color = color_map.get(event['type'], 'gray')
            
            # 根据节点类型设置不同的标记形状
            marker_shape = 'circle' if event['node_type'] == 'wlan0' else 'square' if event['node_type'] == 'P2P' else 'diamond'
            
            # 构建悬停信息
            hover_text = (
                '<b>时间</b>: %{x|%Y-%m-%d %H:%M:%S.%f}<br>'+
                '<b>事件类型</b>: '+event['type']+'<br>'+
                '<b>节点类型</b>: '+event['node_type']+'<br>'+
                '<b>SSID</b>: '+event['ssid']+'<br>'+
                '<b>MAC地址</b>: '+event['mac']+'<br>'
            )
            
            # 为disconnect事件添加reason code
            if event['type'] == 'DISCONNECT':
                hover_text += '<b>Reason Code</b>: '+event['reason_code']+'<br>'
            
            # 添加异常标记
            if event['event_id'] in event_is_abnormal:
                hover_text += '<b>状态</b>: <span style="color:red;">连接异常</span><br>'
            else:
                hover_text += '<b>状态</b>: 连接正常<br>'
            
            hover_text += '<b>事件详情</b>: '+event['message']+'<br>'
            
            fig.add_trace(go.Scatter(
                x=[event['timestamp']],
                y=[event['event_id']],
                mode='markers',
                marker=dict(color=color, size=10, symbol=marker_shape),
                hovertemplate=hover_text,
                name=f"{event['type']} ({event['node_type']}) - {event['ssid']}"
            ))
        
        # 布局设置
        fig.update_layout(
            title='WiFi Connection Process Timeline',
            xaxis=dict(title='时间'),
            yaxis=dict(
                title='事件',
                tickvals=[event['event_id'] for event in data],
                ticktext=[f"{event['type']} ({event['node_type']}) - {event['ssid']}" for event in data]
            ),
            hovermode='closest',
            showlegend=True
        )
        
        # 保存为HTML
        html_path = os.path.join(analysis_dir, 'connection_process.html')
        fig.write_html(html_path)
        print(f"Generated connection_process.html")
    
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
    
    def generate_html_report(self):
        # 创建analysis_report文件夹
        analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
        os.makedirs(analysis_dir, exist_ok=True)
        report_path = os.path.join(analysis_dir, 'wifi_analysis_report.html')
        
        # 检查是否包含极速互传相关事件
        airtransfer_events = [e for e in self.events if e['type'] in ['AIRTRANSFER', 'P2P_STATE', 'WLAN_STATE', 'CONNECT_TO', 'SET_FREQ', 'NEAR_P2P', 'P2P_SELECTED_BSS', 'P2P_ADD_GROUP', 'SCAN_RESULTS_MATCH', 'CAPABILITIES_CHANGED', 'HOSTAPD', 'WIFI_CHANNEL', 'NOW_CONNECT']]
        is_airtransfer_issue = len(airtransfer_events) > 0
        
        # 准备HTML内容
        html_content = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi 故障分析报告</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        h1 {
            text-align: center;
            color: #2c3e50;
        }
        .section {
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .section:last-child {
            border-bottom: none;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .chart-container {
            margin: 20px 0;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        .chart-container iframe {
            width: 100%;
            height: 500px;
            border: none;
        }
        .code-block {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            font-family: monospace;
            white-space: pre-wrap;
        }
        .highlight {
            background-color: #fff3cd;
            padding: 2px 4px;
            border-radius: 3px;
        }
        .divider {
            height: 2px;
            background-color: #e0e0e0;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
'''
        
        # 添加标题
        html_content += '''
        <h1>WiFi 故障分析报告</h1>
        <div class="divider"></div>
'''
        
        # 添加基本信息
        html_content += '''
        <div class="section">
            <h2>基本信息</h2>
            <table>
                <tr>
                    <th>项目</th>
                    <th>内容</th>
                </tr>
'''
        
        if is_airtransfer_issue:
            html_content += f'''
                <tr>
                    <td>分析类型</td>
                    <td>WiFi 极速互传故障分析</td>
                </tr>
                <tr>
                    <td>测试场景</td>
                    <td>Android 设备极速互传</td>
                </tr>
                <tr>
                    <td>测试结果</td>
                    <td>存在极速互传相关问题，可能导致文件传输失败</td>
                </tr>
'''
        else:
            html_content += f'''
                <tr>
                    <td>分析类型</td>
                    <td>WiFi 连接故障分析</td>
                </tr>
                <tr>
                    <td>测试场景</td>
                    <td>Android 设备文件传输（碰传）</td>
                </tr>
                <tr>
                    <td>测试结果</td>
                    <td>存在WiFi连接问题，可能导致文件传输失败</td>
                </tr>
'''
        
        html_content += f'''
                <tr>
                    <td>日志来源</td>
                    <td>{self.log_dir}</td>
                </tr>
                <tr>
                    <td>日志时间</td>
                    <td>{min([e["timestamp"] for e in self.events]).strftime("%Y-%m-%d %H:%M") if self.events else "未知"} ~ {max([e["timestamp"] for e in self.events]).strftime("%H:%M") if self.events else "未知"}</td>
                </tr>
            </table>
        </div>
        <div class="divider"></div>
'''
        
        # 添加案例匹配
        html_content += '''
        <div class="section">
            <h2>【案例匹配】</h2>
'''
        
        if is_airtransfer_issue:
            html_content += '''
            <p>匹配案例：<strong>极速互传连接失败</strong></p>
            <p>匹配原因：日志中显示极速互传过程中存在P2P连接相关错误，可能导致传输中断</p>
'''
        else:
            html_content += '''
            <p>匹配案例：<strong>WiFi连接不稳定导致文件传输失败</strong></p>
            <p>匹配原因：日志中显示文件传输过程中存在WiFi相关错误，可能导致传输中断</p>
'''
        
        html_content += '''
        </div>
        <div class="divider"></div>
'''
        
        # 添加问题现象
        html_content += '''
        <div class="section">
            <h2>【问题现象】</h2>
            <table>
                <tr>
                    <th>序号</th>
                    <th>时间</th>
                    <th>现象</th>
                </tr>
'''
        
        if is_airtransfer_issue:
            issue_events = airtransfer_events
        else:
            issue_events = [e for e in self.events if e['type'] == 'DISCONNECT']
        
        for i, event in enumerate(issue_events):
            time_str = event['timestamp'].strftime('%H:%M:%S')
            html_content += f'''
                <tr>
                    <td>{i+1}</td>
                    <td>{time_str}</td>
                    <td>{event["message"]}</td>
                </tr>
'''
        
        if not issue_events:
            html_content += '''
                <tr>
                    <td>1</td>
                    <td>未知</td>
                    <td>未检测到相关事件</td>
                </tr>
'''
        
        html_content += '''
            </table>
        </div>
        <div class="divider"></div>
'''
        
        # 添加关键发现汇总
        html_content += '''
        <div class="section">
            <h2>【关键发现汇总】</h2>
'''
        
        if is_airtransfer_issue:
            html_content += '''
            <h3>极速互传相关事件</h3>
'''
            for i, event in enumerate(airtransfer_events):
                html_content += f'''
            <p><strong>{event["timestamp"].strftime("%H:%M:%S")} - {event["type"]}: {event["message"]}</strong></p>
'''
            html_content += '''
            <p><strong>分析：</strong> 极速互传过程中可能存在P2P连接问题，导致文件传输失败。</p>
'''
        else:
            disconnect_events = [e for e in self.events if e['type'] == 'DISCONNECT']
            if disconnect_events:
                for i, event in enumerate(disconnect_events):
                    html_content += f'''
            <h3>断连事件：{event["timestamp"].strftime("%H:%M:%S")} {event["message"]}</h3>
            <p><strong>根因：WiFi连接中断，可能导致文件传输失败。</strong></p>
            <table>
                <tr>
                    <th>时间</th>
                    <th>事件</th>
                </tr>
                <tr>
                    <td>{event["timestamp"].strftime("%H:%M:%S.%f")[:-3]}</td>
                    <td>{event["message"]}</td>
                </tr>
            </table>
            <p><strong>分析：</strong> 连接中断可能是由于网络环境干扰、驱动问题或硬件故障导致的。</p>
'''
            else:
                html_content += '''
            <h3>未检测到断连事件</h3>
            <p><strong>根因：WiFi连接稳定，未发现明显问题。</strong></p>
'''
        
        html_content += '''
        </div>
        <div class="divider"></div>
'''
        
        # 添加环境信息
        html_content += '''
        <div class="section">
            <h2>【环境信息】</h2>
            <h3>WiFi信息</h3>
            <table>
                <tr>
                    <th>参数</th>
                    <th>值</th>
                </tr>
                <tr>
                    <td>扫描结果</td>
                    <td>已扫描WiFi网络</td>
                </tr>
                <tr>
                    <td>连接状态</td>
                    <td>存在连接尝试</td>
                </tr>
            </table>
            <h3>信号强度</h3>
'''
        
        if self.rssi_data:
            min_rssi = min([r[1] for r in self.rssi_data])
            max_rssi = max([r[1] for r in self.rssi_data])
            avg_rssi = sum([r[1] for r in self.rssi_data]) / len(self.rssi_data)
            html_content += '''
            <table>
                <tr>
                    <th>参数</th>
                    <th>值</th>
                </tr>
                <tr>
                    <td>最小RSSI</td>
                    <td>{min_rssi} dBm</td>
                </tr>
                <tr>
                    <td>最大RSSI</td>
                    <td>{max_rssi} dBm</td>
                </tr>
                <tr>
                    <td>平均RSSI</td>
                    <td>{avg_rssi:.2f} dBm</td>
                </tr>
            </table>
'''.format(min_rssi=min_rssi, max_rssi=max_rssi, avg_rssi=avg_rssi)
        
        html_content += '''
        </div>
        <div class="divider"></div>
'''
        
        # 添加问题原因总结
        html_content += '''
        <div class="section">
            <h2>【问题原因总结】</h2>
            <table>
                <tr>
                    <th>序号</th>
                    <th>时间</th>
                    <th>根因</th>
                    <th>类型</th>
                </tr>
'''
        
        if is_airtransfer_issue:
            for i, event in enumerate(airtransfer_events):
                time_str = event['timestamp'].strftime('%H:%M:%S')
                html_content += f'''
                <tr>
                    <td>{i+1}</td>
                    <td>{time_str}</td>
                    <td>{event["message"]}</td>
                    <td>极速互传问题</td>
                </tr>
'''
        else:
            disconnect_events = [e for e in self.events if e['type'] == 'DISCONNECT']
            for i, event in enumerate(disconnect_events):
                time_str = event['timestamp'].strftime('%H:%M:%S')
                html_content += f'''
                <tr>
                    <td>{i+1}</td>
                    <td>{time_str}</td>
                    <td>{event["message"]}</td>
                    <td>连接断开</td>
                </tr>
'''
        
        if not issue_events:
            html_content += '''
                <tr>
                    <td>1</td>
                    <td>未知</td>
                    <td>未检测到相关事件</td>
                    <td>正常</td>
                </tr>
'''
        
        html_content += '''
            </table>
            <h3>可能的原因</h3>
            <ul>
'''
        
        if is_airtransfer_issue:
            html_content += '''
                <li><strong>P2P连接问题</strong>：可能存在P2P设备发现、连接或配对失败</li>
                <li><strong>信道干扰</strong>：WiFi信道拥堵导致P2P连接不稳定</li>
                <li><strong>设备兼容性</strong>：不同设备之间的P2P协议兼容性问题</li>
                <li><strong>驱动问题</strong>：WiFi驱动可能存在P2P相关的bug</li>
'''
        else:
            html_content += '''
                <li><strong>网络环境干扰</strong>：可能存在其他设备或信号干扰导致连接断开</li>
                <li><strong>设备驱动问题</strong>：WiFi驱动可能存在不稳定因素</li>
                <li><strong>电源管理</strong>：设备可能进入省电模式导致WiFi断开</li>
                <li><strong>网络配置</strong>：DHCP租约到期或其他网络配置问题</li>
'''
        
        html_content += '''
            </ul>
        </div>
        <div class="divider"></div>
'''
        
        # 添加流程总结
        html_content += '''
        <div class="section">
            <h2>【流程总结】</h2>
            <div class="code-block">
'''
        
        if is_airtransfer_issue:
            html_content += '''极速互传流程：\n'''
        else:
            html_content += '''WiFi连接流程：\n'''
        
        if self.events:
            for event in sorted(self.events, key=lambda x: x['timestamp']):
                time_str = event['timestamp'].strftime('%H:%M:%S')
                html_content += f'''  {time_str} - {event["type"]}: {event["message"]}\n'''
        else:
            html_content += '''  未检测到相关事件\n'''
        
        html_content += '''
            </div>
        </div>
        <div class="divider"></div>
'''
        
        # 添加信号强度与速率分析图表
        html_content += '''
        <div class="section">
            <h2>【信号强度与速率分析】</h2>
            <div class="chart-container">
                <iframe src="rssi_analysis.html"></iframe>
            </div>
            <div class="chart-container">
                <iframe src="rate_analysis.html"></iframe>
            </div>
        </div>
        <div class="divider"></div>
'''
        
        # 添加连接过程分析图表
        html_content += '''
        <div class="section">
            <h2>【连接过程分析】</h2>
            <div class="chart-container">
                <iframe src="connection_process.html"></iframe>
            </div>
        </div>
'''
        
        # 结束HTML内容
        html_content += '''
    </div>
</body>
</html>
'''
        
        # 写入HTML文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Generated HTML report: {report_path}")
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
            # 创建analysis_report文件夹
            analysis_dir = os.path.join(os.path.dirname(self.log_dir), 'analysis_report')
            os.makedirs(analysis_dir, exist_ok=True)
            
            # 准备RSSI数据
            times, rssi_values, rssi_logs = zip(*self.rssi_data)
            rssi_data = []
            for i, (t, r, log) in enumerate(zip(times, rssi_values, rssi_logs)):
                rssi_data.append({
                    'timestamp': t,
                    'value': r,
                    'log': log
                })
            
            # 创建RSSI散点图
            rssi_fig = go.Figure()
            rssi_fig.add_trace(go.Scatter(
                x=[item['timestamp'] for item in rssi_data],
                y=[item['value'] for item in rssi_data],
                mode='markers',
                marker=dict(color='blue', size=8),
                hovertemplate=
                    '<b>时间</b>: %{x|%Y-%m-%d %H:%M:%S.%f}<br>'+
                    '<b>RSSI值</b>: %{y} dBm<br>'+
                    '<b>日志信息</b>: %{text}<br>',
                text=[item['log'] for item in rssi_data],
                name='RSSI'
            ))
            
            rssi_fig.update_layout(
                title='WiFi RSSI Signal Strength',
                xaxis=dict(title='时间'),
                yaxis=dict(title='RSSI (dBm)'),
                hovermode='closest'
            )
            
            # 保存RSSI图表
            rssi_html_path = os.path.join(analysis_dir, 'rssi_analysis.html')
            rssi_fig.write_html(rssi_html_path)
            print(f"Generated rssi_analysis.html")
            
            # 准备速率数据
            if self.rate_data:
                times_rate, rate_values, rate_logs = zip(*self.rate_data)
                rate_data = []
                for i, (t, r, log) in enumerate(zip(times_rate, rate_values, rate_logs)):
                    rate_data.append({
                        'timestamp': t,
                        'value': r,
                        'log': log
                    })
                
                # 创建速率散点图
                rate_fig = go.Figure()
                rate_fig.add_trace(go.Scatter(
                    x=[item['timestamp'] for item in rate_data],
                    y=[item['value'] for item in rate_data],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    hovertemplate=
                        '<b>时间</b>: %{x|%Y-%m-%d %H:%M:%S.%f}<br>'+
                        '<b>速率值</b>: %{y} Kbps<br>'+
                        '<b>日志信息</b>: %{text}<br>',
                    text=[item['log'] for item in rate_data],
                    name='Rate'
                ))
                
                rate_fig.update_layout(
                    title='WiFi Tx Rate',
                    xaxis=dict(title='时间'),
                    yaxis=dict(title='Rate (Kbps)'),
                    hovermode='closest'
                )
                
                # 保存速率图表
                rate_html_path = os.path.join(analysis_dir, 'rate_analysis.html')
                rate_fig.write_html(rate_html_path)
                print(f"Generated rate_analysis.html")
        
        # Plot connection timeline
        self.plot_connection_timeline()
        
        # Plot connection process
        self.plot_connection_process()
        
        # Generate markdown report
        self.generate_markdown_report()
        
        # Generate HTML report
        self.generate_html_report()
        
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
