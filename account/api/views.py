from account import \
    models  # calling the create_auth_token signal from models.py for auto generated tokens
from account.api.serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST', ])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Successfully registered'
            data['username'] = account.username
            data['email'] = account.email

            # createing token manually for TokenAuthentication
            token = Token.objects.get(user=account).key
            data['token'] = token
            # ...

            # Creating token manually for JWT
            # refresh = RefreshToken.for_user(account)

            # data['token'] = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token),
            # }
            # ...

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST', ])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)
