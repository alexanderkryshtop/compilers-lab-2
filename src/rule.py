from common import EPSILON


class Rule:
    def __init__(self, left: str, right: list[str]):
        self.left = left.strip()
        self.right = [elem.strip() for elem in right]

    def __repr__(self):
        right_str = " ".join(self.right) or EPSILON
        return f"{self.left} -> {right_str}"