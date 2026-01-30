import random

stone_art = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper_art = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

scissor_art = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

art_map = {
    "stone": stone_art,
    "paper": paper_art,
    "scissor": scissor_art
}

print("Stone Paper Scissors Game")
print("Choices: stone, paper, scissor")

user_choice = input("Enter your choice: ").lower()

choices = ["stone", "paper", "scissor"]
computer_choice = random.choice(choices)

# Show computer choice with art
print("\nComputer chose:", computer_choice)
print(art_map[computer_choice])

# Show user choice with art (if valid)
if user_choice in art_map:
    print("You chose:", user_choice)
    print(art_map[user_choice])

# Game logic
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
