# Android WiFi Bug Analysis Skill

> Domain: **WiFi / WLAN Connectivity**
> Platform: Android Open Source Project (AOSP)
> Version Scope: Android 10 – 16 (API 29–36)
> Last Updated: 2026

***

## 1. Log Filter Tags

Use these logcat tags to extract WiFi-relevant entries from `main_log_*`, `sys_log_*`, or raw `logcat` captures.

### 1.1 Core WiFi Framework Tags

| Tag                             | Layer         | Description                                                            |
| ------------------------------- | ------------- | ---------------------------------------------------------------------- |
| `WifiService`                   | Framework     | Main WiFi system service entry point; handles API calls from apps      |
| `WifiManager`                   | Framework/App | Client-side WiFi API; logs from apps interacting with WiFi             |
| `WifiStateMachine`              | Framework     | (Legacy, pre-Android 12) WiFi state machine driving connect/disconnect |
| `WifiClientModeImpl`            | Framework     | (Android 12+) Replacement for WifiStateMachine; manages STA mode       |
| `ClientModeImpl`                | Framework     | Alias used in some AOSP branches for WifiClientModeImpl                |
| `WifiConnectivityManager`       | Framework     | Auto-connect logic; decides when and which network to connect          |
| `WifiNetworkSelector`           | Framework     | Scores and selects candidate networks from scan results                |
| `WifiConfigManager`             | Framework     | Manages saved network configurations; add/remove/update                |
| `WifiConfigStore`               | Framework     | Persistent storage of WiFi configurations                              |
| `WifiScanningService`           | Framework     | Manages scan scheduling (single scan, PNO, background scan)            |
| `WifiScoreReport`               | Framework     | Reports WiFi quality score to ConnectivityService                      |
| `WifiScoreCard`                 | Framework     | Historical quality tracking per BSSID/SSID                             |
| `WifiTrafficPoller`             | Framework     | Polls traffic stats for active data transfer detection                 |
| `WifiNative`                    | Framework/JNI | JNI bridge between Java framework and native daemon (wificond/HAL)     |
| `WifiMonitor`                   | Framework     | Parses events from wpa\_supplicant via wificond                        |
| `WifiDiagnostics`               | Framework     | Diagnostic data collection (ring buffers, firmware dumps)              |
| `WifiVendorHal`                 | Framework/HAL | Vendor HAL interaction (IWifiStaIface, IWifiChip)                      |
| `WifiHAL`                       | HAL           | Hardware Abstraction Layer for WiFi chipset                            |
| `WifiP2pManager`                | Framework/App | WiFi Direct (P2P) client API                                           |
| `WifiP2pService`                | Framework     | WiFi Direct service-side logic                                         |
| `WifiP2pNative`                 | Framework     | P2P native interface                                                   |
| `WifiAwareService`              | Framework     | WiFi Aware (NAN) service                                               |
| `WifiRttService`                | Framework     | WiFi Round-Trip-Time ranging service                                   |
| `WifiWatchdogStateMachine`      | Framework     | (Legacy) Monitors WiFi connection quality                              |
| `SupplicantStateTracker`        | Framework     | Tracks wpa\_supplicant state transitions                               |
| `WifiNetworkFactory`            | Framework     | Handles network requests from apps via NetworkRequest                  |
| `WifiNetworkSuggestionsManager` | Framework     | Manages carrier/app network suggestions                                |
| `PasspointManager`              | Framework     | Hotspot 2.0 / Passpoint profile management                             |
| `SoftApManager`                 | Framework     | WiFi Hotspot (tethering) AP mode management                            |
| `WifiApConfigStore`             | Framework     | Hotspot configuration persistence                                      |

### 1.2 Supplicant & Native Daemon Tags

| Tag              | Layer  | Description                                                |
| ---------------- | ------ | ---------------------------------------------------------- |
| `wpa_supplicant` | Native | Core 802.11 authentication & association daemon            |
| `wificond`       | Native | WiFi condition daemon; manages scan & NL80211 interface    |
| `hostapd`        | Native | Access-point daemon for WiFi hotspot mode                  |
| `netd`           | Native | Network daemon; iptables, routing, interface configuration |

### 1.3 Network / IP Layer Tags

| Tag                     | Layer     | Description                                                       |
| ----------------------- | --------- | ----------------------------------------------------------------- |
| `ConnectivityService`   | Framework | System connectivity management; network validation, default route |
| `NetworkAgent`          | Framework | Per-network agent reporting score & capabilities                  |
| `IpClient`              | Framework | IP provisioning state machine (DHCP, static, link-local)          |
| `DhcpClient`            | Framework | DHCP v4 client state machine                                      |
| `Osu`                   | Framework | Online Sign-Up (Passpoint)                                        |
| `IpReachabilityMonitor` | Framework | ARP/ND-based gateway reachability checks                          |
| `NetworkMonitor`        | Framework | Captive portal detection and network validation                   |
| `DnsResolver`           | Native    | DNS resolution                                                    |
| `IpConnectivityLog`     | Framework | IP connectivity event metrics                                     |

### 1.4 Kernel / Driver Level Tags (dmesg / kernel log)

| Tag / Prefix                | Description                             |
| --------------------------- | --------------------------------------- |
| `cfg80211`                  | Linux wireless configuration subsystem  |
| `mac80211`                  | Linux MAC layer for WiFi                |
| `wlan0` / `wlan1`           | WiFi network interface events           |
| `ieee80211`                 | IEEE 802.11 stack messages              |
| `ath` / `ath10k` / `ath11k` | Qualcomm Atheros driver (if applicable) |
| `wcnss` / `icnss`           | Qualcomm WCNSS/ICNSS platform driver    |
| `brcmfmac` / `brcmsmac`     | Broadcom WiFi driver                    |
| `mtk_wlan` / `wmt`          | MediaTek WiFi driver                    |
| `dhd`                       | Broadcom dongle host driver             |
| `CNSS`                      | Qualcomm Connectivity subsystem         |
| `firmware`                  | Firmware load/crash events              |

