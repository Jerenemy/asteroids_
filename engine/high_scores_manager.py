import os
import json
from utils import HIGH_SCORES_FILE

class HighScoresManager:
    """
    A class to manage loading, saving, and updating high scores.
    """

    def __init__(self, file_path=HIGH_SCORES_FILE):
        self.file_path = file_path
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        """
        Load high scores from the JSON file.

        Returns:
            dict: A dictionary of player names and scores.
        """
        if not os.path.exists(self.file_path):
            return {}

        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading high scores file. Returning empty scores.")
            return {}

    def save_high_scores(self):
        """
        Save high scores to the JSON file.
        """
        try:
            with open(self.file_path, 'w') as file:
                json.dump(self.high_scores, file, indent=4)
        except IOError as e:
            print(f"Error saving high scores: {e}")

    def add_score(self, player_name, score):
        """
        Add or update a player's score.

        Args:
            player_name (str): The name of the player.
            score (int): The player's score.
        """
        if player_name in self.high_scores:
            if score > self.high_scores[player_name]:
                self.high_scores[player_name] = score
                print(f"Updated high score for {player_name} to {score}.")
        else:
            self.high_scores[player_name] = score
            print(f"Added new high score for {player_name}: {score}.")

        self.save_high_scores()

    def get_top_scores(self, limit=10):
        """
        Retrieve the top scores.

        Args:
            limit (int): The maximum number of top scores to retrieve.

        Returns:
            list: A list of tuples containing player names and scores, sorted by score.
        """
        sorted_scores = sorted(self.high_scores.items(), key=lambda item: item[1], reverse=True)
        return sorted_scores[:limit]

# Example usage
if __name__ == "__main__":
    manager = HighScoresManager()

    # Add or update scores
    manager.add_score("Alice", 1200)
    manager.add_score("Bob", 900)
    manager.add_score("Charlie", 1500)

    # Retrieve and display top scores
    top_scores = manager.get_top_scores()
    print("Top Scores:")
    for rank, (player, score) in enumerate(top_scores, start=1):
        print(f"{rank}. {player}: {score}")
