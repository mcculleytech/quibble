# Pong Game

A simple one-player pong game written in Python utilizing Pygame. You will play against the computer. This version includes an improved AI with reaction delays and randomized targeting.

## Requirements
- Python 3.x
- Pygame

## Setup and Installation

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

pip install pygame
```

## How to Run

Ensure your virtual environment is activated, then run:

```bash
python main.py
```

## Features
- One-player mode against an intelligent AI.
- Visual scoring system (compatible with environments where font modules may fail).
- Smooth paddle and ball physics.