import threading
import time
import msvcrt
import os
import random

grid_size = 9
textDelay = .03
framerate = 1

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
    def __init__(self, x, y, name, emoji, place, can_collide, speed=1, sortlayer=1, deadEmoji="💀"):
        self.x = x
        self.y = y
        self.name = name
        self.emoji = emoji
        self.place = place
        self.can_collide = can_collide
        self.speed = speed
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
    
    def isInsideOfScreen(self):
        if not (0 <= self.x < grid_size):
            print("is inside of screen x:", self.x)
            return False
        elif not (0 <= self.y < grid_size):
            print("is inside of screen y", self.y)
            return False
        else:
            return True
            
    def interact(self):
        return self.can_collide
        
class GameObjects:
    gameObjects = []
    def __init__(self, name, emoji, nodes, place, can_collide, layer=1):
        # Method body
        self.name = name
        self.emoji = emoji
        self.nodes = nodes
        self.place = place
        self.can_collide = can_collide  # Define collision attribute
        self.layer = layer
        self.path = self.spawn_objects()

    # Makes objects
    def spawn_objects(self):
        path = []
        for i in range(len(self.nodes) - 1):
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[i + 1]
            path.extend(self.interpolate_points(x1, y1, x2, y2))
        for block in path:
            block = gameObject(block[0], block[1], self.name, self.emoji, self.place, self.can_collide, self.layer)
            self.gameObjects.append(block)
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
    
class Spike(GameObjects):
    def __init__(self, name, emoji, nodes, place, can_collide, layer, num_coordinates, grid_size, delay_between_spikes):
        super().__init__(name, emoji, nodes, place, can_collide, layer)
        self.num_coordinates = num_coordinates
        self.grid_size = grid_size
        self.delay_between_spikes = delay_between_spikes
        self.spawn_spikes()


    def spawn_spikes(self):
        threading.Thread(target=self.spawn_spike).start()

    def spawn_spike(self):
        for _ in range(self.num_coordinates):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            gameObject(x, y, "spike", self.emoji, self.place, self.can_collide, self.layer)
            time.sleep(self.delay_between_spikes)

def check_collision(x, y, place):
    for obj in place.getObjects():
        if obj.getPosition() == [x, y]:
            return obj
    return None

def print_grid():
    global running
    while running:
        os.system('cls')  # Clear the console screen
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
        time.sleep(0.1)  # Add a small delay for smoother grid printing

def animate_text(string, delay=textDelay):
    for char in string:
        print(char, end='', flush=True) 
        time.sleep(delay) 
    print()
    time.sleep(1)  

places = {
    "house": Place("house", "You are inside the house.", [4, 5], "⬛"),
}

def generate_random_coordinates(num_coordinates, grid_size):
    coordinates = set()
    while len(coordinates) < num_coordinates:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        coordinates.add((x, y))
    return list(coordinates)

currentPlace = places["house"]

spike = Spike("spike", "🟥", [(1, 1), (1, 2), (1, 3)], places["house"], True, 1,1, grid_size, delay_between_spikes=0.5)



running = True

def main():
    global running
    animate_text("Welcome to the game!", textDelay)
