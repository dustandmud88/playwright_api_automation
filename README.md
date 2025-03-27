# playwright_api_automation
Python API Automation Framework with Playwright

To run all tests inside  issues_test.feature file execute:
 ~~~
 pytest steps/test_issues_steps.py -v 
 ~~~

## Reporting
### Option 1. Pytest-html
Enable reporting by adding --html parameter where value is the path to the report.
Following command will generate basic html report on the report folder under project folder.
 ~~~
pytest steps/test_issues_steps.py -v --html=report/report.html
 ~~~


## Parallelism
### Use pytest-xdist
In order to enable parallelism use -n parameter to indicate how many threads(workers) we desire.
Note: Possible bug. Be aware that after executing without the n and then using -n parameter 
the first time we execute may fail, but then it won't if we continue using the -n parameter.
 ~~~
pytest steps/test_issues_steps.py -v --html=report/report.html -n 3
 ~~~
