"""
Helper static class for getting and saving user scores to file.
"""


class HighScore:
    @staticmethod
    def get_highscore():
        """
        returns highscore from file.
        If no file - (new game) - returns 0
        """
        file_name = "scoreboard"
        try:
            with open(file_name, "r") as file:
                text = file.readline().strip()
                return text
        except FileNotFoundError:
            return "0"

    @staticmethod
    def set_highscore(new_score):
        """
        compares the previous highscore (or 0) against the new user score.
        Saves new user score if greater than previous score.
        new_score: int
        """
        file_name = "scoreboard"
        score = HighScore.get_highscore()

        if new_score > int(score):
            with open(file_name, "w") as file:
                file.write(str(new_score))

