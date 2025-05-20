import numpy as np
import scipy.stats
from network_analyzer.base_network_analyzer import BaseAnalyzer

class ThresholdAnalyzer(BaseAnalyzer):
    def set_normal(self, device, interface, last_bandwidth_in=0, last_bandwidth_out=0):
        super().set_normal(device, interface, last_bandwidth_in, last_bandwidth_out)
        if not 'bw_in_traces' in self.network_status[device][interface]:
            self.network_status[device][interface]['bw_in_traces'] = []
        self.network_status[device][interface]['bw_in_traces'].append(last_bandwidth_in)
        if len(self.network_status[device][interface]['bw_in_traces']) > self.max_traces:
            self.network_status[device][interface]['bw_in_traces'].pop(0)
        if not 'bw_out_traces' in self.network_status[device][interface]:
            self.network_status[device][interface]['bw_out_traces'] = []
        self.network_status[device][interface]['bw_out_traces'].append(last_bandwidth_out)
        if len(self.network_status[device][interface]['bw_out_traces']) > self.max_traces:
            self.network_status[device][interface]['bw_out_traces'].pop(0)

    def internal_trace_processing(self, trace, analysis=True):
        if analysis:
            for device in trace:
                for interface in trace[device]:
                    normal = True
                    message = ''
                    for trace_label,trace_list,bw in [
                        ('average_input_bandwidth', 'bw_in_traces','Input bandwidth'),
                        ('average_output_bandwidth', 'bw_out_traces','Output bandwidth'),
                    ]:
                        data = np.array(self.network_status[device][interface][trace_list])
                        ci = scipy.stats.norm.interval(
                            0.95,
                            loc=np.mean(data),
                            scale=np.std(data)
                        )
                        if trace[device][interface][trace_label] < ci[0]:
                            normal = False
                            message += f'{bw} of {trace[device][interface][trace_label]:.2f} bps is below the confidence interval. '
                        elif trace[device][interface][trace_label] > ci[1]:
                            normal = False
                            message += f'{bw} of {trace[device][interface][trace_label]:.2f} bps is above the confidence interval. '
                    if normal:
                        self.set_normal(
                            device,
                            interface,
                            trace[device][interface]['average_input_bandwidth'],
                            trace[device][interface]['average_output_bandwidth']
                        )
                    else:
                        self.set_abnormal(
                            device,
                            interface,
                            message,
                            trace[device][interface]['average_input_bandwidth'],
                            trace[device][interface]['average_output_bandwidth']
                        )
        else:
            for device in trace:
                for interface in trace[device]:
                    self.set_normal(
                        device,
                        interface,
                        trace[device][interface]['average_input_bandwidth'],
                        trace[device][interface]['average_output_bandwidth']
                    )