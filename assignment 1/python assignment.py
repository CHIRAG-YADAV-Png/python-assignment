## Name: CHIRAG SATBIR YADAV
# Date: 1 November 2025
# Project: Daily Calorie Tracker
# Roll No: 2501730067

import datetime

print("Welcome to the Daily Calorie Tracker!")
print("This program helps you check your total calorie intake each day.\n")

# Ask the user for their daily calorie limit
daily_limit = int(input("Enter your daily calorie limit: "))

# Ask how many meals to calculate
meal_count = int(input("How many meals would you like to calculate? "))

# Set up lists to store meal names and calories
meal_names = []
calorie_list = []

# Collect meal names and calorie values
for i in range(meal_count):
    meal_name = input("Enter meal name for meal #" + str(i+1) + ": ")
    meal_cal = int(input("Enter calories for " + meal_name + ": "))
    meal_names.append(meal_name)
    calorie_list.append(meal_cal)

# Calculate total and average calories
total_calories = sum(calorie_list)
average_calories = total_calories / meal_count

# Compare with daily limit and display warning if needed
if total_calories > daily_limit:
    print("\nWarning: You are consuming more calorie than your limit!")
else:
    print("\nGood job! You are consuming calorie within your daily calorie limit.")

# Print a neat summary 
print("\nCalorie Intake Summary:\n")
print("Meal Name\tCalories")
for j in range(meal_count):
    print(meal_names[j] + "\t" + str(calorie_list[j]))
print("-----------------------------")
print("Total:\t\t" + str(total_calories))
print("Average:\t" + "{:.2f}".format(average_calories))
print("Limit:\t\t" + str(daily_limit))

#  Ask to save session calculation
save_option = input("\nWould you like to save your session calclation to a file? (yes/no): ")

if save_option.lower() == "yes":
    now = datetime.datetime.now()
    filename = "calorie_log_" + ".txt"
    with open(filename, "w") as f:
        f.write("Daily Calorie Tracker Session\n")
        f.write("Date and Time: ")
        f.write("Daily Calorie Limit: " + str(daily_limit) + "\n")
        f.write("\nMeal Name\tCalories\n")
        for j in range(meal_count):
            f.write(meal_names[j] + "\t" + str(calorie_list[j]) + "\n")
        f.write("\nTotal: " + str(total_calories) + "\n")
        f.write("Average: " + "{:.2f}".format(average_calories) + "\n")
        if total_calories > daily_limit:
            f.write("Status: Exceeded the calorie limit!\n")
        else:
            f.write("Status: Within the calorie limit!\n")
    print("Session calculation saved as: " + filename)
else:
    print("Session calculation not saved.")

print("\nThank you for using the Daily Calorie Tracker!")