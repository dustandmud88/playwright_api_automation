@data:demo_play_001
Feature: Branches

  Background:
    Given Store value into request_context
      | demo_play_001 | GITHUB_REPO |

  @regression
  Scenario: List Branches
    Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/branches"
    When I send "GET" request
    Then status 200
    And response should contain
      | field | action | value                 |
      | $     | equals | file:no_branches.json |
