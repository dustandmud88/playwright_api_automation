@data:demo_play_003
Feature: Repository

  Background:
    Given Store value into request_context
      | demo_play_003 | GITHUB_REPO |

  Scenario: Verify repository exists
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}"
    When I send "GET" request
    Then status 200
    And response should contain
      | field         | action     | value                                                                     |
      | $.name        | equals     | demo_play_003                                                             |
      | $.name        | startswith | demo_p                                                                    |
      | $.name        | endswith   | y_003                                                                     |
      | $.owner.login | contains   | dustandmud                                                                |
      | $.url         | equals     | https://api.github.com/repos/dustandmud88/demo_play_003                   |
      | $.permissions | equals     | {"admin": true,"maintain": true,"push": true,"triage": true,"pull": true} |
      | $.permissions | equals     | file:get_repository_permissions.json                                      |
