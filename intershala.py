import pandas as pd
import matplotlib.pyplot as plt
import time

# Load your CSV file
df = pd.read_csv("quiz_questions.csv")

# Function to display a horizontal bar chart
def show_horizontal_bar_chart(difficulty_correct):
    labels = list(difficulty_correct.keys())
    values = list(difficulty_correct.values())
    colors = ["#8dd3c7", "#ffffb3", "#bebada"]

    plt.figure(figsize=(8, 6))
    plt.barh(labels, values, color=colors)
    plt.title("Correct Answers by Difficulty Level")
    plt.xlabel("Number of Correct Answers")
    plt.ylabel("Difficulty Level")
    plt.show()

# Function to display the quiz report
def display_report(correct_count, difficulty_correct):
    print("\nQuiz Report:")
    print(f"Total Correct Answers: {correct_count}")
    print("Correct Answers by Difficulty:")
    for difficulty, count in difficulty_correct.items():
        print(f"  {difficulty.capitalize()}: {count}")
    # Show the horizontal bar chart
    show_horizontal_bar_chart(difficulty_correct)

# Function to display the quiz instructions
def show_instructions():
    print("\nQuiz Instructions:")
    print("1. The quiz consists of multiple-choice questions.")
    print("2. Each question has four options (A, B, C, D).")
    print("3. For each question, enter the letter corresponding to your chosen answer.")
    print("4. You can stop the quiz at any time by selecting the 'Stop Quiz' option.")
    print("5. You have 128 minutes to complete the quiz.")
    print("6. If you run out of time, the quiz will end automatically.")
    print("7. After finishing the quiz, you will receive a report with your performance.")
    print("8. Good luck, and enjoy the quiz!\n")

# Function to conduct the quiz
def conduct_quiz(df, total_time):
    correct_count = 0
    difficulty_correct = {"easy": 0, "medium": 0, "hard": 0}
    question_map = {0: "A", 1: "B", 2: "C", 3: "D"}

    # Group the questions by question_id
    grouped = df.groupby("question_id")
    question_ids = list(grouped.groups.keys())
    total_questions = len(question_ids)

    start_time = time.time()  # Record start time

    for index, question_id in enumerate(question_ids):
        # Check remaining time
        elapsed_time = time.time() - start_time
        remaining_time = total_time - elapsed_time
        if remaining_time <= 0:
            print("\nTime's up!")
            break

        # Display the time remaining
        remaining_minutes = int(remaining_time // 60)
        remaining_seconds = int(remaining_time % 60)
        print(f"Time remaining: {remaining_minutes:02}:{remaining_seconds:02}")

        group = grouped.get_group(question_id)

        # Display the question
        print(f"\nQuestion {index + 1}/{total_questions}: {group.iloc[0]['description']}")
        
        # Display the options
        options = group[["option_description"]].reset_index(drop=True)
        for idx, row in options.iterrows():
            print(f"{question_map[idx]}: {row['option_description']}")

        # Get user input
        while True:
            answer = input("Enter the letter of your answer (A, B, C, D): ").strip().upper()
            if answer in question_map.values():
                answer_idx = list(question_map.keys())[list(question_map.values()).index(answer)]
                break
            else:
                print("Invalid choice. Please enter A, B, C, or D.")

        # Check if the answer is correct
        correct_idx = group[group["is_correct"]].index[0] - group.index[0]
        if answer_idx == correct_idx:
            print("Correct!\n")
            correct_count += 1
            difficulty = group.iloc[0]["predicted_difficulty"]
            difficulty_correct[difficulty] += 1
        else:
            print("Wrong.\n")

        # Ask the user what to do next
        while True:
            print("\nWhat would you like to do next?")
            print("1. Continue to the next question")
            print("2. Stop Quiz and View Report")
            print("3. End Quiz")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                break
            elif choice == "2":
                print("Quiz stopped. Here's your report: ")
                display_report(correct_count, difficulty_correct)
                return
            elif choice == "3":
                print("Ending the quiz. Here's your report: ")
                display_report(correct_count, difficulty_correct)
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

    # Display the final results if the user completes all questions or time runs out
    print("\nQuiz Complete! Here's your report: ")
    display_report(correct_count, difficulty_correct)

# Menu function
def quiz_menu(df):
    total_time = 128 * 60  # Total time for the quiz in seconds (128 minutes)

    while True:
        print("\nQuiz Menu:")
        print("1. Start Quiz")
        print("2. End Quiz")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_instructions()  # Show the quiz instructions
            print("Starting the quiz...\n")
            conduct_quiz(df, total_time)
        elif choice == "2":
            print("Ending the quiz. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Run the quiz menu
quiz_menu(df)
