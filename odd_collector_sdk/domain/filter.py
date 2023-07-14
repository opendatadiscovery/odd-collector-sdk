import re

from funcy import partial
from pydantic import BaseModel


class Filter(BaseModel):
    include: list[str] = [".*"]
    exclude: list[str] = []
    ignore_case: bool = False

    def case_sensitive_flag(self):
        return re.IGNORECASE if self.ignore_case else 0

    def is_allowed(self, value: str) -> bool:
        search = partial(re.search, string=value, flags=self.case_sensitive_flag())
        if any(search(pattern) for pattern in self.exclude):
            return False

        return any(search(pattern) for pattern in self.include)
