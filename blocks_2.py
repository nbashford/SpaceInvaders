"""
class for creating and managing the blocks displayed in the game
- creates initial blocks
- controls shot hit functionality
- controls alien hit functionality
- resets blocks - makes blocks shorter at every level increment
"""

from turtle import *
import math


class Blocks:
    def __init__(self, size, rows, columns):

        # holds the initial size of a block
        self.brick_rows = rows
        self.brick_columns = columns

        # main screen size (w, h)
        self.screen_size = size

        # create the initial block coordinates (single block)
        self.initial_block_hit_coordinates = self.create_initial_block_coordinates(self.brick_rows,
                                                                                   self.brick_columns,
                                                                                   level=1)

        self.block_top_y_axis = (-self.screen_size[1]/2)/ 3   # initial block top y-axis
        self.initial_x = (-self.screen_size[0]) / 2   # initial block left x-axis

        self.block_size = 10  # pixels for square shape - default = 20
        # for aligning block placements
        self.block_off_centre = (((self.block_size * self.brick_rows) / 2) + (self.block_size / 2))

        # holds initial (top left) x and y coordinates for each block
        self.blocks_list = []
        self.get_block_positions()

        # holds each block
        self.block_coordinates = []
        for block in self.blocks_list:
            # creates block with updated coordinates based on the blocks_list position
            self.block_coordinates.append(self.set_block_hit_positions(block))

        # get the block bottom y-axis
        self.block_bottom_y_axis = self.block_coordinates[0][-1][0][1]

    def create_initial_block_coordinates(self, rows, columns, level=1):
        '''
        create initial block coordinates starting from (x=0, y=0),
           decrementing by 10 for each column and for each row.
        - coordinates are appended to a list, with additional flags,
            indicating:
             - [2] = the Turtle object (or None)
             - [3] = if turtle hit (or None)  (not displayed
             - [4] = if Turtle should be initially drawn
        '''

        # define block column indexes to not draw
        left_none_brick = math.floor(self.brick_columns / 4)
        right_none_brick = math.ceil(self.brick_columns * (3/4))
        none_blocks = [i for i in range(left_none_brick, right_none_brick)]

        # define block rows to apply block column indexes to not draw
        applied_rows = self.brick_rows - level - 1

        initial_coordinates = []
        y = 0
        for j in range(0, - rows * 10, -10):  # per row
            row = []
            z = 0
            for i in range(0, columns * 10, 10):  # per column
                # if meets condition to not draw turtle
                if z in none_blocks and y >= applied_rows:
                    # [4] will be False - indicating no turtle to be created
                    row.append([i, j, None, True, False])
                else:
                    row.append([i, j, None, False, True])
                z += 1
            initial_coordinates.append(row)
            y += 1

        return initial_coordinates


    def get_block_positions(self, num_blocks=5):

        """
        gets each blocks top left x, y coordinates for each block
        - to then be applied to the initial block coordinates
        - evenly spaces each block relative to the screen width
        """
        block_gap = self.screen_size[0] / num_blocks
        initial_x = self.initial_x - self.block_off_centre

        for i in range(num_blocks):
            if i != 0:
                self.blocks_list.append([initial_x, self.block_top_y_axis])
            initial_x += block_gap


    def set_block_hit_positions(self, block):
        """
        iterates over the initial_block_hit_coordinates and applies the top left x, y coordinate
        for that block to the coordinates, and adds/creates turtle object at index [2]
        """
        x_difference = block[0]  # initial x-axis coordinate for that block
        y_difference = block[1]  # initial y-axis coordinate for that block

        applied_difference = [[[column[0] + x_difference,  # add the far left-block x-axis
                                column[1] + y_difference,  # add the top block y-axis
                                self.draw_block_hit(x=column[0] + x_difference,
                                                    y=column[1] + y_difference,
                                                    draw=column[4]),  # create a block square
                                column[3]] for column in row] for row in self.initial_block_hit_coordinates]

        return applied_difference  # return new block list holding: coordinates, turtle, and hit flag indicator

    def draw_block_hit(self, x, y, draw):
        """
        draws the turtle at position x, y, if passed draw variable is true.
        Return: Turtle, or None if draw=None
        """
        if draw:
            turtle = Turtle()
            turtle.penup()
            turtle.shape("square")
            turtle.color("green")
            # define square size relative to default 20 pixels square
            turtle.shapesize(stretch_wid=self.block_size/20, stretch_len=self.block_size/20)
            turtle.goto(x, y)
            return turtle
        else:
            return None

    def hide_hit_square(self, block, i, j):
        """
        clears and hides Turtle, sets hit flag to True
        """
        block[i][j][2].hideturtle()
        block[i][j][2].clear()
        block[i][j][2] = None
        block[i][j][3] = True

    def shot_in_range(self, block_number, shot_coordinate, alien=False, moving_right=None):
        """
        controls functionality to remove block squares
        - for spaceship or alien spaceship shots hitting block
            removes single block
        - or alien spaceship hitting shit
        - if alien has hit block - it removes n number of blocks adjacent or above the hit square
                so game shows all squares the alien img hits are removed
        block_number: index for block_coordinates
        shot_coordinate: x, and y position of shot or alien position
        alien: boolean flag indicating if alien img has hit
        moving_right: flag indicating the direction the alien is moving
        """

        def hit_adjacent_squares(block, i, j, moving_right):
            """
            iterates over the 4 previous or 4 ahead columns of the relevant block,
            based on the direction the alien is moving.
            for each column it iterates over, the inner function hit_above_square is called,
            which iterates over all the rows above for that column.
            for each row / each column applicable, that square is removed
            """

            def hit_above_square(block, i, j):
                """
                iterates over all squares above the passed column and initial row and removes the turtle
                """
                for num_row in range(i, i - 4, -1):
                    if num_row < 0:
                        return  # avoid index error
                    try:
                        if not block[num_row][j][3]:  # remove turtle if visible
                            self.hide_hit_square(block, num_row, j)
                    except IndexError:
                        break  # avoid index error

            if moving_right:  # search columns on the left
                for num_column in range(j+1, j-4, -1):
                    if num_column < 0:
                        return  # avoid index error
                    hit_above_square(block, i, num_column)  # pass to function to search rows above
            else:  # search columns on the right
                for num_column in range(j-1, j + 4, 1):
                    hit_above_square(block, i, num_column)  # pass to function to search rows above

        block = self.block_coordinates[block_number]  # get correct block

        for i, row in enumerate(block):
            # if shot/alien y-axis within this block rows y-axis
            if row[0][1] - 7 <= shot_coordinate[1] <= row[0][1] + 7:

                for j, column in enumerate(row):
                    # find the block square that is hit
                    if column[0] - 5 <= shot_coordinate[0] <= column[0] + 5:

                        # if hit by a shot (not alien img)
                        if not alien:
                            if not column[3]:  # if hit square visible
                                self.hide_hit_square(block, i, j)  # remove square turtle
                                return True

                        else:  # hit by an alien
                            hit_adjacent_squares(block, i, j, moving_right)

        return False

    def reset_bricks(self, level=1, rows=None):
        """
        resets and redraws the blocks.
        Redraws the blocks with the new level passed
        """
        if level > 1:  # next level
            self.brick_rows -= 1  # decrement brick_rows so blocks are shorter
        if rows:  # directly set the number of rows (end game)
            self.brick_rows = rows

        # recreate initial block coordinates
        self.initial_block_hit_coordinates = self.create_initial_block_coordinates(self.brick_rows,
                                                                                   self.brick_columns,
                                                                                   level=level)
        # reset blocks list
        self.blocks_list = None
        self.blocks_list = []
        self.get_block_positions()

        # hide, clear, and free up resources/memory of old block turtles
        for block in self.block_coordinates:
            for row in block:
                for column in row:
                    if column[2] is not None:
                        column[2].hideturtle()
                        column[2].clear()
                        column[2] = None

        self.block_coordinates = None

        # recreate blocks
        self.block_coordinates = []
        for block in self.blocks_list:
            self.block_coordinates.append(self.set_block_hit_positions(block))

