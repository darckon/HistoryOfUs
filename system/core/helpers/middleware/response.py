import json


class GenericResponseMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        validate = ''
        init = str(response)
        text = init.split(';')
        if(len(text) > 1):
            text = text[1].replace(' ', '')
            text = text.split('=')
            validate = text[0]
        if not validate == 'charset':
            try:
                response.content_type
                response.format = dict()
                if response.status_code == 200 or response.status_code == 201:
                    response.format["status"] = True
                    response.format["data"] = response.data
                    response.content = json.dumps(response.format)
                else:
                    errors = dict()
                    response.format = dict()
                    if 'detail' in response.data:
                        for key, value in enumerate(response.data):
                            errors[value] = response.data[value]
                    else:
                        for key, value in enumerate(response.data):
                            errors[value] = response.data[value][0]
                    json.dumps(errors)
                    response.format['status'] = False
                    response.format['message'] = errors
                    response.content = json.dumps(response.format)
            except Exception as e:
                print(e)
                pass

        return response
