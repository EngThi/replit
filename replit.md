# Overview

This is a Streamlit-based automation tool designed to automate Google AI Studio login using Playwright browser automation. The application provides a user-friendly interface for configuring and executing automated login processes, with built-in security features for handling credentials and 2FA authentication.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application framework
- **Interface Design**: Single-page application with sidebar configuration panel
- **Components**: 
  - Main form for credential input
  - Sidebar for browser configuration (headless mode, timeout settings)
  - Two-column layout for email/password fields
  - Real-time input validation

## Backend Architecture
- **Core Automation**: Object-oriented design with `GoogleAIStudioAutomation` class
- **Browser Management**: Playwright integration for Chromium browser control
- **Configuration**: Environment variable support for secure credential storage
- **Input Processing**: Utility functions for validation and sanitization

## Security Architecture
- **Credential Management**: Dual approach supporting environment variables and UI input
- **Input Sanitization**: HTML escaping and control character removal
- **Email Validation**: Regex-based email format verification
- **Browser Security**: Anti-detection measures with custom user agents and browser flags

## Browser Automation Design
- **Headless/Headful Modes**: Configurable browser visibility
- **Timeout Management**: Customizable 2FA waiting periods
- **Anti-Detection**: Custom browser arguments to avoid automation detection
- **Viewport Simulation**: Standard desktop resolution simulation

# External Dependencies

## Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Playwright**: Browser automation library for Chromium control
- **Python Standard Library**: `os`, `re`, `html`, `time` modules

## Browser Requirements
- **Chromium**: Primary browser engine via Playwright
- **Browser Extensions**: Disabled for automation compatibility

## Environment Integration
- **Replit Platform**: Designed for Replit deployment environment
- **Environment Variables**: `SEU_EMAIL` and `SUA_SENHA` for credential storage
- **Shell Commands**: Playwright installation via pip and playwright install

## Target Service
- **Google AI Studio**: Primary automation target (aistudio.google.com)
- **Google Authentication**: OAuth login flow with 2FA support