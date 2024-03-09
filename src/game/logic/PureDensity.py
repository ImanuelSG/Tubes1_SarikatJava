import random
from typing import Optional, List
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class PureDensityBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    def needed_steps(self, starting_pos: Position, diamond_pos: Position) -> int:
        """Calculate the number of steps needed to reach the diamond position."""
        return abs(starting_pos.x - diamond_pos.x) + abs(starting_pos.y - diamond_pos.y)

    def get_density(self, diamond: GameObject, bot_pos: Position) -> float:
        """Calculate the density of a diamond based on its points and distance from the bot."""
        return diamond.properties.points / self.needed_steps(bot_pos, diamond.position)

    def generate_best_density(self, diamonds: List[GameObject], board_bot: GameObject) -> None:
        """Find the diamond with the highest density and set it as the goal position."""
        curr_density_max = 0
        curr_density_max_pos = diamonds[0].position
        
        bot_position = board_bot.position
        for diamond in diamonds:
            density = self.get_density(diamond, bot_position)
            if density > curr_density_max:
                curr_density_max = density
                curr_density_max_pos = diamond.position
            
        self.goal_position = curr_density_max_pos

    def next_move(self, board_bot: GameObject, board: Board) -> tuple:
        props = board_bot.properties
        base = board_bot.properties.base
        list_diamonds = board.diamonds
        diamond_button = [d for d in board.game_objects if d.type == "DiamondGameObject"]
        # If there are 5 diamonds in the inventory, move towards the base
        if props.diamonds == 5 : 
            self.goal_position = base
        # If there is only some diamonds left and there the distanc , move towards the diamond trigger button
        elif len(list_diamonds) == 3 and self.needed_steps(board_bot.position, self.goal_position) > self.needed_steps(diamond_button.position, self.goal_position):
            self.goal_position = diamond_button.position
        # If the goal position is not among the diamonds or it's not set yet, generate the best density
        elif all(self.goal_position != diamond.position for diamond in list_diamonds) or self.goal_position is None:
            self.generate_best_density(list_diamonds, board_bot)
        
        current_position = board_bot.position
        delta_x, delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)

        return delta_x, delta_y
