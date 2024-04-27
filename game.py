import random
import time

grid_size = 9

textDelay = .03

class Place:
    def __init__(self, name, description, player_start, emoji):
        self.name = name
        self.description = description
        self.player_start = player_start
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
    def __init__(self, x, y, name, emoji, place, sortlayer = 1):
        self.x = x
        self.y = y
        self.name = name
        self.emoji = emoji
        self.place = place
        self.sortlayer = sortlayer

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

class Link(gameObject):
    def __init__(self, x, y, name, emoji, place,destination = Place):
        super().__init__(x, y, name, emoji, place,1)
        self.destination = destination

    def interact(self):
        global currentPlace 
        currentPlace.removeObject(player)
        currentPlace = self.destination
        currentPlace.addObject(player)

        x,y = places[currentPlace.GetName()].player_start
        player.setPosition(x,y)
        print_grid()
        print(currentPlace.description)

class Player(gameObject):
    def __init__(self, x, y, name, emoji, place, sortlayer):
        super().__init__(x, y, name, emoji, place,sortlayer)

    def check_collision(self,x, y):
        for obj in currentPlace.getObjects():
            if obj.getPosition() == [x, y]:
                return obj
        return None

    def move_player(self):
        move = input("Where do you want to go? (w/s/a/d): ").lower()
        if move == "q":
            print("Exiting the game.")
            return False

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

        collided_obj = self.check_collision(newX,newY)
        print()
        if collided_obj:
            # Handle collision based on object type
            if isinstance(collided_obj, Link):
                collided_obj.interact()
            elif isinstance(collided_obj, Enemy):
                animate_text("You encountered an enemy!",textDelay)
                if not self.FightEnemy():
                    newX, newY = x,y
            elif isinstance(collided_obj, Lake):
                player.setPosition(newX, newY)
                animate_text("You can't swim you idiot", textDelay)
                self.youded()
                exit()
            elif isinstance(collided_obj, Bridge):
                player.setPosition(newX, newY)
        else:
            player.setPosition(newX, newY)
        return True
    
    def youded(self):
        for i in range(grid_size):
            for j in range(grid_size):
                if [i, j] == player.getPosition():
                    print("💀", end=" ")
                else:
                    print("⬛", end=" ")
            print()  

    def FightEnemy(self):
        animate_text("Want to fight the monster yes or no: ", textDelay)
        fight = input()
        if fight == "yes":
            time.sleep(2)
            animate_text("roll for damage", textDelay)
            resulat = random.randint(1, 20)
            animate_text(f"Dice {1}: {resulat}",textDelay)
            time.sleep(1)

            if(resulat > 10):
                animate_text("You have succesfully killed the monster", textDelay)
                enemy.emoji = "💀"
                for i in range(grid_size):
                    for j in range(grid_size):
                        if [i, j] == enemy:
                            print("💀", end=" ")         
            else:
                self.emoji = "💀"
                time.sleep(2)
                animate_text("you died", textDelay)
                self.youded()
                exit()
            return True
                
        elif fight == "no":
            animate_text("nice", textDelay)  
            return False  

class Enemy(gameObject):
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional enemy-specific attributes or methods can be added here
class Bridge(gameObject):
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional enemy-specific attributes or methods can be added here
class Lake(gameObject):
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional enemy-specific attributes or methods can be added here



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

def animate_text(string, delay):
    for char in string:
        print(char, end='', flush=True) 
        time.sleep(delay) 
    print()
    time.sleep(1)  

places = {
    "house": Place("house", "You are inside the house.", [4, 5], "⬛"),
    "outside": Place("outside", "You are outside the house.", [1, 6], "🟩")
}
links = [
    Link(3, 4, "door", "🚪", places["house"],places["outside"]),
    Link(0, 6, "house", "🏠", places["outside"],places["house"])
]

allGameObjects = [gameObject]

enemy = Enemy(3, 3, "enemy", "🦧", places["outside"])
player = Player(4, 5, "player", "✳️ ", places["house"],10)
barn = gameObject(4, 3, "barn", "👦", places["outside"])

currentPlace = places["house"]
player.setPlace(currentPlace)

#Making the lake and bridge
offset = [5,0]
for x in range(2):
    for y in range(9):
        xOffset = x +offset[0]
        yOffset = y +offset[1]
        name = "lake" + str(xOffset) + str(yOffset)
        if name == "lake67" or name == "lake57":
            bridge = Bridge(xOffset,yOffset,name,"🟫", places["outside"])
        else:
            lake = Lake(xOffset,yOffset,name,"🟦", places["outside"])


def main():
    animate_text("Welcome to the game!", textDelay)
    print("Instructions: Move using 'w', 'a', 's', 'd'. Type 'q' to quit.")
    print_grid()

    while True:
        if not player.move_player():
            break
        print_grid()

if __name__ == "__main__":
    main()
