# Django Blog Authentication System Documentation

## Overview
The authentication system provides user registration, login, logout, and profile management functionality.

## Features
- User Registration with email validation
- Secure login/logout
- Profile management
- CSRF protection
- Password hashing

## URLs
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - Profile management (requires login)

## Testing
1. Register a new user at `/register/`
2. Login with credentials at `/login/`
3. Update profile at `/profile/`
4. Logout at `/logout/`

## Security
- All forms include CSRF tokens
- Passwords are hashed using Django's PBKDF2
- Authentication required for protected views
- Email uniqueness validation