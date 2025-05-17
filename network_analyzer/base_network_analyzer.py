from datetime import datetime
import json
from network_analyzer.data_source.prometheus_data_source import PrometheusDataSource

class BaseAnalyzer:
    def __init__(self, data_source_type, data_source_address, polling_period, gui, traffic_type,
                initial_delta, traffic_in_metric, traffic_out_metric, device_name_label,
                interface_name_label,*args, **kwargs):
        if data_source_type == 'prometheus':
            self.data_source = PrometheusDataSource(
                data_source_address=data_source_address,
                traffic_in_metric=traffic_in_metric,
                traffic_out_metric=traffic_out_metric,
                device_name_label=device_name_label,
                interface_name_label=interface_name_label
            )
        self.polling_period = polling_period
        if gui:
            # TODO intialize GUI
            pass
            self.traffic_type = traffic_type
        self.network_graph = {}
        self.initialize_graph(self.data_source.retrieve_previous_info(initial_delta, self.polling_period))

    def initialize_graph(self, data):
        print(json.dumps(data, indent=2))