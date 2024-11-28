"""
class to create all space invaders components as transparent GIF images
- also able to create a Gif background for the game.
"""

from turtle import *
from PIL import Image, ImageOps
import os
import shutil
import sys


ship_ratio = 11/15
ships_per_row = 17


def make_transparent_black_background(img):
    """
    Converts the img to have a transparent layer - where the transparent layer is
    by default 'black' (0, 0, 0)
    """
    img = img.convert("RGBA")
    data = img.getdata()

    new_pixel_data = []
    for item in data:
        if item[:3] == (0, 0, 0):  # black colour
            # add '0' to the alpha channel with black colour
            new_pixel_data.append((0, 0, 0, 0))
        else:
            new_pixel_data.append(item)
    img.putdata(new_pixel_data)  # update the img

    return img


class MakeShapes:
    def __init__(self, size):
        self.screen_size = size  # screen size for main game screen
        self.square_size_small = 80
        self.square_size_large = 40

        self.screen = Screen()  # screen for creating component shapes
        self.turtle = Turtle()  # for drawing shapes
        self.turtle.speed("fastest")
        self.turtle.penup()
        self.turtle.hideturtle()

        # for holding intermediate and final GIF images, anc GIF bg
        self.temp_folder = "./temp_folder"
        self.img_folder = "./game_icons"
        self.bg_img_folder = "./background_images"

        # for gif img width and height - relative to no. ships per row and col
        self.ship_x_scaled = (self.screen_size[0]/ships_per_row) * ship_ratio
        self.ship_y_scaled = (self.screen_size[1]/ships_per_row) * ship_ratio

        self.shapes = []  # holds game components dictionaries

        # -------game components dictionaries-----
        first_ship = {
            "name": "top_ship",
            "rows": 8,
            "columns": 8,
            "colour": "blue",  # initial colour before inverting
            "scale_w": self.ship_x_scaled,  # final pixels width of img
            "scale_h": self.ship_y_scaled,  # final pixels height of img
            "pixels": [  # squares to be drawn
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [0, 1, 0, 0, 0, 0, 1, 0]
            ]
        }
        self.shapes.append(first_ship)

        first_ship_moving = {
            "name": "top_ship_moving",
            "rows": 8,
            "columns": 8,
            "colour": "blue",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 0, 1, 1, 0, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [0, 1, 0, 1, 1, 0, 1, 0],
                [1, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 1]]
        }
        self.shapes.append(first_ship_moving)

        second_ship = {
            "name": "second_ship",
            "rows": 8,
            "columns": 11,
            "colour": "cyan",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0]]
        }
        self.shapes.append(second_ship)

        second_ship_moving = {
            "name": "second_ship_moving",
            "rows": 8,
            "columns": 11,
            "colour": "cyan",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
                [0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
                [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0]]
        }
        self.shapes.append(second_ship_moving)

        third_ship = {
            "name": "third_ship",
            "rows": 8,
            "columns": 12,
            "colour": "red",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]
        }
        self.shapes.append(third_ship)

        third_ship_moving = {
            "name": "third_ship_moving",
            "rows": 8,
            "columns": 12,
            "colour": "red",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0],
                [0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0],
                [0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0]]
        }
        self.shapes.append(third_ship_moving)

        main_ship = {
            "name": "main_ship",
            "rows": 8,
            "columns": 12,
            "colour": "yellow",
            "scale_w": self.ship_x_scaled,
            "scale_h": self.ship_y_scaled,
            "pixels": [
                [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        }
        self.shapes.append(main_ship)

        # flag indicating if the img folder has been made and populated
        self.images_created = self.icon_folder()

    def get_bg_img(self):
        """
        returns a GIF bg image resized to the game screen size.
        Requires a directory named 'background_images' within this repository, and
        an image file placed within it (Not GIF)
        """
        img_file = None
        if os.path.isdir(self.bg_img_folder):  # if directory is present
            if len(self.bg_img_folder) > 0:  # if populated
                for file in os.listdir(self.bg_img_folder):
                    if file.split(".")[1].lower() == "gif":
                        # if a GIF file present - return the GIF img
                        gif_file = os.path.join(self.bg_img_folder, file)
                        return gif_file
                    else:  # img file is the non-GIF file
                        img_file = os.path.join(self.bg_img_folder, file)
                if img_file:  # convert non GIF img to GIF
                    img = Image.open(img_file)
                    name = img_file.split('.')[0]
                    img = img.convert("RGB")
                    img = img.resize((self.screen_size[0], self.screen_size[1]))
                    gif_file = f"{self.bg_img_folder}/{name}.gif"
                    img.save(gif_file, format="GIF")
                    return gif_file
        return None

    def temp_file(self, destroy=False):
        """
        either creates the temporary img folder for turtle shape images.
        If called with destroy=True then it destroys the temporary folder
        """
        if not os.path.isdir(self.temp_folder):
            os.mkdir(self.temp_folder)  # create
        if destroy:
            shutil.rmtree(self.temp_folder)  # destroy

    def get_images(self):
        """
        Returns a list of game component GIF img files.
        If previously created - returns the list from the img folder.
        If not previously created - the components are drawn, saved, and converted to
            GIF images and then the list if GIF files is returned.
        """
        if self.images_created:  # GIF files already created
            files = []
            for file in os.listdir(self.img_folder):
                path = os.path.join(self.img_folder, file)
                files.append(path)
            return files  # return GIF files
        else:  # Need to create the GIF files
            self.make_icon_folder()   # create temporary img folder

            # for displaying progress info to user
            loading_length = 100/len(self.shapes)
            progress_unit = 0

            for shape in self.shapes:
                # for displaying progress info to user
                sys.stdout.write(f"\rStatus: {str(int(round(progress_unit, 0)))}%")
                sys.stdout.flush()

                self.turtle.clear()

                square_size = self.square_size_small
                # if shape["name"] == "block":
                #     square_size = self.square_size_large

                # make shape screen the dimension of the resulting img to be drawn
                self.screen.setup(width=shape['columns'] * square_size + 5,
                             height=shape["rows"] * square_size + 5)
                self.screen.screensize(shape['columns'] * square_size,
                                  shape["rows"] * square_size)

                # go to the top left of the screen
                self.turtle.goto(x=-(self.screen.window_width() / 2),
                                 y=self.screen.window_height() / 2)

                # draw the spaceship
                self.draw_spaceship(shape, square_size)

                # update the progress
                progress_unit += loading_length

            # after all GIF images have been created
            self.temp_file(destroy=True)  # destroy temp folder
            self.turtle.clear()
            self.images_created = True
            return self.get_images()  # call the function within to return list of GIF images

    def draw_spaceship(self, shape, square_size):
        """
        Draws the passed shape - by iterating over the shapes pixels 2D array,
        and drawing squares at valid points.
        """
        # get initial coordinates
        initial_x = self.turtle.xcor()
        initial_y = self.turtle.ycor()

        for i in range(shape["rows"]):  # for each row
            for j in range(shape["columns"]):  # for each column
                # if a 'draw' signal ('1')
                if shape["pixels"][i][j] == 1:
                    # draw square - increments the x-axis of the turtle
                    self.draw_square(shape["colour"], j, shape["columns"], square_size)
                else:
                    # pass to draw square - but will not draw square
                    self.draw_square('white', j, shape["columns"], square_size)

            initial_y -= square_size  # decrements the y-axis
            self.turtle.goto(initial_x, initial_y)  # starting position for new row

        # size of final image
        target_size = (
            int(round(shape["scale_w"])),
            int(round(shape["scale_h"])))

        self.temp_file()
        cv = self.screen.getcanvas()  # get screenshot
        # save as a postscript file to temporary folder
        cv.postscript(file=f"{self.temp_folder}/{shape["name"]}.ps", colormode='color')
        # convert to GIF image from postscript
        self.convert_to_gif(f"{self.temp_folder}/{shape["name"]}.ps", target_size)

    def draw_square(self, colour, j, column_limit, square_size):
        """
        Draws a turtle square and fills with colour passed if colours is not white.
        Moves turtle forward if not at the screen limit.
        """
        _turtle = self.turtle
        if colour != "white":
            _turtle.setheading(0)
            _turtle.pendown()
            _turtle.pencolor(colour)
            _turtle.fillcolor(colour)
            _turtle.begin_fill()
            for _ in range(4):
                _turtle.forward(square_size)
                _turtle.right(90)
            _turtle.end_fill()
            _turtle.penup()
        if j != column_limit-1:
            _turtle.forward(square_size)

    def convert_to_gif(self, path, targ_size):
        """
        Converts img file to GIF
        """
        name = path.split('/')[2].split('.')[0]
        img = Image.open(path)
        img = img.convert("RGB")
        img = img.resize(targ_size)
        img_inv = ImageOps.invert(img)
        img_transparent = make_transparent_black_background(img_inv)  # transparent bg
        img_transparent.save(f"{self.img_folder}/{name}.gif", format="GIF")

    def icon_folder(self):
        """
        Checks whether the GIF component images have been created
        """
        if os.path.isdir(self.img_folder):
            if len(os.listdir(self.img_folder)) > 0:
                return True
            return False
        return False

    def make_icon_folder(self):
        """
        creates the GIF img folder
        """
        os.mkdir(self.img_folder)