### 1.5 Recommended Logcat Filter Command

```bash
# Comprehensive WiFi filter — mainlog
logcat -v threadtime | grep -iE \
  "WifiService|WifiManager|WifiStateMachine|WifiClientModeImpl|ClientModeImpl|\
WifiConnectivityManager|WifiNetworkSelector|WifiConfigManager|WifiConfigStore|\
WifiScanningService|WifiScoreReport|WifiScoreCard|WifiTrafficPoller|WifiNative|\
WifiMonitor|WifiDiagnostics|WifiVendorHal|WifiHAL|\
WifiP2pManager|WifiP2pService|WifiP2pNative|\
WifiAwareService|WifiRttService|\
WifiWatchdogStateMachine|SupplicantStateTracker|\
WifiNetworkFactory|WifiNetworkSuggestionsManager|\
PasspointManager|SoftApManager|WifiApConfigStore|\
wpa_supplicant|wificond|hostapd|\
ConnectivityService|NetworkAgent|IpClient|DhcpClient|\
IpReachabilityMonitor|NetworkMonitor|netd"
```

```bash
# Kernel log WiFi filter
dmesg | grep -iE "cfg80211|mac80211|wlan[0-9]|ieee80211|wcnss|icnss|cnss|dhd|mtk_wlan|wmt|brcmfmac|firmware|ath10k|ath11k"
```

***

## 2. Key Log Patterns

These are the critical patterns to search for when triaging WiFi bugs.

### 2.1 Connection Failures

```
# Association rejection
wpa_supplicant: wlan0: CTRL-EVENT-ASSOC-REJECT bssid=XX:XX:XX:XX:XX:XX status_code=<N>

# Association timeout
wpa_supplicant: wlan0: CTRL-EVENT-SSID-TEMP-DISABLED id=<N> ssid="<SSID>" auth_failures=<N>

# Connection timeout
WifiStateMachine: Timed out waiting for supplicant state change
WifiClientModeImpl: CMD_CONNECTING_WATCHDOG_TIMER

# Network not found after scan
WifiConnectivityManager: connectToNetwork: Cannot find network
WifiNetworkSelector: No candidates selected

# 4-way handshake failure
wpa_supplicant: wlan0: WPA: 4-Way Handshake failed
wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED reason=15  # (4-way handshake timeout)
```

### 2.2 Authentication Errors

```
# Wrong password / PSK mismatch
wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED reason=2  # PREV_AUTH_NOT_VALID
wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED reason=23 # IEEE_802_1X_AUTH_FAILED
SupplicantStateTracker: Authentication failure

# EAP authentication failure (Enterprise)
wpa_supplicant: wlan0: EAP: EAP entering state FAILURE
wpa_supplicant: wlan0: CTRL-EVENT-EAP-FAILURE
wpa_supplicant: wlan0: EAP-TLS: TLS processing failed

# SAE (WPA3) authentication failure
wpa_supplicant: wlan0: SAE: authentication failure
wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED reason=1  # UNSPECIFIED
```

### 2.3 DHCP Failures

```
# DHCP timeout
DhcpClient: DHCP timeout
DhcpClient: Failed to get DHCP lease
IpClient: IP provisioning timed out

# DHCP NAK
DhcpClient: Received DHCPNAK

# DHCP DECLINE (duplicate IP)
DhcpClient: Sending DHCPDECLINE

# No DHCP offer
DhcpClient: No DHCPOFFER received

# IP provisioning failure
IpClient: onProvisioningFailure
WifiStateMachine: IP_CONFIGURATION_LOST
WifiClientModeImpl: CMD_IP_CONFIGURATION_LOST
```

### 2.4 Roaming Issues

```
# Roaming event
wpa_supplicant: wlan0: CTRL-EVENT-CONNECTED - Connection to XX:XX:XX:XX:XX:XX completed [id=N id_str=] (auth) [REASSOCIATE]

# Roaming failure
wpa_supplicant: wlan0: CTRL-EVENT-DISCONNECTED bssid=XX:XX:XX:XX:XX:XX reason=<N> locally_generated=<0/1>
WifiConnectivityManager: Roaming failed

# Excessive roaming
WifiScoreCard: Multiple BSSID changes detected in short window

# BSSID blacklist (bad roam target)
WifiConnectivityManager: BSSID blacklisted: XX:XX:XX:XX:XX:XX
WifiNetworkSelector: Filtered out BSSID XX:XX:XX:XX:XX:XX
```

### 2.5 Scan Failures

```
# Scan failure
WifiScanningService: Scan failed
WifiNative: Scan failed
wificond: Scan failed with error code: <N>

# PNO scan failure
WifiConnectivityManager: Failed to start PNO scan
WifiNative: PNO scan failed

# No scan results
WifiScanningService: No scan results returned
WifiNative: getScanResults failed
```

### 2.6 P2P / WiFi Direct Failures

```
# P2P group formation failure
WifiP2pService: Group formation failed
wpa_supplicant: P2P-GROUP-FORMATION-FAILURE

# P2P device discovery failure
WifiP2pService: Discovery failed
wpa_supplicant: P2P-FIND-STOPPED

# P2P invitation failure
wpa_supplicant: P2P-INVITATION-RESULT status=<N>

# GO negotiation failure
wpa_supplicant: P2P-GO-NEG-FAILURE
```

### 2.7 Hotspot (SoftAP) Issues

```
# Hotspot start failure
SoftApManager: Failed to start soft AP
hostapd: Failed to set up interface
hostapd: Could not set channel for kernel driver

# Client disconnected from hotspot
hostapd: wlan1: STA XX:XX:XX:XX:XX:XX deauthenticated
SoftApManager: Number of connected clients changed

# Hotspot auto-shutdown
SoftApManager: Timeout, no clients connected
```

### 2.8 DNS Resolution Failures

