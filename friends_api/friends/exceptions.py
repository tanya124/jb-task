from django.db import IntegrityError

class FriendshipExistsError(IntegrityError):
    pass
