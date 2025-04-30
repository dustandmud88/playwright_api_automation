# ✈️ Playwright API Automation Framework

## 1. Overview

BDD Lightweight API Automation Framework based on:</br>
![Python](https://img.shields.io/badge/Python-3.13-blue)</br>
![Pytest](https://img.shields.io/badge/Pytest-8.3.4-blue)</br>
![Pytest-Playwright](https://img.shields.io/badge/Pytest_playwright-0.7.0-blue)</br>
![Pytest-BDD](https://img.shields.io/badge/Pytest_BDD-8.1.0-blue)</br>
![Pytest-xdist](https://img.shields.io/badge/Pytest_xdist-3.6.1-blue)</br>
![Pydantic](https://img.shields.io/badge/Pydantic-2.11.3-blue)</br>
![Jsonpath-ng](https://img.shields.io/badge/Jsonpath_ng-1.7.0-blue)</br>
![Pydantic](https://img.shields.io/badge/pytest_check-2.5.3-blue)</br>
![Pytest-html](https://img.shields.io/badge/Pytest_html-4.1.1-red)</br>
![Pytest-json-report](https://img.shields.io/badge/Pytest_json_report-1.5.0-red)</br>
![Pydantic](https://img.shields.io/badge/Allure_pytest-2.13.5-red)</br>

## 2. Installation instructions

### 2.1. Clone git repository

~~~
   git clone https://github.com/dustandmud88/playwright_api_automation.git
   cd playwright_api_automation
~~~

### 2.2. Install Python 3
In our example we'll be using version 3.13. If already installed please omit following command.
~~~
   brew install python@3.13
~~~
Once installed to make it easier to use pip and python instead of pip3 and python3.
Open terminal if bash word is visible execute first line if zsh then execute second one
~~~
   vim ~/.bashrc
   vim ~/.zshrc
~~~
Press i and paste following variables
~~~
   alias python='python3'
   alias pip='pip3'
~~~

To save file:
~~~
   Press ESC key
   Enter ':x' to save and exit vim editor
~~~
On terminal if bash word is visible execute first line if zsh then execute second one
~~~
   source ~/.bashrc
   source ~/.zshrc
~~~

### 2.3. Install PyCharm IDE

- Download and install IDE from : https://www.jetbrains.com/pycharm/download/
- Open IDE and project from playwright_api_automation folder that was cloned. 
- Make sure Python Interpreter is set by following steps:

~~~
   On Pycharm top menu-> Setting
   Project: -> Python Interpreter
   Add Interpreter
      Environment -> Generate new
         Type -> Virtualenv
         Base python -> 3.13
         Python path -> PATH_TO/playwright_api_automation/.venv
   Apply and OK
~~~

### 2.4. Install dependencies
Once Python interpreter is set for our project execute:
~~~
  pip install -r requirements.txt
~~~

Note: to check installed dependencies run

~~~
   pip list
~~~

## 3. Environment Setup

Set environment variables needed:</br>
Open terminal if bash word is visible execute first line if zsh then execute second one

~~~
   vim ~/.bash_profile
   vim ~/.zprofile
~~~

Press i and paste following variables

~~~
   export GITHUB_DEV_API_TOKEN=xxx
   export GITHUB_DEV_USER=xxx
~~~

- In this repository: https://github.com/dustandmud88/playwright_api_automation
  The GitHub User is 'dustandmud88'.
- Token can be generated from 'Personal Access Tokens' here: https://github.com/settings/tokens as a Tokens
  (classic). Grant this user admin rights ass we need to create and delete repositories.

To save file:

~~~
   Press ESC key
   Enter ':x' to save and exit vim editor
   Reboot computer as zprofile or bash_profile init al login once
~~~

# 4. How to run tests

## 4.1 Run all tests

 ~~~
    pytest -v 
 ~~~

## 4.2 Run tests by tag

After k parameter use the proper tag. All Scenarios with smoke tag will run.

 ~~~
    pytest -k smoke 
 ~~~

# 5. How to write a test

- Create a feature file in features folder (if it doesn't exists).
- Name the feature file according to the funcionality being tested.
- First line of feature file must include data tag. In this case repo demo_play_xxx is create on GitHub before feature
  file is created. This is to handle parallelism and manage data independently, so that each feature file has its own
  repository created by using data tag and then at the end of execution gets deleted.

~~~
   @data:demo_play_xxx
~~~

Tags used on feature files will be noted here below on this table as a convention:

| data tag      | feature file       |
|---------------|--------------------|
| demo_play_001 | branches.feature   |
| demo_play_002 | issues.feature     |
| demo_play_003 | repository.feature |

- On background following step must be used, so that data tag GitHub repository created is stored in GITHUB_REPO
  inside request_context in GITHUB_REPO variable.

~~~
   Background:
     Given Store value into request_context
       | demo_play_xxx | GITHUB_REPO |
~~~      

- Create Scenario with a name with corresponding tags if required.

~~~
   @smoke
   Scenario: Verify repository exists
~~~

- Given step to indicate which endpoint will be used. If no headers are provided by default common_headers.json
  are used for the first line. On second line, if desired an external json in data/headers folder could be used
  to provide more headers if needed.

~~~
   Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues"

   Given endpoint "/repos/{GITHUB_USER}/{GITHUB_REPO}/issues" with headers "common_headers.json"
~~~

- When step to indicate the HTTP method that will be used. First one does not provide a body. Second and third
  one provide a body for the request. Second example creates a JSON from the data table with key, value. And
  third example uses an external JSON file under data/payloads folder with name: 'bug_report_pay.json'

~~~
   When I send "GET" request
~~~

~~~
   When I send "POST" request with body
      | title          | body            |
      | [Bug] report 1 | Bug description |
   
   {
    "title": "[Bug] report 1",
    "body": "Bug description"
   }   
   
   When I send "POST" request using payload "bug_report_pay.json"   
~~~

- Then step to indicate the expected status response code.

~~~
   Then status 200

   Then status 201
~~~

- And step for verifying response body. These are all the supported combinations. $ is the root of JSON
response body that uses JSON Path format to indicate field. Action has three values: equals, startswith
and endswith and value contains the value of the field evaluated. In this case field value could be 
a inner JSON Object or an external JSON file (inside data/response folder) as in the last line. 

~~~
    And response contains
      | field         | action     | value                                                                     |
      | $.name        | equals     | demo_play_003                                                             |
      | $.name        | startswith | demo_p                                                                    |
      | $.name        | endswith   | y_003                                                                     |
      | $.owner.login | contains   | dustandmud                                                                |
      | $.url         | equals     | https://api.github.com/repos/dustandmud88/demo_play_003                   |
      | $.permissions | equals     | {"admin": true,"maintain": true,"push": true,"triage": true,"pull": true} |
      | $.permissions | equals     | file:get_repository_permissions.json                                      |
~~~

- About schema validation step please refer to section '9. How to validate schema of API Response'
  for more information.

~~~
   And response matches schema from "repository.repo_schema" file and "RepoSchema" class
~~~

## 6. Reporting

### 6.1. Pytest-html

Enable reporting by adding --html parameter where value is the path to the report.
Following command will generate basic html report on the report folder under project folder.
<br></br>More reference at: https://pytest-html.readthedocs.io/en/latest/user_guide.html#

~~~
   pytest steps/test_issues_steps.py -v --html=report/report.html
~~~

### 6.2. pytest-json-report

Enable reporting by adding --json-report parameter. First command will generate report at
root folder with default report.json name. Otherwise, if needed to specify a specific folder
and report name please use second command below.
<br></br>More reference at: https://pypi.org/project/pytest-json-report/

~~~
   pytest steps/test_issues_steps.py -v --json-report
   pytest steps/test_issues_steps.py -v --json-report-file=report/report.json --json-report
~~~

### 6.3. allure-pytest

Enable reporting by adding --json-report parameter. First command will generate report at
root folder with default report.json name. Otherwise, if needed to specify a specific folder
and report name please use second command below.
<br></br>More reference at: https://allurereport.org/docs/pytest/

~~~
    pytest steps/test_issues_steps.py -v --alluredir=report/allure-results
    allure generate report/allure-results -o report/allure-report --clean
    allure open report/allure-report
    
    or
    
    pytest steps/test_issues_steps.py -v --alluredir=report/allure-results
    allure serve report/allure-results
~~~

## 7. Parallelism

### 7.1. Use pytest-xdist

In order to enable parallelism use -n parameter to indicate how many threads(workers) we desire.
Note: Possible bug. Be aware that after executing without the n and then using -n parameter
the first time we execute may fail, but then it won't if we continue using the -n parameter.
<br></br>
If desire to use full CPU's could set n value as 'auto' if detection fails its set to 1.
<br></br> More reference at: https://pytest-xdist.readthedocs.io/en/stable/

~~~
   pytest steps/test_issues_steps.py -v --html=report/report.html -n 3
   pytest steps/test_issues_steps.py -v --html=report/report.html -n auto
~~~

## 8. Logging

### 8.1. Enable on Console: Log request & response

To enable please add parameter -s to disable output capturing. Also, added v to show the Scenarios
with PASSED or FAIL on the console at the end of each of them.

~~~
   pytest steps/test_issues_steps.py -v -s
~~~

### 8.2. Enable on Pytest-html or allure :

There's no need to add a special parameter just run with the usual param for reporting.

~~~
   pytest steps/test_issues_steps.py --html=report/report.html
~~~

~~~
   pytest steps/test_issues_steps.py --alluredir=report/allure-results
   allure serve report/allure-results
~~~

## 9. How to validate schema of API Response

### 9.1. Export file based on JSON API Response

In order to generate the Pydantic Schema class execute following command:

~~~
   datamodel-codegen --input repo_response.json --input-file-type json --output data/schema/repository/repo_schema.py
~~~

Where --input param is a copy and paste of API Response Body located on the root
of the project. Name of this input file can be anything (will be temporal) .
Make sure a folder is created inside data/schema folder depending on the domain (repository).
--output parameter location of the output (or future exported file)
that will contain the Pydantic Schema class. </br>
After executing the command please open the output file generated
and rename class Model with an appropriate name. In this example,
main class was renamed from Model to RepoSchema. Once export is done please
delete temporal file from --input param.

### 9.2. Use step for schema validation

A proper example is located on 'repository_test.feature' file and Scenario
'Verify repository exists' on step:

~~~
   And response matches schema from "repository.repo_schema" file and "RepoSchema" class
~~~

In this example repo_schema is the file that contains schema class or
if response has inner JSON objects then will contain more classes one per
each one of them. In example step, first param is the relative location of
schema class inside schema folder with dot format (data/schema/repository/repo_schema.py)
and second parameter name of the file exported that contains the Pydantic
schema class are provided.</br></br>
As a result, this step validates if API Response JSON body complies with schema provided. 

