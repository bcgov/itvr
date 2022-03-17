from keycloak import KeycloakOpenID

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

import logging


log = logging.getLogger('KeycloakAuthentication')


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

        # Get the user from the keycloak server based on the token
        user_info = keycloak_openid.userinfo(token)
        username = user_info.get('preferred_username')

        if username != \
                token_info.get('preferred_username'):
            raise exceptions.AuthenticationFailed(
                'Invalid Token'
            )

        # TODO make a ticket to improve this
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            log.warn(
                'KeycloakAuthentication user does not exist'
            )

        if user is None:
            user = User.objects.create_user(username=username)

        return user, None
