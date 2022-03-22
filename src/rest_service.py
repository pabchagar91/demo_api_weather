import requests


class RestService:
    def __init__(self, **kwargs):
        self.url = kwargs.get("url", "")
        self.method = kwargs.get("method", "").upper()
        self.response = None
        self.status = None
        self.params = kwargs.get("params", {})

    def do_request(self):
        self.response = requests.request(method=self.method, url=self.url, params=self.params)
        self.status = self.response.status_code

    def clear_params(self):
        api_key = self.params.get('apikey')
        self.params.clear()
        if api_key:
            self.params['apikey'] = api_key

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url: str):
        self._url = new_url
