def ask_question(question, options, correct_index):
    print(question)
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    
    while True:
        try:
            answer = int(input("Enter the number of your answer: "))
            if 1 <= answer <= len(options):
                return answer == correct_index
            else:
                print("Please enter a valid option number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def quiz():
    questions = [
        {
            "question": "What is the ans of 12*10?",
            "options": ["12", "10", "120", "1211"],
            "correct_index": 3
        },
        {
            "question": "what is the ans of 12%10?",
            "options": ["2", "12", "10", "121"],
            "correct_index": 1
        },
        {
            "question": "Which one is maximum number from 25 & 34?",
            "options": ["25", "34"],
            "correct_index": 2
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["O2", "H2O", "CO2", "NaCl"],
            "correct_index": 2
        },
        {
            "question": "Which element has the atomic number 1?",
            "options": ["Oxygen", "Hydrogen", "Carbon", "Helium"],
            "correct_index": 2
        }
    ]

    score = 0

    print("Welcome to the Quiz Game!")
    print("You will be asked 5 questions. Let's see how many you can answer correctly!\n")

    for q in questions:
        if ask_question(q["question"], q["options"], q["correct_index"]):
            print("Correct!\n")
            score += 1
        else:
            print("Wrong answer.\n")

    print(f"Quiz Over! Your final score is: {score}/{len(questions)}")


quiz()       
