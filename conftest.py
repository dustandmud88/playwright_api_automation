import os
import shutil
import pytest
from os import getenv
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


@pytest.fixture(scope="session")
def temporal_delete(config):
    # TO BE DELETED - once pytest bug is fixed on delete_test_repositories
    # Delete JSON file with GitHub repositories
    if config.get_repositories():
        path_to_file = config.SHARED_DATA_FILE
        if os.path.exists(path_to_file):
            os.remove(path_to_file)

@pytest.fixture
def request_context():
    return {}


@pytest.fixture(scope="function", autouse=True)
def create_test_repository(api_client, config, request):
    data_tag = None
    for temp_marker in request.node.own_markers:
        marker = temp_marker.name
        if marker.startswith("data:"):
            data_tag = marker.split(":")[1].strip()
            config.add_repo(data_tag)
            break

    if not data_tag:
        raise ValueError("Feature file requires @data tag, but none was found")

    # create of a GitHub repository for each feature file
    # Check if the repository already exists
    check_repo = api_client.make_request(
        method="GET",
        endpoint=f"/repos/{config.GITHUB_USER}/{data_tag}"
    )
    if check_repo['status'] == 200:
        print(f"Repository {data_tag} already exists. Skipping creation.")
    else:
        # Before all
        new_repo = api_client.make_request(
            method="POST",
            endpoint="/user/repos",
            payload={"name": f'{data_tag}'}
        )
        assert new_repo['status'] == 201, \
            f"Failed to create repository. Status: {new_repo.status}, Response: {new_repo.text}"
        print(f"Repository {data_tag} created successfully.")


def pytest_configure():
    if os.path.isdir("report"):
        shutil.rmtree("report")
    os.makedirs("report", exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def delete_test_repositories(api_client, config):
    yield
    worker_id = getenv("PYTEST_XDIST_WORKER", "master")
    if worker_id == "master" and config.get_repositories():
        # Bug: https://github.com/pytest-dev/pytest-xdist/issues/1029
        # no worker master when running tests in parallel
        # https://pytest-xdist.readthedocs.io/en/latest/how-to.html#making-session-scoped-fixtures-execute-only-once
        for repo_name in config.get_repositories():
            deleted_repo = api_client.make_request(
                method="DELETE",
                endpoint=f"/repos/{config.GITHUB_USER}/{repo_name}"
            )
            if deleted_repo['status'] == 204:
                print(f"Repository {repo_name} deleted successfully.")
        # Delete JSON file with GitHub repositories
        if config.get_repositories():
            path_to_file = config.SHARED_DATA_FILE
            if os.path.exists(path_to_file):
                os.remove(path_to_file)
