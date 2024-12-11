from tkinter import *
import random
import csv  

class DiceGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dice Game with Bet")
        
        self.player_score = 0
        self.computer_score = 0
        self.bet = 5  
        self.username = ""
        self.game_in_progress = False 
        self.turn = "Player"  
        
        self.create_widgets()
        
    def create_widgets(self):
        
        self.root.config(bg="lightpink")
        
        self.info_label = Label(self.root, text="Welcome to the Dragon Dice Game!", font=("Arial", 16), bg="lightpink", fg="black")
        self.info_label.pack(pady=10)
        
        self.username_label = Label(self.root, text="Enter your username:", font=("Arial", 12), bg="lightpink", fg="black")
        self.username_label.pack()
        
        self.username_entry = Entry(self.root, font=("Arial", 12))
        self.username_entry.pack(pady=5)
        
        self.start_button = Button(self.root, text="Start Game", font=("Arial", 12), command=self.start_game, bg="lightgreen", fg="black")
        self.start_button.pack(pady=10)
        
        self.bet_label = Label(self.root, text="Place a bet on Player or Computer (5 pesos)", font=("Arial", 12), bg="lightpink", fg="black")
        self.bet_label.pack(pady=10)
        
        self.bet_var = StringVar(value="Player")
        self.bet_player_button = Radiobutton(self.root, text="Player", variable=self.bet_var, value="Player", font=("Arial", 12), bg="lightpink", fg="black")
        self.bet_computer_button = Radiobutton(self.root, text="Computer", variable=self.bet_var, value="Computer", font=("Arial", 12), bg="lightpink", fg="black")
        self.bet_player_button.pack()
        self.bet_computer_button.pack()
        
        self.dice_label = Label(self.root, font=("Helvetica", 260), bg="lightpink")
        self.dice_label.pack()
        
        self.roll_button = Button(self.root, text="Roll Dice", font=("Arial", 12), state="disabled", command=self.play_turn, bg="lightgreen", fg="black")
        self.roll_button.pack(pady=10)
        
        self.player_score_label = Label(self.root, text=f"Player Score: {self.player_score}", font=("Arial", 12), bg="lightpink", fg="black")
        self.player_score_label.pack(pady=5)
        
        self.computer_score_label = Label(self.root, text=f"Computer Score: {self.computer_score}", font=("Arial", 12), bg="lightpink", fg="black")
        self.computer_score_label.pack(pady=5)
       
        self.status_label = Label(self.root, text="Status: Waiting to start...", font=("Arial", 12), bg="lightpink", fg="black")
        self.status_label.pack(pady=10)
        
        self.quit_button = Button(self.root, text="Quit", font=("Arial", 12), command=self.quit_game, state="disabled", bg="lightgreen", fg="black")
        self.quit_button.place(x=300, y=10)  
        
        self.restart_button = Button(self.root, text="Restart Game", font=("Arial", 12), command=self.quit_or_restart, state="disabled", bg="lightgreen", fg="black")
        self.restart_button.place(x=250, y=50)  
        
    def start_game(self):
        self.username = self.username_entry.get().strip()
        if self.username:
            self.username_entry.config(state="disabled")
            self.start_button.config(state="disabled")
            self.bet_label.config(state="normal")
            self.bet_player_button.config(state="normal")
            self.bet_computer_button.config(state="normal")
            self.roll_button.config(state="normal")
            self.quit_button.config(state="normal")  
            self.status_label.config(text="Place your bet and roll the dice!")
            self.game_in_progress = True 
        else:
            self.status_label.config(text="Please enter a username.")
    
    def roll_dice(self):
        dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        return random.choice(dice)
    
    def play_turn(self):
        if self.computer_score < 30 and self.player_score < 30:
            self.status_label.config(text=f"{self.turn}'s Turn!") 
            if self.turn == "Player":
                player_roll = self.roll_dice()
                self.dice_label.config(text=player_roll)
                self.status_label.config(text=f"Player rolled: {player_roll}")
                self.player_score += self.dice_value(player_roll)
                self.player_score_label.config(text=f"Player Score: {self.player_score}")
                self.turn = "Computer"  
                
                if self.player_score >= 30:
                    self.end_game("Player")
                    return
            
            elif self.turn == "Computer":
                computer_roll = self.roll_dice()
                self.dice_label.config(text=computer_roll)
                self.status_label.config(text=f"Computer rolled: {computer_roll}")
                self.computer_score += self.dice_value(computer_roll)
                self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")
                self.turn = "Player"  
                
                if self.computer_score >= 30:
                    self.end_game("Computer")
    
    def dice_value(self, dice_unicode):
        dice_map = {'\u2680': 1, '\u2681': 2, '\u2682': 3, '\u2683': 4, '\u2684': 5, '\u2685': 6}
        return dice_map.get(dice_unicode, 0)
    
    def end_game(self, winner):
        if self.bet_var.get() == "Player" and winner == "Player":
            self.bet *= 2 
            self.status_label.config(text=f"Player wins the bet! Bet doubled to {self.bet} pesos.")
            self.save_to_csv(winner, self.bet_var.get(), self.bet)
        elif self.bet_var.get() == "Computer" and winner == "Computer":
            self.bet *= 2  
            self.status_label.config(text=f"Computer wins the bet! Bet doubled to {self.bet} pesos.")
            self.save_to_csv(winner, self.bet_var.get(), self.bet)
        else:
            self.bet = 0  
            self.status_label.config(text=f"{winner} wins, but you lose your bet.")
            self.save_to_csv(winner, self.bet_var.get(), 0)
        
        self.roll_button.config(state="disabled")
        self.restart_button.config(state="normal")
    
    def save_to_csv(self, winner, bet_side, amount):
        loser = "Player" if winner == "Computer" else "Computer"
        with open('game_results.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, winner, loser, bet_side, amount])
        print(f"Saved to CSV: Username: {self.username}, Winner: {winner}, Loser: {loser}, Bet Side: {bet_side}, Amount: {amount}")
    
    def quit_game(self):
        self.status_label.config(text="You quit the game. Goodbye!")
        self.quit_button.config(state="disabled")  
        self.restart_button.config(state="normal")
        self.root.quit()    
    
    def quit_or_restart(self):
        self.username_entry.config(state="normal")
        self.username = ""
        self.username_entry.delete(0, END)  

        self.player_score = 0
        self.computer_score = 0
        self.bet = 5  
        self.player_score_label.config(text=f"Player Score: {self.player_score}")
        self.computer_score_label.config(text=f"Computer Score: {self.computer_score}")
        self.status_label.config(text="Game Over. Please start a new game.")
        
        self.username_entry.config(state="normal")
        self.start_button.config(state="normal")
        self.bet_label.config(state="normal")
        self.bet_player_button.config(state="normal")
        self.bet_computer_button.config(state="normal")
        self.roll_button.config(state="normal")
        
        self.bet_var.set("Player")
        
        self.quit_button.config(state="disabled")
        self.restart_button.config(state="disabled") 

if __name__ == "__main__":
    root = Tk()
    app = DiceGameApp(root)
    root.geometry("400x400")  
    root.mainloop()
