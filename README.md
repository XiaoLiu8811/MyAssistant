# Anti-Sleep Assistant

A Python-based utility that simulates user activity to prevent system sleep by implementing natural mouse movements. The application features a user-friendly GUI for easy configuration and control.

## Features

- Natural mouse movement simulation with Bezier curves
- Configurable movement intervals and ranges
- User-friendly GUI interface
- System tray integration
- Windows startup integration option
- Low resource consumption

## Requirements

- Python 3.x
- Windows 10/11
- Required packages (installed automatically):
  - pyautogui
  - Pillow

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```
   .\venv\Scripts\activate
   ```
4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Activate the virtual environment (if not already activated):
   ```
   .\venv\Scripts\activate
   ```
2. Run the application:
   ```
   python main.py
   ```

## Configuration

### Movement Settings
- **Move Interval**: Set the time between mouse movements (5-15 seconds by default)
- **Move Range**: Set the maximum distance for mouse movements in pixels

### Application Settings
- **Start with Windows**: Enable/disable automatic startup with Windows
- **Minimize to System Tray**: Enable/disable system tray minimization

## Development

The application is built using:
- tkinter for GUI
- pyautogui for mouse control
- Bezier curves for natural movement simulation

## Performance

- CPU Usage: <1%
- Memory Usage: <50MB
- Response Time: <100ms

## Security

- No administrator privileges required
- No data collection
- No network communication

## License

MIT License

## Support

For issues and feature requests, please create an issue in the repository.