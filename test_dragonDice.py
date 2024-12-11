import pytest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from dragonDice import DiceGameApp


@pytest.fixture
def app():
    root = Tk()
    app = DiceGameApp(root)
    return app


def test_start_game(app):
    
    app.username_entry.insert(0, "Player1")
    app.start_game()
    
    
    assert app.username == "Player1"
    assert app.game_in_progress is True
    assert app.status_label.cget("text") == "Place your bet and roll the dice!"


def test_roll_dice(app):
    
    with patch('random.choice', return_value='\u2683'):
        dice_roll = app.roll_dice()
        assert dice_roll == '\u2683'
        

def test_play_turn_player(app):
   
    app.player_score = 10
    app.computer_score = 5
    app.turn = "Player"
    
    with patch('random.choice', return_value='\u2684'):  # Mocking a dice roll of 5
        app.play_turn()
        
        
        assert app.player_score == 15
        assert app.turn == "Computer"  
        

def test_end_game_player_win(app):
    app.bet_var.set("Player")
    app.player_score = 30
    app.computer_score = 10
    
    with patch('builtins.open', MagicMock()):
        app.end_game("Player")
        
        
        assert app.bet == 10
        assert app.status_label.cget("text") == "Player wins the bet! Bet doubled to 10 pesos."
        

def test_save_to_csv(app):
    app.username = "Player1"
    app.bet_var.set("Player")
    app.bet = 5
    
    with patch('builtins.open', MagicMock()):
        with patch('csv.writer') as mock_writer:
            app.save_to_csv("Player", "Player", 10)
            mock_writer.return_value.writerow.assert_called_once_with(["Player1", "Player", "Computer", "Player", 10])


def test_quit_game(app):
    app.quit_game()
    assert app.quit_button.cget("state") == "disabled"
    assert app.status_label.cget("text") == "You quit the game. Goodbye!"
    

def test_restart_game(app):
    app.quit_or_restart()
    assert app.username == ""
    assert app.player_score == 0
    assert app.computer_score == 0
    assert app.status_label.cget("text") == "Game Over. Please start a new game."
