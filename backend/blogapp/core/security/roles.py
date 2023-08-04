from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = "Admin"
    AUTHOR = "Author"
    READER = "Reader"

    @classmethod
    def all_roles(cls):
        return [cls.ADMIN.value, cls.AUTHOR.value, cls.READER.value]
