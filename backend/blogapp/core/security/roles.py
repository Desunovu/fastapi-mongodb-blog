from enum import Enum


class RolesEnum(str, Enum):
    ADMIN = "Admin"
    Author = "Author"
    Reader = "Reader"

    @classmethod
    def all_roles(cls):
        return [
            cls.ADMIN.value,
            cls.Author.value,
            cls.Reader.value
        ]
