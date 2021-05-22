from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User
from django.contrib.auth import logout, get_user_model
from django.utils.translation import ugettext_lazy as ul


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'mobile', 'last_name', 'is_active',
            'is_superuser'
        )
        extra_kwargs = {'password': {'write_only': True},
                        'last_login': {'read_only': True},
                        'is_superuser': {'read_only': True}}


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'mobile', "password", 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate(self, data):
        mobile = data.get("mobile", None)
        if mobile:
            if User.objects.filter(mobile=mobile, is_active=True).exists():
                raise serializers.ValidationError({"detail": "User with this mobile already exists."})
        if mobile is None:
            raise serializers.ValidationError({"detail": "Mobile Number is necessary to fill"})
        return data

    def validate_password(self, value):
        if len(value) > 7:
            return value
        else:
            msg = ul('Password should have minimum 8 characters.')
            raise serializers.ValidationError(msg)


class LoginSerializer(serializers.Serializer):
    """
        login serializer
    """
    username = serializers.CharField(
        allow_blank=False,
        allow_null=False,
        error_messages={'required': 'Please enter a valid mobile/email id.',
                        'blank': 'Please enter a valid mobile/email id.',
                        'null': 'Please enter a valid mobile/email id.'}
    )
    password = serializers.CharField(max_length=128)
