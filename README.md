# Portfolio Webpage

This is the **backend service** for the fullstack portfolio project: **Chatbot Arelia**, developed with **FastAPI** and **PostgreSQL**. It powers a conversational AI chatbot with user authentication and message history storage.

> 📁 This repository is part of a professional portfolio and is actively maintained.

---
## 🌐 Deployment Links
See the finished [Production webpage](https://www.rrtportfolio.com)    

## 🔁 Branch Structure

The repository is organized into **three branches**, each serving a different purpose:

### `main`
- **Purpose:** Production-ready code.
- **Connected to:** Live Railway PostgreSQL database.
- **Deployment target:** Final stable version.
- **Tests:** Should pass all tests before merging.

---

### `qa-staging`
- **Purpose:** Quality Assurance & Testing (Staging).
- **Connected to:** A separate Railway PostgreSQL instance for staging.
- **Deployment target:** QA builds and integration tests.
- **Use case:** Check if new features or fixes work in a live-like environment before promoting them to `main`.

---

### `dev`
- **Purpose:** Development.
- **Connected to:** Local `.env` setup or a dev-specific Railway DB (optional).
- **Use case:** Feature development, testing in isolation, experimentation.

---

## 🧪 Testing Strategy

- Tests are written using **Pytest**.
- Separate `.env` files (`.env`, `.env.staging`, etc.) are used for different environments.
- Test suites are organized into:
  - `test_auth.py`: Authentication and token validation.
  - `test_user.py`: CRUD operations for user accounts.
  - `test_chat_flow.py`: Core chat interactions and history retrieval.

---

## 🚀 Deployment

This backend is deployed on **Railway**, and depending on the branch, it connects to the appropriate database and settings.

Each deployment is linked to its branch in GitHub:
- Changes to `main` update the production backend.
- Changes to `qa-staging` update the QA backend.
- Changes to `dev` remain local or in temporary environments.

---

## 🤖 API Features

- JWT-based Authentication (Login/Register/Delete)
- User email updates
- Secure chat endpoint using OpenAI integration
- Persistent message history
- Force-delete endpoint for QA cleanup

---

## 👨‍💻 Author

Developed by **Roberto Rivera** as part of a personal fullstack developer and QA portfolio.

---

Feel free to contribute or reach out if you’re reviewing this project for hiring or collaboration purposes.
