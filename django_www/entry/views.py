from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from garena_oauth.user import PermitGarenaUser, AuthGarenaUser

import logging
logger = logging.getLogger()

class Profile(APIView):
    authentication_classes = (AuthGarenaUser,)
    permission_classes = (PermitGarenaUser,)
    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        uid = request.user.uid
        return Response({'uid': uid})
