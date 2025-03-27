import pytest
from os import getenv
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
    # Check if the repository already exists
    check_repo = api_client.make_request(
        method="GET",
        endpoint=f"/repos/{config.GITHUB_USER}/{config.GITHUB_REPO}"
    )

    if check_repo.status == 200:
        print(f"Repository {config.GITHUB_REPO} already exists. Skipping creation.")
    else:
        # Before all
        new_repo = api_client.make_request(
            method="POST",
            endpoint="/user/repos",
            payload={"name": f'{config.GITHUB_REPO}'}
        )
        assert new_repo.status == 201, f"Failed to create repository. Status: {new_repo.status}, Response: {new_repo.text}"
        print(f"Repository {config.GITHUB_REPO} created successfully.")

    yield
    # After all
    worker_id = getenv("PYTEST_XDIST_WORKER", "master")
    if worker_id == "master":
        deleted_repo = api_client.make_request(
            method="DELETE",
            endpoint=f"/repos/{config.GITHUB_USER}/{config.GITHUB_REPO}"
        )
        assert deleted_repo.status == 204, f"Failed to delete repository. Status: {deleted_repo.status}"
        print(f"Repository {config.GITHUB_REPO} deleted successfully.")
