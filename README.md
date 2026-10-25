# Car Dealership Inventory System

## 1. Project Overview

The Car Dealership Inventory System is a full-stack web application designed to manage a dealership's vehicle inventory. It allows users to register, log in, browse vehicles, search inventory, and purchase vehicles. Administrators have additional permissions to manage inventory and delete vehicles.

The application uses a React single-page frontend, a FastAPI REST API, and a persistent SQLite database.

## 2. Objectives

- Implement a RESTful API for vehicle inventory management.
- Provide user registration and login using JWT authentication.
- Store user and vehicle information in a persistent database.
- Support vehicle search, updates, purchases, and restocking.
- Provide a responsive user interface using React and Tailwind CSS.
- Apply version control and document the use of AI tools.

## 3. Technology Stack

**Frontend**
- React
- Vite
- HTML5 and CSS3
- Tailwind CSS

**Backend**
- Python
- FastAPI
- SQLAlchemy
- JWT authentication
- Argon2 password hashing

**Database**
- SQLite

**Testing**
- Pytest
- FastAPI TestClient / HTTPX

## 4. Main Features

- User registration and login.
- JWT-based authentication for protected endpoints.
- Add and list vehicles.
- Search vehicles by make, model, and category.
- Update vehicle details.
- Purchase vehicles and decrease stock quantities.
- Restock vehicles.
- Administrator-only vehicle deletion.
- Persistent data storage using SQLite.

Search by price range should be documented as supported only if it is implemented in the current backend.

## 5. Project Structure

```text
car-dealership/
├── backend/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── screenshots/
├── README.md
├── PROMPTS.md
├── TEST_REPORT.md
└── .gitignore
```

## 6. Prerequisites

- Python 3.10 or later
- Node.js and npm
- Git
- A modern web browser

## 7. Installation and Execution

### Backend setup

Open Command Prompt:

```cmd
cd %USERPROFILE%\car-dealership\backend
```

Create a virtual environment if one does not already exist:

```cmd
python -m venv .venv
```

Install dependencies:

```cmd
.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]" sqlalchemy pytest httpx "PyJWT[crypto]" "pwdlib[argon2]" email-validator
```

Configure secrets in the same terminal. Replace these example values with unique secrets:

```cmd
set JWT_SECRET_KEY=ReplaceWithYourOwnLongRandomSecret
set ADMIN_SETUP_KEY=ReplaceWithYourOwnAdminSetupKey
```

Start the API server:

```cmd
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

Keep the backend terminal open while using the frontend.

### Frontend setup

Open a second Command Prompt:

```cmd
cd %USERPROFILE%\car-dealership\frontend
npm install
npm run dev
```

Open the local URL printed in the terminal, usually:

http://localhost:5173

## 8. Authentication and Roles

Users can register and log in. Successful login returns a JWT access token, which is used to access protected endpoints.

Normal registration creates a regular user. The first administrator is created using the dedicated setup endpoint and its configured setup key.

Do not publish real passwords, JWT secrets, administrator setup keys, or database files containing sensitive information.

## 9. API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Health check |
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Log in |
| POST | `/api/auth/setup-admin` | Set up the first administrator |
| GET | `/api/vehicles` | List vehicles |
| GET | `/api/vehicles/search` | Search vehicles |
| POST | `/api/vehicles` | Add a vehicle |
| PUT | `/api/vehicles/{vehicle_id}` | Update a vehicle |
| DELETE | `/api/vehicles/{vehicle_id}` | Delete a vehicle; administrator only |
| POST | `/api/vehicles/{vehicle_id}/purchase` | Purchase a vehicle |
| POST | `/api/vehicles/{vehicle_id}/restock` | Restock inventory; administrator only |

Protected endpoints require valid authentication unless explicitly configured otherwise.

## 10. Screenshots

### Inventory Dashboard

(screenshots/inventory-dashboard.png)

### Login or Registration

(screenshots/login.png)

### Administrator Inventory Controls

(screenshots/admin-controls.png)


## 11. Testing

Automated tests are located in `backend/tests/`. The actual test execution results, including failures or tests not run, are recorded in `TEST_REPORT.md`.

The presence of test files does not imply that the test suite has passed.

## 12. My AI Usage

I used ChatGPT as an AI development assistant during the creation of this project.

AI assistance was used for:
- Understanding the project requirements and planning the implementation.
- Drafting and refining FastAPI backend code.
- Implementing authentication, password hashing, and JWT handling.
- Developing React frontend components and styling.
- Troubleshooting errors encountered during setup.
- Preparing project documentation and submission guidance.

AI assistance helped accelerate development and provided explanations of implementation choices. However, AI-generated suggestions can contain errors, so the code and behavior must be reviewed and verified before release. I remain responsible for understanding the project and explaining its implementation.

The root-level `PROMPTS.md` records the prompts and AI responses used during development, in accordance with the project instructions.

## 13. Limitations and Future Improvements

- Execute and improve automated test coverage.
- Verify all frontend and backend flows.
- Improve transaction handling for concurrent inventory purchases.
- Use production-grade secret management.
- Configure a production database and deployment environment.
- Add further security checks and audit logging.

## 14. Author

**Project:** Car Dealership Inventory System
