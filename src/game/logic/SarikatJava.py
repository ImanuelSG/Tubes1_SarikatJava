from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class sarikatJava(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    #bot adalah GameObject dengan properties
    #all others adalah GameObject
    # list diamonds board.diamonds
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
    
    def getDistance(self,point1:Position,point2:Position):
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)

    def next_move(self, board_bot: GameObject, board: Board):
        current_position = board_bot.position
        escapePosition = self.__escape_from_enemy(board_bot,board)
        if escapePosition ==  current_position:
            list_teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]
            marco = list_teleporters[0]
            polo = list_teleporters[1]
            props = board_bot.properties
            #calculate shortest distance from teleporter
            
            targetTeleporter = marco
            exitTeleporter = polo
            # dm = abs(marco.position.x-current_position.x)+abs(marco.position.y-current_position.y)
            # dp = abs(polo.position.x-current_position.x)+abs(polo.position.y-current_position.y)
            dm = self.getDistance(marco.position,current_position)
            dp = self.getDistance(polo.position,current_position)
            if dp < dm:
                targetTeleporter = polo
                exitTeleporter=marco
            # Analyze new state
            if props.diamonds == 5 :
                # Move to base
                base = board_bot.properties.base
                # teleporter_base_distance = abs(exitTeleporter.position.x - base.x) + abs(exitTeleporter.position.y - base.y)
                teleporter_base_distance = self.getDistance(exitTeleporter.position,base)
                # distance_to_targetTeleporter = abs(targetTeleporter.position.x-current_position.x)+abs(targetTeleporter.position.y-current_position.y)
                distance_to_targetTeleporter = self.getDistance(targetTeleporter.position,current_position)
                td = teleporter_base_distance + distance_to_targetTeleporter
                #distanceBotBase = abs(base.x-current_position.x)+abs(base.y-current_position.y)
                distanceBotBase = self.getDistance(base,current_position)
                if(td < distanceBotBase):
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


            print(current_position)
            if self.goal_position:
                # We are aiming for a specific position, calculate delta
                print(self.goal_position)
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
                if total_teleporter_distance < min(diamond_distance):
                    #let's go to the teleporter
                    delta_x, delta_y = get_direction(
                        current_position.x,
                        current_position.y,
                        targetTeleporter.position.x,
                        targetTeleporter.position.y,
                    )                
                else:
                    #shortest distance procedure
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
        else:
            delta_x, delta_y = get_direction(
            current_position.x,
            current_position.y,
            escapePosition.x,
            escapePosition.y
        )
        return delta_x, delta_y

