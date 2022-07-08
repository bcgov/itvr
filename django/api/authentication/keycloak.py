import base64
from api.utility import format_postal_code
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

    def get_keycloaks(self):
        keycloaks = {}
        bceid_keycloak_openid = KeycloakOpenID(
            server_url=settings.BCEID_KEYCLOAK_URL,
            client_id=settings.BCEID_KEYCLOAK_CLIENT_ID,
            realm_name=settings.BCEID_KEYCLOAK_REALM,
        )
        bcsc_keycloak_openid = KeycloakOpenID(
            server_url=settings.BCSC_KEYCLOAK_URL,
            client_id=settings.BCSC_KEYCLOAK_CLIENT_ID,
            realm_name=settings.BCSC_KEYCLOAK_REALM,
        )
        keycloaks["bcsc"] = bcsc_keycloak_openid
        keycloaks["bceid"] = bceid_keycloak_openid
        return keycloaks

    def authenticate_credentials(self, token):
        keycloaks = self.get_keycloaks()
        for keycloak in keycloaks.values():
            # Decode the token from the front-end
            KEYCLOAK_PUBLIC_KEY = (
                "-----BEGIN PUBLIC KEY-----\n"
                + keycloak.public_key()
                + "\n-----END PUBLIC KEY-----"
            )

            options = {"verify_signature": True, "verify_aud": True, "verify_exp": True}

            try:
                token_info = keycloak.decode_token(
                    token, key=KEYCLOAK_PUBLIC_KEY, options=options
                )
            except Exception:
                continue

            # usernames will be uuids for bceid
            # and long identifiers for bc services card.
            user, created = ITVRUser.objects.get_or_create(
                username=token_info.get("sub"),
                defaults={
                    "display_name": token_info.get("display_name", ""),
                    "email": token_info.get("email", ""),
                    "identity_provider": token_info.get("identity_provider", ""),
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            if token_info.get("identity_provider") == "bcsc":
                user.last_name = token_info.get("family_name")
                user.first_name = token_info.get("given_name")
                user.date_of_birth = token_info.get("birthdate")
                user.street_address = token_info.get("street_address")
                user.locality = token_info.get("locality")
                user.postal_code = format_postal_code(token_info.get("postal_code"))

            return user, token
        raise AuthenticationFailed("Invalid token")
