from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self, folder_name, bucket_name="neuropyservices"):
        self.s3_client = settings.S3_CLIENT
        self.folder_name = folder_name
        self.bucket_name = bucket_name

    def upload_file(self, file_obj, object_name):
        """
        Uploads a file directly from an HTTP request to a specific folder in DigitalOcean Spaces.
        :param file_obj: The file object from the HTTP request (e.g., request.FILES['file'])
        :param bucket_name: The name of the Space (bucket)
        :param folder_name: The folder where the file will be uploaded
        :param object_name: The unique file name in the space
        :return: The presigned URL for the uploaded file
        """
        try:
            full_object_name = f"{self.folder_name}/{object_name}"

            # Upload the file directly from the request
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, full_object_name)
            logger.info(f"File uploaded successfully: {full_object_name}")
            return self.generate_presigned_url(full_object_name)
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise Exception(f"Error uploading file: {e}")

    def generate_presigned_url(self, object_name, expiration=3600):
        """
        Generates a presigned URL to access the uploaded file from the Space.
        :param bucket_name: The name of the Space
        :param object_name: The object name in the space
        :param expiration: Time in seconds for which the URL is valid
        :return: Presigned URL
        """
        try:
            full_object_name = f"{self.folder_name}/{object_name}"
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": full_object_name,
                },
                ExpiresIn=expiration,
            )
            logger.info(f"Generated presigned URL for {full_object_name}")
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            raise Exception(f"Error generating presigned URL: {e}")
