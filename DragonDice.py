from random import randint


def update_score(score, die_value, is_player=False):
    if die_value == 3:
        return max(0, score // 2)
    elif is_player:
        return score + die_value
    else:
        return score + die_value * (2 if die_value % 2 == 0 else 1)


def display_scoreboard(player_score, computer_score):
    print()
    print("#" * 50)
    print(f"Player Score: {player_score}")
    print(f"Computer Score: {computer_score}")
    print("#" * 50)
    print()


def play_turn(is_player=False):
    die_value = randint(1, 6)
    if is_player:
        print(f"Player rolls a {die_value}")
    else:
        print(f"Computer rolls a {die_value}")
    return die_value


def play_game():
    player_score = 0
    computer_score = 0

    welcome_message = """
              Welcome to 'Dragon', a dice game!
        
        In this game, a user and a computer enemy by the name
         roll a die each turn.
        
       [1] On rolling a 3 the player loses half of the total score.
       [2] The computer gets double points for rolling even numbers.
       [3] The computer gets another turn, if it rolls a 6!
       [4] The player loses 1 point at the end of every round.
        
        The first player to reach 60 points wins!
    """

    print(welcome_message)

    username = input("What is your (ign) ingame name? ")

    while True:
        input(f"Hit 'Enter' to roll the die, {username}!\n")

        player_die_value = play_turn(is_player=True)
        player_score = update_score(player_score, player_die_value, is_player=True)

        player_score = max(0, player_score - 1)

        computer_turns = 1
        while computer_turns > 0:
            computer_die_value = play_turn(is_player=False)
            computer_score = update_score(computer_score, computer_die_value)

            if computer_die_value == 6:
                print("Computer rolls a 6 and gets an extra turn!")
                computer_turns += 1
            computer_turns -= 1

        display_scoreboard(player_score, computer_score)

        if player_score >= 60:
            print(f"{username} wins!")
            break
        elif computer_score >= 60:
            print("Computer wins!")
            break


while True:
    play_game()
    while True:
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again == "yes":
            break
        elif play_again == "no":
            print("Thanks for playing! Goodbye!")
            exit()
        else:
            print("Error: Please type 'yes' or 'no'.")

if __name__ == "__main__":
    main()
