from ast import Try
from mimetypes import init
from multiprocessing import context
import random
import time
from typing import Tuple
import msvcrt
import requests


grid_size = 9

textDelay = .03
currentPlace = None
def roll_d20():
    directions = ["a", "d", "s", "w"]
    return random.choice(directions)

class Place:
    def __init__(self, name, description, emoji):
        self.name = name
        self.description = description
        self.objects = []
        self.emoji = emoji

    def GetName(self):
        return self.name
    
    def addObject(self, obj):
        self.objects.append(obj)

    def removeObject(self, obj):
        self.objects.remove(obj)

    def getObjects(self):
        return self.objects

class gameObject:
    isactive = True
    def __init__(self, x, y, name, emoji, place, can_collide, sortlayer = 1, deadEmoji = "💀"):
        self.x = x
        self.y = y
        self.name = name
        self.emoji = emoji
        self.place = place
        self.can_collide = can_collide
        self.sortlayer = sortlayer
        self.deadEmoji = deadEmoji

        place.addObject(self)
        
    def getPosition(self):
        return [self.x, self.y]

    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def setPlace(self, place):
        self.place = place
        
    def getPlace(self):
        return self.place
    
    def deleteObject(self):
        if self.place:
            self.place.removeObject(self)
            self.place = None
        else:
            print("Object is not placed anywhere.")
    
    def interact(self):
        return self.can_collide
        


class LinkObject(gameObject):
    def __init__(self, position: Tuple[int, int], name, emoji, place, link):
        super().__init__(position[0], position[1], name, emoji, place,True, 1)
        self.link = link

    def interact(self):
        self.link.interact()
        

class Link:
    def __init__(self, linkObject1, linkObject2):
        self.linkObject1 = linkObject1
        self.linkObject2 = linkObject2

        linkObject1.link = self
        linkObject2.link = self

    def interact(self):
        global currentPlace  
        currentlinkobject = LinkObject
        currentPlace.removeObject(player)
        if currentPlace == self.linkObject1.place:
            currentlinkobject = self.linkObject2
        elif currentPlace == self.linkObject2.place:
            currentlinkobject = self.linkObject1
        else:
            print("place error")
        
        currentPlace = currentlinkobject.getPlace()
        currentPlace.addObject(player)
        x,y = currentlinkobject.getPosition()
        player.setPosition(x, y)
        print_grid()
        print(currentPlace.description)



class Path():
    def __init__(self, path_emoji, bridge_emoji, nodes, place, collision, layer):
        self.path_emoji = path_emoji
        self.bridge_emoji = bridge_emoji
        self.nodes = nodes
        self.place = place
        self.collision = collision  # Define collision attribute
        self.layer = layer
        self.path = self.make_path()

    #Makes path
    def make_path(self):
        path = []
        for i in range(len(self.nodes) - 1):
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[i + 1]
            path.extend(self.interpolate_points(x1, y1, x2, y2))
        for block in path:
            emoji = self.path_emoji
            collide_obj = check_collision(block[0],block[1], self.place)
            if isinstance(collide_obj, Lake):
                collide_obj.deleteObject()
                emoji = self.bridge_emoji
            block = gameObject(block[0], block[1], "path", emoji, self.place, self.collision, self.layer)
        return path 
    
    def interpolate_points(self, x1, y1, x2, y2):
        path = []
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                path.append([x1, y])
        elif dy == 0:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                path.append([x, y1])
        else:  # Diagonal line (assuming 45 degrees)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    path.append([x, y])
        return path
            
def convertTuple(tup):
    str = "".join(tup)
    return str

