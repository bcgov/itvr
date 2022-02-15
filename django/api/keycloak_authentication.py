from keycloak import KeycloakOpenID

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


class KeycloakAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)

        if not auth:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        try:
            scheme, token = auth.split()
        except ValueError:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        if not token:
            raise exceptions.AuthenticationFailed(
                'Authorization token required'
            )

        keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            realm_name=settings.KEYCLOAK_REALM
        )

        print(settings.KEYCLOAK_URL)
        print(settings.KEYCLOAK_CLIENT_ID)
        print(settings.KEYCLOAK_REALM)

        # Decode the token from the front-end
        KEYCLOAK_PUBLIC_KEY = \
            "-----BEGIN PUBLIC KEY-----\n" + \
            keycloak_openid.public_key() + \
            "\n-----END PUBLIC KEY-----"

        options = {
            'verify_signature': True,
            'verify_aud': True,
            'verify_exp': True
        }

        token_info = keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options=options
        )

        print("TOKEN INFO")
        print(token_info)

        # Get the user from the keycloak server based on the token
        user_info = keycloak_openid.userinfo(token)

        print("USER INFO")
        print(user_info)

        if user_info.get('preferred_username') != \
                token_info.get('preferred_username'):
            raise exceptions.AuthenticationFailed(
                'Invalid Token'
            )

        user = User.objects.filter(
            username=user_info.get('preferred_username')
        ).first()

        return user, None
