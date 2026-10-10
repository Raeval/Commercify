# Project Description
This project is a mock-up e-commerce platform built with FastAPI for the backend and React for the frontend. The app demonstrates the core functionality of an online shopping platform.

# How to Run
## Backend
uvicorn main:app --reload

### env Setup
#### JWT Token
*On terminal write the following command:*
python -c "import secrets; print(secrets.token_hex(32))"

*Paste the output to the env file with the following format:*
JWT_SECRET_KEY={jwt_token}

### Testing Backend
cd backend
python3 -m pytest