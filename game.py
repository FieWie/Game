import random
import time
from typing import Tuple

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

    isactive = True
    def __init__(self, x, y, name, emoji, place, sortlayer = 1, deadEmoji = "💀"):
        self.x = x
        self.y = y
        self.name = name
        self.emoji = emoji
        self.place = place
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

    def deleteObject(self):
        if self.place:
            self.place.removeObject(self)
            self.place = None
        else:
            print("Object is not placed anywhere.")

class LinkObject(gameObject):
    def __init__(self, position: Tuple[int, int], name, emoji, place, link):
        super().__init__(position[0], position[1], name, emoji, place, 1)
        self.link = link

    def interact(self):
        self.link.interact()
        

class Link:
    def __init__(self, linkObject1, linkObject2, destination):
        self.linkObject1 = linkObject1
        self.linkObject2 = linkObject2
        self.destination = destination

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
        

class weapon(gameObject):
    def __init__(self, damage, durability, x, y, name, emoji, place, sortlayer):
        super().__init__(x, y, name, emoji, place,sortlayer)
        self.damage = damage
        self.durability = durability

    def weapon_pickup(self):
        kark = input()
        if kark == "yes":
            bla =  convertTuple(("you have picked up ", self.name))
            animate_text(bla)
            self.deleteObject()
            player.has_sword = True
            return True
        elif kark == "no":
            animate_text("You don't like sharp things, pussy!")
            


    def check_weapon(self):
        pass
        
def convertTuple(tup):
    str = "".join(tup)
    return str

class Player(gameObject):
    def __init__(self, x, y, name, emoji, place, sortlayer):
        super().__init__(x, y, name, emoji, place,sortlayer)
    
    has_sword = False

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
            if isinstance(collided_obj, LinkObject):
                collided_obj.interact()
            elif isinstance(collided_obj, Enemy) and collided_obj.isactive:
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
            elif isinstance(collided_obj, weapon):
                animate_text("Would you like to pick up the woden sword yes or no:")
                collided_obj.weapon_pickup()
                
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
            if not self.has_sword:  # Kontrollerar om spelaren har svärdet
                animate_text("You can't fight without a weapon!", textDelay)
                return False
        
            time.sleep(2)
            animate_text("roll for damage", textDelay)
            resulat = random.randint(1, 20)
            resulat = 20
            animate_text(f"Dice {1}: {resulat}",textDelay)
            time.sleep(1)

            if(resulat > 10):
                enemy.take_damage(wodden_sword.damage)  # Applicera vapnets skada på fienden
                if enemy.health <= 0:
                    enemy.deleteObject()
                    animate_text("You have succesfully killed the monster", textDelay)
                    enemy.emoji = "💀"
                    for i in range(grid_size):
                        for j in range(grid_size):
                            if [i, j] == enemy:
                                print("💀", end=" ")       
                else:
                    animate_text(f"You dealt {wodden_sword.damage} damage to the enemy", textDelay)  
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
    def __init__(self, x, y, name, emoji, place, health):
        super().__init__(x, y, name, emoji, place)
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

def animate_text(string, delay = textDelay):
    for char in string:
        print(char, end='', flush=True) 
        time.sleep(delay) 
    print()
    time.sleep(1)  

places = {
    "house": Place("house", "You are inside the house.", [4, 5], "⬛"),
    "outside": Place("outside", "You are outside the house.", [1, 6], "🟩")
}

linkObjects = {
    "door": LinkObject((8,4), "door", "🚪", places["house"], None),
    "house": LinkObject((0,6), "house", "🏠", places["outside"], None)

}
    
links = {
    "home" : Link(linkObjects["door"], linkObjects["house"], places["outside"])
}

linkObjects["door"].link = links["home"]
linkObjects["house"].link = links["home"]

allGameObjects = [gameObject]

enemy = Enemy(3, 3, "enemy", "🦧", places["outside"],2)
player = Player(4, 5, "player", "🈸", places["house"],10)
barn = gameObject(4, 3, "barn", "👦", places["outside"])
wodden_sword = weapon(1, 10, 3,5,"woden-sword", "🗡️ ",places["house"],0)
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
        if enemy.isactive:
            enemy.monkey_run()
        print_grid()

if __name__ == "__main__":
    main()