```
# DNS failure
NetworkMonitor: HTTPS probe failed for https://www.google.com
NetworkMonitor: Captive portal detected
ConnectivityService: Network has no internet access

# DNS timeout
DnsResolver: DNS query timeout for <domain>
NetworkMonitor: DNS resolution failed

# Captive portal
NetworkMonitor: Captive portal detected for network <N>
ConnectivityService: NetworkAgent captive portal detected
```

### 2.9 Android 16 (API 36) WiFi-Specific Triage Patterns

```
# Local-only connection rejected by user / system approval flow
WifiService: LocalOnlyConnection failed: user rejected request
WifiManager: STATUS_LOCAL_ONLY_CONNECTION_FAILURE_USER_REJECT

# Secure RTT / 802.11az / PASN ranging capability mismatch
WifiRttService: ranging failed - secure ranging required
WifiRttService: PASN comeback timer active
WifiRttService: ranging frame protection not supported
ScanResult: isRangingFrameProtectionRequired=true
ScanResult: isSecureHeLtfSupported=false

# Wi-Fi Direct R2 / PCC / 6 GHz negotiation issues
WifiP2pService: Wi-Fi Direct R2 unsupported on peer
WifiP2pService: PCC mode unsupported
WifiP2pService: bootstrapping method mismatch
WifiP2pService: group owner band 6GHz rejected
WifiP2pService: WPA3 SAE group formation failed

# SoftAP per-band / per-channel / width issues
SoftApManager: configured channels map invalid
SoftApManager: channel width unsupported
hostapd: ACS failed for requested 6 GHz channel
hostapd: DFS or regulatory restriction prevented channel selection
```

### 2.10 RSSI Signal Strength Patterns

```
# RSSI signal strength (MTK)
mtk_cfg80211_get_station: RSSI=-<value>dBm

# Link Quality Monitor (MTK) - 协商速率统计
[wlan][<pid>]wlanLinkQualityMonitor:(SW4 INFO) Link Quality: Tx(rate:<tx_rate>, total:<total>, retry:<retry>, fail:<fail>, RTS fail:<rts_fail>, ACK fail:<ack_fail>), Rx(rate:<rx_rate>, total:<total>, dup:<dup>, error:<error>), PER(<per>), Congestion(idle slot:<idle>, diff:<diff>, AwakeDur:<awake>)

# Throughput Monitor (MTK) - 实时Tput统计
[wlan][<pid>]kalPerMonUpdate:(SW4 INFO) <interval> Tput: <throughput>(<mbps>mbps) [<tx_packets>,<tx_errors>,<rx_packets>,<rx_errors>] Pending:<pending>/<max> LQ[<rssi>,<link_quality>,<snr>,<congestion>] idle:<idle> lv:<level> th:<threshold> fg:<flags>
```

***

<br />

## 3. Analysis Procedure

Follow this step-by-step methodology when analyzing a WiFi bug.

### Step 1: Identify the Symptom Category

Read the bug title, description, and test steps. Classify the issue:

| Category                         | Symptoms                                                                           | Primary Logs                                                                            |
| -------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Connectivity**                 | Cannot connect, drops, authentication failure                                      | main\_log\_\* (wpa\_supplicant, WifiStateMachine, DhcpClient)                           |
| **Performance**                  | Slow speed, high latency, packet loss                                              | main\_log\_\* (WifiScoreReport), kernel\_log\_\* (driver stats)                         |
| **Stability**                    | Random disconnects, WiFi toggle unresponsive, crash                                | main\_log\_\* + kernel\_log\_\* (firmware crash)                                        |
| **Functionality**                | P2P broken, hotspot fails, scan empty                                              | main\_log\_\* (WifiP2pService, SoftApManager, WifiScanningService)                      |
| **Android16 Feature Regression** | Local-only connection rejected, secure RTT fails, Wi-Fi Direct R2/PCC/6 GHz issues | main\_log\_\* (WifiService, WifiManager, WifiRttService, WifiP2pService, SoftApManager) |
| **Power**                        | Excessive battery drain from WiFi, scan storms                                     | main\_log\_\* (WifiScanningService, WifiTrafficPoller)                                  |

**Action:** Tag the bug category and note the expected log areas.

### Step 2: Check WiFi State Machine Transitions

The WiFi state machine is the backbone. Look for the transition path:

```
Expected happy path:
DisconnectedState → ScanModeState → ConnectingState → L2ConnectedState → ConnectedState

For Android 12+:
DisconnectedState → ConnectingState → L2ConnectedState → ConnectedState
```

**What to look for:**

- Did the state machine reach `ConnectingState`? If not → scan or network selection issue.
- Did it reach `L2ConnectedState` but not `ConnectedState`? → DHCP/IP provisioning issue.
- Did it stay in `ConnectedState` briefly then go to `DisconnectedState`? → Roaming or link quality issue.
- Did it get stuck in any state? → Possible deadlock or framework bug.

**Filter:**

```bash
grep -E "transitionTo|processMsg|CMD_" main_log_* | grep -iE "WifiStateMachine|WifiClientModeImpl|ClientModeImpl"
```

### Step 3: Analyze Supplicant State Changes

Trace the wpa\_supplicant control events:

```
Expected connection sequence:
CTRL-EVENT-SCAN-STARTED
CTRL-EVENT-SCAN-RESULTS
CTRL-EVENT-SSID-REENABLED (if previously disabled)
Associating with XX:XX:XX:XX:XX:XX
Associated with XX:XX:XX:XX:XX:XX
CTRL-EVENT-SUBNET-STATUS-UPDATE
CTRL-EVENT-CONNECTED
```

**Failure indicators:**

- `CTRL-EVENT-ASSOC-REJECT` → AP rejected association. Check `status_code`:
  - `status_code=1` → Unspecified failure
  - `status_code=12` → Association denied (AP full)
  - `status_code=17` → Association denied (capabilities mismatch)
  - `status_code=34` → Anti-clogging token required (SAE)
