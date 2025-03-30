import json
from playwright.sync_api import sync_playwright
import allure


class APIClient:
    INDENT = 4

    def __init__(self, config):
        self.base_url = config.BASE_URL
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + config.GITHUB_API_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def make_request(self, method, endpoint, payload=None):
        with (sync_playwright() as p):
            # Log request details
            print("\n***New Request***")
            print(f"Request: {method} {self.base_url}{endpoint}")
            print(f"Headers: {json.dumps(self.headers, indent=self.INDENT)}")
            if payload:
                print(f"Payload: {json.dumps(payload, indent=self.INDENT)}")
            request_context = p.request.new_context(
                base_url=self.base_url,
                extra_http_headers=self.headers
            )

            response = request_context.fetch(endpoint, method=method, data=payload)
            # Log response details
            if response.text():
                print(f"Response [{response.status}]")
            else:
                print(f"Response [{response.status}]: {json.dumps(response.json(), indent=self.INDENT)}")
            print("***End of Request***\n")

            return response
