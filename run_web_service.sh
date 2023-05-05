#!/bin/bash
# This file will run when the web service starts
gunicorn ecommerce.wsgi:application --bind 0.0.0.0:8000 