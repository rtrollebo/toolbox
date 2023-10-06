class APITesterIOException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class APITesterOpenAPIException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)