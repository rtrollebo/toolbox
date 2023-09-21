import requests as r

from common.io import read_file_yaml, write_file_yaml


class TestSequence:
    def __init__(self, testdata_filename):
        self.auth_data = None
        self.testdata_filename = testdata_filename
        self.testdata = read_file_yaml(testdata_filename)
        self.req_names = self.testdata['sequences']
        self.access_token = None

    def run(self):
        self.auth_data = read_file_yaml("authentication.yml")
        self.access_token = self.auth_data['access_token']
        for req_name in self.req_names:
            res = self.send_request(req_name)
            if res.status_code != 200:
                auth_res = self.send_request('authenticateOauth')
                if auth_res.status_code == 200:
                    write_file_yaml("authentication.yml", auth_res.json())
                    self.testdata = read_file_yaml(self.testdata_filename)
                    self.access_token = auth_res.json()['access_token']
                res = self.send_request(req_name)
                assert res.status_code == 200
            print(req_name + ' OK')

    def send_request(self, req_name):
        req = self.testdata['requests'][req_name]
        headers = req['headers']
        if 'Authorization' not in headers:
            headers['Authorization'] = self.auth_data['token_type'] + ' ' + self.access_token
        response = r.request(
            req['method'],
            req['host'] + req['path'],
            headers=headers,
            params=req['params'],
            data=req['data'])
        return response
