from keycloak import KeycloakOpenID
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

import logging


log = logging.getLogger("KeycloakAuthentication")

User = get_user_model()


class KeycloakAuthentication(TokenAuthentication):
    keyword = "Bearer"

    def authenticate_credentials(self, token):
        keycloak_openid = KeycloakOpenID(
            server_url=settings.KEYCLOAK_URL,
            client_id=settings.KEYCLOAK_CLIENT_ID,
            realm_name=settings.KEYCLOAK_REALM,
        )

        # Decode the token from the front-end
        KEYCLOAK_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            + keycloak_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )

        options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}

        try:
            token_info = keycloak_openid.decode_token(
                token, key=KEYCLOAK_PUBLIC_KEY, options=options
            )
        except Exception:
            raise AuthenticationFailed("Invalid Token")

        username = token_info.get("preferred_username")

        # TODO make a ticket to improve this
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            log.warn("KeycloakAuthentication user does not exist")

        if user is None:
            user = User.objects.create_user(username=username)

        return user, token
