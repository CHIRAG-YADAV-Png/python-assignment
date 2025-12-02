# simple_gradebook.py
# Simple GradeBook 
# Author: Chirag Satbir yadav
# Date: 2025-11-15
# Usage: run and choose manual entry or load a CSV like "students.csv"

import csv
import statistics
import sys

def average(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)

def median(scores):
    if not scores:
        return 0
    return statistics.median(scores)

def assign_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"

def manual_entry():
    students = {}
    print("Enter student names and marks.")
    print("Press ENTER on name to stop.")

    while True:
        name = input("Name: ").strip()
        if name == "":
            break   

        marks_input = input("Marks: ").strip()
        try:
            score = float(marks_input)
        except:
            print("Invalid marks! Please enter a number.")
            continue

        students[name] = score

    return students

def load_csv(path):
    students = {}
    try:
        with open(path, newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 2:
                    continue
                name = row[0].strip()
                try:
                    score = float(row[1])
                except:
                    continue
                students[name] = score
    except:
        print("Could not read the CSV file.")
    return students


def analyze(students):
    if not students:
        print("No data to analyze.")
        return

    scores = list(students.values())
    avg = average(scores)
    med = median(scores)

    highest = max(students, key=students.get)
    lowest = min(students, key=students.get)

    grades = {name: assign_grade(score) for name, score in students.items()}

    passed = [name for name, score in students.items() if score >= 40]
    failed = [name for name, score in students.items() if score < 40]

    print("\n--- RESULTS ---")
    print("Average:", avg)
    print("Median :", med)
    print("Highest:", highest, students[highest])
    print("Lowest :", lowest, students[lowest])
    print("Passed :", passed)
    print("Failed :", failed)

    print("\nName".ljust(20), "Marks".ljust(10), "Grade")
    print("-" * 40)
    for name, marks in students.items():
        print(name.ljust(20), str(marks).ljust(10), grades[name])
    print("-" * 40)

def main():
    print("Welcome to GradeBook Analyzer")
    while True:
        print("\n1) Manual Entry")
        print("2) Load CSV File")
        print("3) Exit")

        choice = input("Choose 1/2/3: ").strip()

        if choice == "1":
            data = manual_entry()
            analyze(data)

        elif choice == "2":
            filename = input("Enter CSV filename: ").strip()
            data = load_csv(filename)
            analyze(data)

        elif choice == "3":
            print("Goodbye!")
            sys.exit()

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()