"""
class to create and control alien ship functionality
- creation
- moving
- shooting
- resetting
"""

from turtle import *
from PIL import Image
import operator
import random

# dictionary for mapping character to comparison operator
operator_dict = {
    ">": operator.gt,
    "<": operator.lt}


class AlienShips:
    def __init__(self, size, shape_img, shape_img_moving):

        self.alien_img_list = list(shape_img)  # list of original alien gif images
        self.alien_img_list_moving = list(shape_img_moving)  # list of moving (2nd) alien gif images
        self.alien_img_dims = self.get_alien_dimensions()  # list of gif img dimensions
        self.screen_size = size  # parent screen dimensions
        self.ship_spacing_x = self.screen_size[0] / 17  # alien x-axis spacing
        self.ship_spacing_y = self.screen_size[1] / 15  # alien y-axis spacing

        # create alien turtles for 1st and 2nd set of alien img gif shapes
        self.alien_ship_list = self.create_all_aliens(self.alien_img_list)
        self.alien_ship_list_moving = self.create_all_aliens(self.alien_img_list_moving)

        # container for all alien shots fired
        self.shots_fired = []

        # variable holding no. of columns originally
        self.original_column_length = len(self.alien_ship_list[0])

        # total number of aliens visible
        self.aliens_left = len(self.alien_ship_list) * len(self.alien_ship_list[0])

        # flag indicating which alien img is currently displayed
        self.first_shape_list = True
        # flag indicating current alien moving direction
        self.moving_right = True
        # flag indicating if one ship remaining
        self.last_ship = False
        # flag indicating if no more ships
        self.no_more_ships = False

    def get_highest_y_axis(self):
        """
        returns the top visible aliens rows y-axis
        """
        # ensures returned items are not None
        top_row = [alien for alien in self.alien_ship_list[0] if alien]
        top_row_y_axis = top_row[0].ycor()
        return top_row_y_axis

    def get_lowest_y_axis(self):
        """
        returns the bottom visible aliens rows y-axis
        """
        # ensures returned items are not None
        bottom_row = [alien for alien in self.alien_ship_list[-1] if alien]
        bottom_row_y_axis = bottom_row[0].ycor()
        return bottom_row_y_axis

    def get_lowest_visible_aliens(self):
        """
        return a list of the lowest visible aliens showing for each column
        """
        lowest_alien_list = []  # list holding lowest aliens (1 per row max)

        # variable to hold the current showing alien list
        alien_list = self.alien_ship_list if self.first_shape_list else self.alien_ship_list_moving

        # for each column
        for j in range(self.original_column_length):
            lowest_i = None
            # iterate over each row
            for i, row in enumerate(alien_list):
                if row[j]:  # if alien is visible (not None) in next row
                    lowest_i = i  # assign i to lowest_i

            if lowest_i is not None:  # i.e. there is an alien showing in that column
                lowest_alien_list.append(alien_list[lowest_i][j])  # add that alien to list

        return lowest_alien_list

    def check_shot_in_range(self, shot_y, shot_x):
        """
        Checks if a shot will hit an alien turtle.
        If hit - then removes the turtle from display and deletes the turtle.
         - assigns None in place of Turtle object
         - removes entire row from alien turtle lists if all items in row are None
        """

        # pixels y and x-axis offset from alien turtle img centre
        y_axis_offset = self.alien_img_dims[0][1]/2
        x_axis_offset = self.alien_img_dims[0][0]/2

        # assign current and next alien list dependent on which is currently visible
        if self.first_shape_list:
            alien_list = list(reversed(self.alien_ship_list))
            next_alien_list = list(reversed(self.alien_ship_list_moving))
        else:
            alien_list = list(reversed(self.alien_ship_list_moving))
            next_alien_list = list(reversed(self.alien_ship_list))

        num_rows = len(self.alien_ship_list)-1  # last index of the list

        for i, row in enumerate(alien_list):
            available_aliens_row = [alien for alien in row if alien]  # get all alien Turtles (visible) in current row
            # if shot y-axis within spaceship y-axis
            if (available_aliens_row[0].ycor() - y_axis_offset # bottom of alien img
                    <= shot_y <=
                    available_aliens_row[0].ycor() + y_axis_offset):  # top of alien img

                # for each alien ship of that row
                for j, aliens_ship, in enumerate(row):

                    if aliens_ship:  # if not hit previously / not None

                        # if shot x axis is within the alien x-axis
                        if (aliens_ship.xcor() - x_axis_offset  # left side of alien img
                                <= shot_x <=
                                aliens_ship.xcor() + x_axis_offset):  # right side of alien img

                            # hide and clear alien turtle in both lists
                            alien_list[i][j].hideturtle()
                            alien_list[i][j].clear()
                            next_alien_list[i][j].hideturtle()
                            next_alien_list[i][j].clear()
                            # assign to None to remove resources
                            alien_list[i][j] = None
                            next_alien_list[i][j] = None

                            self.aliens_left -= 1  # decrement no. of aliens left

                            if self.aliens_left == 1:
                                self.last_ship = True

                            # if all items on this row are None (no aliens) - then remove the row
                            if all(ship is None for ship in row):
                                del self.alien_ship_list[num_rows-i]
                                del self.alien_ship_list_moving[num_rows-i]

                            # if alien hit was the last alien
                            if self.aliens_left == 0:
                                self.last_ship = False
                                self.no_more_ships = True

                            return True  # true if alien has been hit
        return False  # false if not hit


    def reset_alien_ships(self):
        """
        Removes and clears all previous alien turtles, and frees memory.
        Recreates all alien turtles in original position
        """
        # hide, clear, and delete any previous alien turtles
        for alien_list in [self.alien_ship_list, self.alien_ship_list_moving]:
            for i in range(len(alien_list)):
                for j in range(len(alien_list[i])):
                    if alien_list[i][j]:
                        alien_list[i][j].hideturtle()
                        alien_list[i][j].clear()
                        alien_list[i][j] = None

        # recreate alien turtle lists
        self.alien_ship_list = None
        self.alien_ship_list = self.create_all_aliens(self.alien_img_list)
        self.alien_ship_list_moving = None
        self.alien_ship_list_moving = self.create_all_aliens(self.alien_img_list_moving)

        # reset class variables and flags
        self.first_shape_list = True
        self.moving_right = True
        self.last_ship = False
        self.no_more_ships = False
        self.aliens_left = len(self.alien_ship_list) * len(self.alien_ship_list[0])

    def remove_all_shots(self):
        """
        Clears all alien shot turtles
        """
        for shot in self.shots_fired:
            shot.hideturtle()
            shot.clear()
            shot = None
        self.shots_fired = []

    def add_shot(self, x, y):
        """
        Adds an alien shot turtle at position x, y.
        Returns a turtle object
        """
        turtle = Turtle()
        turtle.penup()
        turtle.shape("square")
        turtle.color('red')
        turtle.shapesize(stretch_len=0.2, stretch_wid=1)
        turtle.goto(x, y)
        return turtle

    def random_shot(self):
        """
        Creates an alien shot - with coordinates from a random alien ship still visible
        """
        available_alien_ship = []  # holds all visible ships
        for i, row in enumerate(self.alien_ship_list):
            for j, ship in enumerate(row):
                if ship:  # if not None
                    available_alien_ship.append(self.alien_ship_list[i][j])

        # get random visible aliens coordinates - and create a shot
        random_ship = random.choice(available_alien_ship)
        coordinates = random_ship.pos()
        self.shots_fired.append(self.add_shot(coordinates[0],
                                              coordinates[1] - (self.alien_img_dims[0][1] / 2)))

    def move_shots(self, move_amount=5):
        """
        Moves shots fired down by 'move_amount'
        """
        if len(self.shots_fired) > 0:
            for shot in self.shots_fired:
                shot.sety(shot.ycor() - move_amount)

    def move(self, move_amount=10):
        """
        Moves all the ships by 'move_amount', dependent on current moving direction (L or R).
        If moving alien ships would move ships passed the screen boundary - then aliens
          will instead move down the y-axis and the direction is reversed
        """

        # whether the move amount is positive or negative dependent on current direction
        direction = move_amount if self.moving_right else - move_amount

        alien_lists = [self.alien_ship_list, self.alien_ship_list_moving]

        hit_wall = False
        if self.check_hit_wall():  # if will not hit wall when moved
            for alien_ships in alien_lists:
                for row in alien_ships:
                    for ship in row:
                        if ship:  # if ship is not None
                            ship.setx(ship.xcor() + direction)  # update the x-axis

        else:  # if moving will hit wall when moved
            for alien_ships in alien_lists:
                for row in alien_ships:
                    for ship in row:
                        if ship:  # if ship is not None
                            # move the alien down
                            ship.sety(ship.ycor() - (self.ship_spacing_y/1.5))

            # re-assign moving flag if hit wall
            if self.moving_right:
                self.moving_right = False
            else:
                self.moving_right = True

            hit_wall = True

        return hit_wall  # return hit wall indicator


    # FINE - checks if hit the wall
    def check_hit_wall(self):
        """
        checks if the move amount applied to the aliens would cause the aliens to be passed the screen width.
        Returns True if move amount will not go passed the screen, False if will go passed the screen.
        """

        def get_furthest_left_index():
            """
            returns the furthest left alien index
            - breaks early if column index = 0
            """
            current_alien_list = self.alien_ship_list if self.first_shape_list else self.alien_ship_list_moving
            furthest_row = 0
            furthest_column = 20  # random high num, greater than any column index
            for i, row in enumerate(current_alien_list):
                for j, ship in enumerate(row):
                    if ship:  # if Turtle (not None)
                        # if column index is less that furthest column
                        if j < furthest_column:
                            # assign as furthest
                            furthest_row = i
                            furthest_column = j
                        if furthest_column == 0:  # break early if index at 0 (none further left)
                            return furthest_row, furthest_column
            return furthest_row, furthest_column

        def get_furthest_right_index():
            """
            returns the furthest right alien index
            - breaks early if column index = max column index
            """
            current_alien_list = self.alien_ship_list if self.first_shape_list else self.alien_ship_list_moving
            max_column_index = len(self.alien_ship_list[0]) - 1
            furthest_row = 0
            furthest_column = 0
            for i, row in enumerate(current_alien_list):
                for j, ship in enumerate(row):
                    if ship:  # if Turtle (not None)
                        # if column index greater than furthest column
                        if j > furthest_column:
                            # assign as furthest
                            furthest_row = i
                            furthest_column = j
                        if j == max_column_index:  # break early if index at max column index
                            return furthest_row, furthest_column
            return furthest_row, furthest_column

        # assign variables dependent on if moving left or right
        if self.moving_right:
            move = 10
            greater_lesser = ">"
            positive_negative = 1
            furthest_index = get_furthest_right_index()
        else:
            move = -10
            greater_lesser = "<"
            positive_negative = -1
            furthest_index = get_furthest_left_index()

        # comparison operator between the furthest left or right alien to the left or right screen side
        if operator_dict[greater_lesser](
                self.alien_ship_list[furthest_index[0]][furthest_index[1]].xcor()
                + (positive_negative * self.alien_img_dims[0][0] / 2) + move,
                (positive_negative * self.screen_size[0] / 2)):
            return False  # false if will pass the screen
        else:
            return True  # True if does not pass the screen

    def switch_ships(self, switch=True):
        """
        Changes which list of alien turtles is visible - gives the effect of the img is moving.
        Switch set to True - makes the previously hidden alien list visible.
        """
        # get current visible alien list and hidden alien list
        if self.first_shape_list:
            current_alien_list = self.alien_ship_list
            next_alien_list = self.alien_ship_list_moving
            self.first_shape_list = False  # reverse flag
        else:
            current_alien_list = self.alien_ship_list_moving
            next_alien_list = self.alien_ship_list
            self.first_shape_list = True  # reverse flag

        # hide each alien turtle
        for row in current_alien_list:
            for alien_ship in row:
                if alien_ship:
                    alien_ship.hideturtle()
                    alien_ship.clear()
        if switch:
            # display each alien turtle
            for i, row in enumerate(next_alien_list):
                for j, alien_ship in enumerate(row):
                    if alien_ship:
                        alien_ship.showturtle()

    def get_alien_dimensions(self):
        """
        gets the alien img height and width dimensions
        """
        dimensions = []
        for alien_img in self.alien_img_list:
            img = Image.open(alien_img)
            width = img.width
            height = img.height
            dimensions.append([width, height])
        return dimensions

    def create_all_aliens(self, img_list):
        """
        Creates all alien turtles - default 5 rows and 11 aliens per column
        Calculates the alien turtle spacing based on ship_spacing_x and ship_spacing_y.
        'img_list' = a list of alien img gif file (previously registered as turtle shapes
        """
        # 1. calc the initial x-axis position
        # width of the available screen that will hold alien turtles
        ship_container_size_x = self.ship_spacing_x * 11
        # position of this alien container width so it is centred - left x coordinate
        left_side_offset = - self.screen_size[0] / 2 + ((self.screen_size[0] - ship_container_size_x)/2)
        # then centre the x-axis position:
        initial_x_centred = left_side_offset + (self.ship_spacing_x /2)
        starting_x = initial_x_centred

        # 2. calc the initial y-axis position
        ship_container_size_y = self.ship_spacing_y * 5  # container size for aliens - y-axis
        top_side_offset = self.screen_size[1] / 2 - (ship_container_size_y/2)  # length from top of screen
        initial_y_centred = top_side_offset - (self.ship_spacing_y /2)  # subtracting img dims y-axis
        starting_y = initial_y_centred


        alien_ships_container = []
        for i in range(5):  # for each row
            # which rows will have which alien gif image
            if i < 1:
                alien_img = img_list[0]
            elif i < 3:
                alien_img = img_list[1]
            else:
                alien_img = img_list[2]

            row = []
            for j in range(11):  # per column
                row.append(self.create_ship(alien_img,
                                            starting_x,
                                            starting_y))  # create turtle with alien gif image
                starting_x += self.ship_spacing_x  # increment the x-axis position
            starting_y -= self.ship_spacing_y  # increment the y-axis position
            starting_x = initial_x_centred  # reset the x-axis position to far left
            alien_ships_container.append(row)

        return alien_ships_container

    def create_ship(self, alien_shape, x, y):
        """
        Create a turtle object with alien img.
        Alien shape must be a registered turtle shape.
        """
        turtle = Turtle()
        turtle.penup()
        turtle.shape(alien_shape)
        turtle.goto(x, y)
        return turtle

