import click

from network_analyzer.ai_network_analyzer import AiAnalyzer
from network_analyzer.threshold_network_analyzer import ThresholdAnalyzer

@click.command()
@click.option('-t','--analyzer-type', type=click.Choice(['ai', 'threshold'], case_sensitive=False), default='ai', help='Select analyzer type. AI or threshold')
@click.option('--data-source-type', type=click.Choice(['prometheus'], case_sensitive=False), default='prometheus', help='Select data source. Currently only Prometheus available.')
@click.option('--data-source-address', default='http://localhost:9090', help='Address of the monitoring system that acts as data source. For Prometheus, its base url.')
@click.option('-p', '--polling-period', default=60, help='')
@click.option('--gui', default=None, help="JSON file indicating the topology to represent in the GUI. If none, the analyzer will run in CLI mode.")
@click.option('--gui-window-height', default=800, help="Height of the GUI window in pixels.")
@click.option('--gui-window-width', default=600, help="Width of the GUI window in pixels.")
@click.option('--traffic-type', type=click.Choice(['bandwidth', 'bytes'], case_sensitive=False), default='bytes', help='Indicates the type of traffic obtained from the data source. Bytes will be transformed into bandwidth for analysis.')
@click.option('--initial-delta', default=1200)
@click.option('--max-traces', default=100, help="Maximum number of traces used. It helps with performance and prevents overflowing Gemini's token count.")
@click.option('--traffic-in-metric', default='bytesIn')
@click.option('--traffic-out-metric', default='bytesOut')
@click.option('--device-name-label', default='instance')
@click.option('--interface-name-label', default='interfaceName')
def run_analyzer(analyzer_type, data_source_type, data_source_address, polling_period, gui,
                 gui_window_height, gui_window_width, traffic_type, initial_delta, max_traces,
                 traffic_in_metric, traffic_out_metric, device_name_label, interface_name_label):
    if analyzer_type == 'ai':
        Analyzer = AiAnalyzer
    else:
        Analyzer = ThresholdAnalyzer
    analyzer =Analyzer(
        data_source_type=data_source_type,
        data_source_address=data_source_address,
        polling_period=polling_period,
        gui=gui,
        traffic_type=traffic_type,
        initial_delta=initial_delta,
        max_traces=max_traces,
        traffic_in_metric=traffic_in_metric,
        traffic_out_metric=traffic_out_metric,
        device_name_label=device_name_label,
        interface_name_label=interface_name_label,
        gui_window_height=gui_window_height,
        gui_window_width=gui_window_width
    )
    analyzer.start()

if __name__ == '__main__':
    run_analyzer()
