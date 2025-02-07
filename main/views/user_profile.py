from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from main.models.user_profile import UserProfile
from main.serializers.user_profile import UserProfileSerializer


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """To **retrive** and **update** profile attributes"""

    serializer_class = UserProfileSerializer
    
    @swagger_auto_schema(
        operation_description="**Retrieve** and **update** the **user profile** attributes.",
        responses={
            200: UserProfileSerializer,
            404: '**User profile** not found.',
        }
    )
    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")
