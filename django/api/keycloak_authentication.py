import base64
from keycloak import KeycloakOpenID
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


ITVRUser = get_user_model()


def base64_decode(data: str) -> str:
    """
    We can check the identity provider of the token and then
    verify or pass on the request.
    """

    data = data.encode("ascii")

    rem = len(data) % 4

    if rem > 0:
        data += b"=" * (4 - rem)
    return base64.urlsafe_b64decode(data).decode("utf-8")


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

        # usernames will be uuids for bceid
        # and long identifiers for bc services card.
        user, created = ITVRUser.objects.get_or_create(
            username=token_info.get("sub"),
            defaults={
                "display_name": token_info.get("display_name"),
                "email": token_info.get("email"),
                "identity_provider": token_info.get("identity_provider"),
            },
        )

        if created:
            user.set_unusable_password()
            user.save()

        return user, token
