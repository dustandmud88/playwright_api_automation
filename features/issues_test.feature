Feature: Issues

  Scenario: Create a bug report with DataTable
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    When I send "POST" request with body
      | title          | body            |
      | [Bug] report 1 | Bug description |
    Then status 201

  Scenario: Create a bug report with external JSON file
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues" with headers "common_headers.json"
    When I send "POST" request using payload "bug_report_pay.json"
    Then status 201

  @smoke
  Scenario: Get bug report information
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    When I send "POST" request with body
      | title          | body              |
      | [Bug] report 3 | Bug description 3 |
    Then status 201
    And Store response value
      | number | issue_id |
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues/{issue_id}"
    When I send "GET" request
    Then status 200