- `CTRL-EVENT-DISCONNECTED reason=N` → Reason code from AP or local:
  - `reason=2` → Previous auth invalid
  - `reason=3` → Deauth leaving BSS
  - `reason=6` → Class 2 frame from non-auth STA
  - `reason=7` → Class 3 frame from non-assoc STA
  - `reason=15` → 4-way handshake timeout
  - `reason=16` → Group key handshake timeout
  - `locally_generated=1` → Disconnect initiated by our side

### Step 4: Check DHCP Negotiation

After L2 connection, IP provisioning must succeed:

```
Expected DHCP sequence:
DhcpClient: Sending DHCPDISCOVER
DhcpClient: Received DHCPOFFER from <server>
DhcpClient: Sending DHCPREQUEST
DhcpClient: Received DHCPACK from <server>
IpClient: onProvisioningSuccess
```

**Failure checklist:**

- [ ] Is DHCPDISCOVER sent? (If not → L2 not fully connected, or IpClient not started)
- [ ] Is DHCPOFFER received? (If not → DHCP server unreachable, VLAN issue)
- [ ] Is DHCPACK received? (If not → IP conflict, server-side reject)
- [ ] Does IpClient report success? (If not → duplicate address detection failed)
- [ ] What is the lease time? (Very short leases can cause frequent renewals)

**Filter:**

```bash
grep -iE "DhcpClient|IpClient|onProvisioning" main_log_*
```

### Step 5: Verify IP Connectivity

After IP is provisioned, check network validation:

```
Expected validation sequence:
NetworkMonitor: Checking network connectivity
NetworkMonitor: HTTPS probe succeeded for https://www.google.com/generate_204
ConnectivityService: Network validated
```

**Issues:**

- Captive portal detected → Network requires login, may be expected
- Partial connectivity → DNS works but HTTP fails, or vice versa
- No internet → Gateway unreachable, DNS failure, or firewall

**Filter:**

```bash
grep -iE "NetworkMonitor|ConnectivityService|NetworkAgent|IpReachabilityMonitor" main_log_*
```

### Step 6: Look for Error Patterns and Exceptions

Search for exceptions, fatal errors, and ANRs related to WiFi:

```bash
# Java exceptions in WiFi stack
grep -A 10 "Exception" main_log_* | grep -iB 2 -A 8 "wifi\|wpa\|supplicant\|dhcp\|IpClient"

# Fatal / WTF logs
grep -iE "FATAL|WTF|wtf|fatal" main_log_* | grep -i wifi

# ANR involving WiFi
grep -iE "ANR in|not responding" main_log_* | grep -i wifi

# Binder transaction failures
grep -iE "Binder.*wifi\|TransactionTooLargeException" main_log_*
```

### Step 7: Check for Firmware / Driver Crashes

WiFi firmware and driver crashes often manifest as sudden disconnects:

**In kernel log / dmesg:**

```bash
# Firmware crash / assert
grep -iE "firmware crash|firmware assert|fw crash|fw assert|SSR|subsystem restart" kernel_log

# Driver errors
grep -iE "error|fail|timeout|hung|panic" kernel_log_* | grep -iE "wlan|wifi|wcnss|icnss|cnss|dhd|mtk"

# Interface state changes
grep -iE "wlan[0-9].*UP|wlan[0-9].*DOWN|wlan[0-9].*DORMANT" kernel_log

# PCIe/SDIO bus errors (chip communication)
grep -iE "pcie.*error|sdio.*error|mmc.*error|bus.*error" kernel_log_* | grep -iE "wlan|wifi"
```

**Indicators of firmware crash:**

- `subsystem restart` or `SSR` messages → SoC restarted WiFi subsystem
- `wlan0: link is not ready` followed by re-initialization
- Rapid disconnect→reconnect cycle without user action
- `Firmware not responding` or `Firmware crashed`

### Step 8: Correlate with System Events

WiFi bugs often correlate with system-level events:

```bash
# Screen on/off (affects scan behavior and power saving)
grep -iE "Screen.*on|Screen.*off|setInteractive|PowerManagerService.*Going to sleep|PowerManagerService.*Waking up" main_log_*

# Doze / App Standby
grep -iE "DeviceIdleController|mState.*IDLE|DEEP_IDLE|LIGHT_IDLE" main_log_*

# Airplane mode
grep -iE "AirplaneModeOn|AirplaneModeOff|AIRPLANE_MODE" main_log_*

# App-initiated WiFi changes
grep -iE "WifiManager.*enableNetwork|WifiManager.*disconnect|WifiManager.*reconnect" main_log_*

# Thermal throttling
grep -iE "thermal.*throttl|ThermalService|cooling_device" main_log_* kernel_log_*

# Memory pressure
grep -iE "lowmemorykiller|oom_adj|kswapd" kernel_log | head -20
```

**Correlation timeline:** Build a time-ordered sequence of:

1. System event (screen off / doze entered / app switch)
2. WiFi state change (disconnect / scan stop / power save mode)
3. User-visible symptom (no internet, slow connection)

This reveals whether the root cause is a system policy issue vs. a WiFi stack bug.

### Step 9: Android 16 Feature Gates and Capability Checks

For Android 16 / API 36 bugs, explicitly separate framework policy failures from RF/driver failures:

1. Local-only connection:
   - If logs mention `STATUS_LOCAL_ONLY_CONNECTION_FAILURE_USER_REJECT`, treat this as approval/UI rejection, not AP/auth failure.
   - Correlate with app flow, foreground state, and user consent timing.
2. Secure RTT / 802.11az ranging:
   - Check whether AP/peer requires ranging frame protection.
   - Check whether secure HE-LTF is supported on both sides.
   - If PASN/comeback timer appears, classify as secure-ranging negotiation failure before blaming HAL.
3. Wi-Fi Direct R2 / PCC / 6 GHz:
   - Distinguish legacy P2P failures from R2/PCC/bootstrapping/security-type mismatch.
   - Look for `R2`, `PCC`, `bootstrapping`, `WPA3`, `6GHz`, `DIR`, `USD` keywords.
