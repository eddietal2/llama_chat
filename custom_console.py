"""
Custom Module for Console Log formats,
like Colors, Loading Indicators, etc

Something similar to https://rich.readthedocs.io/en/stable/introduction.html
"""
import sys
import time
import os

# ANSI escape codes for colors, etc, in print statements
COLOR_RED = "\033[91m"   # Bright Red
COLOR_GREEN = "\033[92m" # Bright Green
COLOR_YELLOW = "\033[93m" # Bright Yellow
COLOR_BLUE = "\033[94m"  # Bright Blue
COLOR_MAGENTA = "\033[95m"# Bright Magenta
COLOR_CYAN = "\033[96m"  # Bright Cyan
COLOR_WHITE = "\033[97m" # Bright White
RESET_COLOR = "\033[0m" # Reset to default color and formatting

def simple_spinner(duration=3):
    """
    Displays a Spinner Indicator that appears to animation over time.
    """
    spinner_chars = ['-', '\\', '|', '/'] # Characters for the spinner
    start_time = time.time()
    i = 0
    while time.time() - start_time < duration:
        sys.stdout.write(f'\r{COLOR_MAGENTA}Loading {spinner_chars[i % len(spinner_chars)]}')
        sys.stdout.flush()
        time.sleep(0.1) # Controls the speed of the spin
        i += 1
    sys.stdout.write(f'{COLOR_CYAN}\rLoading complete!') # Overwrite with final message and a newline
    sys.stdout.flush()
    print(f'{RESET_COLOR}')

# Clear console log
def clear_console():
    """Clears the console screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')






# Timers
"""
    Tracking the time taken for processes, e.i functions, to complete.
    This is useful for debugging and performance monitoring.
"""
from datetime import datetime

# Start timer
start_time = time.time()
def start_timer_process_timer():
    """
    Starts the timer and prints the start time.
    Normally used to start or initialize a program.
    """
    global start_time
    start_time = time.time()
    print(f"""
    {COLOR_RED}Llama Chat{RESET_COLOR} 
          
    |oooo|        |oooo|
    |oooo| .----. |oooo|
    |Oooo|/\_||_/\|oooO|
    `----' / __ \ `----'
    ,/ |#|/\/__\/\|#| \,
   /  \|#|| |/\| ||#|/  \\
  / \_/|_|| |/\| ||_|\_/ \\
 |_\/    o\=----=/o    \/_|
 <_>      |=\__/=|      <_>
 <_>      |------|      <_>
 | |   ___|======|___   | |
//\\\\  / |O|======|O| \  //\\\\
|  |  | |O+------+O| |  |  |
|\/|  \_+/        \+_/  |\/|
\__/  _|||        |||_  \__/
      | ||        || |
     [==|]        [|==]
     [===]        [===]
      >_<          >_<
     || ||        || ||
     || ||        || ||
     || ||        || ||    -- Art Created by Jay Thaler 
   __|\_/|__    __|\_/|__     (https://www.asciiart.eu/electronics/robots)
  /___n_n___\  /___n_n___\\
""")
    print(f"\n🚀 {COLOR_MAGENTA}~ Started @ ({datetime.now().strftime('%I:%M %p').lower()}){RESET_COLOR}\n")

# End timer
def process_timer_elapsed_time_success():
    """Returns the elapsed time since the start."""
    print(f"\n✅ {COLOR_GREEN}Completed in {time.time() - start_time:.2f} seconds{RESET_COLOR}\n")
    print(f"{COLOR_GREEN}██████████████████{RESET_COLOR}\n")
    print("""
                    | 
    ____________    __ -+-  ____________ 
    \_____     /   /_ \ |   \     _____/
     \_____    \____/  \____/    _____/
      \_____                    _____/
         \___________  ___________/
                   /____\\
    """)
    return time.time() - start_time
def process_timer_elapsed_time_failure():
    """Returns the elapsed time since the start."""
    print(f"\n❌ {COLOR_RED}Completed in {time.time() - start_time:.2f} seconds{RESET_COLOR}\n")
    print(f"{COLOR_RED}██████████████████{RESET_COLOR}\n")
    return time.time() - start_time