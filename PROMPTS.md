# PROMPTS.md — AI Assistance Used for the Car Dealership Inventory System

## Purpose

This file documents representative prompts that can be used to explain the AI-assisted workflow for developing the Car Dealership Inventory System. The prompts are organized by project phase, from understanding the requirements through implementation, testing, documentation, and submission preparation.

**Transparency note:** These are representative prompts reconstructed to describe the kinds of assistance relevant to this project. They are not claimed to be a verbatim transcript of every prompt used during development. If the submission rules specifically require raw, unedited chat logs or public links, include those original logs or links as additional evidence.

---

## 1. Understanding the Assignment and Planning the Project

**Representative prompt**

> Read the Car Dealership Inventory System assignment requirements and break them down into clear functional requirements, technical requirements, API endpoints, frontend features, testing expectations, and submission deliverables. Identify dependencies between tasks and suggest an implementation order. Do not claim a feature is implemented unless it is actually present in the code.

**Purpose:** To understand the assignment before implementation and create a checklist of the required backend, frontend, testing, and documentation work.

## 2. Choosing the Application Architecture and Project Structure

**Representative prompt**

> Help me organize a Car Dealership Inventory System with a FastAPI backend, SQLite database, and React frontend using Vite and Tailwind CSS. Suggest a simple maintainable folder structure, explain the responsibility of each file, and show how the frontend will communicate with the backend API. Keep the design appropriate for a student project.

**Purpose:** To plan the application structure and the responsibilities of its main components.

## 3. Setting Up the FastAPI Backend and Database

**Representative prompt**

> Guide me through setting up the FastAPI backend and SQLite database for the Car Dealership Inventory System. Explain the required Python packages, database connection, SQLAlchemy setup, application entry point, and how to run the server locally. Provide Windows Command Prompt commands where useful and explain how to verify that the server starts.

**Purpose:** To establish the backend development environment and persistent database connection.

## 4. Designing the Database Models and Validation Schemas

**Representative prompt**

> Help me define SQLAlchemy models and Pydantic schemas for users and vehicles in the Car Dealership Inventory System. Include the fields needed for user authentication, vehicle details, price, category, and available quantity. Explain the difference between database models and request/response schemas, and validate inputs appropriately.

**Purpose:** To structure stored data and validate data received from or returned to the API.

## 5. Implementing User Registration and Login

**Representative prompt**

> Help me implement user registration and login in FastAPI for this project. Store password hashes rather than plain-text passwords, validate registration data, handle duplicate email addresses, verify passwords during login, and return an authentication token on successful login. Explain the relevant code and how to test successful and unsuccessful login attempts.

**Purpose:** To implement account creation and authentication safely for the project.

## 6. Protecting API Endpoints and Handling Roles

**Representative prompt**

> Help me add JWT-based authentication to the FastAPI application. Explain how protected endpoints validate bearer tokens and how role-based authorization should restrict administrator-only actions. Show how to handle missing or invalid tokens and how to test access as an unauthenticated user, a regular user, and an administrator.

**Purpose:** To protect API operations and enforce permissions.

## 7. Implementing Vehicle Management APIs

**Representative prompt**

> Help me implement the vehicle API endpoints for creating, listing, searching, updating, and deleting vehicles. Use FastAPI and SQLAlchemy, validate incoming data, return suitable HTTP status codes, handle missing vehicle IDs, and ensure that delete and other administrator-only operations require the correct role. Explain each endpoint and provide examples for testing it in the FastAPI interactive documentation.

**Purpose:** To implement the core vehicle inventory operations required by the assignment.

## 8. Implementing Search and Filtering

**Representative prompt**

> Help me implement vehicle search in the FastAPI backend. Users should be able to search by supported fields such as make, model, category, and price range. Make optional filters work together, validate price bounds, and return predictable results when no vehicles match. Explain how to test each filter.

**Purpose:** To support searching and filtering the vehicle inventory.

## 9. Implementing Purchase and Restock Behaviour

**Representative prompt**

> Help me implement vehicle purchase and restock endpoints. A successful purchase should reduce the available quantity, and a vehicle with zero available stock must not be purchasable. Restocking should increase the quantity and be restricted to administrators. Validate quantities, handle invalid vehicle IDs, and explain how to test the inventory changes.

**Purpose:** To maintain correct inventory quantities and enforce the required business rules.