4. SoftAP channel selection:
   - On Android 16, hotspot failures may come from invalid band→channel mapping or unsupported channel width.
   - Correlate `SoftApManager` with `hostapd` and regulatory / DFS restrictions before escalating to driver/firmware.

***

## 4. Common Root Causes

### 4.1 Connection Failures

| Root Cause                       | Log Indicators                                                                         | Resolution Direction                                     |
| -------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| **Wrong password saved**         | `CTRL-EVENT-DISCONNECTED reason=2`, `auth_failures` incrementing, `SSID-TEMP-DISABLED` | Forget network and re-enter password                     |
| **AP association table full**    | `CTRL-EVENT-ASSOC-REJECT status_code=17`                                               | AP-side config; reduce max clients or kick idle          |
| **Frequency band mismatch**      | Scan results show AP on 5GHz but device only scanning 2.4GHz (or vice versa)           | Check regulatory domain and band settings                |
| **Hidden network not found**     | No scan results for configured hidden SSID, `connectToNetwork: Cannot find network`    | Verify SSID spelling; force active scan                  |
| **EAP misconfiguration**         | `EAP-TLS: TLS processing failed`, `EAP entering state FAILURE`                         | Check certificate, identity, anonymous identity, CA cert |
| **WPA3/SAE incompatibility**     | `SAE: authentication failure`, status\_code=77                                         | Downgrade to WPA2 or update supplicant                   |
| **Local-only approval rejected** | `STATUS_LOCAL_ONLY_CONNECTION_FAILURE_USER_REJECT`                                     | Fix UX / approval flow; not a WiFi chipset defect        |

### 4.2 Disconnection / Drops

| Root Cause                  | Log Indicators                                                        | Resolution Direction                             |
| --------------------------- | --------------------------------------------------------------------- | ------------------------------------------------ |
| **Firmware crash**          | `SSR`, `subsystem restart`, `firmware crash`, rapid interface down/up | Firmware update; collect ramdump for vendor      |
| **AP-initiated deauth**     | `CTRL-EVENT-DISCONNECTED locally_generated=0 reason=3`                | AP-side issue (load balancing, idle timeout)     |
| **DHCP lease expired**      | `DhcpClient: lease expired`, `IP_CONFIGURATION_LOST`                  | Check DHCP server; increase lease time           |
| **Gateway unreachable**     | `IpReachabilityMonitor: FAILURE`, `Lost default router`               | ARP failure; check AP isolation, gateway health  |
| **Poor RSSI / roaming gap** | `RSSI: -80dBm`, `WifiScoreReport: score=<low>`                        | Improve AP coverage; tune roaming aggressiveness |
| **Doze mode disconnect**    | Disconnect shortly after `DeviceIdleController: mState=IDLE`          | Check WiFi keep-alive/allow-while-idle settings  |

### 4.3 Performance Issues

| Root Cause                  | Log Indicators                                         | Resolution Direction                                  |
| --------------------------- | ------------------------------------------------------ | ----------------------------------------------------- |
| **Channel congestion**      | Many BSSIDs on same channel in scan results            | Switch AP to less congested channel                   |
| **Power save aggressive**   | `SET_POWER_SAVE_MODE`, latency spikes after screen off | Tune power save settings; use high-perf WiFi lock     |
| **TX/RX rate drop**         | Link speed drops in `WifiInfo` updates                 | Interference; check for co-channel / adjacent channel |
| **Thermal throttling**      | `thermal throttling`, TX power reduced                 | Reduce workload; check thermal design                 |
| **Driver TX queue backlog** | `netdev_budget` consumed, softirq delay in kernel log  | Driver optimization needed                            |

### 4.4 Scan Failures

| Root Cause                                 | Log Indicators                                                                                               | Resolution Direction                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| **wificond crash**                         | `wificond` died, `DeathRecipient: wificond died`                                                             | Check tombstone; wificond restart logic                     |
| **Regulatory domain wrong**                | Missing channels in scan results, `cfg80211: Regulatory domain changed`                                      | Set correct country code                                    |
| **Scan throttling**                        | `WifiScanningService: Scan request throttled`                                                                | Too many scan requests from apps; normal behavior           |
| **Secure RTT capability mismatch**         | `secure ranging required`, `ranging frame protection not supported`, PASN/comeback timer logs                | Validate AP + STA 802.11az / PASN capability alignment      |
| **Wi-Fi Direct R2 / PCC mismatch**         | `R2 unsupported`, `PCC mode unsupported`, `bootstrapping method mismatch`, `WPA3 SAE group formation failed` | Align peer capabilities; retry in legacy P2P mode if needed |
| **SoftAP invalid channel/width selection** | `configured channels map invalid`, `channel width unsupported`, `ACS failed for requested 6 GHz channel`     | Use supported band/channel/width; verify regulatory domain  |

***

## 5. Severity Assessment

Use these criteria to assess or validate the severity of a WiFi bug:

### Blocker (P0)

- WiFi **cannot be enabled** (toggle fails, service crash loop)
- WiFi firmware crash causes **system reboot** or **kernel panic**
- **Data loss** due to WiFi connectivity issue (e.g., file transfer corruption)
- **Security vulnerability** — open network auto-connect, credential leak
- WiFi completely non-functional on **production builds** for a device SKU

### Critical (P1)

- WiFi **connects but no internet** consistently on common AP types (home routers)
- **Frequent disconnects** (>3 per hour under normal use) without user action
- WiFi **does not reconnect** after airplane mode toggle / sleep-wake
- Hotspot **fails to start** or crashes consistently
- Firmware crash (SSR) occurring **more than once per day** under normal use
- WiFi **throughput <10% of expected** (e.g., <10 Mbps on an 802.11ac link)

### Major (P2)

- WiFi connects but **intermittent drops** (1-3 per day under normal use)
- **Roaming failure** between APs in enterprise environments
- **DHCP timeout** on first connection (but retry succeeds)
- WiFi Direct (P2P) **fails to establish** group consistently
- **Scan results delayed** >10 seconds
- WiFi **performance degradation** (30-50% below expected throughput)

