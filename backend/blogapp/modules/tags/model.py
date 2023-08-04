from beanie import Document


class TagDocument(Document):
    name: str

    class Settings:
        name = "tags"
