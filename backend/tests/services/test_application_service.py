import pytest
from db.models.applications import Application, ApplicationStatus
from db.services.application_service import ApplicationService
from tests.services.conftest import FIXED_DATETIME
from tests.services.conftest import make_flush_handler as _make_flush_handler


@pytest.fixture
def application_service(get_mock_db):
    return ApplicationService(session=get_mock_db)


@pytest.fixture
def mock_application():
    return Application(
        id=1,
        user_id=10,
        job_post_id=20,
        status=ApplicationStatus.DRAFT,
        preference_level=None,
        current_location_id=None,
        applied_at=None,
        updated_at=FIXED_DATETIME,
        closed_at=None,
    )


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

        assert isinstance(result, Application)
        assert result.id == 1
        assert result.user_id == 1
        assert result.job_post_id == 2
        assert result.status == ApplicationStatus.DRAFT

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
        self, application_service, mock_application, assert_models_equal
    ):
        application_service.session.get.return_value = mock_application

        result = application_service.get_application_by_id(1)
        expected = Application(
            id=1,
            user_id=10,
            status=ApplicationStatus.DRAFT,
            preference_level=None,
            job_post_id=20,
            current_location_id=None,
            applied_at=None,
            updated_at=FIXED_DATETIME,
            closed_at=None,
        )
        assert_models_equal(result, expected)

    def test_returns_none_when_not_found_and_raise_err_false(
        self, application_service
    ):
        application_service.session.get.return_value = None

        result = application_service.get_application_by_id(999, raise_not_found=False)

        assert result is None

    def test_raises_when_not_found(self, application_service):
        application_service.session.get.return_value = None

        with pytest.raises(ValueError, match="not found"):
            application_service.get_application_by_id(999)

    def test_raises_when_deleted(self, application_service, mock_application):
        mock_application.deleted_at = FIXED_DATETIME
        application_service.session.get.return_value = mock_application

        with pytest.raises(ValueError, match="not found"):
            application_service.get_application_by_id(1)

    def test_returns_none_when_deleted_and_raise_err_false(
        self, application_service, mock_application
    ):
        mock_application.deleted_at = FIXED_DATETIME
        application_service.session.get.return_value = mock_application

        result = application_service.get_application_by_id(1, raise_not_found=False)

        assert result is None


class TestGetApplicationsForUser:

    def test_returns_applications_for_user(
        self, application_service, mock_application, assert_models_equal
    ):
        application_service.session.query.return_value.filter.return_value.filter.return_value.all.return_value = [
            mock_application
        ]

        result = application_service.get_applications_for_user(10)
        expected = [
            Application(
                id=1,
                user_id=10,
                status=ApplicationStatus.DRAFT,
                preference_level=None,
                job_post_id=20,
                current_location_id=None,
                applied_at=None,
                updated_at=FIXED_DATETIME,
                closed_at=None,
            )
        ]
        for res, exp in zip(result, expected, strict=True):
            assert_models_equal(res, exp)
        

    def test_returns_empty_list_when_no_applications(self, application_service):
        application_service.session.query.return_value.filter.return_value.filter.return_value.all.return_value = (
            []
        )

        result = application_service.get_applications_for_user(999)

        assert result == []


class TestDeleteApplication:

    def test_sets_deleted_at(self, application_service, mock_application):
        application_service.session.get.return_value = mock_application

        result = application_service.delete(1)

        assert result.deleted_at is not None
        assert result.is_deleted is True

    def test_commits_after_delete(self, application_service, mock_application):
        application_service.session.get.return_value = mock_application

        application_service.delete(1)

        application_service.session.commit.assert_called_once()

    def test_raises_when_not_found(self, application_service):
        application_service.session.get.return_value = None

        with pytest.raises(ValueError, match="not found"):
            application_service.delete(999)
