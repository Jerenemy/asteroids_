import json
from utils import HIGH_SCORES_FILE
class HighScoresManager:
    def __init__(self, file_path=HIGH_SCORES_FILE):
        self.file_path = file_path
        self.high_scores = self.get_high_scores_from_file()
        

    def is_high_score(self, score: int, score_type: str) -> bool:
        try: 
            _, high_score = self.get_top_scores(score_type)[0]
            # print(high_score)
            return score >= high_score
        except KeyError as e:
            return False
    
    def get_top_scores(self, score_type: str, limit=10) -> tuple:
        """
        Retrieve the top scores.

        Args:
            limit (int): The maximum number of top scores to retrieve.

        Returns:
            list: A list of tuples containing player names and scores, sorted by score.
        """
        sorted_scores = sorted(self.high_scores[score_type].items(), key=lambda item: item[1], reverse=True)
        return sorted_scores[:limit]
    
    def get_high_scores_from_file(self):
       # Load the JSON file into a dictionary
        with open(self.file_path, "r") as file:
            data = json.load(file)
        return data
    
    def get_player_high_scores(self, name):
        pass
    
    def save_new_high_score(self, name: str, score: int, score_type: str):
        self.high_scores[score_type][name] = score
        self._save_high_scores_to_file()
    
    def _save_high_scores_to_file(self):
        try:
            with open(self.file_path, 'w') as file: #switch to append?
                json.dump(self.high_scores, file, indent=4)
        except IOError as e:
            print(f"Error saving high scores: {e}")

    def get_both_high_scores(self):
        name_points, points_high_score = self.get_top_score('points')
        name_level, level_high_score = self.get_top_score('level')
        return (name_points, points_high_score), (name_level, level_high_score)
    
    def get_top_score(self, score_type: str):
        return self.get_top_scores(score_type)[0]
        # print(type(self.high_scores))
        # print(self.high_scores)
        hss = self.high_scores[score_type]
        max_name = max(hss, key=hss.get)
        high_score = hss[max_name]
        return (max_name, high_score)
    