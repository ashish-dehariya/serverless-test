import requests
from requests.exceptions import HTTPError
import time


class test(object):
    def __init__(self, api_token, data_center, retries=0):
        if not api_token:
            raise ValueError("error: api_token must be set before making API calls")
        if not data_center:
            raise ValueError("error: data_center must be set b
                             efore making API calls")
        self.api_token = api_token
        self.data_center = data_center
        self._max_request_attempts = retries + 1

    def get_base_url(self):
        return 

    def get_headers(self):
        return {"X-API-TOKEN": self.api_token,
                   "Content-Type": "application/json"}

    def get(self, url, **kwargs):
        return self._execute_request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self._execute_request('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self._execute_request('put', url, **kwargs)

    def delete(self, url, **kwargs):
        return self._execute_request('delete', url, **kwargs)

    def _execute_request(self, request_type, url, **kwargs):
        if request_type not in ['get', 'post', 'put', 'delete']:
            raise TypeError('_execute_request request_type must be get, post, put, or delete')
        for i in xrange(self._max_request_attempts):
            try:
                response = None
                if request_type == 'get':
                    response = requests.get(url, **kwargs)
                elif request_type == 'post':
                    response = requests.post(url, **kwargs)
                elif request_type == 'put':
                    response = requests.put(url, **kwargs)
                else:
                    response = requests.delete(url, **kwargs)
                ._check_for_status(response)
                return response
            except HTTPError as e:
                if i == self._max_request_attempts - 1:
                    raise
                time.sleep(2)

    @staticmethod
    def _check_for_status(response):
        if not response.status_code == 200:
            msg = 'Status Code {} '\
                    'for {} request on {} '\
                    'with Body: ({}) and Headers: ({})'.format(response.status_code,
                                                               response.request.method,
                                                               response.request.url,
                                                               response.request.body,
                                                               response.request.headers)
            raise HTTPError(msg)
