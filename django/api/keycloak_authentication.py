from keycloak import KeycloakOpenID
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

import logging


log = logging.getLogger('KeycloakAuthentication')


class KeycloakAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
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

        try:
            token_info = keycloak_openid.decode_token(
                token,
                key=KEYCLOAK_PUBLIC_KEY,
                options=options
            )
        except Exception:
            raise AuthenticationFailed(
                'Invalid Token'
            )

        username = token_info.get('preferred_username')

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

    def authenticate_header(self):
        return self.keyword
