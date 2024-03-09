from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class points(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

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
        dm = abs(marco.position.x-current_position.x)+abs(marco.position.y-current_position.y)
        dp = abs(polo.position.x-current_position.x)+abs(polo.position.y-current_position.y)
        if dp < dm:
            targetTeleporter = polo
            exitTeleporter=marco
        # Analyze new state
        if props.diamonds == 5 :
            # Move to base
            base = board_bot.properties.base
            teleporter_base_distance = abs(exitTeleporter.position.x - base.x) + abs(exitTeleporter.position.y - base.y)
            distance_to_targetTeleporter = abs(targetTeleporter.position.x-current_position.x)+abs(targetTeleporter.position.y-current_position.y)
            td = teleporter_base_distance + distance_to_targetTeleporter
            distanceBotBase = abs(base.x-current_position.x)+abs(base.y-current_position.y)
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
            #gather red diamond
            redDiamonds = [d for d in board.diamonds if d.properties.points == 2]
            diamondDistance = []
            diamonds = board.diamonds
            allDiamondDistance = []
            for i in range(len(diamonds)):
                allDiamondDistance.append(abs(diamonds[i].position.x-current_position.x)+ abs(diamonds[i].position.y - current_position.y))
            for i in range(len(redDiamonds)):
                diamondDistance.append(abs(redDiamonds[i].position.x - current_position.x)+ abs(redDiamonds[i].position.y - current_position.y))
            if props.diamonds == 4: #makes it so that it only searches for blue diamonds if inventory = 4
                min_value = float('inf') 
                for diamond, dis in zip(diamonds, allDiamondDistance):
                    
                    if diamond.properties.points == 1 and dis < min_value:
                        min_value = dis
                        position = diamond.position
                ##[1-> merah,1,1,1]
                chosenDiamond = position                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            else:
                if len(redDiamonds) == 0:
                    chosenDiamond = diamonds[allDiamondDistance.index(min(allDiamondDistance))].position
                else:
                    chosenDiamond = redDiamonds[diamondDistance.index(min(diamondDistance))].position
            print("diamond")
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                chosenDiamond.x,
                chosenDiamond.y,
            )                
        return delta_x,delta_y
