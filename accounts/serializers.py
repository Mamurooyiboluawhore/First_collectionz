from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'full_name', 'email', 'password']
		extra_kwargs = {
			'password': {'write_only': True},
			'pk': {'read_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'full_name', 'email']
		#extra_kwargs = {'pk': {'read_only': True}}


class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField()
	new_password = serializers.CharField()


class ResetPasswordEmailSerializer(serializers.Serializer):
	email = serializers.EmailField()

class ValidateResetPasswordSerializer(serializers.Serializer):
	email = serializers.EmailField()
	otp = serializers.CharField()

class ConfirmPasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField()
	otp = serializers.CharField()
	password_1 = serializers.CharField()
	password_2 = serializers.CharField()


class RegisterSelllerSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'full_name', 'phone', 'email', 'password', 'admin']
		extra_kwargs = {
			'password': {'write_only': True},
			'pk': {'read_only': True},
			'admin': {'read_only': True},
		}

class LoginUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['pk', 'email', 'password']
		extra_kwargs = {
			'password': {'write_only': True},
			'pk': {'read_only': True},
		}

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            # Retrieve the user directly using get() method
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'Invalid email'})

        # Check if password is valid
        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password'})

        data['user'] = user
        return data


    