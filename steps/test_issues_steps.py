import pytest

from pathlib import Path
from pytest_bdd import scenarios, parsers
from pytest_bdd.steps import given, when, then, step
from api.utils import load_json_payload, load_json_header, extract_curly_vars


scenarios(Path(__file__).parent.parent / "features" / "issues_test.feature")
scenarios(Path(__file__).parent.parent / "features" / "repository_test.feature")


@pytest.fixture
def request_context():
    return {}


@given(parsers.parse('endpoint "{value}"'))
@given(parsers.parse('endpoint "{value}" with headers "{headers_name}"'))
def set_endpoint(request_context, config, value, headers_name=None):

    dict_env_vars = vars(config)
    list_vars = extract_curly_vars(value)
    for var in list_vars:
        if var in dict_env_vars.keys():
            value = value.replace(f'{{{var}}}', str(dict_env_vars.get(var)))
        elif var in request_context.keys():
            value = value.replace(f'{{{var}}}', str(request_context.get(var)))
        else:
            raise ValueError(f'Variable {var} on endpoint is not an Environment or request_context variable.')

    request_context["endpoint"] = value
    if headers_name:
        request_context["headers"] = load_json_header(headers_name)


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
    if "headers" not in request_context.keys():
        request_context["response"] = api_client.make_request(
            method=request_context["method"],
            endpoint=request_context["endpoint"],
            payload=request_context["body"]
        )
    else:
        request_context["response"] = api_client.make_request(
            method=request_context["method"],
            endpoint=request_context["endpoint"],
            headers=request_context["headers"],
            payload=request_context["body"]
        )


@then(parsers.parse('status {response_code:d}'))
def verify_status_code(request_context, response_code):
    assert request_context['response']['status'] == response_code


@step(parsers.parse('Store response value "{key}" as "{alias}"'))
def store_response_value(request_context, key, alias):
    response_body = request_context['response']['body']
    request_context[f'{alias}'] = response_body[f'{key}']
