"""Reader for existing unversioned Meta compositions. Never writes a migration."""

from typing import Any

from .._models import Composition
from .common import composition_fields


class LegacyComposition:
    def read(self, data: dict[str, Any]) -> Composition:
        return composition_fields(data, 0)
