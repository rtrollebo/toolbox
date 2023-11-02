import re
import sys
import requests as r

from apitester.io import read_file_yaml, write_file_yaml
from apitester import exception

debug = False

class TestSequence:
    def __init__(self, testdata_filename):
        self.auth_data = None
        self.testdata_filename = testdata_filename
        self.testdata = read_file_yaml(testdata_filename)
        self.req_names = self.testdata['sequences']
        self.access_token = None

    def run(self):
        global debug
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
            if debug:
                print(res.json())
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
            req['host'] + get_path(req['path'], req['pathParams'], path_data=req['pathParams']),
            headers=headers,
            params=req['params'],
            data=req['data'],
            json=req['json'])
        return response


class ApiSpecification:
    """

    """
    def __init__(self, operations, components):
        self.responses = None
        self.operations = operations
        for op in self.operations:
            op._api_specification = self
        self.components = components

    def get_component(self, component: str):
        """

        >>> api_spec = read_open_api('../openapi_petstore.yaml')
        >>> c = api_spec.get_component('Pet')
        >>> 'id' in c['properties']
        True
        >>> 'name' in c['properties']
        True

        """
        return self.components['schemas'][component]



def read_open_api(filename) -> ApiSpecification:
    """
    Parser of
    https://spec.openapis.org/oas/v3.1.0#pathsObject

    :param filename:
    :return:

    >>> api_spec_file = '../openapi_petstore.yaml'
    >>> api_spec = read_open_api(api_spec_file)
    >>> len(api_spec.operations)
    3
    >>> ops = api_spec.operations
    >>> ops[0]._get_component_object()
    'Pets'

    """
    f = read_file_yaml(filename)
    operations = []
    for path in f['paths']:
        for method in f['paths'][path]:
            api_operation = f['paths'][path][method]
            op = ApiSpecificationOperation(api_operation['operationId'], path, method,
                                           api_operation['parameters'] if 'parameters' in api_operation.keys()
                                           else None,
                                           None,
                                           api_operation['description'] if 'description' in api_operation.keys()
                                           else None,
                                           None, api_operation['responses'])
            operations.append(op)
    return ApiSpecification(operations, f['components'])


class ApiSpecificationOperation:

    """
    ApiSpecificationOperation
    """
    def __init__(self, operation_id, path, method, parameters, request_body, description, server, responses):
        self.operation_id = operation_id
        self.path = path
        self.method = method
        self.parameters = parameters
        self.request_body = request_body
        self.description = description
        self.server = server
        self.responses = responses

    @property
    def header_parameters(self):
        return self._extract_parameters('header')

    @property
    def query_parameters(self):
        return self._extract_parameters('query')

    @property
    def payload(self):
        if self.method in ('PUT', 'POST'):
            return '{"placeholder": null}'
        else:
            return None

    @property
    def path_parameters(self):
        path_params_list = re.findall("\\{(.*?)\\}", self.path)
        path_params = {}
        for p in path_params_list:
            path_params[p] = ""
        return path_params

    def expect(self):
        if self.method == 'GET':
            # TODO: generate example response
            pass
        else:
            return {'200': {}}

    def get_path(self, path_data=None):
        """
        Generate full path with path param specification and data.
        >>> SpecOp.get_path(path_data={'foo1': 'bar1', 'foo2': 'bar2'})
        '/api/v1/resource/bar1/bar2'
        """
        return get_path(self.path, self.path_parameters, path_data=path_data)

    def _extract_parameters(self, param_type):
        if param_type not in ('header', 'query'):
            raise exception.APITesterOpenAPIException("Unknown parameter type")
        params = {}
        for p in self.parameters:
            if p['in'] == param_type:
                params[p['name']] = ""
        return params

    def _get_component_object(self, code=200):
        schema = self.responses[str(code)]['content']['application/json']['schema']
        if 'type' in schema.keys() and schema['type'] == 'array':
            return schema['items']['$ref'].split('/')[-1]
        else:
            return schema['$ref'].split('/')[-1]

def get_path(path, path_parameters, path_data=None):
    """

    """
    if path_data is None:
        path_data = {}
    if len(path_data) == 0:
        return path
    full_path = str(path)
    for pp in path_parameters.keys():
        full_path = full_path.replace("{"+pp+"}", str(path_data[pp]))
    return full_path

if __name__ == '__main__':
    import doctest
    doctest.testmod(
        extraglobs={
            'SpecOp': ApiSpecificationOperation(
                None,
                '/api/v1/resource/{foo1}/{foo2}',
                None,
                None,
                None,
                None,
                None,
                {'200': {'content': {'application/json': {'schema': {'#ref': ''}}}}}
            )
        })







