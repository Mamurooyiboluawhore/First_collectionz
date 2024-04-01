from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from .utils import generate_otp, send_otp_email
from .serializers import (
	RegisterUserSerializer,
	UserSerializer,
	ChangePasswordSerializer
)

from .permissions import IsAccountOwner
from .sendmail import send_plain_text_email
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate

User = get_user_model()



# class LoginWithOTP(APIView):
# 	def post(self, request):
# 		email = request.data.get('email', '')
# 		try:
# 			user = User.objects.get(email=email)
# 		except User.DoesNotExist:
# 			return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
		
# 		otp = generate_otp()
# 		user.otp = otp
# 		user.save()

# 		send_otp_email(email, otp)

# 		return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)
	


class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        print(user.otp)  # Print the OTP for debugging purposes

        if user.otp == otp:
            user.otp = None
            user.save()

            # Authenticate the user and create or get an authentication token
            # token, _ = Token.objects.get_or_create(user=user)

            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

		

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            # refresh = RefreshToken.for_user(user)
            otp = generate_otp()
            user.otp = otp
            user.save()
            send_otp_email(user.email, otp)
            send_plain_text_email(
                subject='OTP for Account Verification',
                to_email=user.email,
                message=f'Your OTP for account verification is: {otp}'
            )
            return Response({
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,

                },
                # 'token': {
                #     'refresh': str(refresh),
                #     'access': str(refresh.access_token),
                # },
                'message': 'OTP has been sent to your email.',
            }, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if 'email' in str(e) and 'unique' in str(e):
                return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

user_create = UserCreateAPIView.as_view()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [IsAccountOwner]
	
user_list_viewset = UserViewSet.as_view({'get': 'list'})
user_detail_viewset = UserViewSet.as_view({'get': 'retrieve'})
user_update_viewset = UserViewSet.as_view({'patch': 'partial_update'})

class UserDetailAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request, format=None):
		user = request.user
		serializer = UserSerializer(user, many=False)
		return Response(serializer.data)

user_detail = UserDetailAPIView.as_view()

class ChangePasswordAPIView(generics.GenericAPIView):
	serializer_class = ChangePasswordSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		try:
			serializer.is_valid()
			user = request.user
			if user.check_password(serializer.validated_data.get('old_password')):
				user.set_password(serializer.validated_data.get('new_password'))
				user.save()
				update_session_auth_hash(request, user)
				return Response(
					{'message': 'Password changed succesfully'},
					status=status.HTTP_200_OK
				)
			return Response(
				{'error': 'Incorrect old password'},
				status=status.HTTP_400_BAD_REQUEST
			)
		except Exception as e:
			return Response(
				serializer.errors, status=status.HTTP_400_BAD_REQUEST
			)

change_password = ChangePasswordAPIView.as_view()
