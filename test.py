from datetime import datetime

# Define the given date and time
given_datetime = datetime(2023, 8, 31, 8, 37, 53)
# Get the current date and time
current_datetime = datetime.now()

# Calculate the time difference
time_difference = current_datetime - given_datetime

# Calculate the number of hours passed
hours_passed = time_difference.total_seconds() / 3600

# Display the result
print(f"Hours passed since {given_datetime}: {hours_passed:.2f} hours")
