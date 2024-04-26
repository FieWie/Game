import random

grid_size = 9


class Place:
    def __init__(self, name, description, player_start):
        self.name = name
        self.description = description
        self.player_start = player_start
        self.objects = []

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


places = {
    "house": Place("house", "You are inside the house.", [4, 5]),
    "outside": Place("outside", "You are outside the house.", [1, 6])
}

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
        
def move_player():
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

    for link in links:
        if link.place == currentPlace:
            if [x, y] == link.getPosition():
                link.interact()
                return True

    player.setPosition(x, y)
    return True

def print_grid():
    print(currentPlace)
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
                print("⬛", end=" ")
        print()

links = [
    Link(3, 4, "door", "🚪", places["house"],places["outside"]),
    Link(0, 6, "house", "🏠", places["outside"],places["house"])
]

enemy = gameObject(3, 3, "enemy", "🦧", places["outside"])
chest = gameObject(8, 0, "chest", "💾", places["house"])
player = gameObject(4, 5, "player", "✳️ ", places["house"])
barn = gameObject(4, 3, "barn", "👦", places["outside"])
currentPlace = places["house"]
player.setPlace(currentPlace)

def main():
    print("Welcome to the game!")
    print("Instructions: Move using 'w', 'a', 's', 'd'. Type 'q' to quit.")
    print_grid()

    while True:
        if not move_player():
            break
        print_grid()

if __name__ == "__main__":
    main()
