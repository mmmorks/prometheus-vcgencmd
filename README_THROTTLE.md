# prometheus-vcgencmd (Throttle Bits Fork)

This is a fork of [prometheus-vcgencmd](https://gitlab.com/krink/prometheus-vcgencmd) that adds individual throttle bit metrics for easier consumption in Grafana.

## What's Different

### Original Version
```
vcgencmd_get_throttled{bit="0x50005"} 1
```
The throttle state is stored as a hex string in a label, making it difficult to parse in PromQL.

### This Fork
In addition to keeping the original metric for backwards compatibility, this fork adds 8 new metrics that parse the individual throttle bits:

**Current Status:**
```
vcgencmd_throttle_undervoltage_now 1
vcgencmd_throttle_freq_capped_now 0
vcgencmd_throttle_throttled_now 1
vcgencmd_throttle_soft_temp_limit_now 0
```

**Historical (Since Boot):**
```
vcgencmd_throttle_undervoltage_occurred 1
vcgencmd_throttle_freq_capped_occurred 0
vcgencmd_throttle_throttled_occurred 1
vcgencmd_throttle_soft_temp_limit_occurred 0
```

Each metric is either `0` or `1`, making it trivial to graph and alert on in Grafana.

## Installation

### From GitHub
```bash
sudo pip3 install git+https://github.com/mmmorks/prometheus-vcgencmd.git --break-system-packages
```

### From Local Clone
```bash
git clone https://github.com/mmmorks/prometheus-vcgencmd.git
cd prometheus-vcgencmd
sudo pip3 install . --break-system-packages
```

## Usage

```bash
prometheus-vcgencmd
```

Or with systemd timer (recommended):

```bash
# Create service
sudo tee /etc/systemd/system/rpi-vcgencmd-exporter.service > /dev/null << 'EOF'
[Unit]
Description=Raspberry Pi vcgencmd Metrics Exporter
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/bash -c '/usr/local/bin/prometheus-vcgencmd > /var/lib/node_exporter/textfile_collector/vcgencmd.prom'
User=root
StandardOutput=null
EOF

# Create timer
sudo tee /etc/systemd/system/rpi-vcgencmd-exporter.timer > /dev/null << 'EOF'
[Unit]
Description=Run Raspberry Pi vcgencmd exporter every minute

[Timer]
OnBootSec=30s
OnUnitActiveSec=1min
AccuracySec=5s

[Install]
WantedBy=timers.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable --now rpi-vcgencmd-exporter.timer
```

## Throttle Bit Reference

| Bit | Hex Value | Metric | Meaning |
|-----|-----------|--------|---------|
| 0 | 0x1 | `vcgencmd_throttle_undervoltage_now` | Under-voltage detected now |
| 1 | 0x2 | `vcgencmd_throttle_freq_capped_now` | ARM frequency capped now |
| 2 | 0x4 | `vcgencmd_throttle_throttled_now` | Currently throttled |
| 3 | 0x8 | `vcgencmd_throttle_soft_temp_limit_now` | Soft temperature limit active now |
| 16 | 0x10000 | `vcgencmd_throttle_undervoltage_occurred` | Under-voltage has occurred since boot |
| 17 | 0x20000 | `vcgencmd_throttle_freq_capped_occurred` | Frequency capping has occurred since boot |
| 18 | 0x40000 | `vcgencmd_throttle_throttled_occurred` | Throttling has occurred since boot |
| 19 | 0x80000 | `vcgencmd_throttle_soft_temp_limit_occurred` | Soft temperature limit has occurred since boot |

## Example Grafana Queries

```promql
# Check if currently under-voltage
vcgencmd_throttle_undervoltage_now

# Check if any throttling has occurred since boot
vcgencmd_throttle_throttled_occurred

# Alert if currently throttled
vcgencmd_throttle_throttled_now > 0
```

## Version

1.1.0-throttle-bits

## Grafana Dashboard

### Using the Pre-generated Dashboard

Import the pre-generated dashboard JSON:
```bash
# The dashboard JSON is ready to import into Grafana
cat raspberry-pi-vcgencmd-dashboard.json
```

### Generating the Dashboard

The dashboard is generated using a Python script with the Grafana Foundation SDK:

```bash
# Generate the dashboard JSON
./generate-dashboard.py > raspberry-pi-vcgencmd-dashboard.json
```

The generator script (`generate-dashboard.py`) uses `uv` for dependency management and runs without requiring a virtual environment. It automatically installs the `grafana_foundation_sdk` package when executed.

### Dashboard Features

The generated dashboard includes 31 comprehensive panels organized into 10 rows:

**Temperature & Voltage (8 panels):**
- CPU temperature gauge (0-85°C with green/yellow/orange/red thresholds) + timeseries
- Core voltage gauge (1.0-1.4V) + timeseries
- SDRAM voltages (C/I/P) combined timeseries
- Ring oscillator temperature/voltage/speed gauges + timeseries (alternate sensor validation)

**Clock Frequencies (6 panels):**
- ARM CPU clock gauge (0-1500 MHz with thresholds) + main clocks timeseries
- Core GPU clock gauge (0-500 MHz)
- V3D (3D GPU) clock gauge
- Peripheral clocks timeseries (H264 encoder, EMMC, HDMI, VEC, ISP, UART)

**Memory (6 panels):**
- ARM and GPU memory allocation gauges + timeseries
- OOM (out-of-memory) events counter
- Memory allocation failures counter
- Memory compaction events counter
- OOM lifetime and timing statistics timeseries

**Throttle Status (10 panels):**
- Current status indicators (NOW): Undervoltage, Frequency capping, Throttling, Soft temp limit
- Historical indicators (Occurred since boot) for all 4 conditions
- Timeseries charts for both current and historical status

**What's NOT Included:**
Static/informational metrics are excluded (version info, camera detection, LCD info, HDMI timings) as they don't benefit from time-series visualization.

All panels use simple PromQL queries against the individual throttle bit metrics (0 or 1 values) for easy graphing and alerting.

## Credits

Based on [prometheus-vcgencmd](https://gitlab.com/krink/prometheus-vcgencmd) by Karl Rink.

## License

MIT
