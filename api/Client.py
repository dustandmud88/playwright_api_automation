import json
import allure

from json import JSONDecodeError
from playwright.sync_api import sync_playwright
from api.utils import load_json_header


class APIClient:
    INDENT = 4

    def __init__(self, config):
        self.base_url = config.BASE_URL

    def make_request(self, method, endpoint, headers=None, payload=None):
        with (sync_playwright() as p):
            if not headers:
                headers = load_json_header("common_headers.json")
            # Log request details
            print("\n***New Request***")
            print(f"Request: {method} {self.base_url}{endpoint}")
            print(f"Headers: {json.dumps(headers, indent=self.INDENT)}")
            if payload:
                print(f"Payload: {json.dumps(payload, indent=self.INDENT)}")
            # Attach request to Allure report
            with allure.step(f"API Request: {method} {self.base_url}{endpoint}"):
                # allure.attach(str(self.headers), name="Request Headers", attachment_type=allure.attachment_type.JSON)
                allure.attach(f"{json.dumps(headers, indent=self.INDENT, ensure_ascii=False)}",
                              name="Request Headers", attachment_type=allure.attachment_type.JSON)
                if payload:
                    # allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
                    allure.attach(f"{json.dumps(payload, indent=self.INDENT, ensure_ascii=False)}",
                                  name="Request Payload", attachment_type=allure.attachment_type.JSON)

            request_context = p.request.new_context(
                base_url=self.base_url,
                extra_http_headers=headers
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
            try:
                response_body = response.json()
            except json.decoder.JSONDecodeError:
                response_body = None

            print("***End of Request***\n")

            return {
                "status": response.status,
                "body": response_body,
                "raw": response
            }
