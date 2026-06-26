from unittest.mock import MagicMock

import pytest
from db.models.applications import Application, ApplicationStatus
from db.services.application_service import ApplicationService
from tests.services.conftest import FIXED_DATETIME
from tests.services.conftest import make_flush_handler as _make_flush_handler

import schemas.applications as application_schemas


@pytest.fixture
def application_service(get_mock_db):
    return ApplicationService(session=get_mock_db)


@pytest.fixture
def mock_application():
    mock_application = MagicMock()
    mock_application.id = 1
    mock_application.user_id = 10
    mock_application.job_post_id = 20
    mock_application.status = ApplicationStatus.DRAFT
    mock_application.preference_level = None
    mock_application.current_location_id = None
    mock_application.applied_at = None
    mock_application.updated_at = FIXED_DATETIME
    mock_application.closed_at = None
    return mock_application


def make_flush_handler(added_objects, application_id=1):
    return _make_flush_handler(
        added_objects,
        {
            Application: {
                "id": application_id,
                "status": ApplicationStatus.DRAFT,
                "created_at": FIXED_DATETIME,
                "updated_at": FIXED_DATETIME,
            },
        },
    )


class TestCreateApplication:

    def test_happy_path_returns_application(self, application_service):
        added_objects = []
        application_service.session.add.side_effect = added_objects.append
        application_service.session.flush.side_effect = make_flush_handler(
            added_objects
        )

        result = application_service.create(user_id=1, job_post_id=2)

        assert isinstance(result, application_schemas.ApplicationResponseSchema)
        assert result.id == 1
        assert result.user_id == 1
        assert result.job_post_id == 2
        assert result.status == "draft"

    def test_defaults_to_no_preference_or_location(self, application_service):
        added_objects = []
        application_service.session.add.side_effect = added_objects.append
        application_service.session.flush.side_effect = make_flush_handler(
            added_objects
        )

        result = application_service.create(user_id=1, job_post_id=2)

        assert result.preference_level is None
        assert result.current_location_id is None

    def test_defaults_to_no_applied_at(self, application_service):
        added_objects = []
        application_service.session.add.side_effect = added_objects.append
        application_service.session.flush.side_effect = make_flush_handler(
            added_objects
        )

        result = application_service.create(user_id=1, job_post_id=2)

        assert result.applied_at is None

    def test_sets_preference_level_and_location(self, application_service):
        added_objects = []
        application_service.session.add.side_effect = added_objects.append
        application_service.session.flush.side_effect = make_flush_handler(
            added_objects
        )

        result = application_service.create(
            user_id=1,
            job_post_id=2,
            preference_level="high",
            current_location_id=5,
        )

        assert result.preference_level == "high"
        assert result.current_location_id == 5

    def test_adds_application_before_flush_and_commit(self, application_service):
        added_objects = []
        application_service.session.add.side_effect = added_objects.append
        application_service.session.flush.side_effect = make_flush_handler(
            added_objects
        )

        application_service.create(user_id=1, job_post_id=2)

        application_service.session.add.assert_called_once()
        added_application = application_service.session.add.call_args[0][0]
        assert isinstance(added_application, Application)
        assert added_application.user_id == 1
        assert added_application.job_post_id == 2

        application_service.session.flush.assert_called_once()
        application_service.session.commit.assert_called_once()


class TestGetApplicationById:

    def test_returns_application_when_found(
        self, application_service, mock_application
    ):
        application_service.session.query.return_value.filter.return_value.one.return_value = (
            mock_application
        )

        result = application_service.get_application_by_id(1)

        assert result == application_schemas.ApplicationResponseSchema(
            id=1,
            user_id=10,
            status="draft",
            preference_level=None,
            job_post_id=20,
            current_location_id=None,
            applied_at=None,
            updated_at=FIXED_DATETIME,
            closed_at=None,
        )

    def test_returns_none_when_not_found_and_raise_err_false(
        self, application_service
    ):
        application_service.session.query.return_value.filter.return_value.one_or_none.return_value = (
            None
        )

        result = application_service.get_application_by_id(999, raise_err=False)

        assert result is None

    def test_raises_when_not_found(self, application_service):
        application_service.session.query.return_value.filter.return_value.one.side_effect = (
            Exception("NoResultFound")
        )

        with pytest.raises(Exception, match="NoResultFound"):
            application_service.get_application_by_id(999)


class TestGetApplicationsForUser:

    def test_returns_applications_for_user(
        self, application_service, mock_application
    ):
        application_service.session.query.return_value.filter.return_value.all.return_value = [
            mock_application
        ]

        result = application_service.get_applications_for_user(10)

        assert result == [
            application_schemas.ApplicationResponseSchema(
                id=1,
                user_id=10,
                status="draft",
                preference_level=None,
                job_post_id=20,
                current_location_id=None,
                applied_at=None,
                updated_at=FIXED_DATETIME,
                closed_at=None,
            )
        ]

    def test_returns_empty_list_when_no_applications(self, application_service):
        application_service.session.query.return_value.filter.return_value.all.return_value = (
            []
        )

        result = application_service.get_applications_for_user(999)

        assert result == []
