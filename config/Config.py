import json
import os


class Config:
    LIST_OF_ENVIRONMENTS = ['dev', 'qa']
    DICT_BASE_URLS = {
        "dev": "https://api.github.com",
        "qa": "https://api.github.qa.com"
    }
    SHARED_DATA_FILE = "shared_data.json"

    def __init__(self, env):
        self.env = env

        if self.env not in self.LIST_OF_ENVIRONMENTS:
            raise ValueError(f'env {self.env} variable not in {self.LIST_OF_ENVIRONMENTS}')

        if self.env == 'dev':
            self.GITHUB_API_TOKEN = os.getenv("GITHUB_DEV_API_TOKEN")
            self.GITHUB_USER = os.getenv("GITHUB_DEV_USER")
        elif self.env == 'qa':
            self.GITHUB_API_TOKEN = os.getenv("GITHUB_QA_API_TOKEN")
            self.GITHUB_USER = os.getenv("GITHUB_QA_USER")

        if self.GITHUB_API_TOKEN is None:
            raise ValueError(f'GITHUB_{env.upper()}_API_TOKEN is not set as environment variable')
        if self.GITHUB_USER is None:
            raise ValueError(f'GITHUB_{env.upper()}_USER is not set as environment variable')

        self.data_repositories = set()

    @property
    def BASE_URL(self):
        return self.DICT_BASE_URLS.get(self.env)

    def add_repo(self, repo_name):
        if not os.path.exists(self.SHARED_DATA_FILE):
            with open(self.SHARED_DATA_FILE, "w") as f:
                json.dump([], f)

        with open(self.SHARED_DATA_FILE, "r+") as f:
            data = json.load(f)
            data.append(repo_name)
            f.seek(0)
            json.dump(data, f)

    def get_repositories(self):
        collected_values = None
        try:
            with open(self.SHARED_DATA_FILE, "r+") as f:
                collected_values = json.load(f)
        except FileNotFoundError:
            print("Warning: shared_data.json not found. Using None.")
        except json.JSONDecodeError:
            print("Error: shared_data.json is invalid JSON. Using None.")

        return set(collected_values)
