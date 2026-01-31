#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.12"
# dependencies = ["grafana_foundation_sdk"]
# ///
"""
Grafana Dashboard Generator for prometheus-vcgencmd
Generates Raspberry Pi hardware monitoring dashboard using Grafana Foundation SDK
"""

from grafana_foundation_sdk.builders.dashboard import Dashboard, ThresholdsConfig, DatasourceVariable, QueryVariable
from grafana_foundation_sdk.builders.gauge import Panel as Gauge
from grafana_foundation_sdk.builders.timeseries import Panel as Timeseries
from grafana_foundation_sdk.builders.stat import Panel as Stat
from grafana_foundation_sdk.builders.prometheus import Dataquery as PrometheusQuery
from grafana_foundation_sdk.builders.common import VizLegendOptions
from grafana_foundation_sdk.models.dashboard import DataSourceRef, Threshold, ThresholdsMode, VariableRefresh
from grafana_foundation_sdk.models.common import (
    LineInterpolation,
    LegendDisplayMode,
    LegendPlacement,
)
from grafana_foundation_sdk.cog import encoder

# Common configurations
INSTANCE_FILTER = '{instance="$instance"}'
DATASOURCE = DataSourceRef(type_val="prometheus", uid="${datasource}")

# Panel dimension presets
class Size:
    """Common panel sizes (height, width)"""
    GAUGE = (6, 4)
    STAT = (4, 4)
    HALF = (8, 12)
    FULL = (8, 24)

def prom_query(expr: str, legend: str = "") -> PrometheusQuery:
    """Create a Prometheus query with standard settings"""
    q = PrometheusQuery().expr(expr).ref_id("A")
    if legend:
        q = q.legend_format(legend)
    return q

def gauge_panel(
    title: str,
    description: str,
    query: PrometheusQuery,
    unit: str,
    thresholds: list[tuple[str, float | None]] | None = None,
    size=Size.GAUGE,
    min_value: float | None = None,
    max_value: float | None = None
) -> Gauge:
    """Create a gauge panel with standard configuration

    Args:
        thresholds: List of (color, value) tuples. First should have value=None for base.
                   Example: [("green", None), ("yellow", 60), ("red", 80)]
        min_value: Minimum value for the gauge scale
        max_value: Maximum value for the gauge scale
    """
    h, w = size
    panel = (
        Gauge()
        .title(title)
        .description(description)
        .datasource(DATASOURCE)
        .unit(unit)
        .height(h).span(w)
        .show_threshold_markers(False)
        .show_threshold_labels(False)
        .with_target(query)
    )

    if min_value is not None:
        panel = panel.min(min_value)

    if max_value is not None:
        panel = panel.max(max_value)

    if thresholds:
        panel = panel.thresholds(
            ThresholdsConfig()
            .mode(ThresholdsMode.ABSOLUTE)
            .steps([
                Threshold(color=color, value=value) for color, value in thresholds
            ]))

    return panel

def stat_panel(
    title: str,
    description: str,
    query: PrometheusQuery,
    thresholds: list[tuple[str, float | None]] | None = None,
    size=Size.STAT,
    unit: str = "short"
) -> Stat:
    """Create a stat panel for binary status indicators

    Args:
        thresholds: List of (color, value) tuples for status indication
                   Example: [("green", None), ("red", 1)]
    """
    h, w = size
    panel = (
        Stat()
        .title(title)
        .description(description)
        .datasource(DATASOURCE)
        .unit(unit)
        .height(h).span(w)
        .with_target(query)
    )

    if thresholds:
        panel = panel.thresholds(
            ThresholdsConfig()
            .mode(ThresholdsMode.ABSOLUTE)
            .steps([
                Threshold(color=color, value=value) for color, value in thresholds
            ]))

    return panel