## 10. Writing Automated Tests Using Pytest

**Representative prompt**

> Help me write meaningful Pytest tests for the Car Dealership Inventory System backend. Cover the health endpoint, vehicle creation and listing, search by make and price range, update and delete, purchase quantity changes, purchase attempts with zero stock, restocking, registration, duplicate email, valid and invalid login, and access to protected endpoints without a token. Explain how to run the tests and interpret the results. Do not report a test as passing unless the test runner confirms it.

**Purpose:** To test the main backend behaviours and verify expected results.

## 11. Debugging Test Failures and Environment Issues

**Representative prompt**

> I will provide the exact error message and relevant code from my Car Dealership Inventory System. Help me identify the likely cause, explain the reasoning, and suggest the smallest appropriate fix. Do not guess that a fix worked; tell me how to rerun the affected test or command to verify it. Keep the solution compatible with my current Windows, Python, and project setup.

**Purpose:** To diagnose implementation and environment problems systematically without claiming unverified success.

## 12. Building the React Frontend

**Representative prompt**

> Help me build a React frontend using Vite and Tailwind CSS for the Car Dealership Inventory System. Include registration and login forms, an inventory dashboard, vehicle search and filters, and a clear display of vehicle details and available quantity. Include purchase controls and administrator-only controls for adding, updating, deleting, and restocking vehicles. Keep the UI usable and explain how to run the frontend locally.

**Purpose:** To provide the user interface for the required application features.

## 13. Connecting the Frontend to the Backend

**Representative prompt**

> Help me connect the React frontend to my FastAPI backend. Explain how to configure the API base URL, send registration and login requests, store and send the authentication token appropriately, handle API errors, refresh the displayed inventory after a change, and display useful loading and error messages. Check CORS configuration for local development and do not expose secret keys in frontend code.

**Purpose:** To integrate the interface with the backend APIs and authentication flow.

## 14. Verifying User and Administrator Workflows

**Representative prompt**

> Give me a manual verification checklist for the Car Dealership Inventory System. Include registration, login, viewing and searching inventory, purchasing an available vehicle, preventing a purchase when stock is zero, and administrator actions such as adding, updating, deleting, and restocking vehicles. Separate checks that I must perform in the browser from automated backend tests, and provide space to record actual outcomes.

**Purpose:** To check the end-to-end application and distinguish browser verification from automated API tests.

## 15. Preparing the README and Test Report

**Representative prompt**

> Help me prepare README.md and TEST_REPORT.md for my Car Dealership Inventory System submission. The README should explain the project, features, technologies, folder structure, setup, run commands, API endpoints, screenshots, testing, and AI usage. The test report should list the actual test command, environment, test cases, observed results, warnings, and limitations. Use only results I have provided or verified, and clearly mark anything that still needs to be filled in.

**Purpose:** To document how to set up and use the project and to report testing accurately.

## 16. Preparing the Git Repository and Final Submission

**Representative prompt**

> Help me prepare the Car Dealership Inventory System for submission to a public Git repository. Give me a checklist for organizing files, adding useful screenshots, checking README.md, PROMPTS.md, and TEST_REPORT.md, reviewing Git history, and excluding virtual environments, database files if they contain personal data, passwords, tokens, and local environment files. Explain how to check the repository before sharing it.

**Purpose:** To prepare a clean repository and reduce the risk of exposing secrets or unnecessary local files.

---

## 17. Test Run Evidence Referenced During Submission Preparation

The test output supplied during this conversation showed the command:

```text
.venv\Scripts\python.exe -m pytest tests -v
```

The displayed summary was:

```text
15 passed, 1 warning in 5.04s
```

The visible test names covered the health check; vehicle creation, listing, search, update, and deletion; purchase and zero-stock behaviour; restocking; user registration and duplicate email handling; login with valid and incorrect credentials; and access to a protected endpoint without a token.

This records the output shown in the supplied screenshots. It does not claim that the tests were independently rerun while preparing this file.

---

## 18. Final Notes

- The prompts above are **representative examples**, not a verbatim historical transcript.
- If the evaluator requires raw, unedited AI logs or public links, attach the actual conversation exports or share links as required by the assignment.
- Review public links before submission and ensure they do not expose passwords, JWT secrets, setup keys, access tokens, or other sensitive credentials.
- The project owner should review and understand the final code and be able to explain its design, implementation, and test results.
