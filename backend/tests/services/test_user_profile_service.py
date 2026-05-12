import pytest
from unittest.mock import MagicMock

from db.services.user_profile_service import UserService

import schemas.users as user_schemas


@pytest.fixture(autouse=True)
def user_service():
    session = MagicMock()
    return UserService(db=session)


class TestCreateUserProfile:

    def test_happy_path_returns_profile(self):
        pass

    def test_creates_human_principal_before_profile(self):
        pass

    def test_links_new_principal_id_to_profile(self):
        pass

    def test_active_defaults_to_true(self):
        pass

    def test_optional_fields_are_none_when_not_provided(self):
        pass

    def test_raises_on_duplicate_auth(self):
        pass

    def test_raises_on_missing_first_name(self):
        pass

    def test_raises_on_missing_last_name(self):
        pass


class TestGetUserProfileById:

    def test_returns_profile_when_found(self, user_service):
        mock_profile = MagicMock()
        mock_profile.id = 1
        mock_profile.first_name = "John"
        mock_profile.last_name = "Doe"
        mock_profile.linkedin_url = None
        mock_profile.github_url = None
        mock_profile.active = True
        user_service.db.query.return_value.filter.return_value.one.return_value = (
            mock_profile
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

    def test_raises_when_not_found(self):
        pass


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
