from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication


ITVRUser = get_user_model()


class LoadTestingAuthentication(TokenAuthentication):
    # Use any kind of token in the front end
    # ex. Authorization: Bearer testtoken
    keyword = "Bearer"

    def authenticate_credentials(self, token):
        # This requires a user to be present in the database.
        user = ITVRUser.objects.first()
        return user, token
