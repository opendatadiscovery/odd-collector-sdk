import re

from funcy import partial
from pydantic import BaseModel, validator


class Filter(BaseModel):
    include: list[str] = []
    exclude: list[str] = []
    ignore_case: bool = False

    @validator("include", always=True)
    def check_include(cls, include):
        if not include:
            return [".*"]
        else:
            return include

    def case_sensitive_flag(self):
        return re.IGNORECASE if self.ignore_case else 0

    def is_allowed(self, value: str) -> bool:
        match = partial(re.match, string=value, flags=self.case_sensitive_flag())
        if any(match(pattern) for pattern in self.exclude):
            return False

        return any(match(pattern) for pattern in self.include)