class Player(gameObject):
    has_sword = False

    def __init__(self, x, y, name, emoji, place, collision, sortlayer):
        super().__init__(x, y, name, emoji, place,collision,sortlayer)
        self.current_weapon = None
        
    def move_player(self, move):
        x, y = player.getPosition()
        newX,newY = x,y

        if move == "w" and x > 0:
            newX -= 1
        elif move == "s" and x < grid_size - 1:
            newX += 1
        elif move == "a" and y > 0:
            newY -= 1
        elif move == "d" and y < grid_size - 1:
            newY += 1

        collided_obj = check_collision(newX,newY, currentPlace)
        if collided_obj:
            if isinstance(collided_obj, gameObject) and collided_obj.can_collide:
                #Checks if the player can move
                player.setPosition(newX, newY)  
                collided_obj.interact()  
        else:
            player.setPosition(newX, newY)     

    def check_collision_player(self):
        collided_obj = check_collision(self.x,self.y, currentPlace)
        if collided_obj and not isinstance(collided_obj, LinkObject):
            if isinstance(collided_obj, gameObject) and collided_obj.can_collide:
                #Checks if the player can move
                player.setPosition(self.x, self.y)  
                collided_obj.interact()
                   
        else:
            player.setPosition(self.x, self.y)   

    def youded(self):
        for i in range(grid_size):
            for j in range(grid_size):
                if [i, j] == player.getPosition():
                    print("💀", end=" ")
                else:
                    print("⬛", end=" ")
            print()
        exit()

    def observe_player_quests(self):
        string = "The player has currently completed these quests:"
        for quest in quests:
            if quest.is_completed():
                string += (f"\n- {quest.quest_information()}")
                
        
        string += ("\n"*2 +"And has not completed these quests:")
        for quest in quests:
            if not quest.is_completed():
                string += (f"\n- {quest.quest_information()}")
        return string


class Weapon(gameObject):
    def __init__(self, damage, durability, x, y, name, emoji, place,collision, sortlayer):
        super().__init__(x, y, name, emoji, place,collision,sortlayer)
        self.damage = damage
        self.durability = durability
        self.current_name = None

    def interact(self):
        animate_text(f"Would you like to pick up the {self.name} yes or no:")
        kark = input()
        if kark == "yes":
            animate_text(("you have picked up "+ self.name))
            self.take_weapon()
            return True
        elif kark == "no":
            animate_text("You don't like sharp things, pussy!")
            return False
        else:
            animate_text("haha")
            return False    
    
    def take_weapon(self):
        player.current_weapon = self
        player.has_sword = True
        print("current weapon: ", player.current_weapon.name)
        inventory.add_item(self)
        self.place.removeObject(self)
        self.place = None
        
    def drop_weapon(self, x,y,place):
        inventory.remove_item(self)
        self.place = place
        self.place.addObject(self)
        self.x = x
        self.y = y

class Food(gameObject):
    def __init__(self, x, y, name, emoji, place, can_collide):
        super().__init__(x, y, name, emoji, place, can_collide)
    pass

class Inventory:
    weapons = []
    food = []

    def add_item(self, item):
        if isinstance(item, Weapon):
            print("weapon added")
            self.weapons.append(item)
        elif isinstance(item, Food):
            self.food.append(item)

    def remove_item(self, item):
        if isinstance(item, Weapon):
            self.items.remove(item)
            print(f"{item.name} has been dropped from your inventory.")
        elif isinstance(item, Food):
            self.items.remove(item)
            print(f"{item.name} has been dropped from your inventory.")
        else:
            print(f"{item.name} is not in your inventory.")

    def check_weapons(self):
        print(len(self.weapons))
        string = ""
        if len(self.weapons) != 0:
            string += "You currently have these weapons:\n"
            for weapon in self.weapons:
                string += f"- {weapon.name}. Damage: {weapon.damage}. Durability {weapon.durability} \n"
        else: string += ("You do not have any weapons yet." + "\n"*2)

        if len(self.food) != 0:
            string += "You currently have these foods:\n"
            for food in self.food:
                string += f"- {food.name} \n"
        else: string += "You do not have any food yet.\n"
        animate_text(string)


