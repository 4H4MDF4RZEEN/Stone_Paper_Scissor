import random

print("Stone Paper Scissors Game")
print("Choices: stone, paper, scissor")

user_choice = input("Enter your choice: ").lower()

choices = ["stone", "paper", "scissor"]
computer_choice = random.choice(choices)

print("Computer chose:", computer_choice)

if user_choice == computer_choice:
    print("Result: It's a tie!")
elif user_choice == "stone" and computer_choice == "scissor":
    print("Result: You win!")
elif user_choice == "paper" and computer_choice == "stone":
    print("Result: You win!")
elif user_choice == "scissor" and computer_choice == "paper":
    print("Result: You win!")
elif user_choice in choices:
    print("Result: You lose!")
else:
    print("Invalid input! Please choose stone, paper, or scissor.")
