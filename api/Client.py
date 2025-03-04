from playwright.sync_api import sync_playwright


class APIClient:
    def __init__(self, config):
        self.base_url = config.BASE_URL
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + config.GITHUB_API_TOKEN,
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def make_request(self, method, endpoint, payload=None):
        with sync_playwright() as p:
            request_context = p.request.new_context(
                base_url=self.base_url,
                extra_http_headers=self.headers
            )
            response = request_context.fetch(endpoint, method=method, data=payload)
            return response
