from django.contrib.auth import logout, get_user_model
from functools import partial
from rest_framework.exceptions import ValidationError
from ..accounts.serializers import UserRegistrationSerializer, UserSerializer, LoginSerializer
from ..accounts.models import User, AuthTokenModel
from collections import namedtuple
from rest_framework.response import Response
from random import randint
from django.contrib.auth import login
from django.conf import settings

User = namedtuple('User',
                  ['username', 'email', 'mobile', 'password', 'first_name', 'last_name'])


def _parse_data(data, cls):
    """
    Generic function for parse user data using
    specified validator on `cls` keyword parameter.
    Raises: ValidationError exception if
    some errors found when data is validated.
    Returns the validated data.
    """
    serializer = cls(data=data)
    if not serializer.is_valid():
        raise ValidationError(serializer.errors)
    return serializer.validated_data


parse_register_user_data = partial(_parse_data, cls=UserRegistrationSerializer)
parse_auth_login_data = partial(_parse_data, cls=LoginSerializer)


def auth_register_user(request):
    """
    params: request
    return: user
    """
    user_model = get_user_model()
    data = parse_register_user_data(request.data)
    user_data = User(
        mobile=data.get('mobile'),
        email=data.get('email', None),
        password=data.get('password'),
        first_name=data.get('first_name', None),
        last_name=data.get('last_name', None),
        username=data.get('username')
    )
    user = None
    # Check email is register as a active user
    try:
        user = get_user_model().objects.get(mobile=data.get('mobile'), is_active=True)
    except get_user_model().DoesNotExist:
        pass
    try:
        user = get_user_model().objects.get(username=data.get('username'), is_active=True)
    except get_user_model().DoesNotExist:
        pass
    # if user is not exist, create a Inactive user
    if not user:
        un_active_user = user_model.objects.filter(username=user_data.username, is_active=False)
        if un_active_user:
            user_model.objects.filter(username=user_data.username, is_active=False).delete()

        user = user_model.objects.create_user(**dict(user_data._asdict()), is_active=True)
    user_obj = user_model.objects.filter(username=data.get('username')).first()
    if user_obj:
        user_obj.set_password(data.get('password'))
        user_obj.save()
    return UserRegistrationSerializer(user).data


def get_user_from_email_or_mobile(username):
    user_model = get_user_model()
    username_user = user_model.objects.filter(username=username).first()
    user = username_user if username_user else None
    return user


def generate_auth_data(request, user):
    token, created = AuthTokenModel.objects.get_or_create(user=user)
    login(request, user)
    auth_data = {
        "token": token.key,
        "user": UserSerializer(user, context={'request': request}).data
    }
    return auth_data


def auth_login(request):
    """
    params: request
    return: token, password
    """
    data, auth_data = parse_auth_login_data(request.data), None
    username, password = data.get('username'), data.get('password')
    if username and password:
        user = get_user_from_email_or_mobile(username)
        if not user:
            return Response({'detail': 'User does not exists.'})
        if user.check_password(password):
            if not user.is_active:
                return Response({'detail': 'User account is disabled.'})
            auth_data = generate_auth_data(request, user)
            return Response(auth_data)
        else:
            return Response({'detail': 'Incorrect Username or password.'})
    else:
        return Response({'detail': 'Must Include username and password.'})


def upload_file(instance, image):
    print(instance._meta, image)
    return 'task/{model}/{image}'.format(
        model=instance._meta.model_name, image=str(randint(100000, 999999)) + "_" + image
    )

def file_extension_validator(value):
    valid_extensions_file = ('pdf', 'png', 'jpeg', 'jpg')
    try:
        if value:
            file_name = value.name
            file_extension = file_name.split('.')[-1].lower()
            if file_extension in valid_extensions_file:
                if value.size > int(settings.MAX_UPLOAD_SIZE):
                    raise ValidationError("Please keep the file size under 100 MB")
            else:
                raise ValidationError("Please upload file in PDF/PNG/JPG/JPEG formats.")
    except Exception:
        return True

def create_update_record(request, serializer_class, model_class):
    request_data = request.data.copy() if not isinstance(request, dict) else request
    data_id = request_data.pop('id', None)
    if data_id:
        data_obj = model_class.objects.get(id=data_id)
        serializer = serializer_class(instance=data_obj, data=request_data, partial=True)
    else:
        serializer = serializer_class(data=request_data)
    serializer.is_valid(raise_exception=True)
    update_object = serializer.save()
    return serializer_class(instance=update_object).data