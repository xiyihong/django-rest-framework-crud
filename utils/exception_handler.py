from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.exceptions import JsonResponse

from utils.response import ResponseBody


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, ValidationError):
        error_msg = exc.get_full_details()
    else:
        try:
            error_msg = str(exc.detail)
        except:
            error_msg = str(exc)
    if response is not  None:
        response.data.clear()
        response.data = dict()
        response.data['code'] = response.status_code
        response.data['message'] = error_msg
        response.data['data'] = []
        response.status_code = 200

    return response


def server_error(request, *args, **kwargs):
    data = ResponseBody()
    data.code = 500
    data.msg = "Server Error (500)"
    return JsonResponse(
        data=data,
        status=status.HTTP_200_OK,
    )

def bad_request(request, exception, *args, **kwargs):
    data = ResponseBody()
    data.code = 400
    data.msg = "Bad Request (400)"
    return JsonResponse(
        data=data,
        status=status.HTTP_200_OK,
    )