# PINK Air Painter

Cute Pixel Air Painter is an interactive hand gesture-controlled drawing application developed with Python and computer vision.

The application uses a webcam and real-time hand tracking to transform hand movements into digital drawings. Users can draw in the air, control the canvas, and interact with visual effects using simple hand gestures.

## Overview

The goal of this project is to create a fun and intuitive drawing experience without requiring a mouse or touchscreen.

Using MediaPipe Hands and OpenCV, the application detects hand landmarks, analyzes finger positions, and recognizes different gestures to perform specific actions.

## Features

- Real-time air drawing with hand movements
- Webcam-based hand tracking
- Index finger drawing system
- Open-hand gesture to clear the canvas
- Peace sign gesture to lock and unlock drawing
- Pinch gesture to move drawings
- Hand-controlled particle effects
- Smooth drawing experience
- Cute pastel-style graphical interface
- Interactive computer vision experience

## Technologies Used

- Python
- OpenCV
- MediaPipe Hands
- NumPy
- Tkinter
- Pillow

## Installation

### Clone the repository

```bash
git clone x gti repo x
```

### Move into the project directory

```bash
cd x repo x
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Start the application:

```bash
python air_painter.py
```

Make sure your webcam is connected and that Python has permission to access it.

## Gesture Controls

| Gesture | Action |
|---------|--------|
| Index finger extended | Draw on the canvas |
| Open hand | Clear the canvas |
| Peace sign | Lock or unlock drawing mode |
| Pinch gesture | Move the drawing |
| Middle finger gesture | Generate particle effects |

## How It Works

The application captures live video from the webcam and processes each frame using MediaPipe Hands.

The model detects hand landmarks and tracks important points such as fingertips and joints. The application analyzes distances and finger positions to identify gestures.

Each recognized gesture triggers a different interaction:

- Drawing follows the movement of the index finger
- Gestures modify the canvas state
- Hand movements create visual effects

This creates a natural human-computer interaction experience based on computer vision.

## Project Structure

```
cute-pixel-air-painter/
│
├── air_painter.py          # Main application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Ignored files
│
└── assets/                 # Images and resources
```

## Requirements

- Python 3.9 or higher
- Webcam
- Working internet connection for installing dependencies

## Future Improvements

- Add multiple brush colors
- Add brush size customization
- Save and load drawings
- Improve gesture recognition accuracy
- Add more particle effects
- Support multiple hands tracking
- Add more drawing tools
