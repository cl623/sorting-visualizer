import pygame
import random

pygame.font.init()

# --- CONSTANTS (The "Settings" for the simulation) ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BAR_WIDTH = 10
FPS = 60

# Colors (R, G, B)
COLOR_BACKGROUND = (30, 30, 30)   # Dark Grey (Modern IDE look)
COLOR_BAR_DEFAULT = (100, 200, 255) # Light Blue
COLOR_BAR_COMPARE = (255, 100, 100) # Red (Active comparison)
COLOR_BAR_SORTED = (100, 255, 100)  # Green (Final state)
COLOR_BAR_SWAP = (255, 255, 0) # Yellow (Active swap)
TEXT_COLOR = (255, 255, 255) # White
FONT = pygame.font.SysFont(None, 36)
text_surface = FONT.render("R = Reset, Space = Start/Pause", True, TEXT_COLOR)
text_rect = text_surface.get_rect()
text_rect.center = (SCREEN_WIDTH // 2, 10)

class SortingVisualizer:
    def __init__(self):
        """Initialize the visualization window and data."""
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sorting Algorithm Visualizer - Bubble Sort")
        self.clock = pygame.time.Clock()
        
        # Calculate how many bars fit on screen
        self.num_bars = SCREEN_WIDTH // BAR_WIDTH
        self.data = []
        self.reset_data()
        
        # Generator state
        self.sorting_algorithm = None
        self.is_sorting = False

    def reset_data(self):
        """Generates a new random list of heights."""
        # Create a list of random heights between 10 and SCREEN_HEIGHT - 10
        self.data = [random.randint(10, SCREEN_HEIGHT - 10) for _ in range(self.num_bars)]
        self.sorting_algorithm = None
        self.is_sorting = False

    def selection_sort_generator(self):
        """
        A Python Generator that yields control back to the main loop
        after every comparison. This allows us to visualize each step.
        """
        n = len(self.data)
        
        # Traverse through all array elements
        for i in range(n):
            # Find the minimum element in the unsorted part of the array
            min_index = i
            for j in range(i + 1, n):
                if self.data[j] < self.data[min_index]:
                    min_index = j
                
                # YIELD: Tell the main loop "I am currently looking at indices i and min_index"
                # This allows the visualizer to paint them RED before moving on.
                yield i, min_index
                
                # The actual sorting logic
                if self.data[i] > self.data[min_index]:
                    # Swap if the element found is greater than the next element
                    self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
                    
            # Optimization: The element at 'i' is now guaranteed to be sorted.
            # We could mark it as green here if we wanted to be fancy.

    def bubble_sort_generator(self):
        """
        A Python Generator that yields control back to the main loop
        after every comparison. This allows us to visualize each step.
        """
        n = len(self.data)
        
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                
                # YIELD: Tell the main loop "I am currently looking at indices j and j+1"
                # This allows the visualizer to paint them RED before moving on.
                yield j, j + 1
                
                # The actual sorting logic
                if self.data[j] > self.data[j + 1]:
                    # Swap if the element found is greater than the next element
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    
            # Optimization: The element at 'n-i-1' is now guaranteed to be sorted.
            # We could mark it as green here if we wanted to be fancy.

    def draw(self, active_indices=None):
        """
        Draws the current state of the list.
        active_indices: A tuple of (index1, index2) that are currently being compared.
        """
        self.window.fill(COLOR_BACKGROUND)

        for i, height in enumerate(self.data):
            # Default color
            color = COLOR_BAR_DEFAULT
            
            # If we are currently sorting and this bar is one of the ones being compared
            if active_indices and i in active_indices:
                color = COLOR_BAR_COMPARE
            

            # Draw the text
            self.window.blit(text_surface, text_rect)

            # Draw the bar
            # Rect arguments: (x, y, width, height)
            pygame.draw.rect(
                self.window, 
                color, 
                (i * BAR_WIDTH, SCREEN_HEIGHT - height, BAR_WIDTH - 1, height)
            )

        pygame.display.update()

    def run(self):
        """Main Game Loop."""
        running = True
        
        while running:
            # 1. Handle Events (Keyboard/Mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 'R' Key resets the array
                        self.reset_data()
                    elif event.key == pygame.K_1:
                        # '1' starts/pauses the sort
                        if not self.is_sorting:
                            self.is_sorting = True
                            self.sorting_algorithm = self.bubble_sort_generator()
                    elif event.key == pygame.K_2:
                        # '2' starts/pauses the sort
                        if not self.is_sorting:
                            self.is_sorting = True
                            self.sorting_algorithm = self.selection_sort_generator()
                    elif event.key == pygame.K_SPACE:
                        # 'Space' starts/pauses the sort
                        self.is_sorting = not self.is_sorting

            # 2. Update State (Step through the algorithm)
            active_indices = None
            
            if self.is_sorting and self.sorting_algorithm:
                try:
                    # Get the next comparison indices from the generator
                    active_indices = next(self.sorting_algorithm)
                except StopIteration:
                    # The generator is finished (list is sorted)
                    self.is_sorting = False
                    self.sorting_algorithm = None

            # 3. Draw
            self.draw(active_indices)
            
            # Cap the frame rate
            self.clock.tick(FPS)

        pygame.quit()

# Entry point
if __name__ == "__main__":
    visualizer = SortingVisualizer()
    visualizer.run()