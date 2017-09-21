#!/usr/bin/env python

import sys

def encode(filename):
    with open(filename) as feed:
        puzzle = [[int(cell) for cell in str(line.strip("\n"))] for line in feed]

    print(puzzle)
    return puzzle

def solve(puzzle):

    #TODO

    return puzzle

def decode(puzzle, cfg, new_filename):

    if(cfg.upper() == 'P'):
        print("\nSolved Sudoku:")
        for set in puzzle:
            output = " ".join(str(value) for value in set)
            print(output)
    else:
        new_filename = "solved_" + new_filename

        f = open(new_filename, 'w')
        for set in puzzle:
            output = " ".join(str(value) for value in set)
            f.write(output + "\n")
        print("Sudoku was stored as", new_filename)

    return

def main(n):

    if len(n) != 2:
        sys.exit("Usage: {}".format(sys.argv[0]))

    puzzle_unsolved = encode(n[1])
    puzzle_solved = solve(puzzle_unsolved)

    print("Print or store solved/unsolved sudoku?")
    while(1):
        cfg = input("Press P to print or S to store: ")
        if cfg.upper() == 'P' or cfg.upper() == 'S':
            decode(puzzle_solved, cfg, n[1])
            break

    return

if __name__ == "__main__":
    main(sys.argv)
