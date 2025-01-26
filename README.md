# Quiz Question Difficulty Prediction and Quiz Management System

This project involves two key functionalities:

1. **Predicting Difficulty for Quiz Questions**: We predict the difficulty of quiz questions based on their descriptions and detailed solutions using clustering techniques.
2. **Quiz Management**: The system allows users to take a quiz, track their performance, and provides reports with visualizations.

## Files Overview

### 1. `quiz_questions.csv`
Contains data for each quiz question, including:
- `question_id`: Unique identifier for each question.
- `description`: The prompt or description of the question.
- `topic`: The subject or category the question belongs to.
- `detailed_solution`: A detailed explanation or solution of the question.
- `option_id`: Identifier for each answer option.
- `option_description`: The description of the answer options (A, B, C, D).
- `is_correct`: Whether the option is correct or not.
- `predicted_difficulty`: The predicted difficulty level (Easy, Medium, Hard).

### 2. `categorized_questions.csv`
Contains the processed data with predicted difficulty, which is the output after running the prediction model.

- `id`: Unique identifier for each question (same as `question_id` in `quiz_questions.csv`).
- `description`: Description of the question.
- `detailed_solution`: Solution for the question.
- `predicted_difficulty`: The predicted difficulty level of the question.

### 3. `quiz_report.py`
Handles the quiz process, tracks user performance, and generates a report at the end. The report includes:
- **Number of Correct Answers**
- **Breakdown of Correct Answers by Difficulty Level**
- **Visualization of Correct Answers by Difficulty**

## Process Overview

### Step 1: Difficulty Prediction
- The description and detailed solution of each question are combined into one text.
- Features like word count, sentence count, Flesch Reading Ease score, and Gunning Fog Index are extracted.
- The text is vectorized using TF-IDF.
- The features are scaled, and KMeans clustering is used to group questions into three difficulty levels (Easy, Medium, Hard).

### Step 2: Quiz Management
The system lets users take the quiz, where:
- **The total quiz time is 128 minutes.**
- After each question, the user is informed about the time remaining.
- Users can view a report with their performance after completing the quiz or stopping it midway.

### Step 3: Report and Visualization
At the end of the quiz, the user receives:
- The total number of correct answers.
- A breakdown of correct answers by difficulty level (Easy, Medium, Hard).
- A horizontal bar chart visualizing the number of correct answers for each difficulty level.

## Requirements

Make sure you have the following Python libraries installed:

- `pandas`
- `sklearn`
- `textstat`
- `matplotlib`

You can install these libraries using pip:

```bash
pip install pandas scikit-learn textstat matplotlib
