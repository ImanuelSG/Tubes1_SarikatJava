import random
from typing import Optional, List

from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class HeuristicDensityBot(BaseLogic):
    def __init__(self):
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0
        self.isending = False
    
    def needed_steps(self, starting_pos: Position, diamond_pos: Position) -> int:
        """Calculate the number of steps needed to reach the diamond position."""
        return abs(starting_pos.x - diamond_pos.x) + abs(starting_pos.y - diamond_pos.y)

    def get_density(self, diamond: GameObject, bot_pos: Position) -> float:
        """Calculate the density of a diamond based on its points and distance from the bot."""

        return diamond.properties.points / self.needed_steps(bot_pos, diamond.position)

    def generate_best_density(self, diamonds: List[GameObject], board_bot: GameObject) -> None:
        """Find the diamond with the highest density and set it as the goal position."""
        """But with special note that we have a threshold of 3 steps which means"""
        """Say that we have 2 best options of diamonds, 1 point with 5 steps or 2 points with 9 steps"""
        """It will choose the 1 point with 5 steps because the difference is more than 3"""
        """But if we have 1 point with 5 steps and 2 points with 8 steps, it will choose the 2 points"""

        curr_density_max = 0
        curr_density_max_pos = diamonds[0].position
        curr_density_max_points = 0
        curr_max_steps = 0

        sec_density_max = 0
        sec_density_max_pos = diamonds[0].position
        sec_density_max_points = 0
        sec_max_steps = 0

        bot_position = board_bot.position
        curr_diamond = board_bot.properties.diamonds
        for diamond in diamonds:
            points = diamond.properties.points
            density = self.get_density(diamond, bot_position)
            steps = self.needed_steps(bot_position, diamond.position)
            if curr_diamond == 4:
                if density > curr_density_max and diamond.properties.points == 1:
                    curr_density_max = density
                    curr_density_max_pos = diamond.position
                    curr_density_max_points = diamond.properties.points
                    curr_max_steps = self.needed_steps(bot_position, diamond.position)
                elif density > sec_density_max and diamond.properties.points == 1:
                    sec_density_max = density
                    sec_density_max_pos = diamond.position
                    sec_density_max_points = diamond.properties.points
                    sec_max_steps = self.needed_steps(bot_position, diamond.position)
            else:
                if density > curr_density_max:
                    curr_density_max = density
                    curr_density_max_pos = diamond.position
                    curr_density_max_points = diamond.properties.points
                    curr_max_steps = self.needed_steps(bot_position, diamond.position)
                elif density > sec_density_max:
                    sec_density_max = density
                    sec_density_max_pos = diamond.position
                    sec_density_max_points = diamond.properties.points
                    sec_max_steps = self.needed_steps(bot_position, diamond.position)
        
        if (curr_density_max_points == 2):
            if (curr_max_steps - sec_max_steps > 3 and sec_density_max_points == 1):
                curr_density_max_pos = sec_density_max_pos
        self.goal_position = curr_density_max_pos

    def next_move(self, board_bot: GameObject, board: Board):
        props = board_bot.properties
        list_diamonds = board.diamonds
        base = board_bot.properties.base
        diamond_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
       
        if (props.diamonds == 5) or (board_bot.properties.milliseconds_left < self.needed_steps(base, board_bot.position) * 1000 and board_bot.properties.milliseconds_left < 8000)  or self.isending:
            # Move to base
            if (board_bot.properties.milliseconds_left < self.needed_steps(base, board_bot.position) * 1000 and board_bot.properties.milliseconds_left < 8000):
                self.isending = True
            self.goal_position = base
        elif len(list_diamonds) == 3 and self.goal_position!=None and self.needed_steps(board_bot.position, self.goal_position) > self.needed_steps(diamond_button[0].position, self.goal_position):
            self.goal_position = diamond_button.position
        elif all(self.goal_position != diamond.position for diamond in list_diamonds) or self.goal_position is None:
            self.generate_best_density(list_diamonds, board_bot)

        current_position = board_bot.position
            
        delta_x, delta_y = get_direction(
                current_position.x,
                current_position.y,
                self.goal_position.x,
                self.goal_position.y,
            )

        return delta_x, delta_y
