from combined_gess import GessGame, UNFINISHED

run = True
while run:
    a = GessGame()
    while a.get_game_state() == UNFINISHED and run:

        start = input("Choose a start position: ")
        end = input("Choose an end position: ")
        if start[0].lower() == "q" or end[0].lower() == "q":
            run = False
        elif start[0] == 'R' or end[0] == "R":
            a.resign_game()
        else:
            a.make_move(start, end)

    print(a.get_game_state())
    choice = input("Again? Y/N")

    run = True
    if choice[0].lower() == "n":
        run = False