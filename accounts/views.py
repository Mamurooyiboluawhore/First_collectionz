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
	ChangePasswordSerializer,
	ValidateResetPasswordSerializer,
	ConfirmPasswordResetSerializer,
	ResetPasswordEmailSerializer,
    UserLoginSerializer
	
)

from .permissions import IsAccountOwner
from .sendmail import send_plain_text_email, Send_email_with_zoho_server
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from django.utils import timezone
# from datetime import timezone


User = get_user_model()


class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        print(user.otp)  # Print the OTP for debugging purpose

        if user.otp == otp:
            # check if token has expired
            time_difference = max(user.created_at, user.updated_at)
            mins_difference = (
                timezone.now() - time_difference
            ).total_seconds() / 60
            if mins_difference > 2:
                response = {
                    "response_status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": "OTP token expired. Try again.",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
            user.otp_verified = True  # Mark OTP as verified
            user.otp = None
            user.save()

            # Authenticate the user and create or get an authentication token
            # token, _ = Token.objects.get_or_create(user=user)

            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

		


class ResendOtpView(APIView):
      def patch(self, request):
            """Resends a new OTP to the registered Email ID
                Payload:
                    {
                        "email": "user@example.com"
                    }
            """
            
            email = request.data.get('email')
            try:
                  user = User.objects.get(email=email)

            except User.DoesNotExist:
                  response = {'response_status':'error',
                              'status_code':status.HTTP_404_NOT_FOUND,
                              'message':'User does not exist'}
                  return Response(response, status=status.HTTP_404_NOT_FOUND)
            if user.otp is None:
                  response = {
                        'message': "Your account already verified"
                  }
                  return Response(response, status=status.HTTP_400_BAD_REQUEST)
            otp = generate_otp()
            user.otp=otp
            user.save()
            Send_email_with_zoho_server(message=otp, to_email=email)
            

            response ={
                  'message': 'new otp has been sent to your email!',
                  'status': status.HTTP_200_OK
            }
            return Response(response, status=status.HTTP_200_OK)
      
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
            # send_otp_email(user.email, otp)
            Send_email_with_zoho_server(
                # subject='OTP for Account Verification',
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


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            if user.otp_verified:
            # Generate tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response_data = {
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'message': 'You are logged in' 
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': access_token,
                    }
            }
                response = Response(response_data, status=status.HTTP_200_OK)
                return response
            else:
                return Response({'error': 'OTP not verified. Please verify OTP first.'}, status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError:
            return Response({'error': 'OTP not verified. Please verify OTP first.'}, status=status.HTTP_401_UNAUTHORIZED)

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


class PasswordResetAPIView(generics.GenericAPIView):
	serializer_class = ResetPasswordEmailSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data.get('email', '')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
		otp = generate_otp()
		user.otp = otp
		user.save()

		SyntaxError(email, otp)

		return Response({
			'message': 'OTP has been sent to your email',
			'status': status.HTTP_200_OK
		}, status=status.HTTP_200_OK)

password_reset = PasswordResetAPIView.as_view()

class ValidatePasswordResetOTPAPIView(generics.GenericAPIView):
	serializer_class = ValidateResetPasswordSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data.get('email', '')
		otp = serializer.validated_data.get('otp', '')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
		if user.otp == otp:
			return Response({
				'message': 'OTP is valid',
				'status': status.HTTP_200_OK
			}, status=status.HTTP_200_OK)
		return Response({
			'error': 'Invalid OTP',
			'status':status.HTTP_400_BAD_REQUEST
		}, status=status.HTTP_400_BAD_REQUEST)

validate_password_reset_otp = ValidatePasswordResetOTPAPIView.as_view()

class ConfirmPasswordResetAPIView(generics.GenericAPIView):
	serializer_class = ConfirmPasswordResetSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data.get('email', '')
		otp = serializer.validated_data.get('otp', '')
		password_1 = serializer.validated_data.get('password_1', '')
		password_2 = serializer.validated_data.get('password_2', '')
		try:
			user = User.objects.get(email=email)
		except:
			return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
		if user.otp == otp:
			if password_1 == password_2:
				user.otp = None
				user.set_password(serializer.validated_data.get('password_1'))
				user.save()
				update_session_auth_hash(request, user)
				return Response(
					{'message': 'Password reset succesful'},
					status=status.HTTP_200_OK
				)
			return Response({
				'error': 'password_1 not same as password_2',
				'status':status.HTTP_400_BAD_REQUEST
			}, status=status.HTTP_400_BAD_REQUEST)
		return Response({
			'error': 'Invalid OTP',
			'status':status.HTTP_400_BAD_REQUEST
		}, status=status.HTTP_400_BAD_REQUEST)

confirm_password_reset = ConfirmPasswordResetAPIView.as_view()


class Testemail(APIView):
      def get(self, request):
            Send_email_with_zoho_server()
            response = {
                  'message': 'email sent',
                  'status': 200
            }
            return Response(response, status=status.HTTP_200_OK)

