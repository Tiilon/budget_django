# from django.contrib.auth import authenticate
# import jwt
# import traceback
# from django.utils.functional import SimpleLazyObject
# from django.utils.deprecation import MiddlewareMixin
# from django.contrib.auth.models import AnonymousUser
# from rest_framework import authentication
# from user.models import User
# from django.conf import LazySettings
# from django.contrib.auth.middleware import get_user
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.request import Request

# settings = LazySettings()

# def get_user_jwt(request):
#     user = None
#     try:
#         user_jwt = JWTAuthentication().authenticate(Request(request))
#         if user is None:
#             user = user_jwt[0]
#     except:pass
#     return user or AnonymousUser()

# class JWTAuthentication(object):
#     def process_request(self, request):
#         request.user = SimpleLazyObject(lambda:get_user_jwt(request))



#     # @staticmethod
#     # def get_jwt_user(request):
        
#     #     user = get_user(request)
#     #     if user.is_authenticated():
#     #         return user
#     #     jwt_authentication = JWTAuthentication()
#     #     authenticated =jwt_authentication.authenticate(request)
#     #     if authenticated:
#     #         user,jwt = authenticated
#     #     return user


#         # token = request.Meta.get('HTTP_AUTHORIZATION', None)

#         # user = AnonymousUser()
#         # if token is not None:
#         #     try:
#         #         user = jwt.decode(token, settings.SECRET_KEY)
#         #         user = User.objects.get(id=user.data.user_id)
#         #     except Exception as e:
#         #         traceback.print_exc
#         # return user
