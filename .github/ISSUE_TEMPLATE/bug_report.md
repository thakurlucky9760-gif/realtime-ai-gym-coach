name: Bug Report
description: File a bug report to help us improve the AI Gym Coach
title: "[BUG]: "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: Thanks for taking the time to fill out this bug report!
  - type: input
    id: exercise
    attributes:
      label: Affected Exercise
      description: Which exercise mode was active when the bug occurred?
      placeholder: e.g. Squats, Push-ups, Biceps Curls
    validations:
      required: true
  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
    validations:
      required: true
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce this behavior?
      placeholder: |
        1. Start application with 'streamlit run main.py'
        2. Select 'Squats' from sidebar
        3. Click 'Start Workout'
        4. See error...
    validations:
      required: true
  - type: textarea
    id: environment
    attributes:
      label: Environment Info
      description: OS, Python version, Browser, Camera type
      value: |
        - OS: Windows 11 / Linux / macOS
        - Python Version: 3.11.x
        - Browser: Chrome / Edge / Firefox
    validations:
      required: true
