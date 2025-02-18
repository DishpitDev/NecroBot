from typing import Any
from peridata import Property, PersistentStorage

USER_AVAILABLE_DATA: dict[str, Property[Any]] = {
    "necrocoins": Property[int](0, False),
}

class UserDataManager(PersistentStorage):
    def __init__(self, user_id: int):
        super().__init__(USER_AVAILABLE_DATA, f"data/users/{user_id}.json")
