from rest_framework import generics
from rest_framework.exceptions import NotFound
from main.models.user_profile import UserProfile
from main.serializers.user_profile import UserProfileSerializer


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """to retrive and update profile attributes"""

    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")
