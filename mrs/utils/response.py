class ResponseHttp:

    def __init__(self, data=None, error=None):

        if error is None:
            error = ''

        if data is None:
            data = ''

        self.result = {
            'result': data,
            'error': error
        }
