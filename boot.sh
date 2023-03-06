#!/bin/bash
source venv/bin/activate
flask db upgrade
venv/bin/python app.py
