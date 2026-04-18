# Software Testing Project: Career Opportunity Management Web Application

## Course Context

- Course Assignment: Software Testing Project
- Instructor: Prof. Hyrmet Mydyti, PhD
- Academic Year: 2024/2025

## Project Objective

This project implements a Python web application for managing career opportunities and applies multiple software testing methodologies to validate its functionality. The system allows users to register, authenticate, create job postings, and apply for jobs through REST API endpoints, with a simple HTML frontend for the main pages.

The testing goal is to demonstrate:

- unit testing of isolated logic
- integration testing of API and database interaction
- system testing of complete user workflows
- REST API testing for correctness and error handling
- the use of mocks and patches to isolate dependencies

## Application Overview

The application is built with:

- FastAPI for the web framework and REST API
- SQLAlchemy for persistence
- SQLite for the database
- Pydantic for request and response validation
- Passlib and JWT-based authentication for login security

### Main Features

- user registration
- login and token generation
- job creation by authenticated users
- job listing
- job application by authenticated users
- HTML pages for home, signup, and signin

## Project Structure

```text
app/
  main.py
  database/__init__.py
  models/__init__.py
  routers/__init__.py
  schemas/__init__.py
  services/__init__.py
templates/
tests/
  conftest.py
  test_services.py
  test_integration.py
  test_system.py
pytest.ini
requirements.txt
```

## Test Plan

### Scope

The test plan covers four required levels:

1. Unit tests
2. Integration tests
3. System tests
4. REST API tests

The focus is correctness, error handling, and realistic workflow validation.

### Testing Tools and Frameworks

- `pytest`: primary test runner and assertion framework
- `fastapi.testclient.TestClient`: endpoint testing without running a separate server
- `unittest.mock.patch`: dependency isolation for unit tests
- `SQLAlchemy` test database overrides: integration and system testing with a separate SQLite database

### Strategy by Test Type

#### 1. Unit Tests

Unit tests target small service-layer functions in isolation:

- password hashing and verification
- JWT access token creation
- patched tests that isolate Passlib and JWT calls

These tests verify business logic independently from the API or database.

#### 2. Integration Tests

Integration tests validate collaboration between:

- FastAPI routes
- request validation
- SQLAlchemy persistence
- dependency overrides for the test database

Covered scenarios include:

- successful registration
- duplicate registration rejection
- empty jobs list retrieval
- invalid login handling
- invalid registration payload handling
- unauthorized job creation rejection
- missing-job application rejection
- invalid application payload rejection

#### 3. System Tests

The system test simulates a realistic end-to-end workflow:

1. employer registers and logs in
2. employer creates a job
3. applicant registers and logs in
4. applicant applies to the created job

The test verifies that authenticated identities are used correctly for both job ownership and application ownership.

#### 4. REST API Tests

REST API testing is represented across the integration and system test suite. The suite checks:

- successful responses
- expected status codes
- response structure
- validation failures
- authentication failures
- resource-not-found behavior

## Mocks and Patches

Mocks and patches are used in the unit test suite to isolate dependencies that should not need full cryptographic or token-generation behavior during wrapper testing.

Implemented examples:

- patching `app.services.pwd_context.hash` to verify hashing delegation
- patching `app.services.jwt.encode` to verify token creation delegation and payload generation

This improves isolation and demonstrates how external or library-backed behavior can be controlled in tests.

## Important Improvements Made for the Submission

To align the project more closely with the assignment requirements, the following improvements were added:

- authenticated users now own the jobs they create
- authenticated users are now recorded as the applicants when applying
- the application endpoint no longer requires duplicate `job_id` data in both the URL and the request body
- API test coverage was expanded to include invalid and unauthorized scenarios
- patched unit tests were added
- `pytest.ini` was added so pytest only collects tests from the `tests/` directory
- this README now serves as the written project report

## Test Cases Summary

### Unit Tests

- password hashing produces a non-plain-text result
- password verification accepts valid credentials
- password verification rejects invalid credentials
- hashing function delegates to Passlib when patched
- token generation returns an encoded token
- token creation delegates to JWT encoding when patched

### Integration and REST API Tests

- register user successfully
- reject duplicate registration
- return an empty jobs list when no jobs exist
- reject login with incorrect credentials
- reject invalid registration input with `422`
- reject unauthenticated job creation with `401`
- reject application to a missing job with `404`
- reject invalid application payload with `422`

### System Test

- complete employer and applicant workflow from registration through application submission

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the test suite:

```bash
pytest
```

Or explicitly:

```bash
py -3.13 -m pytest tests
```

Run the application:

```bash
py -3.13 -m uvicorn app.main:app --reload
```

## Expected Outcomes

The expected outcomes of this test suite are:

- core service functions behave correctly
- API endpoints return the correct responses for valid inputs
- invalid and unauthorized requests are rejected safely
- realistic user workflows operate across multiple components
- dependency isolation can be demonstrated through patch-based tests

## Challenges and Solutions

### Challenge 1: Hardcoded ownership weakened realism

Earlier behavior used hardcoded IDs for job creation and application submission. This made the workflow less realistic and reduced the value of end-to-end testing.

Solution:

- route handlers were updated to use the authenticated user from the token

### Challenge 2: Application endpoint required duplicate job identifiers

The original request schema required `job_id` in the body even though the endpoint already included `/jobs/{job_id}` in the URL.

Solution:

- the redundant body field was removed to make the API contract cleaner and easier to test

### Challenge 3: Missing mocks and patches

The original suite did not demonstrate dependency isolation.

Solution:

- patch-based unit tests were added for hashing and token generation

### Challenge 4: Pytest collection issue

The project contained a text artifact that could interfere with collection in some configurations.

Solution:

- `pytest.ini` was added to restrict test discovery to the `tests/` directory

## Documentation Quality and Organization

The project documentation is organized to match the assignment rubric:

- application objective
- tools and frameworks
- test strategy
- test categorization
- mocks and patches
- implementation improvements
- outcomes and challenges

## Conclusion

This submission now demonstrates the required testing categories for a Python career opportunity management web application. It includes unit, integration, system, and REST API testing, along with mock/patch usage and a written testing report. The project is structured to show both application functionality and a testing-focused engineering approach.
