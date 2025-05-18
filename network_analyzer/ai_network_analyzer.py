import json
from google import genai
from google.genai import types
from settings import GEMINI_API_KEY
from network_analyzer.base_network_analyzer import BaseAnalyzer

class AiAnalyzer(BaseAnalyzer):
    def __init__(self, data_source_type, data_source_address, polling_period, gui, traffic_type, initial_delta, max_traces,
                 traffic_in_metric, traffic_out_metric, device_name_label, interface_name_label, gui_window_height,
                 gui_window_width, *args, **kwargs):
        self.context = []
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=genai.types.Schema(
                type = genai.types.Type.OBJECT,
                required = ["abnormal_traffic_pattern"],
                properties = {
                    "abnormal_traffic_pattern": genai.types.Schema(
                        type = genai.types.Type.BOOLEAN,
                    ),
                    "affected_interfaces_per_device": genai.types.Schema(
                        type = genai.types.Type.ARRAY,
                        items = genai.types.Schema(
                            type = genai.types.Type.OBJECT,
                            properties = {
                                "device_name": genai.types.Schema(
                                    type = genai.types.Type.STRING,
                                ),
                                "affected_interfaces": genai.types.Schema(
                                    type = genai.types.Type.ARRAY,
                                    items = genai.types.Schema(
                                        type = genai.types.Type.OBJECT,
                                        properties = {
                                            "interface_name": genai.types.Schema(
                                                type = genai.types.Type.STRING,
                                            ),
                                            "message": genai.types.Schema(
                                                type = genai.types.Type.STRING,
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    ),
                }
            ),
            system_instruction=[
                types.Part.from_text(
                    text='\n'.join([
                        'You are going to receive network traffic data with a timestamp.',
                        'Analyze if the traffic seems normal compared to previous timestamps.',
                        'Return wether the traffic seems anomalous or not.',
                        'If the traffic seems anomalous, return a list of affected interfaces per device with a message that explains what may be the cause of the anomaly.',
                        'If both the input and output bandwidth of the same interface are 0, the link it belongs to is likely down.',
                        'If several links connected to a device are down, but the device kkeps generating data traces, said device is likely misconfigured.',
                        'If an interface suffers a significant decrease of traffic while another one suffers an analogous increase, the network may be suffering a Man in the Middle attack.'
                    ])
                )
            ]
        )
        super().__init__(data_source_type, data_source_address, polling_period, gui, traffic_type, initial_delta,
                         max_traces, traffic_in_metric, traffic_out_metric, device_name_label, interface_name_label,
                         gui_window_height, gui_window_width, *args, **kwargs)

    def adapt_trace(self, trace):
        adapted_trace = {
            "timestamp": self.current_timestamp.ctime(),
            "interfaces_per_device": []
        }
        for device in trace:
            device_interfaces = {
                "device_name": device,
                "interfaces": []
            }
            for interface in trace[device]:
                device_interfaces['interfaces'].append(
                    {
                        "interface_name": interface,
                        "average_input_bandwidth": f'{trace[device][interface]['average_input_bandwidth']} bps',
                        "average_output_bandwidth": f'{trace[device][interface]['average_output_bandwidth']} bps',
                    }
                )
            adapted_trace['interfaces_per_device'].append(device_interfaces)
        return adapted_trace

    def internal_trace_processing(self, trace, analysis=True):
        self.context.append(
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=json.dumps(self.adapt_trace(trace)))
                ]
            )
        )
        if len(self.context) > 2*self.max_traces:
            self.context = self.context[2:]
        if analysis:
            response = ""
            for chunk in self.client.models.generate_content_stream(
                model="gemini-2.5-flash-preview-04-17",
                contents=self.context,
                config=self.config
            ):
                response += chunk.text or ''
            self.context.append(
                types.Content(
                    role="model",
                    parts=[
                        types.Part.from_text(text=response)
                    ]
                )
            )
            output = json.loads(response)
            if output['abnormal_traffic_pattern']:
                for device in trace:
                    for interface in trace[device]:
                        pending = True
                        for affected_device in output['affected_interfaces_per_device']:
                            if device == affected_device['device_name']:
                                for affected_interface in affected_device['affected_interfaces']:
                                    if interface == affected_interface['interface_name']:
                                        pending = False
                                        self.set_abnormal(
                                            device,
                                            interface,
                                            affected_interface['message'],
                                            last_bandwidth_in=trace[device][interface]['average_input_bandwidth'],
                                            last_bandwidth_out=trace[device][interface]['average_output_bandwidth']
                                        )
                        if pending:
                            self.set_normal(
                                device,
                                interface,
                                last_bandwidth_in=trace[device][interface]['average_input_bandwidth'],
                                last_bandwidth_out=trace[device][interface]['average_output_bandwidth']
                            )
            else:
                for device in trace:
                    for interface in trace[device]:
                        self.set_normal(
                            device,
                            interface,
                            last_bandwidth_in=trace[device][interface]['average_input_bandwidth'],
                            last_bandwidth_out=trace[device][interface]['average_output_bandwidth']
                        )
        else:
            for device in trace:
                for interface in trace[device]:
                    self.set_normal(
                        device,
                        interface,
                        last_bandwidth_in=trace[device][interface]['average_input_bandwidth'],
                        last_bandwidth_out=trace[device][interface]['average_output_bandwidth']
                    )