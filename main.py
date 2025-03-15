import tkinter as tk
from tkinter import ttk
import pyautogui
import random
import time
import math
from PIL import Image, ImageTk
import sys
import json
from pathlib import Path

# AntiSleepAssistant: Main application class that manages mouse movement simulation
# Features:
# - GUI interface for control and configuration
# - Natural mouse movement using Bezier curves
# - Configurable movement intervals and ranges
# - System tray and Windows startup integration
class AntiSleepAssistant:
    def __init__(self):
        # Initialize main window and default configuration
        self.root = tk.Tk()
        self.root.title("Anti-Sleep Assistant")
        self.root.geometry("300x400")
        
        # Default configuration settings
        self.config = {
            'move_interval': (5, 15),    # Random interval between moves (seconds)
            'move_range': (100, 100),     # Maximum movement range (pixels)
            'autostart': False,           # Auto start with Windows
            'minimize_to_tray': True      # Minimize to system tray when closing
        }
        
        self.is_running = False          # Service state flag
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Stopped")
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.toggle_button = ttk.Button(status_frame, text="Start", command=self.toggle_service)
        self.toggle_button.grid(row=0, column=1, padx=5)
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="5")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Interval settings
        ttk.Label(settings_frame, text="Move Interval (seconds):").grid(row=0, column=0, sticky=tk.W)
        self.interval_min = ttk.Entry(settings_frame, width=5)
        self.interval_min.insert(0, str(self.config['move_interval'][0]))
        self.interval_min.grid(row=0, column=1, padx=2)
        
        ttk.Label(settings_frame, text="to").grid(row=0, column=2)
        self.interval_max = ttk.Entry(settings_frame, width=5)
        self.interval_max.insert(0, str(self.config['move_interval'][1]))
        self.interval_max.grid(row=0, column=3, padx=2)
        
        # Movement range settings
        ttk.Label(settings_frame, text="Move Range (pixels):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.range_x = ttk.Entry(settings_frame, width=5)
        self.range_x.insert(0, str(self.config['move_range'][0]))
        self.range_x.grid(row=1, column=1, padx=2)
        
        ttk.Label(settings_frame, text="x").grid(row=1, column=2)
        self.range_y = ttk.Entry(settings_frame, width=5)
        self.range_y.insert(0, str(self.config['move_range'][1]))
        self.range_y.grid(row=1, column=3, padx=2)
        
        # Autostart option
        self.autostart_var = tk.BooleanVar(value=self.config['autostart'])
        ttk.Checkbutton(settings_frame, text="Start with Windows", 
                       variable=self.autostart_var).grid(row=2, column=0, 
                       columnspan=4, sticky=tk.W, pady=5)
        
        # Minimize to tray option
        self.minimize_var = tk.BooleanVar(value=self.config['minimize_to_tray'])
        ttk.Checkbutton(settings_frame, text="Minimize to System Tray", 
                       variable=self.minimize_var).grid(row=3, column=0, 
                       columnspan=4, sticky=tk.W)
        
    def toggle_service(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.toggle_button.config(text="Stop")
            self.status_label.config(text="Running")
            self.start_mouse_movement()
        else:
            self.toggle_button.config(text="Start")
            self.status_label.config(text="Stopped")
    
    def start_mouse_movement(self):
        # Main function for mouse movement simulation
        if not self.is_running:
            return
            
        # Get current mouse position as starting point
        current_x, current_y = pyautogui.position()
        
        # Calculate target position within configured range
        # Adds random offset to current position while respecting range limits
        target_x = current_x + random.randint(-self.config['move_range'][0], self.config['move_range'][0])
        target_y = current_y + random.randint(-self.config['move_range'][1], self.config['move_range'][1])
        
        # Ensure target position stays within screen boundaries
        screen_width, screen_height = pyautogui.size()
        target_x = max(0, min(target_x, screen_width))
        target_y = max(0, min(target_y, screen_height))
        
        # Generate smooth, natural-looking movement path
        points = self.generate_natural_movement(current_x, current_y, target_x, target_y)
        
        # Execute mouse movement along generated path
        for point in points:
            if not self.is_running:
                break
            pyautogui.moveTo(point[0], point[1], duration=0.1)
        
        # Schedule next movement with random interval
        interval = random.uniform(self.config['move_interval'][0], self.config['move_interval'][1])
        self.root.after(int(interval * 1000), self.start_mouse_movement)
    
    def generate_natural_movement(self, start_x, start_y, end_x, end_y):
        # Generates natural-looking mouse movement using quadratic Bezier curves
        # This creates smooth, human-like motion instead of straight lines
        points = []
        num_points = 10  # Number of points in the curve (affects smoothness)
        
        for i in range(num_points + 1):
            t = i / num_points
            # Add randomness to control points for more natural movement
            ctrl_x = (start_x + end_x) / 2 + random.randint(-20, 20)
            ctrl_y = (start_y + end_y) / 2 + random.randint(-20, 20)
            
            # Calculate points along quadratic Bezier curve
            # Formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            x = (1 - t) * ((1 - t) * start_x + t * ctrl_x) + t * ((1 - t) * ctrl_x + t * end_x)
            y = (1 - t) * ((1 - t) * start_y + t * ctrl_y) + t * ((1 - t) * ctrl_y + t * end_y)
            
            points.append((int(x), int(y)))
        
        return points
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AntiSleepAssistant()
    app.run()