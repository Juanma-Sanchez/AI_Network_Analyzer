import json
import time
from datetime import datetime
from network_analyzer.data_source.prometheus_data_source import PrometheusDataSource

class BaseAnalyzer:
    def __init__(self, data_source_type, data_source_address, polling_period, gui, traffic_type,
                initial_delta, max_traces, traffic_in_metric, traffic_out_metric, device_name_label,
                interface_name_label, gui_window_height, gui_window_width, *args, **kwargs):
        if data_source_type == 'prometheus':
            self.data_source = PrometheusDataSource(
                data_source_address=data_source_address,
                traffic_in_metric=traffic_in_metric,
                traffic_out_metric=traffic_out_metric,
                device_name_label=device_name_label,
                interface_name_label=interface_name_label
            )
        self.polling_period = polling_period
        self.max_traces = max_traces
        self.network_graph = {}
        self.last_timestamp = None
        self.current_timestamp = None
        self.traffic_type = traffic_type
        if gui:
            # TODO intialize GUI
            pass
        else:
            self.gui = None
        self.initialize_graph(self.data_source.retrieve_previous_info(initial_delta, self.polling_period))

    def initialize_graph(self, data: dict):
        for timestamp,trace in data.items():
            self.process_trace(timestamp, trace, analysis=False)

    def process_trace(self, timestamp, trace, analysis=True):
        self.current_timestamp = datetime.fromtimestamp(int(timestamp))
        if self.last_timestamp:
            if self.current_timestamp > self.last_timestamp:
                if self.traffic_type == 'bytes':
                    trace = self.bytes_to_bandwidth(trace)
                self.internal_trace_processing(trace, analysis)
        else:
            for device in trace:
                for interface in trace[device]:
                    self.set_normal(device, interface)
                    if self.traffic_type == 'bytes':
                        self.network_graph[device][interface]['traffic_in'] = trace[device][interface]['traffic_in']
                        self.network_graph[device][interface]['traffic_out'] = trace[device][interface]['traffic_out']
        self.last_timestamp = self.current_timestamp

    def set_normal(self, device, interface, last_bandwidth_in=0, last_bandwidth_out=0):
        if not device in self.network_graph:
            self.network_graph[device] = {}
        if interface in self.network_graph[device]:
            if self.network_graph[device][interface].get('status') != 'Normal':
                self.network_graph[device][interface]['last_change'] = self.current_timestamp.ctime()
                self.network_graph[device][interface]['message'] = ""
            self.network_graph[device][interface]['status'] = 'Normal'
            self.network_graph[device][interface]['last_bandwidth_in'] = last_bandwidth_in
            self.network_graph[device][interface]['last_bandwidth_out'] = last_bandwidth_out
        else:
            self.network_graph[device][interface] = {
                "status": "Normal",
                "last_change": self.current_timestamp.ctime(),
                "message": "",
                "last_bandwidth_in": last_bandwidth_in,
                "last_bandwidth_out": last_bandwidth_out
            }

    def set_abnormal(self, device, interface, message, last_bandwidth_in=0, last_bandwidth_out=0):
        if not device in self.network_graph:
            self.network_graph[device] = {}
        if interface in self.network_graph[device]:
            if self.network_graph[device][interface].get('status') != 'Abnormal':
                self.network_graph[device][interface]['last_change'] = self.current_timestamp.ctime()
            self.network_graph[device][interface]['message'] = message
            self.network_graph[device][interface]['status'] = 'Abormal'
            self.network_graph[device][interface]['last_bandwidth_in'] = last_bandwidth_in
            self.network_graph[device][interface]['last_bandwidth_out'] = last_bandwidth_out
        else:
            self.network_graph[device][interface] = {
                "status": "Abormal",
                "last_change": self.current_timestamp.ctime(),
                "message": message,
                "last_bandwidth_in": last_bandwidth_in,
                "last_bandwidth_out": last_bandwidth_out
            }
        print('WARNING ABNORMAL TRAFFIC PATTERN IN INTERFACE {} OF DEVICE {}'.format(interface, device))
        print(json.dumps(self.network_graph[device][interface], indent=2))

    def bytes_to_bandwidth(self, trace):
        new_trace = {}
        for device in trace:
            new_trace[device] = {}
            if not device in self.network_graph:
                self.network_graph[device] = {}
            for interface in trace[device]:
                new_trace[device][interface] = {}
                if interface in self.network_graph[device]:
                    delta_time = (self.current_timestamp - self.last_timestamp).total_seconds()
                    delta_bytes_in = trace[device][interface]['traffic_in'] - self.network_graph[device][interface]['traffic_in']
                    if delta_bytes_in < 0:
                        delta_bytes_in += 2**32
                    delta_bytes_out = trace[device][interface]['traffic_out'] - self.network_graph[device][interface]['traffic_out']
                    if delta_bytes_out < 0:
                        delta_bytes_out += 2**32
                    new_trace[device][interface]['average_input_bandwidth'] = delta_bytes_in/delta_time
                    new_trace[device][interface]['average_output_bandwidth'] = delta_bytes_in/delta_time
                else:
                    self.set_normal(device, interface)
                    new_trace[device][interface]['average_input_bandwidth'] = 0
                    new_trace[device][interface]['average_output_bandwidth'] = 0
                self.network_graph[device][interface]['traffic_in'] = trace[device][interface]['traffic_in']
                self.network_graph[device][interface]['traffic_out'] = trace[device][interface]['traffic_out']
        return new_trace

    def internal_trace_processing(self, trace, analysis=True):
        pass

    def start(self):
        if self.gui:
            # TODO start GUI
            pass
        try:
            while(True):
                info = self.data_source.retrieve_info()
                for timestamp,trace in info.items():
                    self.process_trace(timestamp, trace)
                time.sleep(self.polling_period)
        except Exception as e:
            if self.gui:
                # TODO stop GUI
                pass
            raise e