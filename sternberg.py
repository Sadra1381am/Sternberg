import pygame
import random
import time
import statistics
import csv
import matplotlib.pyplot as plt

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
                if event.unicode == '.':
                    response = True
                elif event.unicode == ',':
                    response = False
        # Check response time
        if time.time() - start_time >= PROBE_DISPLAY_TIME:  # If response within probe display time
            response = False  # Consider it incorrect
    return response, time.time() - start_time

# Function to simulate the Sternberg Short-Term Memory Task
def simulate_sternberg_task(num_trials):
    correct_responses = 0
    incorrect_responses = 0
    response_times = []
    task_details = []
    
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
        
        response, response_time = simulate_handle_response(probe)
        response_times.append(response_time)
        
        if response == (probe in number_set):
            correct_responses += 1
        else:
            incorrect_responses += 1

        task_details.append((number_set, probe, response, probe in number_set))

    return correct_responses, incorrect_responses, response_times, task_details

# Function to calculate statistical features based on response times
def calculate_statistics(response_times):
    mean = statistics.mean(response_times)
    median = statistics.median(response_times)
    stdev = statistics.stdev(response_times)
    return mean, median, stdev

# Function to export the results to a CSV file and update it every time the program is run
def export_results_to_csv(correct_responses, incorrect_responses, response_times, task_details, filename='result.csv'):
    try:
        with open(filename, 'r') as csvfile:
            # Count the number of runs in the CSV file
            num_runs = sum(1 for line in csvfile if 'Index Task' in line)
    except FileNotFoundError:
        # If the file does not exist, initialize the run count to 0
        num_runs = 0

    index_run = num_runs + 1  # Increment the index run
    index_task = 1
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Index Run', 'Index Task', 'Shown Number', 'Probe Number', 'User Answer', 'Correct Answer', 'Accuracy Rate', 'Mean Response Time', 'Median Response Time', 'Standard Deviation']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()

        for i, (number_set, probe, response, correct) in enumerate(task_details):
            accuracy_rate = correct_responses / (correct_responses + incorrect_responses) * 100 if correct_responses + incorrect_responses > 0 else 0
            mean, median, stdev = calculate_statistics(response_times)
            writer.writerow({'Index Run': index_run,
                             'Index Task': index_task,
                             'Shown Number': number_set,
                             'Probe Number': probe,
                             'User Answer': response,
                             'Correct Answer': correct,
                             'Accuracy Rate': f'{accuracy_rate:.2f}%',
                             'Mean Response Time': mean,
                             'Median Response Time': median,
                             'Standard Deviation': stdev})
            index_task += 1

# Function to plot the data using matplotlib based on the CSV file
def plot_data(filename='result.csv'):
    data = {'Index Run': [], 'Index Task': [], 'Shown Number': [], 'Probe Number': [], 'User Answer': [], 'Correct Answer': [], 'Accuracy Rate': [], 'Mean Response Time': [], 'Median Response Time': [], 'Standard Deviation': []}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data['Index Run'].append(int(row['Index Run']))
            data['Index Task'].append(int(row['Index Task']))
            data['Shown Number'].append(row['Shown Number'])
            data['Probe Number'].append(row['Probe Number'])
            data['User Answer'].append(row['User Answer'])
            data['Correct Answer'].append(row['Correct Answer'])
            data['Accuracy Rate'].append(float(row['Accuracy Rate'].rstrip('%')))
            data['Mean Response Time'].append(float(row['Mean Response Time']))
            data['Median Response Time'].append(float(row['Median Response Time']))
            data['Standard Deviation'].append(float(row['Standard Deviation']))

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    for i in range(1, max(data['Index Run']) + 1):
        indices = [idx for idx, val in enumerate(data['Index Run']) if val == i]
        plt.plot([data['Index Task'][idx] for idx in indices], [data['Correct Answer'][idx] for idx in indices], label=f'Run {i} - Correct Answer')
        plt.plot([data['Index Task'][idx] for idx in indices], [data['User Answer'][idx] for idx in indices], label=f'Run {i} - User Answer')
    plt.xlabel('Index Task')
    plt.ylabel('Responses')
    plt.legend()

    plt.subplot(2, 1, 2)
    for i in range(1, max(data['Index Run']) + 1):
        indices = [idx for idx, val in enumerate(data['Index Run']) if val == i]
        plt.plot([data['Index Task'][idx] for idx in indices], [data['Mean Response Time'][idx] for idx in indices], label=f'Run {i} - Mean Response Time')
        plt.plot([data['Index Task'][idx] for idx in indices], [data['Median Response Time'][idx] for idx in indices], label=f'Run {i} - Median Response Time')
        plt.plot([data['Index Task'][idx] for idx in indices], [data['Standard Deviation'][idx] for idx in indices], label=f'Run {i} - Standard Deviation')
    plt.xlabel('Index Task')
    plt.ylabel('Time (seconds)')
    plt.legend()

    plt.tight_layout()
    plt.show()

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
# Set font
font = pygame.font.Font(None, FONT_SIZE)

# Run the simulation with specified parameters
num_trials = 12  # Number of trials to run
correct_responses, incorrect_responses, response_times, task_details = simulate_sternberg_task(num_trials)

# Calculate statistical features based on response times
mean, median, stdev = calculate_statistics(response_times)

# Export the results to a CSV file
export_results_to_csv(correct_responses, incorrect_responses, response_times, task_details)

# Display the final result
print(f"Correct: {correct_responses}, Incorrect: {incorrect_responses}")
print(f"Mean Response Time: {mean}, Median Response Time: {median}, Standard Deviation: {stdev}")

# Plot the data using matplotlib based on the CSV file
plot_data()

# Close Pygame and stop running
pygame.quit()
exit()
