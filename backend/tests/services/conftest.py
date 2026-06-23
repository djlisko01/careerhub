from datetime import datetime, timezone as tz
from unittest.mock import MagicMock

import pytest

FIXED_DATETIME = datetime(2024, 1, 1, tzinfo=tz.utc)


@pytest.fixture(autouse=True, scope="module")
def patch_datetime():
    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2024, 1, 1, tzinfo=tz)

    with pytest.MonkeyPatch.context() as mp:
        mp.setattr("db.services.user_profile_service.datetime", FixedDateTime)
        yield

@pytest.fixture
def get_mock_db() -> MagicMock:
    mock_db = MagicMock()
    return mock_db