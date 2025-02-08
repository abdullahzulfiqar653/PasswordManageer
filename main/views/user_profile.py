from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from main.models.user_profile import UserProfile
from main.serializers.user_profile import UserProfileSerializer


class UserProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    serializer_class = UserProfileSerializer

    def get_object(self):
        try:
            return self.request.user.profile
        except UserProfile.DoesNotExist:
            raise NotFound("User profile not found.")

    @swagger_auto_schema(
        operation_description="""
        **Retrieve User Profile Details**  

        The following attributes will be returned when fetching the user profile:  

        - **ID:**   
        Unique identifier of the user profile.  

        - **Image:**  
        URL of the user's profile image.  

        - **Address:**  
        User's address (can be empty).  

        - **Features Data:** 
        Additional profile-related information.  

        - **URL:**  
        Direct link to the user's profile.  
        """,
        responses={
            200: UserProfileSerializer,
            404: "**User profile** not found.",
        },
    )
    def get(self, request, *args, **kwargs):
        """Handles retrieving the user profile."""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
         operation_description="""
                **Update User Profile**  

                Users can update the following attribute:  

                - **Image:** *(file, optional)*  
                Upload a new profile image. The image will be stored on S3, and its URL will be generated.  
                """,
        request_body=UserProfileSerializer,
        responses={
            200: "Profile updated successfully.",
            400: "Invalid data provided.",
            404: "**User profile** not found.",
        },
    )
    def put(self, request, *args, **kwargs):
        """Handles updating user profile details."""
        return super().put(request, *args, **kwargs)
