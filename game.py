import random

grid_size = 9


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
    def __init__(self, x, y, name, emoji, place):
        self.x = x
        self.y = y
        self.name = name
        self.emoji = emoji
        self.place = place

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
        super().__init__(x, y, name, emoji, place)
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
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional player-specific attributes or methods can be added here
    
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
        if move == "w" and x > 0:
            x -= 1
        elif move == "s" and x < grid_size - 1:
            x += 1
        elif move == "a" and y > 0:
            y -= 1
        elif move == "d" and y < grid_size - 1:
            y += 1

        #If go through door

        self.setPosition(x, y)

        collided_obj = self.check_collision(x,y)
        if collided_obj:
            # Handle collision based on object type
            if isinstance(collided_obj, Link):
                collided_obj.interact()
            elif isinstance(collided_obj, Enemy):
                print("You encountered an enemy!")
            elif isinstance(collided_obj, Chest):
                print("You found a chest!")

        else:
            player.setPosition(x, y)
        return True        


    

class Enemy(gameObject):
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional enemy-specific attributes or methods can be added here
 
class Chest(gameObject):
    def __init__(self, x, y, name, emoji, place):
        super().__init__(x, y, name, emoji, place)
        # Additional enemy-specific attributes or methods can be added here
 


def print_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            #Loop all gameobjects
            object_found = False
            obj = gameObject
            
            for obj in currentPlace.objects:
                if [i,j] == obj.getPosition():
                    object_found = True
                    break
                else:
                    object_found = False

            if object_found:
                print(obj.emoji, end=" ")
            else:
                print(currentPlace.emoji, end=" ")
        print()

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
chest = Chest(8, 0, "chest", "💾", places["house"])
player = Player(4, 5, "player", "✳️ ", places["house"])
barn = gameObject(4, 3, "barn", "👦", places["outside"])
currentPlace = places["house"]
player.setPlace(currentPlace)

for x in range(2):
    for y in range(9):
        offset = [5,0]
        xOffset = x +offset[0]
        yOffset = y +offset[1]
        name = "lake" + str(xOffset) + str(yOffset)
        if name == "lake67" or name == "lake57":
            bridge = gameObject(xOffset,yOffset,name,"🟫", places["outside"])
        else:
            lake = gameObject(xOffset,yOffset,name,"🟦", places["outside"])



def main():
    print("Welcome to the game!")
    print("Instructions: Move using 'w', 'a', 's', 'd'. Type 'q' to quit.")
    print_grid()

    while True:
        if not player.move_player():
            break
        print_grid()

if __name__ == "__main__":
    main()