### Minor (P3)

- WiFi status **UI not updating** correctly (cosmetic)
- Minor **scan result inaccuracy** (stale BSSID listed)
- **Occasional slow reconnect** after sleep (<1 per day)
- WiFi Direct works but **takes >30 seconds** to establish
- **Log noise** — excessive logging from WiFi stack (no functional impact)

### Trivial (P4)

- Log formatting issues
- Deprecated API usage warnings with no functional impact
- Missing translations in WiFi settings UI

***

## 6. Output Format Template

When producing a bug analysis report, use this structure:

```
## Bug Analysis Report

**Bug ID:** <Jira ID>
**Title:** <Bug title>
**Severity:** <Blocker|Critical|Major|Minor>
**Component:** WiFi
**Sub-area:** <Connectivity|Performance|Stability|Functionality|Power>

### Symptom Summary
<One paragraph describing the user-visible problem>

### Log Analysis
- **State Machine Path:** <trace of WiFi state transitions observed>
- **Supplicant Events:** <key wpa_supplicant events and their meaning>
- **DHCP Status:** <DHCP negotiation outcome>
- **Network Validation:** <connectivity check results>
- **Error Patterns:** <exceptions, crashes, failures found>
- **System Correlation:** <related system events: doze, screen, thermal>
- **Android 16 Checks:** <local-only approval, secure RTT/PASN, Wi-Fi Direct R2/PCC, SoftAP channel-width constraints>

### Root Cause Assessment
<Diagnosis of the most likely root cause with supporting evidence from logs>

### Confidence Level
<High|Medium|Low> — <explanation of confidence>

### Recommended Actions
1. <First action item>
2. <Second action item>
3. <Third action item>

### Additional Data Needed
- <Any missing info that would help confirm diagnosis>
```

***

## 7. Quick Reference: WiFi Disconnect Reason Codes (IEEE 802.11)

| Code | Meaning                                                          |
| ---- | ---------------------------------------------------------------- |
| 1    | Unspecified reason                                               |
| 2    | Previous authentication no longer valid                          |
| 3    | Deauthenticated because station is leaving                       |
| 4    | Disassociated due to inactivity                                  |
| 5    | Disassociated because AP is unable to handle all associated STAs |
| 6    | Class 2 frame received from non-authenticated STA                |
| 7    | Class 3 frame received from non-associated STA                   |
| 8    | Disassociated because station is leaving BSS                     |
| 9    | STA requesting (re)association not authenticated                 |
| 14   | MIC failure                                                      |
| 15   | 4-Way Handshake timeout                                          |
| 16   | Group Key Handshake timeout                                      |
| 34   | Requested from peer STA as it does not want to use the mechanism |
| 45   | Peer STA does not support requested cipher suite                 |

***

***

## 3. Vendor-Specific Patterns

> This section covers QCOM and MTK WiFi chipset / firmware log surface that is
> vendor-proprietary but commonly observed in real bug reports on commercial devices.

### 3.1 QCOM WiFi (qcwcn / WCNSS / wlan kernel)

QCOM WiFi components on Android: `wlan_hdd` (WLAN Host Driver), `wcnss` (WCNSS daemon),
`qcwcn` (QCOM WiFi framework shim), `WLAN_NV` (binning NV blob), thermal.

**Key log sources:**

| Tag / Keyword       | Component          | Meaning                                             |
| ------------------- | ------------------ | --------------------------------------------------- |
| `wlan_hdd`          | Kernel/HDD         | wlan host driver events, STA/FW interface events    |
| `wcnss_ctrl`        | WCNSS daemon       | WCNSS firmware interaction, SSR (Subsystem Restart) |
| `qcwcn`             | QCOM framework     | QCOM-specific WiFi state and power events           |
| `WLAN_NV` / `nvbin` | NV blob            | Antenna / TX power NV download status               |
| `thermal` + `wlan`  | Thermal            | WiFi TX power backoff due to thermal                |
| `SVC`               | SVC logs           | Qualcomm SVC framework WiFi indicators              |
| `WCNSS_qcom_wlan`   | Kernel ring buffer | Low-level firmware trace                            |

**Common QCOM WiFi failure patterns:**

```
wlan_hdd: [E] %s: FAIL: set assoc req IE failed, result=<N>
wlan_hdd: [E] %s: set_key failed, cipher=<N>, error=<N>
wcnss: [F] wcnss: saw firmware crash, reason=0x%04x
wcnss: [E] wcnss: FW assertion: assertion_type=<N>, line=<N>
qcwcn: [E] %s: driver down, status=%d
qcwcn: [W] %s: thermal_throt_level=%d, reduce TX power
WLAN_NV: [E] nvbin download failed: status=%d
thermal_engine: wlan: thermal_zone trip, temp=%d threshold=%d
```

**QCOM WiFi SSR (Subsystem Restart) sequence:**

```
wcnss: [I] wcnss: initiating SSR
wcnss: [E] wcnss: FW crash detected, target_type=%d
kernel: wlan: wcnss: subsys-restart: reason=0x%x
kernel: wlan: wcnss: shutting down
kernel: wcnss: subsys-restart: reset nucleaus
wcnss: [I] wcnss: FW reloading
wcnss: [I] wcnss: FW ready after SSR
```

**QCOM WiFi triage checklist:**

- [ ] Check `wcnss` for SSR: crash reason, before attributing to framework
- [ ] Check `thermal_engine` for TX backoff / thermal throttling
- [ ] Check `nvbin` for NV blob download failure (antenna calibration lost)
- [ ] Check `wlan_hdd set_key failed` for WPA3/GCMP cipher issues
- [ ] Check `qcwcn driver down` vs framework `WifiClientModeImpl` — distinguish chip vs OS
- [ ] For QCOM location-specific WiFi: also check `location_hub` / `gpsone_daemon`

### 3.2 MTK WiFi (Mediatek / conninfra / meta)

