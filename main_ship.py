"""
Class for creating and controlling main user spaceship functionality
"""

from turtle import *
from PIL import Image


class MainShip:
    def __init__(self, ship_img, screen_size):

        self.screen_dims = screen_size  # parent screen dimensions
        self.y_axis_main = (-self.screen_dims[1]/2) + (self.screen_dims[1]/8)  # spaceship y-axis
        self.ship_image = ship_img  # spaceship gif image
        self.ship_image_dims = self.get_img_dimensions()

        self.main_ship = None  # holds the spaceship turtle object
        self.create_ship()
        self.main_ship_top = self.y_axis_main + self.ship_image_dims[1]/2  # spaceship top y-axis
        self.main_ship_bottom = self.y_axis_main - self.ship_image_dims[1]/2  # spaceship bottom y-axis
        self.main_ship_off_centre = self.ship_image_dims[0]/2  # spaceship x-axis offset from centre

        self.shots_fired = []  # holds the spaceships shots fired
        self.shot_length = 0.2
        self.shot_width = 1

        self.lives = 2  # counter for number of lives
        self.ship_lives = self.create_ship_lives()  # create turtle lives

        self.boundary_line = None  # holds bottom boundary line turtle
        self.boundary_line_y = self.y_axis_main-30
        self.create_boundary()

    def reset_main_ship(self, end_game=False):
        """
        resets spaceship into starting position, and recreates turtle lives
        """
        if end_game:  # reset lives to default
            self.lives = 2
        self.main_ship.goto(0, self.y_axis_main)  # staring position
        for life in self.ship_lives:
            # hide / clear life turtles
            life.hideturtle()
            life.clear()
            life = None
        self.ship_lives = None
        self.ship_lives = self.create_ship_lives()

    def remove_all_shots(self):
        """
        remove all shot turtles
        """
        for i in range(len(self.shots_fired)):
            self.shots_fired[i].hideturtle()
            self.shots_fired[i].clear()
            self.shots_fired[i] = None
        self.shots_fired = []

    def get_img_dimensions(self):
        """
        get spaceship gif img dimensions
        """
        img = Image.open(self.ship_image)
        width = img.width
        height = img.height
        return width, height

    def create_ship(self, *args):
        """
        creates ship and places it into starting position.
        Pass a 2 length list for ship turtle with custom positions (for Life turtles)
        """
        turtle = Turtle()
        turtle.shape(self.ship_image)
        turtle.penup()
        if args:
            turtle.goto(args[0], args[1])
            return turtle
        else:
            turtle.goto(0, self.y_axis_main)
            self.main_ship = turtle

    def create_ship_lives(self):
        """
        creates n ship life turtles - places at bottom left of screen with equal gaps between
        """
        ship_lives = []
        placement = self.screen_dims[0] / 17
        initial_x = -(self.screen_dims[0])/2 + placement
        initial_y = (-self.screen_dims[1]/2) + (self.screen_dims[1]/20)
        for _ in range(self.lives):
            # pass args to create ship at specified position
            ship_lives.append(self.create_ship(initial_x, initial_y))
            initial_x += placement  # increment x-axis
        return ship_lives

    def create_boundary(self):
        """
        creates boundary line at bottom of the screen
        - separates the spaceship from the lives turtles
        """
        turtle = Turtle()
        turtle.penup()
        turtle.shape("square")
        ratio_x = self.screen_dims[0]/20
        turtle.shapesize(stretch_len=ratio_x,  # width of the screen
                         stretch_wid=0.2)
        turtle.color("green")
        turtle.goto(0, self.boundary_line_y)
        self.boundary_line = turtle

    def add_shot(self):
        """
        add a shot (turtle) from the spaceship.
        starts from the top of the main ships coordinates
        """
        turtle = Turtle()
        turtle.penup()
        turtle.shape("square")
        turtle.color("white")
        turtle.shapesize(stretch_len=self.shot_length, stretch_wid=self.shot_width)
        turtle.goto(self.main_ship.xcor(),
                    self.main_ship.ycor() + (self.ship_image_dims[1]/2))  # + half height of ship img
        self.shots_fired.append(turtle)

    def move_left(self, scale=1):
        """
        Move space-ship to the left if spaceship img does not go passed the screen edge.
        Scale: multiplies the distance the spaceship will move
        """
        if not self.main_ship.xcor() - self.ship_image_dims[0]/2 - (10*scale) < -(self.screen_dims[0]/2):
            self.main_ship.goto(self.main_ship.xcor() - (10*scale), self.y_axis_main)

    def move_right(self, scale=1):
        """
        Move space-ship to the right if spaceship img does not go passed the screen edge.
        Scale: multiplies the distance the spaceship will move
        """
        if not self.main_ship.xcor() + self.ship_image_dims[0]/2 + (10*scale) > self.screen_dims[0]/2:
            self.main_ship.goto(self.main_ship.xcor() + (10*scale), self.y_axis_main)

    def shot_move_up(self, shot_move=10):
        """
        moves the shot up by default 10 pixels
        """
        for shot in self.shots_fired:
            shot.sety(shot.ycor() + shot_move)

    def shot_in_range(self):
        """
        spaceship is 'shot' - removes a life.
        Return: False if user was on last life (0), or True if had 1 + lives before
        """
        if self.lives == 0:
            return False
        self.main_ship.goto(0, self.y_axis_main)  # got to starting position
        self.lives -= 1  # decrement lives
        for life_turtle in self.ship_lives:
            life_turtle.hideturtle()
            life_turtle.clear()
            life_turtle = None
        self.ship_lives = self.create_ship_lives()
        return True