class Enemy(gameObject):
    def __init__(self, x, y, name, emoji, place, collision,health):
        super().__init__(x, y, name, emoji, place, collision, sortlayer=2)
        self.health = health
    rörelse_riktning = 1
    def monkey_run(self):
        self.y += self.rörelse_riktning
        if self.y == 0 or self.y == grid_size - 1:
        # Ändra rörelseriktningen för att få objektet att gå åt motsatt håll
            self.rörelse_riktning *= -1
        # Additional enemy-specific attributes or methods can be added here
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0  # Säkerställ att hälsan inte går under noll

    def deleteObject(self):
        self.isactive = False
        self.emoji = self.deadEmoji
        self.can_collide = False
    def cow_walk(self):
        if not self.isactive:
            return
        walk = roll_d20()
        if walk == "w" and self.x > 0:  
            self.x -= 1
        elif walk == "s" and self.x < grid_size - 1:  
            self.x += 1
        elif walk == "a" and self.y > 0:  
            self.y -= 1
        elif walk == "d" and self.y < grid_size - 1:  
            self.y += 1
    def interact(self ):
        self.FightEnemy()

    def FightEnemy(self):
        string = "Want to fight the "+self.name + " yes or no: "
        animate_text(string, textDelay)
        fight = input()
        if fight == "yes":
        
            if not player.has_sword:  # Kontrollerar om spelaren har svärdet
                animate_text("You can't fight without a weapon!", textDelay)
                return False
            while True:
                time.sleep(2)
                animate_text("roll for damage", textDelay)
                resulat = random.randint(1, 20)
                resulat = 20
                animate_text(f"Dice {1}: {resulat}",textDelay)
                time.sleep(1)

                if(resulat > 10):
                    self.take_damage(player.current_weapon.damage)  # Applicera vapnets skada på fienden
                    if self.health <= 0:
                        animate_text(f"You dealt {player.current_weapon.damage} damage to the {self.name}", textDelay)
                        self.deleteObject()
                        animate_text("You have succesfully killed the "+self.name, textDelay)
                        self.emoji = "💀"
                        self.Kill_enemy()
                        break       
                    else:
                        animate_text(f"You dealt {player.current_weapon.damage} damage to the {self.name}", textDelay)
                        animate_text("Would you like to continue to fight yes or no", textDelay)
                        continues = input()
                        if continues == "yes":
                            continue
                        elif continues == "no":
                            break
                        else:
                            animate_text("Type it right next time", textDelay)
                else:
                    player.emoji = "💀"
                    time.sleep(2)
                    animate_text("you died", textDelay)
                    player.youded()
                    exit()  
        elif fight == "no":
            animate_text("nice", textDelay)  
            return False  
    def Kill_enemy(self):
        print("ded")

class Bear(Enemy):
    def __init__(self, x, y, name, emoji, place, collision, health):
        super().__init__(x, y, name, emoji, place, collision, health)
    
    def interact(self):
        return super().interact()
    def Kill_enemy(self):
        self.setPosition(self.x +1, self.y)


class KingCow(Enemy):
    def __init__(self, x, y, name, emoji, place, collision, health):
        super().__init__(x, y, name, emoji, place, collision, health)

    def cow_king_walk(self, crown = gameObject):
        if not self.isactive:
            return
        walk = roll_d20()
        print("Walk", walk)
        if walk == "w" and self.x > 1:  
            self.x -= 1
        elif walk == "s" and self.x < grid_size - 1:  
            self.x += 1
        elif walk == "a" and self.y > 0:  
            self.y -= 1
        elif walk == "d" and self.y < grid_size - 1:  
            self.y += 1
        crown.setPosition((self.x -1), self.y)

    def deleteObject(self):
        kill_king_cow.complete()
        self.isactive = False
        self.emoji = self.deadEmoji
        self.can_collide = False
    
class Lake(gameObject):
    def __init__(self, x, y, name, emoji, place, collision):
        super().__init__(x, y, name, emoji, place,collision, sortlayer=0)

    def interact(self):
        animate_text("You can't swim you idiot", textDelay)
        player.youded()


