import requests
import json


class Achievement:
    def __init__(self, name, condition):
        self.name = name
        self.condition = condition
        self.unlocked = False
    
    def check_condition(self, game_state):
        if not self.unlocked and self.condition(game_state):
            self.unlock()
    
    def unlock(self):
        self.unlocked = True
        print(f'Achievement Unlocked: {self.name}!')

class AchievementSystem:
    def __init__(self):
        self.achievements = []
    
    def add_achievement(self, achievement):
        self.achievements.append(achievement)
    
    def check_achievements(self, game_state):
        for achievement in self.achievements:
            achievement.check_condition(game_state)

class Player:
    def __init__(self):
        self.achievements = AchievementSystem()

    def add_achievement(self, achievement):
        self.achievements.add_achievement(achievement)

    def check_achievements(self, game_state):
        self.achievements.check_achievements(game_state)


def observe_player_achievements():
    string = "The player has curreny unlocked these achievements:"
    for achievement in player.achievements.achievements:
        if achievement.unlocked:
            string += (f"- {achievement.name}")
    
    string += ("And has not unlocked achievements:")
    for achievement in player.achievements.achievements:
        if not achievement.unlocked:
            string += (f"- {achievement.name}")
    print(string)
    return string

# Example conditions and game state
# (Assuming similar conditions and game state as before)

def visit_forest(game_state):
    return game_state['visit forest']
def visit_cave(game_state):
    return game_state['visit cave']
def kill_monkey(game_state):
    return game_state['killed monkey']

# Initialize player and NPC
player = Player()
# Define achievements
player.add_achievement(Achievement('visit forest',visit_forest))
player.add_achievement(Achievement('visit cave',visit_cave))
player.add_achievement(Achievement('killed monkey',kill_monkey))

# Example game state
game_state = {
    'visit forest': True,
    'visit cave': False,
    'killed monkey': True
}

# Player checks achievements based on game state
player.check_achievements(game_state)

# NPC observes player's achievements



api_key = "nJF8Lsuw6SVaAV8j07lUiezGAGF86FAzRhy1ohg7b7ab7b59"
url = "https://teachgpt.ssis.nu/api/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

"""
TO do
Add achivment system to give the NPC a context about what player has done and doesnt
For example input: Player has taken sword:
output: Player should kill the monkey.

"""

context ="""
You are a Villager in a game. 
Your task is to help the player further into the game.
You should not answer any other questions unless its about descriptions provided below.
You should answer in short sentences preferably 1-2.



If the player questions about what he has left to do, then you should anwer like this: 
"You have this left:
"""+ observe_player_achievements() + """

If the player questions about a special achievement 

"""

interpret_message = """
Your task is to interpret the input and you sould answer with a "/" + the thing the input want to know more about

Example: "/monster"

""" + observe_player_achievements()

def interpret_chat():
    pass

def process_chat():
    pass


print("Hej vad kan jag hjälpa till med")
while True:
    message = input()
        
    payload = {
    "model": "Yi-34B-Chat-GPTQ",
        "messages": [
            {
            "role": "system",
            "content": context
            },
            {
            "role": "user",
            "content": message
            }
        ],
    }
    response = requests.post(url, json=payload, headers=headers)

    jsonFile = {}
    if response.status_code != 200:
        print("Error:")
        print(response.text)


    response = response.json()['choices'][0]['message']['content']
    print(response)
