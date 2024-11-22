### Overview
Our team, consisting of four members — Kirill Krinkin, Iaroslav Chelombitko, Ilia Nechaev, and Kamaliia Alisheva — forms the AI Tests team. Our primary goal is to ensure that the generated code meets the necessary standards for usability and approval.

###  Problem Statement (technology perspective)
The problem we are to solve is to develop a system that will take as an input the directory with the code and tests it.

### Objectives
- Test the code in case of any unused entities in it
- Test the typing of the code
- Smoke test
- Functional tests based on project description
- Deployment
- Approval

### Features
- Unused Code Checks: We employ various established methods to verify whether the code contains unused elements and ensure adequate typing. For the code to progress, it must pass all tests without any failures or "errors." These tests are conducted using a combination of tools.
- Smoke test: we check that the code can be run without any errors and it runs on specific port.
- Deploy: after all test passed we deploy the code to the server.
- All checks and deployment are done via CI/CD pipeline on GitHub Actions.

### Timeline
- 18.11: Deliverables:
	- Task understanding
	- Base unused code checks
  	- Synthetic code (tests) generation
- 19.11: Deliverables:
	- Unused code checks
	- Smoke test
	- Deploy
- 20.11: Deliverables:
	- Functionl tests
- 21.11: Deliverables:
	- tbd
### Team
- Kirill Krinkin
- Ilia Nechaev
- Iaroslav Chelombitko
- Kamaliia Alisheva

### Risks and Mitigation Strategies

At least two!

| Risk   | Impact          | Probability     | Mitigation Strategy  |
| ------ | --------------- | --------------- | -------------------- |
| Insufficient user-case coverage | **High**/Medium/Low | High/**Medium**/Low | We will not only rely on the synthetic tests, but actuallywork with other teams to get the "real-code" to test; more strict tests overall |
| Github-actions limits | High/**Medium**/Low | High/**Medium**/Low | Set up all the actions that way to mitigate it. Actions run separation |
### Success Criteria
- Automatic GitHub Action run when the code is commited.
- Correctly returned exit codes for each keys
- End-to-end correct feedback sending

### Appendix

Before building image don't forget to create `.env` file and put there your `OPENAI_API_KEY`

**How to run**
```
docker build -t ai-tests .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v <PROJECT_DIR>:/project ai-tests
```
