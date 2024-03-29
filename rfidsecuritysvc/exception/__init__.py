class BaseError(Exception):
    pass


class MediaNotFoundError(BaseError):
    pass


class DuplicateMediaError(BaseError):
    pass


class PermissionNotFoundError(BaseError):
    pass


class DuplicatePermissionError(BaseError):
    pass


class ConfigNotFoundError(BaseError):
    pass


class DuplicateConfigError(BaseError):
    pass


class MediaPermNotFoundError(BaseError):
    pass


class DuplicateMediaPermError(BaseError):
    pass


class DuplicateAssociationError(BaseError):
    pass


class AssociationNotFoundError(BaseError):
    pass


class DeviceNotFoundError(BaseError):
    pass


class DuplicateGuestError(BaseError):
    pass


class GuestNotFoundError(BaseError):
    pass


class DuplicateGuestMediaError(BaseError):
    pass


class GuestMediaNotFoundError(BaseError):
    pass


class DuplicateSoundError(BaseError):
    pass


class SoundNotFoundError(BaseError):
    pass
