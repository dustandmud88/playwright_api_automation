@data:demo_play_003
Feature: Repository

  Background:
    Given Store value into request_context
      | demo_play_003 | GITHUB_REPO |

  Scenario: Verify repository exists
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}"
    When I send "GET" request
    Then status 200
      # TO DO: implement response body validation