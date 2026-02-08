import random
import time
from collections import Counter, deque, defaultdict

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

choices = ["stone", "paper", "scissor"]
beats = {"stone": "scissor", "paper": "stone", "scissor": "paper"}
counters = {v: k for k, v in beats.items()}  # what beats each move

def normalize_choice(inp: str):
    if not inp:
        return None
    s = inp.strip().lower()
    mapping = {
        "s": "stone", "st": "stone", "stone": "stone",
        "p": "paper", "pa": "paper", "paper": "paper",
        "sc": "scissor", "scissor": "scissor", "scissors": "scissor"
    }
    return mapping.get(s)

def decide_winner(user: str, cpu: str):
    if user == cpu:
        return "tie"
    return "you" if beats[user] == cpu else "cpu"

def print_round(user, cpu, result):
    print("\nComputer chose:", cpu)
    print(art_map[cpu])
    print("You chose:", user)
    print(art_map[user])
    if result == "tie":
        print("Result: It's a tie!")
    elif result == "you":
        print("Result: You win!")
    else:
        print("Result: You lose!")

class AdaptiveCPU:
    def __init__(self, history_size=50, exploration_rate=0.15, use_markov=True):
        self.history_size = history_size
        self.exploration_rate = exploration_rate  # probability to pick random move
        self.use_markov = use_markov

        self.history = deque(maxlen=history_size)  # recent player moves
        self.freq = Counter()                       # overall freq in history window
        # Markov chain counts: given previous move, count next moves
        self.markov = defaultdict(Counter)
        self.last_player_move = None

    def update(self, player_move):
        if self.last_player_move is not None:
            self.markov[self.last_player_move][player_move] += 1
        self.last_player_move = player_move

        if len(self.history) == self.history.maxlen:
            # if deque will evict, decrement freq for popped value
            # Python deque doesn't provide the popped value before append, so do manually
            # work-around: when full, pop left and adjust
            left = self.history.popleft()
            self.freq[left] -= 1
            if self.freq[left] == 0:
                del self.freq[left]
            # append new
            self.history.append(player_move)
            self.freq[player_move] += 1
        else:
            self.history.append(player_move)
            self.freq[player_move] += 1

    def predict_most_frequent(self):
        if not self.freq:
            return None
        # returns player's most frequent recent move
        return self.freq.most_common(1)[0][0]

    def predict_markov(self):
        if not self.use_markov or self.last_player_move is None:
            return None
        nxt_counts = self.markov.get(self.last_player_move)
        if not nxt_counts:
            return None
        return nxt_counts.most_common(1)[0][0]

    def predict(self):
        # Combine predictors: prefer Markov if available, else freq; fall back to random
        markov_pred = self.predict_markov()
        freq_pred = self.predict_most_frequent()

        if markov_pred and freq_pred:
            # Weighted choice: more weight to markov (0.7) and freq (0.3)
            if random.random() < 0.7:
                return markov_pred
            else:
                return freq_pred
        if markov_pred:
            return markov_pred
        if freq_pred:
            return freq_pred
        return random.choice(choices)

    def choose(self):
        # exploration
        if random.random() < self.exploration_rate:
            return random.choice(choices)

        predicted_player_move = self.predict()
        # choose move that beats predicted_player_move
        cpu_move = counters.get(predicted_player_move, random.choice(choices))
        return cpu_move

def main():
    score = {"you": 0, "cpu": 0, "ties": 0}
    cpu_ai = AdaptiveCPU(history_size=50, exploration_rate=0.15, use_markov=True)

    print("Stone Paper Scissors Game")
    print("Choices: stone, paper, scissor  (also accept s/p/sc/scissors).")
    print("Type 'q' or 'quit' to exit.\n")

    try:
        while True:
            raw = input("Enter your choice: ")
            if raw.strip().lower() in ("q", "quit", "exit"):
                break

            user = normalize_choice(raw)
            if not user:
                print("Invalid input. Try: stone/paper/scissor (or s/p/sc).")
                continue

            print("Computer is choosing...", end="", flush=True)
            time.sleep(0.5)
            print()

            cpu = cpu_ai.choose()
            result = decide_winner(user, cpu)

            print_round(user, cpu, result)

            if result == "tie":
                score["ties"] += 1
            elif result == "you":
                score["you"] += 1
            else:
                score["cpu"] += 1

            # update CPU with player's move AFTER deciding outcome
            cpu_ai.update(user)

            print(f"Score — You: {score['you']}  CPU: {score['cpu']}  Ties: {score['ties']}\n")

    except KeyboardInterrupt:
        print("\nExiting...")

    print("\nFinal Score")
    print(f"You: {score['you']}, CPU: {score['cpu']}, Ties: {score['ties']}")
    print("Thanks for playing!")

if __name__ == "__main__":
    main()
