import enum


class EnumBase(str, enum.Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
