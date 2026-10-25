Test Report — Car Dealership Inventory System

1\. Overview

This report documents the automated backend tests executed for the Car Dealership Inventory System. The tests were run using Pytest from the project's backend directory.

2\. Test Environment

Item	Details

Operating system	Windows

Python	3.14.3

Test framework	Pytest 9.1.1

Test file	tests/test\_main.py

Backend framework	FastAPI

Database	SQLite (project configuration)





3\. Test Execution

Command used:

.venv\\Scripts\\python.exe -m pytest tests -v

Result from the supplied terminal screenshot:

\- Total tests collected: 15

\- Tests passed: 15

\- Tests failed: 0

\- Pass rate: 100%

\- Reported execution time: 5.04 seconds

\- Warnings: 1 deprecation warning

All 15 tests passed in the displayed test run. This report reflects the terminal output supplied for the project; the test suite has not been independently rerun while preparing this document.

4\. Test Cases Covered

The following test cases are visible in the supplied Pytest output.

No.	Test case	Purpose	Result

1	test\_health\_check	Checks that the health endpoint responds as expected.	PASSED

2	test\_create\_vehicle	Checks vehicle creation.	PASSED

3	test\_list\_vehicles	Checks retrieval/listing of vehicles.	PASSED

4	test\_search\_vehicles\_by\_make	Checks vehicle search by make.	PASSED

5	test\_search\_vehicles\_by\_price\_range	Checks vehicle search by price range.	PASSED

6	test\_update\_vehicle	Checks updating an existing vehicle.	PASSED

7	test\_delete\_vehicle	Checks deleting a vehicle.	PASSED

8	test\_purchase\_vehicle\_decreases\_quantity	Checks that purchasing reduces available quantity.	PASSED

9	test\_cannot\_purchase\_vehicle\_with\_zero\_stock	Checks that a vehicle with zero stock cannot be purchased.	PASSED

10	test\_restock\_vehicle	Checks restocking vehicle inventory.	PASSED

11	test\_register\_new\_user	Checks registration of a new user.	PASSED

12	test\_register\_duplicate\_email	Checks handling of duplicate email registration.	PASSED

13	test\_login\_with\_valid\_credentials	Checks login with valid credentials.	PASSED

14	test\_login\_with\_wrong\_password	Checks rejection of an incorrect password.	PASSED

15	test\_protected\_endpoint\_without\_token	Checks that a protected endpoint rejects a request without a token.	PASSED





5\. Warnings

Pytest reported one StarletteDeprecationWarning related to the test-client dependency and the use of httpx with starlette.testclient. The warning did not cause any tests to fail.



The warning can be reviewed during maintenance by checking the compatible versions and recommendations for the project's FastAPI, Starlette, and HTTPX dependencies. Do not change dependencies solely to remove the warning without confirming compatibility.



6\. Result and Limitations

The supplied test output shows that all 15 automated backend tests passed. This supports the conclusion that the specific behaviours covered by those tests worked as expected in that run.



7\. Conclusion

The recorded Pytest run completed with 15 passed, 0 failed, and 1 warning in 5.04 seconds. The results provide evidence of successful automated testing for the listed

