#!/bin/bash

# Run Django tests

echo "Running Django tests..."
source venv/bin/activate
python manage.py test books

echo "Tests completed!"