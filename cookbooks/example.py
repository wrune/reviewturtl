# example.py

# Importing necessary modules
import math
import json
import os

# Global variables
PI = math.pi

# Function definition
def calculate_area(radius):
    """Calculate the area of a circle given its radius."""
    if radius <= 0:
        raise ValueError("Radius must be positive")
    return PI * (radius ** 2)

# Class definition
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return calculate_area(self.radius)

    def circumference(self):
        return 2 * PI * self.radius

# Function demonstrating conditionals and loops
def print_circle_properties(circles):
    for circle in circles:
        if isinstance(circle, Circle):
            print(f"Circle with radius {circle.radius}:")
            print(f" - Area: {circle.area()}")
            print(f" - Circumference: {circle.circumference()}")
        else:
            print("Invalid circle object")

# List comprehensions
def generate_circles(count):
    return [Circle(radius) for radius in range(1, count + 1)]

# Exception handling
def safe_calculate_area(radius):
    try:
        return calculate_area(radius)
    except ValueError as e:
        print(f"Error: {e}")

# File I/O
def save_circles_to_file(circles, filename):
    with open(filename, 'w') as f:
        json.dump([circle.radius for circle in circles], f)

def load_circles_from_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            radii = json.load(f)
            return [Circle(radius) for radius in radii]
    return []

if __name__ == "__main__":
    # Generate circles
    circles = generate_circles(5)

    # Print properties
    print_circle_properties(circles)

    # Safe calculation
    safe_calculate_area(-3)

    # Save and load circles
    filename = "circles.json"
    save_circles_to_file(circles, filename)
    loaded_circles = load_circles_from_file(filename)

    print("\nLoaded circles from file:")
    print_circle_properties(loaded_circles)
