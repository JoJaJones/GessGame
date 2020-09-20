from constants import *
from GessGame import GessGame

run = True
test_count = 1  # update to next test number on subsequent executions

with open("generated_tests.py", "a+") as outfile:
    # comment out next line on subsequent executions
    # outfile.write("import unittest\nfrom GessGame import GessGame\n\n\nclass TestGess(unittest.TestCase):\n")

    try:
        while run:
            a = GessGame(True)
            outfile.write(f"    def test_{test_count:03}(self):\n")
            outfile.write(f"        t = GessGame()\n")
            test_count += 1
            while a.get_game_state() == UNFINISHED and run:

                start = input("Choose a start position: ")
                end = input("Choose an end position: ")
                if start[0].lower() == "q" or end[0].lower() == "q":
                    run = False
                elif start[0] == 'R' or end[0] == "R":
                    a.resign_game()
                    outfile.write(f"        self.assertTrue(t.resign_game())\n")
                else:
                    if a.make_move(start, end):
                        outfile.write(f"        self.assertTrue(t.make_move('{start}','{end}'))\n")
                    else:
                        outfile.write(f"        self.assertFalse(t.make_move('{start}','{end}'))\n")

            print(a.get_game_state())
            outfile.write(f"        self.assertEqual(t.get_game_state(), '{a.get_game_state()}')\n\n")
            choice = input("Again? Y/N")

            run = True
            if choice[0].lower() == "n":
                run = False
            else:
                outfile.write("\n")
    except:
        print("You dun goofed")


# todo position update logic needs work can incorrectly delete active pieces if start and end squares overlap
# todo obstruction logic doesn't work for footprint but pieces

