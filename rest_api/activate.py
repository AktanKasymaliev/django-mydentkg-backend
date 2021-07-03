from rest_api.serializers.client_user_serializers import ForgotPasswordSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, renderer_classes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from rest_framework import status, response
from customUser.models import User
from .token import account_activation_token
from doctorsUser.models import DoctorUser


@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def activate_client(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, 
            User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return response.Response('Your account activated', status=status.HTTP_200_OK)
    else:
        return response.Response('Error 404', status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@renderer_classes([JSONRenderer])
def activate_doctors(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = DoctorUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, 
            User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return response.Response('Your account activated', status=status.HTTP_200_OK)
    else:
        return response.Response('Error 404', status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@renderer_classes([JSONRenderer])
def reset_password(request, uidb64, token):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid) if isinstance(request.user, User) \
                else DoctorUser.objects.get(pk=uid)
            if serializer.is_valid():
                if not user.check_password(serializer.data.get("old_password")):
                    return response.Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)
                if user is not None and account_activation_token.check_token(user, token):
                    user.set_password(serializer.data.get("new_password"))
                    user.save()
                    return response.Response({
                        'status': 'success',
                        'code': status.HTTP_200_OK,
                        'message': 'Password updated successfully',
                        'data': []
                    })
                else:
                    return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, 
            User.DoesNotExist):
            user = None
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
