"""
Class to display and control user information.
Loading page, next level, end game, score, level, highscore
"""

from turtle import *

LOADING_FONT = ("Arial", 60, "bold")
PROGRESS_FONT = ("Arial", 40, "bold")
LOADING_PAGE_FONT = ("Arial", 40, "normal")
HEADING_FONT = ("Arial", 20, "bold")


class InfoDisplay:
    def __init__(self, screen_dims, highscore):
        self.screen_setup = screen_dims  # parent screen dimensions
        # ------ hold the turtle text objects-------
        self.loading_text = None
        self.progress_bar = None
        self.game_end_text = None
        self.next_level_text = None
        self.current_score = None
        self.current_level = None
        self.highscore_turtle = None

        self.progress = ""
        self.aliens_hit = 0
        self.player_level = 1

        # create score label and score text
        self.create_score()
        self.score_label = self.create_score_label()

        # create level label and level text
        self.create_level()
        self.level_label = self.create_level_label()

        # create highscore label and highscore text
        self.create_highscore(score=highscore)
        self.highscore_label = self.create_highscore_label()

        # define boundary line at top of screen
        self.boundary_line_y = self.screen_setup[1]/2 - (self.screen_setup[1]/2) / 10
        self.top_barrier_line = self.create_top_barrier()

    def get_score(self):
        """
        return current score
        """
        return self.aliens_hit

    def create_highscore_label(self):
        """
        creates highscore label turtle text
        """
        turtle = Turtle()
        turtle.color("white")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(self.screen_setup[0]/2 - ((self.screen_setup[0]/2) / 2.5),
                    - self.screen_setup[1]/2 + ((self.screen_setup[1]/2) / 13))
        turtle.write("HIGHSCORE: ", move=False, font=HEADING_FONT, align="left")
        return turtle

    def create_highscore(self, score=0, new_score=False):
        """
        creates highscore label turtle text.
        """
        if not new_score:
            turtle = Turtle()
            turtle.color("white")
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(self.screen_setup[0] / 2 - ((self.screen_setup[0] / 2) / 10),
                        - self.screen_setup[1] / 2 + ((self.screen_setup[1] / 2) / 13))
            turtle.write(f"{score}", move=False, font=HEADING_FONT, align="left")
            self.highscore_turtle = turtle
        else:
            self.highscore_turtle.clear()
            self.highscore_turtle.write(f"{score}", move=False, font=HEADING_FONT, align="left")

    def create_score_label(self):
        """
        creates score label turtle text
        """
        turtle = Turtle()
        turtle.color("white")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(-self.screen_setup[0]/2 + ((self.screen_setup[0]/2) / 10),
                    self.screen_setup[1]/2 - ((self.screen_setup[1]/2) / 13))
        turtle.write("SCORE: ", move=False, font=HEADING_FONT, align="left")
        return turtle

    def create_level_label(self):
        """
        creates level label turtle text
        """
        turtle = Turtle()
        turtle.color("white")
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(self.screen_setup[0]/2 - (self.screen_setup[0]/2) / 5,
                    self.screen_setup[1]/2 - (self.screen_setup[1]/2) / 13)
        turtle.write("LEVEL: ", move=False, font=HEADING_FONT, align="right")
        return turtle

    def create_score(self, updated_score=False, score=None):
        """
        Creates the initial score turtle text.
        Can update the score with updated_score flag, which clears previous text, and displays
        the incremented no. of aliens hit.
        Can pass also score=0 to reset the score.
        """
        if not updated_score:  # initial creation
            turtle = Turtle()
            turtle.color("white")
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(-self.screen_setup[0]/2 + ((self.screen_setup[0]/2) / 3),
                        self.screen_setup[1]/2 - ((self.screen_setup[1]/2) / 13))
            turtle.write(f"{self.aliens_hit}", move=False, font=HEADING_FONT, align="left")
            self.current_score = turtle
        else:  # update score
            if score == 0:  # for new game - reset score
                self.aliens_hit = score
            else:  # increment score
                self.aliens_hit += 1
            self.current_score.clear()
            self.current_score.write(f"{self.aliens_hit}", move=False, font=HEADING_FONT, align="left")

    def create_level(self, updated_level=False, level=None):
        """
        Creates the initial level turtle text.
        Can update the score with updated_level flag, which clears previous text, and displays
        the incremented player level.
        Can pass also level to reset the level.
        """
        if not updated_level:
            turtle = Turtle()
            turtle.color("white")
            turtle.penup()
            turtle.hideturtle()
            turtle.goto(self.screen_setup[0]/2 - (self.screen_setup[0]/2) / 10,
                        self.screen_setup[1]/2 - (self.screen_setup[1]/2) / 13)
            turtle.write(f"{self.player_level}", move=False, font=HEADING_FONT, align="right")
            self.current_level = turtle
        else:
            if level:
                self.player_level = level
            else:
                self.player_level += 1
            self.current_level.clear()
            self.current_level.write(f"{self.player_level}", move=False, font=HEADING_FONT, align="right")

    def create_top_barrier(self):
        """
        creates the barrier at the top of the screen
        """
        turtle = Turtle()
        turtle.color('green')
        turtle.penup()
        turtle.shape('square')
        ratio_x = self.screen_setup[0] / 20  # width of the screen
        turtle.shapesize(stretch_len=ratio_x, stretch_wid=0.2)
        turtle.goto(0, self.screen_setup[1]/2 - (self.screen_setup[1]/2) / 10)
        return turtle

    def end_game(self, level):
        """
        Displays end game text - indicating the level and score
        """
        turtle = Turtle()
        turtle.penup()
        turtle.hideturtle()
        turtle.color("green")
        turtle.goto(0, (self.screen_setup[1]/2)/2)
        turtle.write(f". . .GAME OVER. . .\n\n Reached level: {level}\n\nScore: {self.aliens_hit}",
                     move=False, font=PROGRESS_FONT, align="center")
        self.game_end_text = turtle

    def reset_info_text(self):
        """
        resets all info texts to default
        """
        self.game_end_text.hideturtle()
        self.game_end_text.clear()
        self.game_end_text = None

        # update the score and level to default starting
        self.create_score(updated_score=True, score=0)
        self.create_level(updated_level=True, level=1)

    def next_game(self, level):
        """
        Displays next level text - indicating next level
        """
        turtle = Turtle()
        turtle.penup()
        turtle.hideturtle()
        turtle.color("green")
        turtle.goto(0, (self.screen_setup[1]/2)/2)
        turtle.write(f"NEXT LEVEL\n\n Level: {level}",
                     move=False, font=PROGRESS_FONT, align="center")
        self.next_level_text = turtle

    def remove_loading_page(self):
        """
        removes initial loading text from screen
        """
        if self.loading_text:
            self.loading_text.hideturtle()
            self.loading_text.clear()
        self.progress_bar.hideturtle()
        self.progress_bar.clear()

    def remove_next_level_text(self):
        """
        remove next level text from screen
        """
        self.next_level_text.hideturtle()
        self.next_level_text.clear()
        self.next_level_text = None

    def write_loading_text(self):
        """
        write loading game title text
        """
        turtle = Turtle()
        turtle.penup()
        turtle.hideturtle()
        turtle.color('green')
        turtle.goto(0, (self.screen_setup[1]/2)/2)
        turtle.write("SPACE INVADERS", move=False, font=LOADING_FONT, align="center")
        self.loading_text = turtle

    def create_progress_bar(self):
        """
        displays an incrementing progress bar - to reflect game loading
        """
        if self.progress_bar:  # remove previous turtle
            self.progress_bar.hideturtle()
            self.progress_bar.clear()
            self.progress_bar = None
        # create turtle progress bar text
        self.progress += "#"
        turtle = Turtle()
        turtle.penup()
        turtle.hideturtle()
        turtle.goto(0, 0)
        turtle.color("green")
        turtle.write(f"{self.progress.ljust(15, "-")}",
                     move=False, font=LOADING_PAGE_FONT, align="center")
        self.progress_bar = turtle
