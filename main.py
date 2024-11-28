"""
Main file for running the space invaders game
"""

from turtle import *
from shapes import MakeShapes
from Info_page import InfoDisplay
from main_ship import MainShip
from blocks_2 import Blocks
from alien_ships_2 import AlienShips
import time
import game_loop_logic
import random
from highscores import HighScore


# Function to draw stars as small dots
def draw_bg_stars(num_stars):
    star_turtle = Turtle()
    star_turtle.penup()
    star_turtle.hideturtle()
    star_turtle.speed("fastest")  # Maximize drawing speed
    for _ in range(num_stars):
        # Random position
        x = random.randint(int(round(-size[0]/2)), int(round(size[0]/2)))
        y = random.randint(int(round(-size[1]/2)), int(round(size[1]/2)))
        star_turtle.goto(x, y)
        # Random color
        star_turtle.dot(random.randint(2, 6), random.choice(["white", "light yellow", "light blue"]))


def select_game_icons(*search_string):
    icon_files = []
    for string in search_string:
        for shape_file in all_shapes:
            if string in shape_file:
                screen.register_shape(shape_file)
                icon_files.append(shape_file)
                all_shapes.pop(all_shapes.index(shape_file))
    return tuple(icon_files)


def loading_page():
    loading_page = True
    k = 0
    while loading_page:
        if k == 0:
            info.write_loading_text()
        info.create_progress_bar()
        if k == 15:
            info.remove_loading_page()
            loading_page = False
        k += 1
        screen.update()
        time.sleep(0.2)


size = 1000, 800  # default screen size

# make space invaders components
shapes = MakeShapes(size)
# get gif file names for all space invader game components
all_shapes = shapes.get_images()
# background = shapes.get_bg_img()  # background for game if needed

# --------------------SCREEN SETUP---------------------
screen = Screen()
screen.setup(size[0], size[1])
# if background:
#     screen.bgpic(background)
screen.title("Space Invaders")
screen.tracer(0)
screen.bgcolor("black")

# Add background stars to screen
draw_bg_stars(200)

# ------------------TURTLE COMPONENT SETUP--------------
# create info turtles - score, level, highscore
info = InfoDisplay(size, HighScore.get_highscore())

main_ship = select_game_icons("main_ship")  # select main ship gif file
top_ship_mov, second_ship_mov, third_ship_mov = select_game_icons(  # select aliens ship moving gif file
    "top_ship_moving",
    "second_ship_moving",
    "third_ship_moving")
top_ship, second_ship, third_ship = select_game_icons(  # select aliens ship gif file
    "top_ship",
    "second_ship",
    "third_ship")

# create main spaceship
space_ship = MainShip(main_ship[0], size)

# create block shields
block_rows = 9
block_columns = 11
blocks = Blocks(size, rows=block_rows,
                columns=block_columns)

loading_page()  # add loading page - optional

# create alien spaceships
aliens = AlienShips(size, (top_ship, second_ship, third_ship),
                    (top_ship_mov, second_ship_mov, third_ship_mov))


# ------------------ Functions for in-game User functionality----------------------
def move_ship_left(scale=1):
    """
    moves ship left
    """
    space_ship.move_left(scale)


def move_ship_right(scale=1):
    """
    moves ship right
    """
    space_ship.move_right(scale)


def add_shot(time_interval=0.35):
    """
    adds a shot from the main user spaceship
    - limits shooting interval using flags and timer mechanism
    """
    global shot_fired, first_shot_timer
    if not shot_fired:  # if no shot previously
        space_ship.add_shot()  # add shot
        shot_fired = True  # update shot fired
        first_shot_timer = time.time()  # set the timer
        return

    if shot_fired:  # if shot has already been fired
        second_shot_timer = time.time()
        # if trying to fire within too close to first shot - stop
        if second_shot_timer - first_shot_timer < time_interval:
            return
        else:  # reset flags and call function again
            shot_fired = False
            first_shot_timer = None
            add_shot()


def new_game_reset():
    """
    when user runs out of lives or spaceship passes user - resets game to base level
    """
    global j, i, alien_ship_move_speed, original_speed, alien_shoot_interval, initial_shoot_interval, speed, level

    aliens.switch_ships(switch=False)  # hide current aliens
    info.end_game(level)  # display end game text
    space_ship.remove_all_shots()  # remove spaceship shots
    aliens.remove_all_shots()  # remove alien shots
    screen.update()
    HighScore.set_highscore(info.get_score())  # update saved highscore
    info.create_highscore(score=HighScore.get_highscore(),
                          new_score=True)  # update highscore turtle
    time.sleep(5)
    info.reset_info_text()  # reset all info turtle text for next game
    aliens.reset_alien_ships()  # place aliens in starting position
    level = 1
    blocks.reset_bricks(rows=block_rows)  # reset block positions
    space_ship.reset_main_ship(end_game=True)  # reset main spaceship

    # reset global variables to base values
    j = 0
    i = 0
    alien_ship_move_speed = 15
    speed = 0.01
    original_speed = speed
    initial_shoot_interval = 20
    alien_shoot_interval = random.randint(initial_shoot_interval, initial_shoot_interval * 2)


