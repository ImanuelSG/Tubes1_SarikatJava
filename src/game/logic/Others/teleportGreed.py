from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ...util import get_direction

class teleportGreed(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def getDistance(self,point1:Position,point2:Position):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    #bot adalah GameObject dengan properties
    #all others adalah GameObject
    # list diamonds board.diamonds
    def next_move(self, board_bot: GameObject, board: Board):
        list_teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        marco = list_teleporters[0]
        polo = list_teleporters[1]
        props = board_bot.properties
        #calculate shortest distance from teleporter
        current_position = board_bot.position
        targetTeleporter = marco
        exitTeleporter = polo
        dm = self.getDistance(marco.position,current_position)
        dp = self.getDistance(polo.position,current_position)
        if dp < dm:
            targetTeleporter = polo
            exitTeleporter=marco
        # Analyze new state
        if props.diamonds == 5 :
            # Move to base
            base = board_bot.properties.base
            teleporter_base_distance = self.getDistance(exitTeleporter.position,base)
            distance_to_targetTeleporter = self.getDistance(targetTeleporter.position,current_position)
            td = teleporter_base_distance + distance_to_targetTeleporter
            distanceBotBase = self.getDistance(base,current_position)
            if(td < distanceBotBase) and distance_to_targetTeleporter != 0:
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    targetTeleporter.position.x,
                    targetTeleporter.position.y,
                )  
                return delta_x,delta_y
            else:
                self.goal_position = base
        else:
            # gather diamond
            self.goal_position = None


        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            #diamond yg paling dekat dari player
            diamonds = board.diamonds
            diamond_pos = []
            for i in range(len(diamonds)):
                diamond_pos.append(diamonds[i].position)
            teleporter_diamond_distance =[]
            diamond_distance = []
            diamond_points = []
            for i in range(len(diamonds)):
                teleporter_diamond_distance.append(self.getDistance(diamond_pos[i],exitTeleporter.position))
                diamond_distance.append(self.getDistance(diamond_pos[i],current_position))
                diamond_points.append(diamonds[i].properties.points)
            distance_to_targetTeleporter = self.getDistance(targetTeleporter.position,current_position)
            total_teleporter_distance = distance_to_targetTeleporter + min(teleporter_diamond_distance)
            print(distance_to_targetTeleporter)
            if total_teleporter_distance < min(diamond_distance) and distance_to_targetTeleporter != 0 :
                #let's go to the teleporter
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    targetTeleporter.position.x,
                    targetTeleporter.position.y,
                )                
            else:
                #shortest distance procedure
                #watch out for accidental teleports !!!
                # if (current_position.x + 1 == marco.position.x and current_position.y == marco.position.y) or (current_position.x - 1 == marco.position.x and current_position.y == marco.position.y) or (current_position.x + 1 == polo.position.x and current_position.y == polo.position.y)  or (current_position.x - 1 == polo.position.x and current_position.y == polo.position.y) :
                #     return 0,1 # go up
                # elif (current_position.x == marco.position.x and current_position.y+1 == marco.position.y) or (current_position.x == marco.position.x and current_position.y-1 == marco.position.y) or (current_position.x == polo.position.x and current_position.y+1 == polo.position.y)or (current_position.x == polo.position.x and current_position.y-1 == polo.position.y):
                #     return -1,0 #goes to the left
                if props.diamonds == 4: #makes it so that it only searches for blue diamonds if inventory = 4
                    min_value = float('inf') 
                    for diamond, dis in zip(diamonds, diamond_distance):
                        
                        if diamond.properties.points == 1 and dis < min_value:
                            min_value = dis
                            position = diamond.position
                    ##[1-> merah,1,1,1]
                    chosenDiamond = position                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
                else:
                    chosenDiamond = diamond_pos[diamond_distance.index(min(diamond_distance))]

                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    chosenDiamond.x,
                    chosenDiamond.y,
                )
        return delta_x, delta_y

