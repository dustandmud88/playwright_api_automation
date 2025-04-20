import json
import pytest
import pytest_check
from pathlib import Path
from pytest_bdd import scenarios, parsers
from pytest_bdd.steps import given, when, then, step
from api.utils import load_json_payload, load_json_header, extract_curly_vars, get_nested_response_value, \
    load_json_response

scenarios(Path(__file__).parent.parent / "features" / "issues_test.feature")
scenarios(Path(__file__).parent.parent / "features" / "repository_test.feature")
scenarios(Path(__file__).parent.parent / "features" / "branches_test.feature")


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


@step(parsers.parse('Store response value'))
def store_response_value(request_context, datatable=None):
    response_body = request_context['response']['body']
    if datatable and len(datatable[0]) == 2:
        for row in datatable:
            key = row[0]
            alias = row[1]
            request_context[f'{alias}'] = get_nested_response_value(response_body, key)
    else:
        raise ValueError('datatable of step not provided with at least one row with 2 columns')


@step('Store value into request_context')
def store_response_value(request_context, datatable=None):
    if datatable and len(datatable[0]) == 2:
        for row in datatable:
            value = row[0]
            alias = row[1]
            request_context[f'{alias}'] = value
    else:
        raise ValueError('datatable of step not provided with at least one row with 2 columns')


@then('response should contain')
def verify_status_code(request_context, datatable=None):
    def validate_table_headers(table):
        assert len(table) == 3, 'Datatable headers are not three'
        assert table[0] == 'field', f"Datatable first column is not 'field', but was '{table[0]}'"
        assert table[1] == 'action', f"Datatable second column is not 'action', but was '{table[1]}'"
        assert table[2] == 'value', f"Datatable third column is not 'value', but was '{table[2]}'"

    response_body = request_context['response']['body']
    table_headers = datatable[0]
    validate_table_headers(table_headers)
    action_expected_values = ["equals", "contains", "startswith", "endswith"]

    for row in datatable[1:]:
        field, action, expected_value = row[0], row[1], row[2]
        actual_value = get_nested_response_value(response_body, field)
        assert action in action_expected_values, f"Action '{action}' not in {action_expected_values}"

        if action == "equals":
            if type(actual_value) is dict:
                if expected_value.startswith("file:"):
                    file_name = expected_value.split(":", 1)[1]
                    expected_value = load_json_response(file_name)
                else:
                    expected_value = json.loads(expected_value)
            pytest_check.equal(expected_value, actual_value,
                               f"Expected {field} to be equal to {expected_value}, but actual value: {actual_value}")
        elif action == "contains":
            pytest_check.is_in(expected_value, actual_value,
                               f"Expected {field} to contain {expected_value}, but actual value: {actual_value}")
        elif action == "startswith":
            pytest_check.is_true(actual_value.startswith(expected_value),
                                 f"Expected {field} to startswith {expected_value}, but actual value: {actual_value}")
        elif action == "endswith":
            pytest_check.is_true(actual_value.endswith(expected_value),
                                 f"Expected {field} to endswith {expected_value}, but actual value: {actual_value}")
