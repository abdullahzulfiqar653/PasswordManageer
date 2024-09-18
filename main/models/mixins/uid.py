import shortuuid
from collections import Counter
from common.contants import MODEL_CODES


class UIDMixin:
    UID_PREFIX = None  # This should be defined in the model inheriting from UIDMixin.

    def set_uid(self):
        """
        Generates and assigns a unique ID (UID) to the object if it doesn't already have one.
        The UID consists of a prefix and a randomly generated short UUID.

        :return: The generated or existing UID of the object.
        """

        # Find the items that are repeated
        repeated = [
            item for item, count in Counter(MODEL_CODES.values()).items() if count > 1
        ]
        if repeated:
            raise ValueError(
                f"Model codes must be unique. The following code(s) are repeated: {', '.join(repeated)}."
            )
        
        self.UID_PREFIX = MODEL_CODES.get(self.__class__.__name__)

        # Ensure that the model has a valid UID_PREFIX
        if not isinstance(self.UID_PREFIX, str) or not self.UID_PREFIX:
            raise ValueError("UID_PREFIX is required and must be a non-empty string.")

        # Ensure the prefix has a minimum length of 4 characters
        if len(self.UID_PREFIX) < 3:
            raise ValueError("UID_PREFIX must be at least 4 characters long.")

        # Only set the UID if it doesn't exist
        if not self.id:
            self.id = self._generate_unique_uid()

        return self.id

    def _generate_unique_uid(self):
        """
        Generates a unique UID by combining the UID_PREFIX and a random short UUID.
        Ensures the UID is unique in the database.

        :return: A unique UID.
        """
        uid = self.UID_PREFIX + shortuuid.ShortUUID().random(length=12)
        # Ensure the generated UID is unique in the model's database
        while self.__class__.objects.filter(id=uid).exists():
            uid = self.UID_PREFIX + shortuuid.ShortUUID().random(length=12)
        return uid
