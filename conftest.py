import pytest
from typing import Generator

from api.Client import APIClient
from config.Config import Config


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against (dev or qa)",
    )


@pytest.fixture(scope="session")
def api_client(config):
    return APIClient(config)


@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def config(env):
    return Config(env)


@pytest.fixture
def request_context():
    return {}


@pytest.fixture(scope="session", autouse=True)
def create_test_repository(api_client, config
                           ) -> Generator[None, None, None]:
    # Before all
    new_repo = api_client.make_request(
        method="POST",
        endpoint="/user/repos",
        payload={"name": config.GITHUB_REPO}
    )
    assert new_repo.status == 201
    yield
    # After all
    deleted_repo = api_client.make_request(
        method="DELETE",
        endpoint="/repos/" + config.GITHUB_USER + "/" + config.GITHUB_REPO
    )
    assert deleted_repo.status == 204
