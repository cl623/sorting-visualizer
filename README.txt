# Sorting Algorithm Visualizer

A Python tool that visualizes how sorting algorithms work in real-time. I built this to demonstrate $O(n^2)$ logic frame-by-frame, making it easier to trace comparisons and swaps than standard static diagrams.

## Why I Built This
In introductory CS courses, it's easy to understand the *concept* of a bubble sort, but harder to visualize exactly how it manipulates memory. Debuggers are great, but they don't give you the big picture of the algorithm's efficiency.

This tool is designed for the classroom. It slows down the execution so students can:
* **Watch** the "cursor" move through the array.
* **See** exactly when a comparison happens (Red) vs. when a swap happens.
* **Compare** the visual speed of different algorithms side-by-side.

## Technical Implementation: Python Generators
The biggest challenge with visualizing algorithms is keeping the UI responsive. A standard sorting function runs to completion instantly, which freezes the screen.

Instead of threading, I used **Python Generators (`yield`)**.

The sorting algorithm doesn't return a final list; it yields control back to the main loop after every single comparison. This allows the Pygame loop to draw one specific frame of the sort, handle user input, and then ask the algorithm for the "next step."

```python
# snippet from visualizer.py
def bubble_sort_generator(self):
    for i in range(n):
        for j in range(0, n - i - 1):
            # Pauses execution here to let the UI draw the red bars
            yield j, j + 1  
            
            if self.data[j] > self.data[j + 1]:
                self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]

```
## Setup & Usage
Dependencies
Python 3.8+

Pygame

Run Locally
Bash
```
git clone [https://github.com/YOUR_USERNAME/sorting-visualizer.git](https://github.com/YOUR_USERNAME/sorting-visualizer.git)
cd sorting-visualizer
pip install pygame
python visualizer.py
```

## Controls
SPACE: Start or Pause the sort.

R: Reset with new random data.

1: Bubble Sort.

2: Selection Sort.

## Future Improvements
Implement Merge Sort and Quicksort (requires refactoring the generator logic for recursion).

Add an "Operations Counter" to display real-time comparisons vs. swaps.

Christian Laggui Master's Candidate in AI I am focusing on Computer Science education and currently seeking full-time Lecturer roles. https://www.linkedin.com/in/christian-laggui/