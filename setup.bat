:: This file is used to create a virtual environment for the project and install the dependencies
:: It is recommended to use the venv module for this, but it is not always available

@echo off

:: Create a virtual environment if it doesn't already exist
if not exist venv (
    @echo Creating virtual environment...
    python -m venv venv
)

@echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
