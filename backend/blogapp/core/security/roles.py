from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = "Admin"
    AUTHOR = "Author"
    READER = "Reader"

    @classmethod
    def all_roles(cls):
        return [cls.ADMIN.value, cls.AUTHOR.value, cls.READER.value]

    @classmethod
    def role_to_value(cls, role):
        return {
            cls.ADMIN: 3,
            cls.AUTHOR: 2,
            cls.READER: 1,
        }.get(role, 0)