MTK WiFi components: `conninfra` (Connectivity Infrastructure driver), `wlan` (MTK wlan driver),
`met` (MACE / Meta WiFi logs), `epo` (Extended Position Observer — MTK A-GPS blob).

**Key log sources:**

| Tag / Keyword  | Component       | Meaning                                                     |
| -------------- | --------------- | ----------------------------------------------------------- |
| `conninfra`    | Kernel/Driver   | MTK connectivity infra driver — WiFi/BT/FM power sequencing |
| `wlan`         | MTK wlan driver | MTK WLAN events, TX/RX stats, scan results                  |
| `met`          | MET logging     | MTK microsecond-level WiFi trace                            |
| `epo`          | EPO blob        | MTK assisted-GPS EPO (Extended Prediction Orbit) blob       |
| `wifi_hotspot` | MTK hotspot     | MTK WiFi hotspot / softAP manager                           |
| `mediatek`     | Mediatek kernel | General Mediatek kernel WiFi events                         |
| `tx_power`     | TX power        | MTK TX power table lookup failures                          |

**Common MTK WiFi failure patterns:**

```
conninfra: [E] %s: wifi power on fail, reason=%d
conninfra: [E] %s: connsys reset fail, subsystem=wifi, ret=%d
wlan: [E] op=%d reason=%d // TX/RX error
wlan: [E] scan: cannot find target AP, reason=NO_MATCH
met: [E] wifi_tx_error: queue=%d stop_reason=%d
mediatek: [E] wifi: %s: failed, err=%d
epo: [E] epo_download: failed, network_unavailable
wifi_hotspot: [E] ap_issue: client_assoc_fail, reason=%d
```

**MTK WiFi SSR sequence (conninfra):**

```
conninfra: [I] conninfra: wifi subsystem reset start
conninfra: [E] conninfra: wifi subsys ASSERT, func=%s, line=%d
kernel: conninfra: subsys_reset: target=wifi
conninfra: [I] conninfra: wifi reload start
conninfra: [I] conninfra: wifi ready
```

**MTK WiFi triage checklist:**

- [ ] Check `conninfra` for power-on failure (boot or resume path)
- [ ] Distinguish `conninfra` wifi reset from framework disconnect
- [ ] Check `met` for sustained TX queue stalls or airtime exhaustion
- [ ] For A-GPS: also check `epo` blob download status before attributing to SUPL
- [ ] For MTK softAP: check `wifi_hotspot` client association failure codes

### 3.3 QCOM vs MTK at a Glance

| Signal             | QCOM                             | MTK                              |
| ------------------ | -------------------------------- | -------------------------------- |
| Chip reset         | `wcnss: FW crash / SSR`          | `conninfra: wifi subsys ASSERT`  |
| Thermal TX backoff | `thermal_engine: wlan`           | `conninfra thermal` + `tx_power` |
| Firmware NV blob   | `WLAN_NV: nvbin download failed` | `epo` (GPS blob, not WiFi NV)    |
| Low-level driver   | `wlan_hdd`                       | `wlan` + `mediatek`              |
| Connectivity infra | N/A (separate)                   | `conninfra` (WiFi + BT/FM)       |
| Diagnostic trace   | `qcwcn` / `WCNSS_qcom_wlan`      | `met`                            |

---

## 4. WiFi Data Visualization

使用Plotly库将WiFi日志数据可视化为交互式时间序列图表，便于分析WiFi性能趋势。

### 4.1 Visualization Overview

可视化工具支持以下WiFi性能指标：

| 指标 | 描述 | 单位 |
|------|------|------|
| RSSI | 信号强度 | dBm |
| TX Rate | 发送速率 | Mbps |
| RX Rate | 接收速率 | Mbps |
| Throughput | 吞吐量 | Kbps |
| PER | 丢包率 | % |
| Link Quality | 链路质量 | 数值 |

### 4.2 Python Visualization Code

