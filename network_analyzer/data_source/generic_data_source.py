class GenericDataSource:
    def __init__(self, data_source_address, *args, **kwargs):
        self.data_source_address = data_source_address

    def retrieve_previous_info(self, delta, polling_period) -> dict:
        return {}

    def retireve_info(self) -> dict:
        return {}
