# prometheus-vcgencmd

prometheus raspberry pi vcgencmd

---
prometheus-vcgencmd exports the [vcgencmd](https://www.raspberrypi.org/documentation/raspbian/applications/vcgencmd.md) command in prometheus format. vcgencmd is a command line utility that can get various pieces of information from the VideoCore GPU on a [Raspberry pi](https://en.wikipedia.org/wiki/Raspberry_Pi) device.  Use prometheus-vcgencmd and prometheus node_exporter to pickup your raspberry pi vcgencmd readings.  You will have to install the **vcgencmd** command on your raspberry pi device (libraspberrypi-bin).

>Linux only
>>Raspberry Pi only

[![Python 3.0](https://img.shields.io/badge/python-3.0-blue.svg)](https://www.python.org/downloads/release/python-300/)  
[![Package Version](https://img.shields.io/pypi/v/prometheus-vcgencmd.svg)](https://pypi.python.org/pypi/prometheus-vcgencmd/)  

https://en.wikipedia.org/wiki/Linux  
https://en.wikipedia.org/wiki/Raspberry_Pi  

---

### requires a raspberry pi device
```
libraspberrypi-bin
```
requires: */usr/bin/vcgencmd*
```
apt-get install libraspberrypi-bin
```
---

### pip install  prometheus-vcgencmd
```
pip install prometheus-vcgencmd
```
provides command line command tool:
```
prometheus-vcgencmd
```
https://pypi.org/project/prometheus-vcgencmd

---
### clone and run via src
```
git clone https://gitlab.com/krink/prometheus-vcgencmd.git
python3 prometheus-vcgencmd/src/prometheus_vcgencmd/prometheus_vcgencmd.py
```
https://gitlab.com/krink/prometheus-vcgencmd

---

### command line prometheus-vcgencmd
the *vcgencmd* command requires root privileges
```
user@pi3:~$ sudo prometheus-vcgencmd
vcgencmd_info{version="0.0.0-1"} 1
vcgencmd_version{date="Jan  8 2021 14:33:35",copyright="Copyright (c) 2012 Broadcom",version="194a85abd768c7334bbadc3f1911c10a7d18ed14"} 1
vcgencmd_get_camera{supported="0"} 0
vcgencmd_get_throttled{bit="0x0"} 1
vcgencmd_measure_temp{scale="Celsius"} 47.8
vcgencmd_measure_volts_core{description="VC4 core voltage"} 1.3000
vcgencmd_measure_volts_sdram_c{description=""} 1.2000
vcgencmd_measure_volts_sdram_i{description=""} 1.2000
vcgencmd_measure_volts_sdram_p{description=""} 1.2250
vcgencmd_display_power{description="display power state id"} 0
vcgencmd_get_mem_arm{unit="Mbytes"} 948
vcgencmd_get_mem_gpu{unit="Mbytes"} 76
vcgencmd_mem_oom_events{} 0
vcgencmd_mem_oom_lifetime{unit="Mbytes"} 0
vcgencmd_mem_oom_total_time{unit="ms"} 0
vcgencmd_mem_oom_max_time{unit="ms"} 0
vcgencmd_mem_reloc_stats_alloc_failures{} 0
vcgencmd_mem_reloc_stats_compactions{} 0
vcgencmd_mem_reloc_stats_legacy_block_fails{} 0
vcgencmd_measure_clock_arm{unit="frequency(48)"} 900000000
vcgencmd_measure_clock_core{unit="frequency(1)"} 400000000
vcgencmd_measure_clock_h264{unit="frequency(28)"} 0
vcgencmd_measure_clock_isp{unit="frequency(45)"} 0
vcgencmd_measure_clock_v3d{unit="frequency(46)"} 275000000
vcgencmd_measure_clock_uart{unit="frequency(22)"} 48000000
vcgencmd_measure_clock_pwm{unit="frequency(25)"} 0
vcgencmd_measure_clock_emmc{unit="frequency(50)"} 200000000
vcgencmd_measure_clock_pixel{unit="frequency(29)"} 338000
vcgencmd_measure_clock_vec{unit="frequency(10)"} 108000000
vcgencmd_measure_clock_hdmi{unit="frequency(0)"} 0
vcgencmd_measure_clock_dpi{unit="frequency(4)"} 0
vcgencmd_get_lcd_info{info="720 480 24"} 0
vcgencmd_hdmi_timings{info="0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0"} 1
vcgencmd_read_ring_osc_speed{unit="MHz"} 3.453
vcgencmd_read_ring_osc_volts{unit="Volts"} 1.3000
vcgencmd_read_ring_osc_temperature{scale="Celsius"} 47.2
user@pi3:~$
```
---

### set as a crontab for prometheus node_exorter to pickup
```
*/5 * * * * /usr/local/bin/prometheus-vcgencmd >/var/lib/prometheus/node-exporter/vcgencmd.prom
```
you can download the prometheus node_exporter from [prometheus.io](https://prometheus.io/) or install via package "apt-get install prometheus-node-exporter"  Prometheus node_exporter can pickup properly formatted prometheus files ending with a ".prom" file extension.  Any file that resides in the '--collector.textfile.directory=' with a .prom file extension is parsed automatically.  [node_exporter](https://github.com/prometheus/node_exporter) Textfile Collector.

---

### run as a python module
```
python3 -m prometheus_vcgencmd
```
---
### run in python shell
```
$ python3
>>> import prometheus_vcgencmd
>>> prometheus_vcgencmd.Prometheus_Vcgencmd().stdout()
```
---

### works on
tested and works on *"cat /proc/cpuinfo"*
```
Model		: Raspberry Pi 4 Model B Rev 1.4
Model		: Raspberry Pi 3 Model B Rev 1.2

```