```python
#!/usr/bin/env python3
"""
WiFi Performance Visualization Tool
使用Plotly绘制WiFi日志数据的交互式时间序列折线图
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import random
import os
import sys


def create_wifi_visualization(df, output_file='wifi_performance.html'):
    """
    使用Plotly创建WiFi性能数据的交互式可视化
    
    参数:
        df: pandas DataFrame，包含WiFi日志数据
        output_file: 输出HTML文件路径
    """
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            'RSSI Signal Strength (dBm)',
            'TX/RX Link Quality (Mbps)',
            'Throughput (Kbps)'
        ),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    # RSSI折线图
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['rssi'],
            mode='lines+markers',
            name='RSSI',
            line=dict(color='green', width=2),
            marker=dict(
                size=8,
                color=df['rssi'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title='RSSI (dBm)', len=0.25, y=0.85)
            ),
            customdata=df[['log_time', 'link_quality']].values,
            hovertemplate=(
                '<b>Time:</b> %{customdata[0]}<br>'
                '<b>RSSI:</b> %{y} dBm<br>'
                '<b>Link Quality:</b> %{customdata[1]}<br>'
                '<extra></extra>'
            )
        ),
        row=1, col=1
    )
    
    # TX Rate折线图
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['tx_rate'],
            mode='lines+markers',
            name='TX Rate',
            line=dict(color='blue', width=2),
            marker=dict(size=8, symbol='circle'),
            customdata=df[['log_time', 'rx_rate', 'total_tx', 'retry_tx', 'fail_tx']].values,
            hovertemplate=(
                '<b>Time:</b> %{customdata[0]}<br>'
                '<b>TX Rate:</b> %{y} Mbps<br>'
                '<b>RX Rate:</b> %{customdata[1]} Mbps<br>'
                '<b>Total TX:</b> %{customdata[2]}<br>'
                '<b>Retry TX:</b> %{customdata[3]}<br>'
                '<b>Fail TX:</b> %{customdata[4]}<br>'
                '<extra></extra>'
            )
        ),
        row=2, col=1
    )
    
    # RX Rate折线图
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['rx_rate'],
            mode='lines+markers',
            name='RX Rate',
            line=dict(color='green', width=2),
            marker=dict(size=8, symbol='square'),
            customdata=df[['log_time', 'tx_rate', 'total_rx', 'dup_rx', 'error_rx']].values,
            hovertemplate=(
                '<b>Time:</b> %{customdata[0]}<br>'
                '<b>RX Rate:</b> %{y} Mbps<br>'
                '<b>TX Rate:</b> %{customdata[1]} Mbps<br>'
                '<b>Total RX:</b> %{customdata[2]}<br>'
                '<b>Dup RX:</b> %{customdata[3]}<br>'
                '<b>Error RX:</b> %{customdata[4]}<br>'
                '<extra></extra>'
            )
        ),
        row=2, col=1
    )
    
    # Throughput折线图
    fig.add_trace(
        go.Scatter(
            x=df['timestamp'],
            y=df['throughput'],
            mode='lines+markers',
            name='Throughput',
            line=dict(color='purple', width=2),
            marker=dict(
                size=8,
                color=df['throughput'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title='Tput (Kbps)', len=0.25, y=0.15)
            ),
            customdata=df[['log_time', 'throughput', 'pending', 'per', 'idle_slot', 'awake_dur']].values,
            hovertemplate=(
                '<b>Time:</b> %{customdata[0]}<br>'
                '<b>Throughput:</b> %{y} Kbps (%{customdata[1]:.2f} Mbps)<br>'
                '<b>Pending:</b> %{customdata[2]}<br>'
                '<b>PER:</b> %{customdata[3]}%<br>'
                '<b>Idle Slot:</b> %{customdata[4]}<br>'
                '<b>Awake Duration:</b> %{customdata[5]}<br>'
                '<extra></extra>'
            )
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        title=dict(
            text='<b>WiFi Performance Dashboard</b><br>'
                 '<sup>RSSI Signal Strength | TX/RX Link Quality | Throughput</sup>',
            x=0.5,
            font=dict(size=20)
        ),
        height=1000,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        template='plotly_white',
        hovermode='closest'
    )
    
    fig.update_xaxes(title_text="Time", row=3, col=1)
    fig.update_yaxes(title_text="RSSI (dBm)", range=[-90, -40], row=1, col=1)
    fig.update_yaxes(title_text="Rate (Mbps)", range=[0, 4500], row=2, col=1)
    fig.update_yaxes(title_text="Throughput (Kbps)", range=[0, 100000], row=3, col=1)
    
    fig.write_html(output_file, include_plotlyjs=True, full_html=True)
    print(f"Interactive HTML visualization saved to: {output_file}")
    return fig


def main(log_path=None):
    """
    主函数，支持从命令行接收log路径
    
    参数:
        log_path: 输入log文件或目录路径，输出将保存到该路径下
    """
    print("WiFi Performance Visualization Tool")
    print("=" * 50)
    
    # 确定输出路径
    if log_path:
        # 如果提供了log路径，将输出保存到该路径下
        if os.path.isdir(log_path):
            output_dir = log_path
        else:
            output_dir = os.path.dirname(log_path)
        
        # 确保输出目录存在
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        
        output_file = os.path.join(output_dir, 'wifi_performance_visualization.html')
        print(f"Input log path: {log_path}")
        print(f"Output will be saved to: {output_file}")
    else:
        # 默认输出到当前目录
        output_file = 'wifi_performance_visualization.html'
        print(f"No input path specified, output will be saved to: {output_file}")
    
    # 这里应该从实际log文件中解析数据
    # df = parse_wifi_logs(log_path)
    
    # 示例：创建模拟数据
    df = create_sample_data()
    print(f"\nCreated sample data with {len(df)} entries")
    
    fig = create_wifi_visualization(df, output_file)
    
    print(f"\nVisualization complete!")
    print(f"Open {output_file} in a web browser to view the interactive chart")
    
    return df, fig


if __name__ == "__main__":
    # 支持命令行参数传入log路径
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
        df, fig = main(log_path)
    else:
        df, fig = main()
```

### 4.3 Usage

**命令行使用：**

```bash
# 指定log路径，输出将保存到该路径下
python wifi_visualization.py "d:\\path\\to\\wifi\\logs"

# 不指定路径，输出保存到当前目录
python wifi_visualization.py
```

**Python代码中使用：**

```python
from wifi_visualization import create_wifi_visualization
import pandas as pd

# 准备数据
df = pd.DataFrame({
    'timestamp': [...],
    'rssi': [...],
    'tx_rate': [...],
    'rx_rate': [...],
    'throughput': [...],
    # ... 其他字段
})

# 生成可视化
create_wifi_visualization(df, 'output.html')
```

### 4.4 Chart Features

| 功能 | 描述 |
|------|------|
| **悬停提示** | 鼠标悬停显示时间、数值和详细日志信息 |
| **缩放** | 支持框选缩放、滚轮缩放 |
| **平移** | 拖动平移时间轴 |
| **图例** | 点击图例显示/隐藏对应数据系列 |
| **导出** | 支持保存为PNG图片 |

### 4.5 Data Fields

可视化所需的数据字段：

| 字段名 | 类型 | 描述 |
|--------|------|------|
| `timestamp` | datetime | 日志时间戳 |
| `rssi` | int | 信号强度(dBm) |
| `tx_rate` | int | 发送速率(Mbps) |
| `rx_rate` | int | 接收速率(Mbps) |
| `throughput` | int | 吞吐量(Kbps) |
| `total_tx` | int | 总发送包数 |
| `retry_tx` | int | 重试发送包数 |
| `fail_tx` | int | 发送失败包数 |
| `total_rx` | int | 总接收包数 |
| `dup_rx` | int | 重复接收包数 |
| `error_rx` | int | 接收错误包数 |
| `per` | float | 丢包率(%) |
| `idle_slot` | int | 空闲时隙 |
| `awake_dur` | int | 唤醒时长 |
| `pending` | int | 待处理包数 |
| `link_quality` | int | 链路质量 |
| `log_time` | str | 日志时间字符串 |

