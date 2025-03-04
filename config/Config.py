import os


class Config:
    LIST_OF_ENVIRONMENTS = ['dev', 'qa']
    DICT_BASE_URLS = {
        "dev": "https://api.github.com",
        "qa": "https://api.github.qa.com"
    }

    def __init__(self, env):
        self.env = env

        if self.env not in self.LIST_OF_ENVIRONMENTS:
            raise ValueError(f'env {self.env} variable not in {self.LIST_OF_ENVIRONMENTS}')

        if self.env == 'dev':
            self.GITHUB_API_TOKEN = os.getenv("GITHUB_DEV_API_TOKEN")
        elif self.env == 'qa':
            self.GITHUB_API_TOKEN = os.getenv("GITHUB_QA_API_TOKEN")

        if self.GITHUB_API_TOKEN is None:
            raise ValueError('GITHUB_API_TOKEN is not set as environment variable')

        self.GITHUB_USER = os.getenv("GITHUB_USER")
        if self.GITHUB_USER is None:
            raise ValueError('GITHUB_USER is not set as environment variable')

        self.GITHUB_REPO = os.getenv("GITHUB_REPO")
        if self.GITHUB_REPO is None:
            raise ValueError('GITHUB_REPO is not set as environment variable')

    @property
    def BASE_URL(self):
        return self.DICT_BASE_URLS.get(self.env)
