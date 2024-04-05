#!/bin/bash

gunicorn "app:create_app()"
