# Cracking-tools
  
**WARNING:** This tool is provided for **authorized security testing and educational purposes only**.  
Unauthorized use against systems you do not own or have explicit permission to test is **illegal** and violates GitHub’s Terms of Service. The author assumes no liability for misuse.

## Overview
AuthCracker-LogSim simulates a simple login system (e.g., a dummy API or local script) and demonstrates how an attacker could attempt to guess valid username/password pairs using wordlists. It is designed to help developers, pentesters, and students understand:
- The importance of strong password policies
- Account lockout mechanisms
- Rate limiting and CAPTCHA
- Logging and monitoring failed login attempts

## Features
- Dictionary attack simulation against a mock login endpoint
- Multi‑threaded (configurable) testing with delay to avoid overloading
- Customizable wordlists (usernames / passwords)
- Reports found credentials to a log file
- Built‑in safe mode (forces a minimum delay between attempts)

## Requirements
- Python 3.8+
- No external dependencies (uses `requests` if testing HTTP, else pure Python)

## Installation
```bash
