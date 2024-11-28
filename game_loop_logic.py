"""
Module helping the interactions between classes for game functionality
- helps avoid cluttering in main game loop logic
"""
import operator

operator_dict = {
    ">": operator.gt,
    "<": operator.lt}

def check_shot_hit_block(shot_list, blocks):
    """
    checks if an alien or spaceship shot will hit a block in the game
    - if the shots y-axis and x-axis are withing the blocks then the block and the
      shots coordinates are passed to block class to remove the hot block
    """
    for shot in shot_list:
        # if within the y axis range of blocks
        if blocks.block_bottom_y_axis <= shot.ycor() <= blocks.block_top_y_axis + 6:
            # iterate over each block
            for i, single_block in enumerate(blocks.block_coordinates):
                # if shot within the block x-axis
                if (single_block[0][0][0] - blocks.block_size/2  # left block square x-ax - square pixel offset
                        <= shot.xcor() <=
                        single_block[0][-1][0] + blocks.block_size/2):  # right block square x-ax - square pixel offset
                    # pass to block class to remove block square
                    block_hit = blocks.shot_in_range(i, shot.pos())

                    if block_hit:  # remove the shot if hit the block
                        shot.hideturtle()
                        shot.clear()
                        shot_list.pop(shot_list.index(shot))


def check_alien_hit_block(aliens, blocks):
    """
    checks if an alien spaceship has hit a block
    - if an alien spaceship y-axis and x-axis are withing the blocks then the
      alien coordinates and block number are passed to block class to remove relevant block squares
    """
    # size of alien img y-axis offset from centre of turtle
    alien_y_axis_offset = ((aliens.alien_img_dims[0][1]) / 2) - 1

    # get the lowest alien y-axis
    lowest_alien_y = aliens.get_lowest_y_axis() - alien_y_axis_offset

    # checks if lowest alien y-axis within the y axis range of the blocks
    if blocks.block_top_y_axis + 10 >= lowest_alien_y >= blocks.block_bottom_y_axis - 10:

        # get the list of lowest aliens spaceships per row - subset of all alien spaceships
        alien_list = aliens.get_lowest_visible_aliens()

        # size of alien img x-axis offset from centre of turtle
        alien_x_axis_offset = - (aliens.alien_img_dims[0][0] / 2) - 5
        if aliens.moving_right:
            alien_x_axis_offset = abs(alien_x_axis_offset)

        # for each alien in the bottom alien row list
        for single_alien in alien_list:

            # if alien within the block y-axis
            if blocks.block_top_y_axis + 10 >= single_alien.ycor() - alien_y_axis_offset >= blocks.block_bottom_y_axis - 10:

                # for each block
                for i, single_block in enumerate(blocks.block_coordinates):
                    # define the left and right block boundary
                    block_left_side = single_block[0][0][0] - blocks.block_size/2
                    block_right_side = single_block[0][-1][0] + blocks.block_size/2

                    # if alien within the x-axis of the block
                    if block_left_side <= single_alien.xcor() + alien_x_axis_offset <= block_right_side:
                        # pass to block class to remove relevant block squares
                        block_hit = blocks.shot_in_range(i,
                                                         (single_alien.xcor() + alien_x_axis_offset,
                                                          single_alien.ycor() - alien_y_axis_offset),
                                                         alien=True,
                                                         moving_right=aliens.moving_right)


def check_passed_line(shot_list, ref_object, spaceship=False):
    """
    removes alien shots if passed a boundary line
    """
    # diff. comparison operator dependant on if spaceship or alien shot
    greater_lesser = ">" if spaceship else "<"
    for shot in shot_list:
        # if shit passed y-axis of screen boundary
        if operator_dict[greater_lesser](shot.ycor(), ref_object.boundary_line_y):
            # remove the shot turtle
            shot.hideturtle()
            shot.clear()
            shot_list.pop(shot_list.index(shot))
            del shot


def check_shot_hit_space_ship(shot_list, space_ship):
    """
    checks if alien shot will hit the user space ship
    - calls space_ship class for shot hit functionality
    return: Boolean - if user has more lives left
    """
    for shot in shot_list:
        # if shot within the y-axis range of spaceship
        if space_ship.main_ship_bottom <= shot.ycor() <= space_ship.main_ship_top:
            # if shot within the x-axis range of spaceship
            if (space_ship.main_ship.xcor() - space_ship.main_ship_off_centre
                    <= shot.xcor() <=
                    space_ship.main_ship.xcor() + space_ship.main_ship_off_centre):
                # pass to space_ship class - returns indicator of more lives
                more_lives = space_ship.shot_in_range()
                if more_lives:
                    # remove shot
                    shot.hideturtle()
                    shot.clear()
                    shot_list.pop(shot_list.index(shot))
                    del shot
                    return True
                else:
                    return False
    return True


def check_shot_hit_alien(shot_list, aliens, space_ship):
    """
    checks if spaceship shot will hit an alien spaceship
    - if the shots y-axis are withing the aliens -
      pass the shot coordinates to alien_ships class for hit functionality
    Return: True if hit alien, False if not hit alien
    """
    # get top and bottom y-axis for remaining alien spaceships
    top_alien_y = aliens.get_highest_y_axis()
    bottom_alien_y = aliens.get_lowest_y_axis() - (aliens.alien_img_dims[0][1] / 2)  # subtract img x-axis offset

    shot_y_axis_offset = (space_ship.shot_width * 20)/2  # pixel offset from shot turtle centre

    for shot in shot_list:
        # if shot within the visible alien y-axis range
        if top_alien_y >= shot.ycor() + shot_y_axis_offset >= bottom_alien_y:

            # passes to alien_ships for hit functionality
            hit = aliens.check_shot_in_range(shot.ycor() + shot_y_axis_offset,
                                             shot.xcor())
            if hit: # if hit alien - remove shot
                shot.hideturtle()
                shot.clear()
                shot_list.pop(shot_list.index(shot))
                shot = None
                del shot
                return True
    return False


def check_alien_passed_finish(aliens, main_ship):
    """
    checks whether the lowest visible alien y-axis has passed the user y-axis
    """
    bottom_alien_y = aliens.get_lowest_y_axis()  # get lowest alien y-axis
    if bottom_alien_y <= main_ship.main_ship_top:
        return True  # if lower than user
    return False  # not lower



