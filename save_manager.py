
import json
import os

SAVE_FILE = "save_data.json"

class SaveManager:
    def __init__(self):
        self.data = self.load()

    def load(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_data()
        return self.get_default_data()

    def get_default_data(self):
        return {
            'credits': 0,
            'upgrades': {
                'speed': 0,
                'fire_rate': 0,
                'health': 0,
                'magnet': 0
            },
            'leaderboard': [
                {'name': 'ACE', 'score': 1000},
                {'name': 'NEO', 'score': 800},
                {'name': 'ZOE', 'score': 500}
            ]
        }

    def save(self):
        with open(SAVE_FILE, 'w') as f:
            json.dump(self.data, f)

    def add_score(self, name, score):
        self.data['leaderboard'].append({'name': name, 'score': score})
        # Sort and keep top 5
        self.data['leaderboard'].sort(key=lambda x: x['score'], reverse=True)
        self.data['leaderboard'] = self.data['leaderboard'][:5]
        self.save()

    def add_credits(self, amount):
        self.data['credits'] += amount
        self.save()

    def upgrade_item(self, item_name, cost):
        if self.data['credits'] >= cost:
            self.data['credits'] -= cost
            self.data['upgrades'][item_name] += 1
            self.save()
            return True
        return False