def next_level():
    """
    when all alien ships shot - setup next game level
    - increase alien speed
    - reduce size of blocks
    - increase alien shoot interval
    """
    global i, j, alien_shoot_interval, initial_shoot_interval, alien_ship_move_speed, original_speed, level, speed
    aliens.switch_ships(switch=False)  # hide current aliens
    level += 1  # increment level counter
    info.next_game(level)  # should be new level
    info.create_level(updated_level=True)  # show next level info
    aliens.remove_all_shots()  # remove all alien shots
    screen.update()
    time.sleep(5)
    info.remove_next_level_text()  # reset info turtle text
    aliens.reset_alien_ships()  # place aliens in starting position
    blocks.reset_bricks(level)  # reset block positions - level passed to reduce block size
    space_ship.reset_main_ship()  # reset main spaceship
    space_ship.remove_all_shots()  # remove all spaceship shots

    # Assign global variables to base values or new (next level) values
    j = 0
    i = 0
    alien_ship_move_speed = 15
    initial_shoot_interval -= 2  # decrease time for aliens to shoot
    alien_shoot_interval = random.randint(initial_shoot_interval, initial_shoot_interval * 2)

    speed *= 0.8  # increase game speed
    original_speed = speed


def end_game():
    """
    stops and closes the game
    """
    global play
    play = False
    screen.bye()


# ------------------- User keyboard interactions -------------------
screen.listen()
screen.onkeypress(move_ship_left, "Left")  # move left
screen.onkeypress(lambda: move_ship_left(scale=2.3), "a")  # move left faster
screen.onkeypress(move_ship_right, "Right")  # move right
screen.onkeypress(lambda: move_ship_right(scale=2.3), "d")  # move right faster
screen.onkeypress(add_shot, "space")  # add shot
screen.onkeypress(end_game, "q")  # quit game


# ------------Global game variables-------------
# flags limiting user shoot interval
shot_fired = False
first_shot_timer = None
second_shot_timer = None
play = True

# flags for controlling when aliens move and when aliens shoot
i = 0
j = 0
alien_ship_move_speed = 15
initial_shoot_interval = 20
alien_shoot_interval = random.randint(initial_shoot_interval, initial_shoot_interval * 2)

level = 1  # initial user level

speed = 0.01  # game speed
original_speed = speed


# -----------------Game Loop Logic------------------
while play:

    # increments the counters
    i += 1
    j += 1
    time.sleep(speed)
    screen.update()  # update the screen

    # if counter j greater than alien shoot interval - fire a random alien shot
    if j > alien_shoot_interval:
        aliens.random_shot()
        # reset counter for shoot interval
        j = 0

    # if counter i greater than alien_ship_move_speed - move aliens
    if i > alien_ship_move_speed:
        hit_wall = aliens.move()
        # check if aliens passed user
        passed_finish = game_loop_logic.check_alien_passed_finish(aliens, space_ship)
        if passed_finish:
            # end game if passed user
            new_game_reset()
        # check if alien hit blocks
        game_loop_logic.check_alien_hit_block(aliens, blocks)
        # switch each aliens img
        aliens.switch_ships()

        # if aliens moved and hit wall - alien speed increases
        if hit_wall:
            if alien_ship_move_speed > 1:
                alien_ship_move_speed -= 1
        # reset counter for move speed
        i = 0

    # moves spaceship shots and checks if hit block or alien
    if space_ship.shots_fired:
        space_ship.shot_move_up()  # move shots
        game_loop_logic.check_shot_hit_block(space_ship.shots_fired, blocks)  # hit block interaction
        game_loop_logic.check_passed_line(space_ship.shots_fired, info, spaceship=True)
        hit_alien = game_loop_logic.check_shot_hit_alien(space_ship.shots_fired,
                                                         aliens,
                                                         space_ship)  # hit alien interaction

        if hit_alien:  # increment score if hit alien
            info.create_score(updated_score=True)

    # moves alien spaceship shots and checks if hit block or user spaceship
    if aliens.shots_fired:
        aliens.move_shots ()  # move shots
        game_loop_logic.check_shot_hit_block(aliens.shots_fired, blocks)  # hit block interaction
        game_loop_logic.check_passed_line(aliens.shots_fired, space_ship)
        more_lives = game_loop_logic.check_shot_hit_space_ship(aliens.shots_fired,
                                                               space_ship)  # hit spaceship interaction

        if not more_lives:  # if hit spaceship and no more user lives
            new_game_reset()  # end game

    # Increase speed significantly of the last alien ship
    if aliens.last_ship:
        if speed == original_speed:
            alien_ship_move_speed = 0

    # set up next level if all alien ships shot
    if aliens.no_more_ships:
        next_level()


screen.mainloop()