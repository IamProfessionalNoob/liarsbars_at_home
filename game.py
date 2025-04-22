import random

class LiarsBarRevolver:
    def __init__(self, chambers=6):
        self.chambers = chambers
        # Increase probability of not getting shot by placing bullet in last 2 chambers
        self.bullet_position = random.randint(chambers-2, chambers-1)
        self.current_position = 0
        self.players = []
        self.current_player_index = 0
        self.scores = {}
        self.bullets_per_player = {}
        self.round_stats = {}
        self.bullets_used = 0
        self.bullets_left = chambers - 1
        self.selected_table = None
        self.game_over = False
        self.spinning = False
        self.spin_result = None
        self.round_number = 1
        self.previous_players = set()  # Store previously played players
    
    def select_random_table(self):
        tables = ["Ace's Table", "King's Table", "Queen's Table"]
        self.selected_table = random.choice(tables)
        return self.selected_table
    
    def add_player(self, name):
        # Check if player name is empty or None
        if not name or not name.strip():
            return False, "Player name cannot be empty"
            
        # Check if player already exists
        if name in self.players:
            return False, f"Player {name} already exists"
            
        # Check if maximum players reached
        if len(self.players) >= 4:
            return False, "Maximum players reached (4)"
            
        # Add the player
        self.players.append(name)
        self.scores[name] = 0
        self.bullets_per_player[name] = 0
        self.round_stats[name] = {"bullets": 0, "survived": True}
        self.previous_players.add(name)  # Add to previous players set
        return True, f"Player {name} added successfully"
    
    def select_player(self, player_name):
        if player_name in self.players:
            self.current_player_index = self.players.index(player_name)
            return True, f"Selected player: {player_name}"
        return False, f"Player {player_name} not found"
    
    def shoot(self, player_name=None):
        if not self.players or self.game_over:
            return {
                "hit": False, 
                "player": None, 
                "bullets_used": self.bullets_used, 
                "bullets_left": self.bullets_left,
                "game_over": True
            }
        
        # If player_name is provided, select that player
        if player_name:
            success, message = self.select_player(player_name)
            if not success:
                return {
                    "hit": False,
                    "player": None,
                    "bullets_used": self.bullets_used,
                    "bullets_left": self.bullets_left,
                    "game_over": False,
                    "error": message
                }
        
        current_player = self.players[self.current_player_index]
        self.bullets_used += 1
        self.bullets_left = self.chambers - self.bullets_used
        self.bullets_per_player[current_player] += 1
        self.round_stats[current_player]["bullets"] += 1
        
        if self.current_position == self.bullet_position:
            # Player is eliminated
            eliminated_player = self.players[self.current_player_index]
            self.players.pop(self.current_player_index)
            self.round_stats[eliminated_player]["survived"] = False
            
            if len(self.players) == 1:
                # Game over, update scores
                winner = self.players[0]
                self.scores[winner] += 1
                self.game_over = True
                return {
                    "hit": True, 
                    "player": eliminated_player,
                    "bullets_used": self.bullets_per_player[eliminated_player],
                    "bullets_left": self.bullets_left,
                    "game_over": True,
                    "winner": winner,
                    "round_stats": self.round_stats,
                    "round_number": self.round_number
                }
            else:
                # Adjust current player index after elimination
                self.current_player_index = self.current_player_index % len(self.players)
                return {
                    "hit": True, 
                    "player": eliminated_player,
                    "bullets_used": self.bullets_per_player[eliminated_player],
                    "bullets_left": self.bullets_left,
                    "game_over": False,
                    "round_stats": self.round_stats
                }
        else:
            # Safe shot
            self.current_position = (self.current_position + 1) % self.chambers
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            return {
                "hit": False, 
                "player": current_player,
                "bullets_used": self.bullets_per_player[current_player],
                "bullets_left": self.bullets_left,
                "game_over": False,
                "round_stats": self.round_stats
            }
    
    def reset_game(self, chambers=None):
        # Store current players before reset
        current_players = self.players.copy()
        
        if chambers:
            self.chambers = chambers
        # Keep the same probability adjustment in reset
        self.bullet_position = random.randint(self.chambers-2, self.chambers-1)
        self.current_position = 0
        self.current_player_index = 0
        self.bullets_used = 0
        self.bullets_left = self.chambers - 1
        self.selected_table = None
        self.game_over = False
        self.round_number += 1
        
        # Clear round stats and bullets for new round
        self.bullets_per_player = {player: 0 for player in self.scores}
        self.round_stats = {player: {"bullets": 0, "survived": True} for player in self.scores}
        
        # Restore players for next round
        self.players = current_players
    
    def reset_scoreboard(self):
        for player in self.scores:
            self.scores[player] = 0
        return "Scoreboard reset successfully"
    
    def get_current_player(self):
        if not self.players or self.game_over:
            return None
        return self.players[self.current_player_index]
    
    def get_scores(self):
        return self.scores
    
    def get_previous_players(self):
        return list(self.previous_players)
    
    def get_game_state(self):
        current_player = self.get_current_player()
        return {
            "selected_table": self.selected_table,
            "current_player": current_player,
            "bullets_used": self.bullets_per_player.get(current_player, 0) if current_player else 0,
            "bullets_left": self.bullets_left,
            "chambers": self.chambers,
            "players": self.players,
            "game_over": self.game_over,
            "round_number": self.round_number,
            "bullets_per_player": self.bullets_per_player,
            "round_stats": self.round_stats,
            "previous_players": list(self.previous_players)
        }
    
    def spin(self):
        if not self.players:
            return False, "No players in the game"
        if self.spinning:
            return False, "Already spinning"
            
        self.spinning = True
        self.spin_result = random.choice(self.players)
        self.current_player_index = self.players.index(self.spin_result)
        self.spinning = False
        return True, f"Spinning... {self.spin_result} goes first!" 
