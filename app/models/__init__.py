from app.database import Base
from app.models.posts import Post

__all__ = [
    # Base Model Object to export after attaching the models with it
    "Base",

    # All the models attached to the upper Base class
    "posts"
]
