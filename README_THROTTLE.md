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

## Credits

Based on [prometheus-vcgencmd](https://gitlab.com/krink/prometheus-vcgencmd) by Karl Rink.

## License

MIT
