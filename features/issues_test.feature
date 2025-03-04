Feature: Issues

  Scenario: Create a bug report
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"
    When I send "POST" request with body
      | title               | body                |
      | [Feature] request 1 | Feature description |
    Then status 201
