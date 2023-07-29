from beanie import Document


class Tag(Document):
    name: str

    class Settings:
        name = "tags"
