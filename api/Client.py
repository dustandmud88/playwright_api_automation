import json
import logging
import os
from json import JSONDecodeError

import allure_commons
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
            # Attach request to Allure report
            with allure.step(f"API Request: {method} {self.base_url}{endpoint}"):
                # allure.attach(str(self.headers), name="Request Headers", attachment_type=allure.attachment_type.JSON)
                allure.attach(f"{json.dumps(self.headers, indent=self.INDENT, ensure_ascii=False)}",
                              name="Request Headers", attachment_type=allure.attachment_type.JSON)
                if payload:
                    # allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
                    allure.attach(f"{json.dumps(payload, indent=self.INDENT, ensure_ascii=False)}",
                                  name="Request Payload", attachment_type=allure.attachment_type.JSON)

            request_context = p.request.new_context(
                base_url=self.base_url,
                extra_http_headers=self.headers
            )
            response = request_context.fetch(endpoint, method=method, data=payload)
            # Log response details
            try:
                print(f"Response [{response.status}]: {json.dumps(response.json(), indent=self.INDENT)}")
            except JSONDecodeError:
                print(f"Response [{response.status}]")
            # Attach response to Allure report
            with allure.step(f"API Response: {method} {self.base_url}{endpoint}"):
                allure.attach(str(response.status), name="Response Status", attachment_type=allure.attachment_type.TEXT)
                if response.text():
                    allure.attach(f"{json.dumps(response.json(), indent=self.INDENT, ensure_ascii=False)}",
                                  name="Response Body", attachment_type=allure.attachment_type.JSON)
            print("***End of Request***\n")

            return response
