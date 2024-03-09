from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class SquareDensity(BaseLogic):
    def __init__(self):
        self.goal_position: Optional[Position] = None
        self.target_path: List[GameObject] = []
        self.achieved_head: Optional[bool] = False
        self.path_head: Optional[GameObject] = None

    def __escape_from_enemy(self, my_bot:GameObject, board: Board) -> Position:
        list_bots = board.bots
        for a_bot in (list_bots):
            if (a_bot.properties.name != my_bot.properties.name):
                distance_x = abs(a_bot.position.x - my_bot.position.x)
                distance_y = abs(a_bot.position.y - my_bot.position.y)
                if distance_x == 1 and distance_y == 0:
                    print(a_bot.properties.name)    
                    return Position(x=my_bot.position.x, y=abs(my_bot.position.y-1))
                elif distance_y == 1 and distance_x == 0:
                    print(a_bot.properties.name)
                    return Position(x=abs(my_bot.position.x-1), y=my_bot.position.y)
                else:
                    return Position(x=my_bot.position.x, y=my_bot.position.y)

    def __max_area_to_distance(self, my_bot: GameObject, board: Board):
        self.achieved_head = False
        list_diamond = board.diamonds
        length = len(list_diamond)
        density = 0
        for i in range(length):
            count = 1
            temp_diamonds = [list_diamond[i]]
            curr_diamond = list_diamond[i]
            for j in range(length):
                if (i != j and abs(curr_diamond.position.x-list_diamond[j].position.x) <= 1 and abs(curr_diamond.position.y-list_diamond[j].position.y) <= 1):
                    if(my_bot.properties.diamonds != 4 or list_diamond[j].properties.points != 2):
                        temp_diamonds.append(list_diamond[j])
                        count += 1
            distance = abs(temp_diamonds[0].position.x - my_bot.position.x) + abs(temp_diamonds[0].position.y - my_bot.position.y)
            if (distance != 0):
                temp_density =  count / (distance * 5)
                if (temp_density > density):
                    density = temp_density
                    self.target_path = temp_diamonds
                    self.path_head = self.target_path[0]
        # print(self.target_path)

    def next_move(self, my_bot: GameObject, board: Board):
        ##initialize props
        props = board_bot.properties
        base = board_bot.properties.base
        list_diamonds = board.diamonds
        current_position = board_bot.position

        ##initialize teleporters
        list_teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        marco = list_teleporters[0]
        polo = list_teleporters[1]
        targetTeleporter = marco
        exitTeleporter = polo
        dm = self.needed_steps(marco.position,current_position)
        dp = self.needed_steps(polo.position,current_position)


        ##Cari teleporter terdekat
        if dp < dm:
            targetTeleporter = polo
            exitTeleporter=marco
        

        ##Cari jarak ke teleporter terdekat
        distance_to_targetTeleporter = self.needed_steps(targetTeleporter.position,current_position)


        escape_position = self.__escape_from_enemy(my_bot, board)
        if (escape_position == my_bot.position):
            if props.diamonds == 5:
                self.goal_position = props.base
            else:
                temp = []
                for x in (self.target_path):
                    if (x in board.diamonds):
                        temp.append(x)
                self.target_path = temp
                if(len(self.target_path) != 0):
                    if (props.diamonds == 4 and self.target_path[0].properties.points == 2):
                        self.target_path = self.target_path[1:]
                    elif (self.achieved_head == False and self.path_head not in self.target_path):
                        self.__max_area_to_distance(my_bot, board, targetTeleporter, exitTeleporter, distance_to_targetTeleporter )
                    elif (self.achieved_head == True):
                        if(my_bot.position == self.target_path[0]):
                            self.target_path = self.target_path[1:]
                    elif (my_bot.position == self.path_head.position):
                        self.achieved_head = True
                        self.target_path = self.target_path[1:]
                if(len(self.target_path) == 0):
                    self.__max_area_to_distance(my_bot, board, targetTeleporter, exitTeleporter, distance_to_targetTeleporter)
                self.goal_position = self.target_path[0].position
        else:
            print("Escape!")
            self.goal_position = escape_position

        print(self.goal_position)
        print([p.position for p in self.target_path])
        delta_x, delta_y = get_direction(
            my_bot.position.x,
            my_bot.position.y,
            self.goal_position.x,
            self.goal_position.y,
        )
        return delta_x, delta_y