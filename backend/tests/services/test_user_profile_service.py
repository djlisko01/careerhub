import pytest
from unittest.mock import MagicMock
from services.user_profile import UserProfileService


@pytest.fixture
def mock_dao():
    return MagicMock()


@pytest.fixture
def user_profile_service(mock_dao):
    session = MagicMock()
    return UserProfileService(session, mock_dao)


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

    def test_returns_profile_when_found(self):
        pass

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
