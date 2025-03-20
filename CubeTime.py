import random
import time
import json
import keyboard

# Scramble generation rules
MOVE_SETS = {
    2: ["U", "R", "F"],
    3: ["U", "R", "F", "D", "L", "B", "D2", "U2", "L2", "R2", "F2", "B2"],
    4: ["U", "R", "F", "D", "L", "B", "Uw", "Rw", "Fw2", "Uw2", "Rw2", "Fw", "D2", "U2", "L2", "R2", "F2", "B2"]
}

MODIFIERS = ["", "'"]
SCRAMBLE_LENGTH = {2: 9, 3: 20, 4: 40}

# Load previous times
def load_times():
    try:
        with open("times.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"2x2": [], "3x3": [], "4x4": []}

def save_times(times):
    with open("times.json", "w") as file:
        json.dump(times, file, indent=4)

# Generate scramble without redundant moves
def generate_scramble(cube_size):
    moves = MOVE_SETS[cube_size]
    scramble = []
    prev_move = ""
    
    for _ in range(SCRAMBLE_LENGTH[cube_size]):
        move = random.choice(moves)
        while move == prev_move:
            move = random.choice(moves)
        
        # Ensure moves ending in '2' do not get a modifier
        if move.endswith("2"):
            modifier = ""
        else:
            modifier = random.choice(MODIFIERS)
        
        scramble.append(move + modifier)
        prev_move = move
    
    return " ".join(scramble)

# Main timer function
def start_timer():
    times = load_times()
    while True:
        try:
            cube_size = int(input("Enter cube size (To exit: 0): "))
            if cube_size == 0:
                break
            if cube_size not in [2, 3, 4]:
                print("Invalid selection. Try again.")
                continue

            scramble = generate_scramble(cube_size)
            print(f"Scramble: {scramble}")
            print("Press SPACE to start ...")
            keyboard.wait("space")
            start = time.time()
            print("Timing started! Press SPACE again to stop.")
            keyboard.wait("space")
            solve_time = round(time.time() - start, 2)
            print(f"Solve time: {solve_time} seconds")

            key = f"{cube_size}x{cube_size}"
            times[key].append(solve_time)
            save_times(times)
        
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    start_timer()
