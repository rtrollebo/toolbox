import re
import sys
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
        auth_request = self.testdata['authenticationRequest']
        if auth_request is not None:
            self.auth_data = read_file_yaml("authentication.yml")
            self.access_token = self.auth_data['access_token']
        for req_name in self.req_names:
            res = self.send_request(req_name)
            if res.status_code != 200 and auth_request is not None:
                auth_res = self.send_request(auth_request)
                if auth_res.status_code == 200:
                    write_file_yaml("authentication.yml", auth_res.json())
                    self.testdata = read_file_yaml(self.testdata_filename)
                    self.access_token = auth_res.json()['access_token']
                res = self.send_request(req_name)
            sys.stdout.write(str(res.status_code))
            assert res.status_code == 200
            sys.stdout.write(' '+req_name+' \tOK\n')

    def send_request(self, req_name):
        auth_request = self.testdata['authenticationRequest']
        req = self.testdata['requests'][req_name]
        headers = req['headers']
        if 'Authorization' not in headers and auth_request is not None:
            headers['Authorization'] = self.auth_data['token_type'] + ' ' + self.access_token
        response = r.request(
            req['method'],
            req['host'] + req['path'],
            headers=headers,
            params=req['params'],
            data=req['data'])
        return response


class ApiSpecification:
    def __init__(self, operations):
        self.operations = operations


def read_open_api(filename) -> ApiSpecification:
    """
    Parser of
    https://spec.openapis.org/oas/v3.1.0#pathsObject

    :param filename:
    :return:
    """
    f = read_file_yaml(filename)
    operations = []
    for path in f['paths']:
        for method in f['paths'][path]:
            api_operation = f['paths'][path][method]
            op = ApiSpecificationOperation(api_operation['operationId'], path, method, None, None,
                                           api_operation['description'], None)
            operations.append(op)
    return ApiSpecification(operations)


class ApiSpecificationOperation:

    """
    ApiSpecificationOperation
    """
    def __init__(self, operation_id, path, method, parameters, request_body, description, server):
        self.operation_id = operation_id
        self.path = path
        self.method = method
        self.parameters = parameters
        self.request_body = request_body
        self.description = description
        self.server = server

    def get_path(self, path_data={}):
        """
        Generate full path with path param specification and data.
        >>> SpecOp.get_path({'foo': 'bar'})
        '/api/v1/resource/bar'
        """
        if len(path_data) == 0:
            return self.path
        path_params = re.findall("\\{(.*?)\\}", self.path)
        for pp in path_params:
            self.path = self.path.replace("{"+pp+"}", str(path_data[pp]))
        return self.path

if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={'SpecOp': ApiSpecificationOperation(None, '/api/v1/resource/{foo}', None, None, None, None, None)})







