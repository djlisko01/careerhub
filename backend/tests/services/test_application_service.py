import pytest
from db.models.applications import Application, ApplicationStatus
from db.services.application_service import ApplicationService
from tests.services.conftest import FIXED_DATETIME
from tests.services.conftest import make_flush_handler as _make_flush_handler

import schemas.applications as application_schemas


@pytest.fixture
def application_service(get_mock_db):
    return ApplicationService(session=get_mock_db)


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
