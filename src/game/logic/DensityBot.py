import random
from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class DensityBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    # def defendMechanism(self, board_bot: GameObject, board: Board):
    #     if ()

    def neededSteps (startingpos: Position, diamondpos: Position):
        return abs(basepos.x - diamondpos.x) + abs(basepos.y - diamondpos.y)

    def getDensity (diamond : GameObject, base : Position, botpos : Position):
        return ((diamond.points / neededSteps(base, diamond.position))*0.5 + (diamond.points/neededSteps(botpos, diamond.position))*0.5)

    def generatePreferedDiamondPath(self, board: Board, board_bot: GameObject):
        listdiamonds = board.diamonds()
        currDensityMax = board.diamonds[0]
        currDensityMaxPos = board.diamonds[0].position
        base = board_bot.properties.base
        position = board_bot.position
        for diamond in listdiamonds:
            density = getDensity(diamond, base, position)
            if density > currDensityMax:
                currDensityMax = density
                currDensityMaxPos = diamond.position
        self.goal_position = currDensityMaxPos

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        listdiamonds = board.diamonds()
        print(listdiamonds)
        if (props.diamonds == 5) or (props.diamonds == 4 and self.getDensity())  :
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        
        elif (listdiamonds.length <= 1):
            diamondbutton = board.game_objects.type == "DiamondButtonGameObject"
            self.goal_position = diamondbutton.position

        elif (self.goal_position not in listdiamonds.position):
            generatePreferedDiamondPath(board, board_bot)

        current_position = board_bot.position
            
        delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y
