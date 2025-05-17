import requests
from datetime import datetime, timedelta, timezone
from network_analyzer.data_source.generic_data_source import GenericDataSource

class PrometheusDataSource(GenericDataSource):
    def __init__(self, data_source_address, traffic_in_metric, traffic_out_metric, device_name_label,
                  interface_name_label, *args, **kwargs):
        super().__init__(data_source_address, *args, **kwargs)
        self.traffic_in_metric = traffic_in_metric
        self.traffic_out_metric = traffic_out_metric
        self.device_name_label = device_name_label
        self.interface_name_label = interface_name_label

    def retrieve_previous_info(self, delta, polling_period):
        previous_info = {}
        end = datetime.now(timezone.utc).replace(tzinfo=None)
        start = end - timedelta(seconds=delta)
        traffic_in_data = requests.get(
            url=f'{self.data_source_address}/api/v1/query_range',
            params={
                'query': self.traffic_in_metric,
                'start': start.isoformat() + 'Z',
                'end': end.isoformat() + 'Z',
                'step': polling_period
            }
        ).json()
        traffic_out_data = requests.get(
            url=f'{self.data_source_address}/api/v1/query_range',
            params={
                'query': self.traffic_out_metric,
                'start': start.isoformat() + 'Z',
                'end': end.isoformat() + 'Z',
                'step': polling_period
            }
        ).json()
        for data_list,label in [
                (traffic_in_data['data']['result'], 'traffic_in'),
                (traffic_out_data['data']['result'], 'traffic_out')
            ]:
            for data in data_list:
                device = data['metric'][self.device_name_label] 
                interface = data['metric'][self.interface_name_label]
                for value in data['values']:
                    if not value[0] in previous_info:
                        previous_info[value[0]] = {}
                    if not device in previous_info[value[0]]:
                        previous_info[value[0]][device] = {}
                    if not interface in previous_info[value[0]][device]:
                        previous_info[value[0]][device][interface] = {}
                    previous_info[value[0]][device][interface][label] = int(value[1])
                
        return previous_info