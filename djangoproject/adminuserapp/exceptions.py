# exceptions.py

from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        # 检查是否为认证失败的异常
        if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
            response.data = {
                'code': response.status_code,
                'message': 'Authentication credentials were not provided.'
            }
        else:
            response.data = {
                'code': response.status_code,
                'message': response.data.get('detail', 'An error occurred.')
            }

    return response