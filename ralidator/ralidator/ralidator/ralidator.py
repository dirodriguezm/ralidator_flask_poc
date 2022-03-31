class Ralidator:
    def __init__(self, filters_map, token):
        self.filters_map = filters_map
        self.token = token

    def apply_filters(self, response):
        print("response", response)
        for filt in self.filter_keys:
            response = self.filters_map[filt](response)
        return response

    def set_filters(self, filters):
        self.filter_keys = filters

    def set_permissions(self, permissions):
        self.permissions = permissions

    def check_allowed(self):
        return self.token in self.permissions
