from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                return Response({
                    'result': 'refresh token 不存在'
                }, status=401)
            refresh = RefreshToken(refresh_token) # 如果refresh token 过期了，会报异常
            if settings.SIMPLE_JWT['ROTATE_REFRESH_TOKENS']:
                pass

        except:
            return Response({
                'result': "refresh token 过期了"
            }, status=401) #必须加上401