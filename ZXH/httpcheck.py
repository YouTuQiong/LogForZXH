from rest_framework.response import Response
content_type = "application/json; charset=utf-8"
def noLogin():
    return Response(content_type=content_type,data={"message": "noLogin",
                     "state": "233",
                     "data": ""})
