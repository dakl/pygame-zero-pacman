from dataclasses import dataclass


@dataclass
class CustomActor:
    x: int
    y: int
    width: int
    height: int

    def colliderect(self, other) -> bool:
        if self.height == 0 or self.width == 0 or other.height == 0 or other.width == 0:
            return False

        # // A.left   < B.right  &&
        # // A.top    < B.bottom &&
        # // A.right  > B.left   &&
        # // A.bottom > B.top
        return (
            self.x < other.x + other.width
            and self.x + self.width > other.x
            and self.y < other.y + other.height
            and self.y + self.height > other.y
        )

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.width

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.height
