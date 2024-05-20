
def move_player(self):
        print("Where do you want to go? (w/s/a/d): ")
        move = msvcrt.getch().decode('utf-8').lower()
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

        player.setPosition(newX, newY)      


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
