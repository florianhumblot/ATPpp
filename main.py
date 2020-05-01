import os
import sys
import threading
from functools import reduce
from pprint import pprint
from time import time
import argparse

import Lexer
import Parser
import ATPTools


# pparseProgram :: str -> Parser.ProgramState
@ATPTools.copyParameters
def parseProgram(infile: str = "example_programs/loop.atp++") ->Parser.ProgramState:
    """
    Parses a program from a given input file.
    :param infile: str the path to a ATP++ file
    :return: ProgramState
    """
    with open(infile, "r") as file:
        program_text = list(Lexer.strToLines(file.read()))
        tokens = Lexer.lexInput(program_text)
        unknown_tokens = list(zip(map(lambda x: x[1] is None, tokens), program_text))
        unknown_count = reduce(lambda x, y: x + y, map(lambda x: int(x[0]), unknown_tokens))
        if unknown_count > 0:
            list(map(lambda x: print("Unkown token `{0}` on line {1}".format(x[1][1], x[0])) if x[1][0] else None,
                     enumerate(unknown_tokens)))
            exit(-1)
        ps = Parser.ProgramState()
        ps.instructions = tokens
        ps.labels = Parser.parseLabels(ps.instructions)
        return ps


class run:
    """
    Class for running our parser in a different thread to circumvent the stack limit on the python interpreter.
    """
    def __call__(self, infile: str = "example_programs/counter_machine.atp++"):
        """
        Runs the parser
        :param infile: str the path to a ATP++ file
        :return: None
        """
        self.run_program(parseProgram(infile))

    @ATPTools.copyParameters
    def run_program(self, program_state: Parser.ProgramState) -> Parser.ProgramState:
        """
        Runs the program based on the current program state that is provided.
        :param program_state: The current program state
        :return: the program state after executing the current line
        """
        if program_state.current_pos == len(program_state.instructions) - 1:
            print("finished")
            print(program_state)
            return program_state
        return self.run_program(Parser.runProgram(program_state))


if __name__ == '__main__':
    argParser = argparse.ArgumentParser(description="Interpreter for ATP++ programs")
    argParser.add_argument('-i', '--input', type=str, nargs='?', help="Full path to the input program")
    arguments = argParser.parse_args()
    if arguments.input is None:
        input_file = input("Please enter a path to the input program:")
    else:
        input_file = arguments.input
    valid_file = False
    while not valid_file:
        if os.path.exists(input_file):
            valid_file = True
            break
        else:
            print("The file at {0} does not exist".format(input_file))
        input_file = input("Please enter a path to the input program:")
    start_time = time()
    sys.setrecursionlimit(0x1000000)
    threading.stack_size(256000000)  # set stack to 256mb
    t = threading.Thread(target=run(), kwargs={"infile":input_file})
    t.start()
    t.join()