class NPC(gameObject):
    api_key = "nJF8Lsuw6SVaAV8j07lUiezGAGF86FAzRhy1ohg7b7ab7b59"
    url = "https://teachgpt.ssis.nu/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    context ="""
        You are a Villager in a game. 
        Your task is to help the player further into the game.
        You should only answer with the information about the quests provided below.
        You should answer in short sentences preferably 1-2 sentences in total.

        If the player questions about what he has left to do, then you should anwer like this: 
        "You have this left: (then the quest he has left)"
        """
    
    def __init__(self, x, y, name, emoji, place, can_collide, sortlayer=1, deadEmoji="💀"):
        super().__init__(x, y, name, emoji, place, can_collide, sortlayer, deadEmoji)
    
    def interact(self):
        animate_text("What can i help with?. To exit, write bye.")
        while True:
            message = input()
            if message == "bye":
                animate_text("I see you later my friend!")
                break
                
            payload = {
            "model": "Yi-34B-Chat-GPTQ",
                "messages": [
                    {
                    "role": "system",
                    "content": self.context + player.observe_player_quests()
                    },
                    {
                    "role": "user",
                    "content": message
                    }
                ]
            }
            response = requests.post(self.url, json=payload, headers=self.headers)
            if response.status_code != 200:
                print("Error:")
                print(response.text)

            response = response.json()['choices'][0]['message']['content']
            animate_text(response)


class Quest:
    def __init__(self, name, location, reward, quests_parent):
        self.name = name
        self.location = location
        self.reward = reward
        self.completed = False
        quests_parent.append(self)

    def quest_information(self):
        string = self.name + ", located at: " + self.location + ", Reward: " + self.reward
        return string
    
    def complete(self):
        if not self.completed:
            self.completed = True
            animate_text(f"Quest completed: {self.name}! Reward: {self.reward}")
  
    def is_completed(self):
        return self.completed

def check_cows_dead(cowslist, cutscene):
    cows = cowslist
    all_dead = all(not cow.isactive for cow in cows)
 
    if all_dead and not cutscene:
        animate_text("You have killed all the cows", textDelay)
        animate_text("Yooooooo what is happening", textDelay)
        return True
    return False
                
def spanw_kingCow():
    global KingCow_crown
    kingCow = KingCow(5,0,"KingCow","🐄",places["farm"],True,10)
    KingCow_crown = gameObject(4,0,"crown","👑",places["farm"],True, 5)
    animate_text("Is that the KingCow?", textDelay)
    return kingCow
#Checks the mainobject if there is one and returns.  
def check_collision(x,y, place):
    for obj in place.getObjects():
            if obj.getPosition() == [x, y]:
                return obj
    return None

def check_input():
    while True:
        print("Where do you want to go? (w/s/a/d) or h for help: ")
        letter = msvcrt.getch().decode('utf-8').lower()
        print("\n"*2)
        if letter in ["w", "a", "s", "d"]:
            player.move_player(letter)
            break
        elif letter == "u":
            animate_text(player.observe_player_quests())
        elif letter == "i":
            inventory.check_weapons()
        elif letter == "l":
            player.current_weapon.drop_weapon(player.x, player.y, player.place)
            animate_text("You dropped weapon lol!")
            break

        elif letter == "h":
            string = """
