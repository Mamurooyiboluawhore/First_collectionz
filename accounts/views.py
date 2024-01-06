from rest_framework import generics, status, viewsets
from rest_framework.response import Response 
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
	RegisterUserSerializer,
	UserSerializer,
	ChangePasswordSerializer
)

from .permissions import IsAccountOwner
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash

User = get_user_model()



class UserCreateAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterUserSerializer
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		refresh = RefreshToken.for_user(user)
		return Response({
			'user': UserSerializer(user).data,
			'token': {
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			}
		})

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
		if serializer.is_valid():
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
		return Response(
			serializer.errors, status=status.HTTP_400_BAD_REQUEST
		)

change_password = ChangePasswordAPIView.as_view()
