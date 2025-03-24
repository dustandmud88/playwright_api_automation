Feature: Repository

    Scenario: Verify repository exists
      Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}"
      When I send "GET" request
      Then status 200
      # TO DO: implement response body validation