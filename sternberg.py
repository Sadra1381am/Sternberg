import pygame
import random
import time
import statistics

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Display settings
WIDTH = 1400
HEIGHT = 800
FPS = 60

# Font settings
FONT_SIZE = 32
FONT_COLOR = BLACK

# Timing settings
DISPLAY_NUMBER_TIME = 4  # Display time for numbers (in seconds)
BLANK_TIME = 10  # Blank screen time (in seconds)
PROBE_DISPLAY_TIME = 4  # Display time for the probe (in seconds)
TASK_TIME = DISPLAY_NUMBER_TIME + BLANK_TIME + PROBE_DISPLAY_TIME  # Total time for each task (in seconds)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sternberg Short-Term Memory Task")
clock = pygame.time.Clock()

# Function to generate random numbers with varying digit lengths within specified ranges
def generate_number_set(length, digit_length):
    numbers = []
    for _ in range(length):
        if digit_length == 1:
            num = random.randint(0, 9)
        else:
            num = random.randint(10**(digit_length-1), 10**digit_length - 1)
        numbers.append(str(num))
    return numbers

# Function to display text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


# Function to simulate displaying a number set
def simulate_display_number_set(number_set):
    screen.fill(WHITE)
    num_count = len(number_set)
    for i, number in enumerate(number_set):
        x_offset = WIDTH // 2
        y_offset = (i * (HEIGHT // (num_count + 1))) + (HEIGHT // (2 * (num_count + 1)))
        draw_text(number, font, FONT_COLOR, x_offset, y_offset)
    pygame.display.flip()
    time.sleep(DISPLAY_NUMBER_TIME)


# Function to simulate displaying a blank screen
def simulate_display_blank():
    screen.fill(WHITE)
    pygame.display.flip()
    time.sleep(BLANK_TIME)  # Display blank screen for specified duration


# Function to simulate displaying a probe
def simulate_display_probe(probe):
    screen.fill(WHITE)
    draw_text(f"Probe: {probe}", font, FONT_COLOR, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    time.sleep(PROBE_DISPLAY_TIME)  # Display probe for specified duration


# Function to simulate handling user response
def simulate_handle_response(probe):
    response = None
    start_time = time.time()
    while response is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA:
                    response = ','
                elif event.key == pygame.K_PERIOD:
                    response = '.'
        # Check response time
        if time.time() - start_time <= 4:  # If response within 4 seconds
            response = ','  # Consider it incorrect
    return response



# Function to simulate the Sternberg Short-Term Memory Task
# Function to simulate the Sternberg Short-Term Memory Task
def simulate_sternberg_task(num_trials):
    correct_responses = 0
    incorrect_responses = 0
    response_times = []
    
    for current_trial in range(1, num_trials + 1):
        if current_trial <= 4:
            digit_length = 1  # Numbers between 1 to 9
        elif current_trial <= 8:
            digit_length = 2  # Numbers between 10 to 99
        elif current_trial <= 12:
            digit_length = 3  # Numbers between 100 to 999
        else:
            digit_length = 4  # Numbers between 1000 to 9999
        
        number_set_length = random.randint(5, 10)
        number_set = generate_number_set(number_set_length, digit_length)
        simulate_display_number_set(number_set)
        
        simulate_display_blank()
        
        probe = random.choice(number_set)
        simulate_display_probe(probe)
        
        start_time = time.time()
        response = simulate_handle_response(probe)
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)
        
        if (response == '.' and probe in number_set) or (response == ',' and probe not in number_set):
            correct_responses += 1
        else:
            incorrect_responses += 1

    return correct_responses, incorrect_responses, response_times

# Function to display final result
def simulate_display_result(correct_responses, incorrect_responses, response_times):
    screen.fill(WHITE)
    draw_text("Task Results", font, FONT_COLOR, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Correct: {correct_responses}", font, FONT_COLOR, WIDTH // 2, HEIGHT // 2)
    draw_text(f"Incorrect: {incorrect_responses}", font, FONT_COLOR, WIDTH // 2, HEIGHT // 2 + FONT_SIZE)
    
    accuracy_rate = (correct_responses / (correct_responses + incorrect_responses)) * 100
    draw_text(f"Accuracy Rate: {accuracy_rate:.2f}%", font, FONT_COLOR, WIDTH // 2, HEIGHT // 2 + 2 * FONT_SIZE)
    
    average_response_time = statistics.mean(response_times)
    draw_text(f"Average Response Time: {average_response_time:.2f} seconds", font, FONT_COLOR, WIDTH // 2, HEIGHT // 2 + 3 * FONT_SIZE)

    pygame.display.flip()
    time.sleep(20)  # Display results for 5 seconds

# Display instructions
screen.fill(WHITE)
rules_text = [
    "Welcome to the Sternberg Short-Term Memory Task!",
    "Instructions:",
    "1. Remember the numbers presented.",
    "2. Once the numbers are removed, indicate whether the single number presented was in the previous set.",
    "3. Use '.' to indicate Yes and ',' to indicate No.",
    "4. Respond as quickly and accurately as possible using only your right index finger.",
]

font_small = pygame.font.Font(None, 24)
for i, line in enumerate(rules_text):
    text = font_small.render(line, True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50 + i * 30))
pygame.display.update()
time.sleep(10)

# Main game loop
while True:  # Run indefinitely
    # Set font
    font = pygame.font.Font(None, FONT_SIZE)

    # Run the simulation with specified parameters
    num_trials = 12  # Number of trials to run
    correct_responses, incorrect_responses, response_times = simulate_sternberg_task(num_trials)

    # Display the final result
    simulate_display_result(correct_responses, incorrect_responses, response_times)

    # Keep the program running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