def timeseries_panel(
    title: str,
    description: str,
    query: PrometheusQuery,
    unit: str,
    size=Size.HALF,
    legend_calcs: list[str] = ["mean", "max"],
    min_value: float | None = None,
    max_value: float | None = None
) -> Timeseries:
    """Create a timeseries panel with standard styling

    Args:
        legend_calcs: Legend calculations to display, e.g. ["mean", "max"]
        min_value: Minimum Y-axis value
        max_value: Maximum Y-axis value
    """
    h, w = size
    panel = (
        Timeseries()
        .title(title)
        .description(description)
        .datasource(DATASOURCE)
        .unit(unit)
        .height(h).span(w)
        .line_width(2)
        .fill_opacity(20)
        .line_interpolation(LineInterpolation.SMOOTH)
        .with_target(query)
    )

    if min_value is not None:
        panel = panel.min(min_value)

    if max_value is not None:
        panel = panel.max(max_value)

    if legend_calcs:
        legend_opts = (
            VizLegendOptions()
            .calcs(legend_calcs)
            .display_mode(LegendDisplayMode.TABLE)
            .placement(LegendPlacement.BOTTOM)
            .show_legend(True)
        )
        panel = panel.legend(legend_opts)

    return panel

def create_dashboard() -> Dashboard:
    """Generate the complete Raspberry Pi vcgencmd dashboard"""

    dashboard = (
        Dashboard("Raspberry Pi Hardware Monitoring (vcgencmd)")
        .uid("rpi-vcgencmd")
        .tags(["raspberry-pi", "vcgencmd", "hardware", "monitoring"])
        .refresh("30s")
        .editable()
        .time("now-1h", "now")
        .timezone("browser")
        .with_variable(
            DatasourceVariable("datasource")
            .type("prometheus")
            .label("Data Source")
        )
        .with_variable(
            QueryVariable("instance")
            .label("Instance")
            .datasource(DATASOURCE)
            .query("label_values(vcgencmd_info, instance)")
            .refresh(VariableRefresh.ON_DASHBOARD_LOAD)
        )

        # Row 1: Temperature & Voltage
        .with_panel(timeseries_panel(
            "Temperature",
            "CPU and ring oscillator temperature readings",
            prom_query(
                f'label_replace('
                f'  label_replace('
                f'    {{__name__=~"vcgencmd_measure_temp|vcgencmd_read_ring_osc_temperature",instance="$instance"}}, '
                f'    "sensor", "CPU", "__name__", "vcgencmd_measure_temp"), '
                f'  "sensor", "Ring Osc", "__name__", "vcgencmd_read_ring_osc_temperature")',
                "{{sensor}}"
            ),
            unit="celsius",
            size=Size.HALF,
            min_value=0,
            max_value=85
        ))
        .with_panel(timeseries_panel(
            "Voltages",
            "Core, ring oscillator, and SDRAM voltages",
            prom_query(
                f'label_replace('
                f'  label_replace('
                f'    label_replace('
                f'      {{__name__=~"vcgencmd_measure_volts_.*|vcgencmd_read_ring_osc_volts",instance="$instance"}}, '
                f'      "voltage", "SDRAM $1", "__name__", "vcgencmd_measure_volts_sdram_([cip])"), '
                f'    "voltage", "Core", "__name__", "vcgencmd_measure_volts_core"), '
                f'  "voltage", "Ring Osc", "__name__", "vcgencmd_read_ring_osc_volts")',
                "{{voltage}}"
            ),
            unit="volt",
            size=Size.HALF,
            min_value=0,
            max_value=1.4
        ))

        # Row 2: Clock Frequencies
        .with_panel(timeseries_panel(
            "Clock Frequencies",
            "All clock frequencies (ARM, GPU, peripherals)",
            prom_query(
                f'label_replace({{__name__=~"vcgencmd_measure_clock_.*",instance="$instance"}}, "clock", "$1", "__name__", "vcgencmd_measure_clock_(.*)")',
                "{{clock}}"
            ),
            unit="hertz",
            size=Size.FULL,
            min_value=0
        ))

        # Row 3: Memory Allocation
        .with_panel(stat_panel(
            "ARM Memory",
            "Memory allocated to ARM CPU",
            prom_query(f'vcgencmd_get_mem_arm{{instance="$instance"}}'),
            thresholds=[("green", None)],
            size=(4, 6),
            unit="mbytes"
        ))
        .with_panel(stat_panel(
            "GPU Memory",
            "Memory allocated to GPU",
            prom_query(f'vcgencmd_get_mem_gpu{{instance="$instance"}}'),
            thresholds=[("green", None)],
            size=(4, 6),
            unit="mbytes"
        ))

        # Row 4: Memory Stats
        .with_panel(stat_panel(
            "OOM Events",
            "Out-of-memory events count",
            prom_query(f'vcgencmd_mem_oom_events{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1), ("red", 10)],
            size=(4, 4),
            unit="short"
        ))
        .with_panel(stat_panel(
            "Alloc Failures",
            "Memory allocation failures",
            prom_query(f'vcgencmd_mem_reloc_stats_alloc_failures{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1), ("red", 10)],
            size=(4, 4),
            unit="short"
        ))
        .with_panel(stat_panel(
            "Compactions",
            "Memory compaction events",
            prom_query(f'vcgencmd_mem_reloc_stats_compactions{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("blue", 1)],
            size=(4, 4),
            unit="short"
        ))
        .with_panel(timeseries_panel(
            "Memory OOM Metrics",
            "Out-of-memory lifetime and time statistics",
            prom_query(
                f'label_replace({{__name__=~"vcgencmd_mem_oom_.*",instance="$instance"}}, "metric", "$1", "__name__", "vcgencmd_mem_oom_(.*)")',
                "{{metric}}"
            ),
            unit="short",
            size=(6, 12),
            min_value=0
        ))


        # Row 5: Ring Oscillator
        .with_panel(timeseries_panel(
            "Ring Oscillator Speed",
            "Ring oscillator frequency over time",
            prom_query(f'vcgencmd_read_ring_osc_speed{{instance="$instance"}}', "Ring Osc"),
            unit="hertz",
            size=Size.FULL,
            min_value=0
        ))

        # Row 6: Historical Throttle Status
        .with_panel(stat_panel(
            "Undervoltage Occurred",
            "Undervoltage has occurred since boot",
            prom_query(f'vcgencmd_throttle_undervoltage_occurred{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1)],
            size=(4, 6),
            unit="short"
        ))
        .with_panel(stat_panel(
            "Freq Capped Occurred",
            "Frequency capping has occurred since boot",
            prom_query(f'vcgencmd_throttle_freq_capped_occurred{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1)],
            size=(4, 6),
            unit="short"
        ))
        .with_panel(stat_panel(
            "Throttled Occurred",
            "Throttling has occurred since boot",
            prom_query(f'vcgencmd_throttle_throttled_occurred{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1)],
            size=(4, 6),
            unit="short"
        ))
        .with_panel(stat_panel(
            "Soft Temp Limit Occurred",
            "Soft temperature limit has occurred since boot",
            prom_query(f'vcgencmd_throttle_soft_temp_limit_occurred{INSTANCE_FILTER}'),
            thresholds=[("green", None), ("yellow", 1)],
            size=(4, 6),
            unit="short"
        ))

        # Row 7: Throttle Status Over Time
        .with_panel(timeseries_panel(
            "Throttle Status",
            "Real-time throttle status indicators",
            prom_query(
                f'label_replace({{__name__=~"vcgencmd_throttle_.*_now",instance="$instance"}}, "status", "$1", "__name__", "vcgencmd_throttle_(.*)_now")',
                "{{status}}"
            ),
            unit="short",
            size=Size.FULL,
            min_value=0,
            max_value=1
        ))
    )

    return dashboard

if __name__ == "__main__":
    import json

    dashboard = create_dashboard().build()
    json_str = encoder.JSONEncoder(sort_keys=True, indent=2).encode(dashboard)

    # Parse and modify to disable gradient effects on gauges
    dashboard_dict = json.loads(json_str)
    for panel in dashboard_dict.get("panels", []):
        if panel.get("type") == "gauge":
            # Disable effects.gradient at panel level (this is the key setting)
            if "options" not in panel:
                panel["options"] = {}
            if "effects" not in panel["options"]:
                panel["options"]["effects"] = {}
            panel["options"]["effects"]["gradient"] = False

    print(json.dumps(dashboard_dict, sort_keys=True, indent=2))
