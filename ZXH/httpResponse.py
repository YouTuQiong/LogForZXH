from rest_framework.response import Response
from rest_framework.status import *

content_type = "application/json; charset=utf-8"


# status = Response.status_code;
def noLogin():
    return Response(content_type=content_type, data={"message": "noLogin",
                                                     "state": "233",
                                                     "data": ""})


def Json(data, status=None, state=None, message=None):
    if status is None:
        status = 200
    if state is None:
        state = "200"
    if message is None:
        message = 'ok'
    return Response(content_type=content_type, data={"message": message,
                                                     "state": state,
                                                     "data": data,
                                                     }, status=status)


def isLogin(request):
    return request.session.get('user_id')


def IPAddress(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip
