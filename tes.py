import threading
import time
import msvcrt
import os

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
    
class Path(GameObjects):
    def __init__(self, name, path_emoji, bridge_emoji, nodes, place, can_collide, layer):
        super().__init__(name, path_emoji, bridge_emoji, nodes, place, can_collide, layer)
        self.path = self.spawn_objects()

    # Makes path
    def spawn_objects(self):
        path = []
        for i in range(len(self.nodes) - 1):
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[i + 1]
            path.extend(self.interpolate_points(x1, y1, x2, y2))
        for block in path:
            emoji = self.emoji
            collide_obj = check_collision(block[0], block[1], self.place)
            if isinstance(collide_obj, Lake):
                collide_obj.deleteObject()
                emoji = self.bridge_emoji
            block = gameObject(block[0], block[1], "path", emoji, self.place, self.can_collide, self.layer)
        return path 

class ObstacleHandler:
    def __init__(self):
        self.obstacles = []
        self.obstacle_threads = []

    def add_obstacle(self, obstacle):
        self.obstacles.append(obstacle)
        thread = threading.Thread(target=obstacle.move)
        self.obstacle_threads.append(thread)

    def remove_obstacle(self, obstacle):
        self.obstacles.remove(obstacle)

    def move_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.move()

    def interact_obstacles(self, other_object):
        for obstacle in self.obstacles:
            if obstacle.getPosition() == other_object.getPosition():
                obstacle.interact(other_object)

class Lazer(GameObjects):
    def __init__(self, name, emoji, nodes, place, directionX, directionY, can_collide, layer):
        super().__init__(name, emoji, nodes, place, can_collide, layer)
        self.directionX = directionX
        self.directionY = directionY

    def move(self):
        for obj in self.gameObjects:
            x, y = obj.getPosition()
            newX = x + self.directionX
            newY = y + self.directionY
            obj.setPosition(newX, newY)
            if player.getPosition() == [newX, newY]:
                player.youded()

            

def convertTuple(tup):
    str = "".join(tup)
    return str

class Player(gameObject):
    has_sword = False

    def __init__(self, x, y, name, emoji, place, collision, sortlayer):
        super().__init__(x, y, name, emoji, place, collision, sortlayer)
        self.current_weapon = None
        
    def move_player(self):
        global running
        while running:
            if msvcrt.kbhit():
                move = msvcrt.getch().decode('utf-8').lower()
                if move == "q":
                    print("Exiting the game.")
                    running = False
                    return

                x, y = self.getPosition()
                newX, newY = x, y

                if move == "w" and x > 0:
                    newX -= 1
                elif move == "s" and x < grid_size - 1:
                    newX += 1
                elif move == "a" and y > 0:
                    newY -= 1
                elif move == "d" and y < grid_size - 1:
                    newY += 1
                else:
                    continue

                collided_obj = check_collision(newX, newY, currentPlace)
                if collided_obj:
                    if isinstance(collided_obj, gameObject) and collided_obj.can_collide:
                        print("Collide with object: ", collided_obj.name)
                        self.setPosition(newX, newY)
                        collided_obj.interact()
                else:
                    self.setPosition(newX, newY)      
            time.sleep(0.05)  # Add a small delay to prevent too rapid movement
    
    def youded(self):
        global running
        running = False
        for i in range(grid_size):
            for j in range(grid_size):
                if [i, j] == self.getPosition():
                    print("💀", end=" ")
                else:
                    print("⬛", end=" ")
            print()
        exit()

    def interact(self):
        player.youded()

class Enemy(gameObject):
    def __init__(self, x, y, name, emoji, place, collision, health):
        super().__init__(x, y, name, emoji, place, collision, sortlayer=2)
        self.health = health
    rörelse_riktning = 1
    def monkey_run(self):
        global running
        while running: 
            newY =  self.y + self.rörelse_riktning

            collided_obj = check_collision(self.x, newY, currentPlace)
            if collided_obj:
                if isinstance(collided_obj, gameObject) and collided_obj.can_collide:
                    print("Collide with object: ", collided_obj.name)
                    self.setPosition(self.x, newY)
                    collided_obj.interact()
            else:
                self.setPosition(self.x, newY)    
            if self.y == 0 or self.y == grid_size - 1:
                # Ändra rörelseriktningen för att få objektet att gå åt motsatt håll
                self.rörelse_riktning *= -1
            # Additional enemy-specific attributes or methods can be added here
              
            time.sleep(framerate)
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0  # Säkerställ att hälsan inte går under noll

    def deleteObject(self):
        self.isactive = False
        self.emoji = self.deadEmoji
        self.can_collide = False

    def interact(self):
        player.youded()

# Checks the main object if there is one and returns.
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

currentPlace = places["house"]

#enemy = Enemy(3, 3, "monkey", "🦧", places["house"], True, 3)
player = Player(4, 5, "player", "🈸", places["house"], True, 10)

ye = [[4, 9], [5, 14]]
obstacles = Lazer("obj", "❗", ye, places["house"], 0,-1,True, 1)

running = True

def main():
    global running
    animate_text("Welcome to the game!", textDelay)
    print("Instructions: Move using 'w', 'a', 's', 'd'. Type 'q' to quit.")

    print_thread = threading.Thread(target=print_grid)
    input_thread = threading.Thread(target=player.move_player)

    print_thread.start()
    input_thread.start()

    # Create an ObstacleHandler and add your obstacles to it
    obstacle_handler = ObstacleHandler()
    obstacle_handler.add_obstacle(obstacles)

    # Start a new thread for the obstacle handler
    obstacle_thread = threading.Thread(target=obstacle_handler.move_obstacles)
    obstacle_thread.start()

    while running:
        time.sleep(framerate)

    input_thread.join()
    running = False
    print_thread.join()
    obstacle_thread.join()  # Join the obstacle thread

if __name__ == "__main__":
    main()