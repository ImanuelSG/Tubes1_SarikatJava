from typing import Optional

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction

class ShortestDistance(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    #bot adalah GameObject dengan properties
    #all others adalah GameObject
    # list diamonds board.diamonds
    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        # Analyze new state
        if props.diamonds == 5 :
            # Move to base
            base = board_bot.properties.base
            self.goal_position = base
        else:
            # gather diamond
            self.goal_position = None

        current_position = board_bot.position
        if self.goal_position:
            # We are aiming for a specific position, calculate delta
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )
        else:
            #diamond yg paling dekat
            diamonds = board.diamonds
            diamond_pos = []
            for i in range(len(diamonds)):
                diamond_pos.append(diamonds[i].position)
            diamond_distance = []
            diamond_points = []
            for i in range(len(diamonds)):
                diamond_distance.append(((diamond_pos[i].x-current_position.x)**2+(diamond_pos[i].y-current_position.y)**2)**(1/2))
                diamond_points.append(diamonds[i].properties.points)
            if props.diamonds ==4: #makes it so that it only searches for blue diamonds if inventory = 4
                min_value = float('inf')  
                for dis, pts in zip(diamond_distance, diamond_points):
                    if pts == 1 and dis < min_value:
                        min_value = dis
                temp = min_value
                chosenDiamond = diamond_pos[diamond_distance.index(temp)]
            else:
                chosenDiamond = diamond_pos[diamond_distance.index(min(diamond_distance))]
            delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                chosenDiamond.x,
                chosenDiamond.y,
            )
        return delta_x, delta_y
