from enum import Enum


class ItemType(Enum):
    DELICATE_MIRROR = 1


class Item:
    def __init__(self, name, image, item_type):
        self.name = name
        self.image = image
        self.item_type = item_type


def magic_mirror():
    return Item(
        "a beautifully delicate mirror",
        None,
        ItemType.DELICATE_MIRROR,
    )


def item_factory(item_type: int):
    if item_type == ItemType.DELICATE_MIRROR.value:
        return magic_mirror()
