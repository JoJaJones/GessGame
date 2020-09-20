files_to_copy = ["constants.py", "GessGame.py", "Board.py", "Piece.py", "Display.py", "Stone.py", "Player.py"]

with open("combined_gess.py", "w+") as outfile:
    for file in files_to_copy:
        with open(file, "r") as infile:
            for line in infile:
                if "import" not in line:
                    outfile.write(line)