Move with: "W/A/S/D".
Open inventory with: "I".
See all quests with: "U".
Get help with: "H"."""
            animate_text(string)
            time.sleep(2)
            print("\n"*2)
            continue
        elif letter == "q":
            animate_text("Exiting the game.")
            exit()
        else:
            break
        time.sleep(1)
        print_grid()

def print_grid():
    print("\n" * 10)
    for i in range(grid_size):
        for j in range(grid_size):
            # Initialize variables to track the object with the highest sort layer
            highest_sort_layer_obj = None
            highest_sort_layer = float('-inf')  # Initialize with negative infinity
            
            # Loop through all game objects in the current place
            for currentObj in currentPlace.objects:
                if [i, j] == currentObj.getPosition():
                    if currentObj.sortlayer > highest_sort_layer:
                        highest_sort_layer = currentObj.sortlayer
                        highest_sort_layer_obj = currentObj
            
            if highest_sort_layer_obj:
                print(highest_sort_layer_obj.emoji, end=" ")  # Print the emoji of the object with the highest sort layer
            else:
                print(currentPlace.emoji, end=" ")  # Print the emoji of the current place if no object is found
        print()

def animate_text(string, delay = textDelay):
    for char in string:
        print(char, end='', flush=True) 
        time.sleep(delay) 
    print()
    time.sleep(1)  



quests = []

kill_king_cow = Quest(
    name="Kill king Cow",
    location="Farm",
    reward= "None",
    quests_parent= quests
)

explore_mansion = Quest(
    name="Explore mansion",
    location="Town",
    reward="Candy",
    quests_parent= quests
)




places = {
    "house": Place("house", "You are inside the house.", "⬛"),
    "outside": Place("outside", "You are outside the house.", "🟩"),
    "forest": Place("forest", "You have entered the forest","🟩"),
    "cave": Place("cave", "Yo is dark here","⬛"),
    "hut": Place("hut", "This is nasty","🟫"),
    "deep_forest": Place("Deep_forest", "this is deep","🟩"),
    "town": Place("town", "YOOOO, is that a villager??","🟩"),
    "farm":Place("farm","Konrad love this","🟩"),
    "desert":Place("desert","Its so hot here","🟨"),
}

linkObjects = {
    "door": LinkObject((8,4), "door", "🚪", places["house"], None),
    "house": LinkObject((0,6), "house", "🏠", places["outside"], None),
    "grass": LinkObject((8,7), "grass", "⬛", places["outside"], None),
    "black": LinkObject((0,7), "black", "⬛", places["forest"], None),
    "cave_entrance": LinkObject((4,0),"entrance","⬛", places["forest"], None),
    "inside_cave": LinkObject((4,8),"cave_exit","⬛", places["cave"], None),
    "hut_outside": LinkObject((3,3),"entrance_hut","🛖 ",places["forest"],None),
    "inside_hut": LinkObject((8,4),"exit_hut","⬛",places["hut"],None),
    "Deep_forest_entrance": LinkObject((8,7),"Deep_forest_entrance","⬛",places["forest"],None),
    "Deep_forest_exit": LinkObject((0,7),"Deep_forest_exit","⬛",places["deep_forest"],None),
    "town_entrance": LinkObject((7,8),"town_entrace","🟫",places["deep_forest"],None),
    "town_exit": LinkObject((7,0),"town_exit","🟫",places["town"],None),
    "farm_entrance": LinkObject((8,7),"farm_entrance","🟫",places["town"],None),
    "farm_exit": LinkObject((0,7),"farm_exit","🟫",places["farm"],None),
    "desert_entrence": LinkObject((4,0),"desert_entrence","🏜️ ",places["deep_forest"],None),
    "desert_exit": LinkObject((4,8),"desert_exit","🟩",places["desert"],None),

}
    
links = {
    "home" : Link(linkObjects["door"], linkObjects["house"]),
    "outside" : Link(linkObjects["grass"], linkObjects["black"]),
    "forest" : Link(linkObjects["cave_entrance"], linkObjects["inside_cave"]),
    "cave" : Link(linkObjects["cave_entrance"], linkObjects["inside_cave"]),
    "hut" : Link(linkObjects["hut_outside"],linkObjects["inside_hut"]),
    "deep_forest" : Link(linkObjects["Deep_forest_entrance"], linkObjects["Deep_forest_exit"]),
    "town" : Link(linkObjects["town_entrance"], linkObjects["town_exit"]),
    "farm" : Link(linkObjects["farm_entrance"], linkObjects["farm_exit"]),
    "desert" : Link(linkObjects["desert_entrence"], linkObjects["desert_exit"]),

}

inventory = Inventory()

enemy = Enemy(3, 3, "monkey", "🦧", places["outside"],True,3)
player = Player(4, 5, "player", "🈸", places["house"],True,10)
orge = Enemy(5,3, "orge","🧌 ",places["forest"],True,2)
bear = Bear(4,1, "bear", "🧸", places["deep_forest"],True,2)
wodden_sword = Weapon(1, 10, 3,5,"woden-sword", "🗡️ ",places["house"],True,0)
knife = Weapon(10, 10,0,0,"knife","🔪",places["outside"],True,0)
villager = NPC(6,5, "Villager", "🫅 ", places["town"], True)
cow_list = [
    Enemy(5,3,"Cow","🐄",places["farm"],True,2),
    Enemy(7,3,"Cow","🐄",places["farm"],True,2),
    Enemy(6,6,"Cow","🐄",places["farm"],True,2)
]


currentPlace = places["house"]
player.setPlace(currentPlace)

#Outside
offset = [5,0]
for x in range(2):
    for y in range(9):
        xOffset = x +offset[0]
        yOffset = y +offset[1]
        name = "lake" + str(xOffset) + str(yOffset)
        lake = Lake(xOffset,yOffset,name,"🟦", places["outside"], True)
nodes = [[1,6], [3,6], [3,7], [8,7]]
path = Path("⬛", "🟫", nodes, places["outside"], True, 1)

#Forest
stone = gameObject(5,0,"stone", "🪨 ", places["forest"],False)
stone2 = gameObject(3,0,"stone","🪨 ", places["forest"],False)
trees = [[8,5],[0,5]]
tree = Path("🌲","",trees,places["forest"], False, 1)

#Town
town_path_nodes = [[7,1],[7,3],[2,3],[7,3],[7,5], [7,5], [7,7], [8,7], [0,7]]
town_path = Path("🟫", "", town_path_nodes, places["town"], True, 1)
mansion = gameObject(1,3,"mansion","🛕",places["town"],False)
houses = [[5,2],[3,2],[5,4],[3,4],[3,6],[5,6],[3,8],[5,8] ]
for house in houses:
    housess = gameObject(house[0],house[1],"house","🏠",places["town"],False)

#deep_forest
rode = [[7,8],[7,7]]
rodes = Path("🟫","",rode,places["deep_forest"], True, 1)
forest_trees = [[3,7],[1,5],[2,0],[6,4],[7,1],[0,3],[4,2],[8,6],[5,0],[3,7], [1, 4], [2, 6], [6, 0], [4, 5], [7, 3], [0, 1], [5, 8], [1, 2],[8,4],[3,7],[5,0],[3,0]]
for tree in forest_trees:
    forest_tree = gameObject(tree[0],tree[1],"tree", "🌲",places["deep_forest"],False)

#farm
farm_path = [[0,7],[7,7]]
farm_rode = Path("🟫","",farm_path,places["farm"], True, .1)
Farm_markCheck = [[3,1],[3,6]]
farm_marken = Path ("🟩","",Farm_markCheck,places["farm"],True, .2)
Farm_markCheck = [[6,1],[6,6]]
farm_marken = Path ("🟩","",Farm_markCheck,places["farm"],True, .2)
farm_mark = [[1,1],[8,6]]
farm_marken = Path("🟨","",farm_mark,places["farm"],True, .1)

#desert
cactus_pos = [[4,4],[7,1],[6,6],[2,1],[8,4],[7,8],[0,6],[2,7]]
for pos in cactus_pos:
    cactus = gameObject(pos[0],pos[1],"cactus","🌵", places["desert"], True)


cutscene = False
kingwalk = False
def main():
    animate_text("Welcome to the game!", textDelay)
    print("Instructions: Move using 'w', 'a', 's', 'd'. Type h for help.")
    print_grid()
    while True:
        
        check_input()
        if enemy.isactive:
            enemy.monkey_run()
        global cutscene
        global kingCow
        if check_cows_dead(cow_list, cutscene):
            cutscene = True
            kingCow = spanw_kingCow()
            print(kingCow)

        if cutscene:
            kingCow.cow_king_walk(KingCow_crown) 
        for cow in cow_list:
            cow.cow_walk()
        print_grid()
if __name__ == "__main__":
    main()

