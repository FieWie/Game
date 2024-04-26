grid_size = 9
player = [4, 5]
door = [8, 4]
chest = [8, 0]
lake = [7,1],[7,2],[7,0],[7,3],[7,4],[7,5],[7,6],[7,8],[7,9],[6,0],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6],[6,8],[6,9]
brige = [7,7],[6,7]
stig = [2,6],[3,6],[4,7],[5,7],[1,6],[3,7],[8,7]
import random
import time

movment = 1
def roll_d20():
    return random.randint(1, 20)


antal_rullingar = 1





def print_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            if [i, j] == player:
                print("🈸", end=" ")
            elif [i, j] == door:
                print("🚪", end=" ")
            elif [i, j] == chest:
                print("💾", end=" ")
            else:
                print("⬛", end=" ")
        print()

def move_player(move):
    global player
    x, y = player
    if move == "w" and x > 0:
        player = [x - 1, y]
    elif move == "s" and x < grid_size - 1:
        player = [x + 1, y]
    elif move == "a" and y > 0:
        player = [x, y - 1]
    elif move == "d" and y < grid_size - 1:
        player = [x, y + 1]
def outside():
    for i in range(grid_size):
        for j in range(grid_size):
            if[i, j] == player:
                print("🈸", end=" ")
            elif [i ,j] == house:
                print("🏠", end=" ")
            elif [i ,j] in lake:
                print("🟦", end=" ")
            elif [i, j] == enemy:
                print("🦧", end=" ")
            elif [i, j] in brige:
                print("🟫", end=" ")
            elif [i, j] in stig:
                print("⬛", end=" ")    
            else:
                print("🟩", end=" ")
        print()

def youded():
    for i in range(grid_size):
        for j in range(grid_size):
            if [i, j] == player:
                print("💀", end=" ")
            else:
                print("⬛", end=" ")
        print()        
                
def respawn():
    print()

    



class weapon:
    def __init__(self, damage, Durability):
        self.damage = damage
        self.Durability = Durability
        

Sword = weapon(2,10)



print_grid()

enemy = []

while True:
    move = input("Vart vill du gå? (w/s/a/d): ").lower()
    if move == "q":
        print("Avslutar spelet.")
        break
    move_player(move)
    print_grid()

    if player == chest:
        sword = input("You want to take the sword?(yes/no)").lower()
        if sword == "yes":
            print("You gained the sword")
        elif sword == "no":
            print("You don't like sharp things pussy")    
    
    if player == door:
        answer = input("You want to go outside? (yes/no): ").lower()
        if answer == "yes":
            print("Go go outside")
            player = [1, 6]
            house = [0, 6]
            enemy = [3, 3]
            
            

            outside() 


            while True:
                    move = input("Vart vill du gå? (w/s/a/d): ").lower()
                    if move == "q":
                        print("Avslutar spelet.")
                        break
                    move_player(move)
                    outside()

                    enemy[1] += movment
                    if enemy[1] == 0 or enemy[1] == grid_size - 1:
                        movment *= -1

                    if player == house:
                        break
                    if player in lake:
                        print("You can't swim you idiot")
                        time.sleep(2)
                        youded()
                        exit()

                    if player == enemy:
                        fight = input("Want to fight the monster yes or no: ")
                        if fight == "yes":
                            time.sleep(2)
                            print("roll for damage")

                            for i in range(antal_rullingar):
                                
                                resulat = roll_d20()
                                print(f"Dice {i+1}: {resulat}")
                                time.sleep(2)

                                if(resulat > 10):
                                    print("You have succesfully killed the monster")
                                    for i in range(grid_size):
                                        for j in range(grid_size):
                                            if [i, j] == enemy:
                                                print("💀", end=" ")
                                    
                                    
                                else:
                                    youded()
                                    time.sleep(2)
                                    print("you died")
                                    exit()
                                    
                        elif fight == "no":
                    
                            print("nice")    



            
        else:
            print("you stay inside")
