# playwright_api_automation

Python API Automation Framework with Playwright

To run all tests inside issues_test.feature file execute:

 ~~~
 pytest steps/test_issues_steps.py -v 
 ~~~

## Reporting

### Option 1. Pytest-html

Enable reporting by adding --html parameter where value is the path to the report.
Following command will generate basic html report on the report folder under project folder.
<br></br>More reference at: https://pytest-html.readthedocs.io/en/latest/user_guide.html#

 ~~~
pytest steps/test_issues_steps.py -v --html=report/report.html
 ~~~

### Option 2. pytest-json-report

Enable reporting by adding --json-report parameter. First command will generate report at
root folder with default report.json name. Otherwise, if need to specify a specific folder
and report name please use second command below.
<br></br>More reference at: https://pypi.org/project/pytest-json-report/

 ~~~
pytest steps/test_issues_steps.py -v --json-report
pytest steps/test_issues_steps.py -v --json-report-file=report/report.json --json-report
 ~~~

### Option 3. allure-pytest

Enable reporting by adding --json-report parameter. First command will generate report at
root folder with default report.json name. Otherwise, if need to specify a specific folder
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

## Parallelism

### Use pytest-xdist

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

## Logging

### Option 1. Enable on Console: Log request & response

To enable please add parameter -s to disable output capturing. Also, added v to show the Scenarios
with PASSED or FAIL on the console at the end of each of them.

 ~~~
pytest steps/test_issues_steps.py -v -s
 ~~~

### Option 2. Enable on Pytest-html or allure :

There's no need to add a special parameter just run with the usual param for reporting.

 ~~~
 pytest steps/test_issues_steps.py --html=report/report.html
 ~~~

 ~~~
pytest steps/test_issues_steps.py --alluredir=report/allure-results
allure serve report/allure-results
 ~~~


## How to validate schema of API Response

### Export file based on JSON API Response

In order to generate the Pydantic Schema class execute following command: 
~~~
 datamodel-codegen --input repo_response.json --input-file-type json --output data/schema/repository/repo_schema.py
~~~
Where --input param is a copy paste of API Response Body located on the root
of the project. Name of this input file can be anything (will be temporal) . 
Make sure a folder is created inside data/schema folder depending on the domain (repository).
--output parameter location of the output (or future exported file) 
that will contain the Pydantic Schema class. </br>
After executing the command  please open the output file generated
and rename class Model with an appropriate name. In this example,
main class was renamed from Model to RepoSchema. Once export is done please
delete temporal file from --input param.


### Use step for schema validation

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

