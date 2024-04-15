import sqlite3


class NBAPropBets:
    
    def __init__(self, db_path):
        self.db_path = db_path

    def get_player_avg(self, name, prop):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {prop} FROM playeravgs WHERE name=?", (name,))
            result = cursor.fetchone()
            return result[0] if result else None

    def player_exists(self, name):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT EXISTS(SELECT 1 FROM playeravgs WHERE name=?)", (name,))
            return cursor.fetchone()[0] == 1

    def check_prop_bet(self, name, prop, prop_bet, under_over):
        avg = self.get_player_avg(name, prop)
        if avg is None:
            suggestions = self.suggest_player_names()
            return f"Player not found. Did you mean: {suggestions[0]} or {suggestions[1]}?", False
        if under_over == "under" and avg < prop_bet:
            return "Good bet.", True
        elif under_over == "over" and avg > prop_bet:
            return "Good bet.", True
        else:
            return "Bad bet.", True

    def suggest_player_names(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM playeravgs ORDER BY RANDOM() LIMIT 2")
            results = cursor.fetchall()
            return [result[0] for result in results]

    def get_player_count(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM playeravgs")
            count = cursor.fetchone()[0]
            return count

    def run_cli(self):
        while True:
            player_name = input("Enter player's name (or type 'exit' to quit): ").strip()
            if player_name.lower() == 'exit':
                break

            if not self.player_exists(player_name):
                suggestions = self.suggest_player_names()
                print(f"Player not found. Did you mean: {suggestions[0]} or {suggestions[1]}?")
                continue

            prop = input("Enter the prop to check (points, rebounds, assists): ").lower().strip()
            if prop not in ["points", "rebounds", "assists"]:
                print("Invalid prop. Please enter 'points', 'rebounds', or 'assists'.")
                continue

            under_over = input("Is the bet for under or over the average? ").lower().strip()
            if under_over not in ["under", "over"]:
                print("Invalid input. Please enter 'under' or 'over'.")
                continue

            try:
                prop_bet = float(input(f"Enter the prop bet for {player_name}'s {prop}: ").strip())
            except ValueError:
                print("Please enter a valid number for the prop bet.")
                continue

            result, found = self.check_prop_bet(player_name, f"avg_{prop}", prop_bet, under_over)
            if not found:
                print(result)
            else:
                print(result)


db_path = '2022szn.db'
prop_bets = NBAPropBets(db_path)
prop_bets.run_cli()
