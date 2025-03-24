from pathlib import Path
import pytest
from pytest_bdd import scenarios, parsers
from pytest_bdd.steps import given, when, then

from api.utils import load_json_payload

scenarios(Path(__file__).parent.parent/"features"/"issues_test.feature")
scenarios(Path(__file__).parent.parent/"features"/"repository_test.feature")


@pytest.fixture
def request_context():
    return {}


@given(parsers.parse('endpoint "{value}"'))
def set_endpoint(request_context, config, value):
    request_context["endpoint"] = value.format(**config.__dict__)


@when(parsers.parse('I send "{http_method}" request using payload "{payload_name}"'))
@when(parsers.parse('I send "{http_method}" request with body'))
@when(parsers.parse('I send "{http_method}" request'))
def send_post_request(request_context, api_client, http_method, datatable=None, payload_name=None):
    request_context["method"] = http_method
    temporal_body_dict = {}

    if datatable is not None:
        if len(datatable) != 2:
            raise ValueError(f"Expected 2 rows, but got {len(datatable)} rows.")
        for column in range(len(datatable[1:])):
            if datatable[0][column] not in temporal_body_dict:
                temporal_body_dict[datatable[0][column]] = datatable[1][column]

    if payload_name is not None:
        temporal_body_dict = load_json_payload(payload_name)

    request_context["body"] = temporal_body_dict
    request_context["response"] = api_client.make_request(
        method=request_context["method"],
        endpoint=request_context["endpoint"],
        payload=request_context["body"]
    )


@then(parsers.parse("status {response_code:d}"))
def verify_status_code(request_context, response_code):
    assert request_context['response'].status == response_code
