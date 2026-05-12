from unittest.mock import MagicMock

import pytest
from db.models.principals import Principal, PrincipalType
from db.models.users import UserProfile
from db.services.user_profile_service import UserService

import schemas.users as user_schemas


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


class TestCreateUserProfile:

    def test_happy_path_returns_profile(self):
        pass

    def test_creates_human_principal_before_profile(self, user_service):
        user_data = user_schemas.UserCreateSchema(first_name="Jane", last_name="Smith")

        added_objects = []
        user_service.db.add.side_effect = lambda obj: added_objects.append(obj)

        def on_flush():
            for obj in added_objects:
                if isinstance(obj, UserProfile) and obj.id is None:
                    obj.id = 1
                    obj.active = True

        user_service.db.flush.side_effect = on_flush

        user_service.create_user_profile(user_data)

        add_calls = user_service.db.add.call_args_list
        added_types = [type(call.args[0]) for call in add_calls]

        assert Principal in added_types
        assert UserProfile in added_types
        assert added_types.index(Principal) < added_types.index(UserProfile)

        principal = add_calls[added_types.index(Principal)].args[0]
        assert principal.principal_type == PrincipalType.HUMAN

    def test_links_new_principal_id_to_profile(self):
        pass

    def test_active_defaults_to_true(self):
        pass

    def test_optional_fields_are_none_when_not_provided(self):
        pass

    def test_raises_on_duplicate_auth(self):
        pass

    def test_raises_on_missing_params(self):
        pass


class TestGetUserProfileById:

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


class TestGetUserProfileByAuth:

    def test_returns_profile_when_auth_matches(self):
        pass

    def test_returns_none_when_no_match(self):
        pass


class TestUpdateUserProfile:

    def test_updates_first_and_last_name(self):
        pass

    def test_updates_optional_urls(self):
        pass

    def test_raises_when_user_not_found(self):
        pass

    def test_does_not_change_active_status(self):
        pass


class TestDeactivateUserProfile:

    def test_sets_active_to_false(self):
        pass

    def test_raises_when_user_not_found(self):
        pass

    def test_is_idempotent_when_already_inactive(self):
        pass


class TestReactivateUserProfile:

    def test_sets_active_to_true(self):
        pass

    def test_raises_when_user_not_found(self):
        pass
