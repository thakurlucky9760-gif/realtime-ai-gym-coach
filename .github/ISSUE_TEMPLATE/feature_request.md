name: Feature Request
description: Suggest an idea or new exercise detector for AI Gym Coach
title: "[FEATURE]: "
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: We appreciate suggestions for new workouts, AI cues, or UI features!
  - type: textarea
    id: suggestion
    attributes:
      label: Feature Description
      description: A clear and concise description of the feature or new exercise.
    validations:
      required: true
  - type: textarea
    id: biomechanics
    attributes:
      label: Biomechanics & Angles (if proposing a new exercise)
      description: What joint angles and landmark IDs should be tracked?
      placeholder: e.g. Lateral Raises tracking shoulder abduction angle between torso and humerus (landmarks 11, 13, 23).
  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Add any mockups, screenshots, or reference literature.
