from datetime import datetime, timezone as tz
from unittest.mock import MagicMock

import pytest
from db.models.principals import Principal, PrincipalType
from db.models.users import UserProfile
from db.services.user_profile_service import InactiveUserError, UserService
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

import schemas.users as user_schemas

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


def get_mock_db() -> MagicMock:
    mock_db = MagicMock()
    return mock_db


@pytest.fixture
def user_service():
    db = get_mock_db()
    return UserService(db=db)


@pytest.fixture
def mock_user_create():
    mock_profile = MagicMock()
    mock_profile.id = 1
    mock_profile.first_name = "John"
    mock_profile.last_name = "Doe"
    mock_profile.linkedin_url = None
    mock_profile.github_url = None
    mock_profile.active = True
    return mock_profile


def make_flush_handler(added_objects, principal_id=99, profile_id=1):
    def on_flush():
        for obj in added_objects:
            if isinstance(obj, Principal) and obj.id is None:
                obj.id = principal_id
            if isinstance(obj, UserProfile) and obj.id is None:
                obj.id = profile_id
                obj.active = True

    return on_flush


class TestCreateUserProfile:

    def test_happy_path_returns_profile(self, user_service):
        user_data = user_schemas.UserCreateSchema(
            first_name="John",
            last_name="Doe",
            linkedin_url="https://linkedin.com/in/johndoe",
            github_url="https://github.com/johndoe",
        )
        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(added_objects)

        result = user_service.create_user_profile(user_data)

        assert isinstance(result, user_schemas.UserReponseSchema)
        assert result.id == 1
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.linkedin_url == "https://linkedin.com/in/johndoe"
        assert result.github_url == "https://github.com/johndoe"
        assert result.active is True

    def test_creates_human_principal_before_profile(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(added_objects)

        user_service.create_user_profile(user_data)

        add_calls = user_service.db.add.call_args_list
        added_types = [type(call.args[0]) for call in add_calls]

        assert Principal in added_types
        assert UserProfile in added_types
        assert added_types.index(Principal) < added_types.index(UserProfile)

        principal = add_calls[added_types.index(Principal)].args[0]
        assert principal.principal_type == PrincipalType.HUMAN

    def test_links_new_principal_id_to_profile(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(
            added_objects, principal_id=42, profile_id=7
        )

        user_service.create_user_profile(user_data)

        user_profile = next(
            obj for obj in added_objects if isinstance(obj, UserProfile)
        )
        assert user_profile.principal_id == 42

    def test_active_defaults_to_true(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(added_objects)

        result = user_service.create_user_profile(user_data)

        assert result.active is True

    def test_optional_fields_are_none_when_not_provided(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(added_objects)

        result = user_service.create_user_profile(user_data)

        assert result.linkedin_url is None
        assert result.github_url is None

    def test_raises_on_duplicate_auth(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)
        user_service.db.flush.side_effect = make_flush_handler(added_objects)
        user_service.db.commit.side_effect = IntegrityError(
            statement=None, params=None, orig=Exception("duplicate key value")
        )

        with pytest.raises(IntegrityError):
            user_service.create_user_profile(user_data)

    def test_raises_on_missing_params(self):
        with pytest.raises(ValidationError):
            user_schemas.UserCreateSchema()


class TestGetUserProfile:

    def test_returns_profile_when_found(self, user_service, mock_user_create):
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        result = user_service.get_user_profile_by_id(1)

        assert result == user_schemas.UserReponseSchema(
            id=1,
            first_name="John",
            last_name="Doe",
            linkedin_url=None,
            github_url=None,
            active=True,
        )

    def test_returns_none_when_not_found_and_raise_err_false(self, user_service):
        user_service.db.query.return_value.filter.return_value.one_or_none.return_value = (
            None
        )
        result = user_service.get_user_profile_by_id(999, raise_err=False)

        assert result is None


class TestUpdateUserProfile:

    def test_updates_first_and_last_name(self, user_service, mock_user_create):
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.update_user_profile(id=1, first_name="Jane", last_name="Smith")

        assert user_service.db.commit.called
        assert mock_user_create.first_name == "Jane"
        assert mock_user_create.last_name == "Smith"
        assert mock_user_create.updated_at == FIXED_DATETIME

    def test_updates_optional_urls(self, user_service, mock_user_create):
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.update_user_profile(
            id=1,
            linkedin_url="https://linkedin.com/in/jane",
            github_url="https://github.com/jane",
        )

        assert user_service.db.commit.called
        assert mock_user_create.linkedin_url == "https://linkedin.com/in/jane"
        assert mock_user_create.github_url == "https://github.com/jane"
        assert mock_user_create.updated_at == FIXED_DATETIME

    def test_raises_when_user_not_found(self, user_service):
        user_service.db.query.return_value.filter.return_value.one.side_effect = (
            Exception("NoResultFound")
        )
        with pytest.raises(Exception, match="NoResultFound"):
            user_service.update_user_profile(id=999, first_name="Jane")

    def test_raises_when_user_inactive(self, user_service, mock_user_create):
        mock_user_create.active = False
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        with pytest.raises(
            InactiveUserError, match="Cannot update an inactive user profile."
        ):
            user_service.update_user_profile(id=1, first_name="Jane")


class TestDeactivateUserProfile:

    def test_sets_active_to_false(self, user_service, mock_user_create):
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.deactivate_user(id=1)

        assert user_service.db.commit.called
        assert mock_user_create.active is False
        assert mock_user_create.updated_at == FIXED_DATETIME

    def test_raises_when_user_not_found(self, user_service):
        user_service.db.query.return_value.filter.return_value.one.side_effect = (
            Exception("NoResultFound")
        )
        with pytest.raises(Exception, match="NoResultFound"):
            user_service.deactivate_user(id=999)

    def test_is_idempotent_when_already_inactive(self, user_service, mock_user_create):
        local_fixed_datetime = datetime(2023, 1, 1, tzinfo=tz.utc)
        mock_user_create.active = False
        mock_user_create.updated_at = local_fixed_datetime
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.deactivate_user(id=1)

        assert not user_service.db.commit.called
        assert mock_user_create.active is False
        assert mock_user_create.updated_at == local_fixed_datetime


class TestReactivateUserProfile:

    def test_sets_active_to_true(self, user_service, mock_user_create):
        mock_user_create.active = False
        mock_user_create.updated_at = FIXED_DATETIME
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.reactivate_user(id=1)

        assert user_service.db.commit.called
        assert mock_user_create.active is True
        assert mock_user_create.updated_at == FIXED_DATETIME

    def test_set_active_to_true_already_active(self, user_service, mock_user_create):
        mock_user_create.active = True
        mock_user_create.updated_at = FIXED_DATETIME
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_user_create
        )
        user_service.reactivate_user(id=1)

        assert not user_service.db.commit.called
        assert mock_user_create.active is True
        assert mock_user_create.updated_at == FIXED_DATETIME

    def test_raises_when_user_not_found(self, user_service):
        user_service.db.query.return_value.filter.return_value.one.side_effect = (
            Exception("NoResultFound")
        )
        with pytest.raises(Exception, match="NoResultFound"):
            user_service.reactivate_user(id=999)
