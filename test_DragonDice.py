from DragonDice import update_score, play_round, check_winner

def test_update_score_player_normal():
    # Test for normal score update for the player
    assert update_score(10, 4, is_player=True) == 14

def test_update_score_player_penalty():
    # Test penalty for player rolling a 3
    assert update_score(20, 3, is_player=True) == 10

def test_update_score_computer_even():
    # Test bonus points for computer rolling an even number (4)
    assert update_score(5, 4, is_player=False) == 13

def test_update_score_computer_odd():
    # Test normal points for computer rolling an odd number (3)
    assert update_score(5, 3, is_player=False) == 8

def test_check_winner_player_wins():
    # Test when player wins
    assert check_winner(60, 50, "Francis") == "Francis wins!"

def test_check_winner_computer_wins():
    # Test when computer wins
    assert check_winner(50, 60, "Rea") == "Computer wins!"

def test_check_winner_no_winner():
    # Test when no one has won yet
    assert check_winner(50, 40, "Jean") is None