import sys
import threading
from functools import reduce
from pprint import pprint
from time import time

import Lexer
import Parser
import ATPTools

@ATPTools.copyParameters
def parseProgram(infile: str = "example_programs/loop.atp++"):
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
    def __call__(self):
        self.run_program(parseProgram())

    @ATPTools.copyParameters
    def run_program(self, program_state: Parser.ProgramState) -> Parser.ProgramState:
        if program_state.current_pos == len(program_state.instructions) -1:
            print("finished")
            print(program_state)
            return program_state
        return self.run_program(Parser.runProgram(program_state))


# print(Lexer.JumpGreaterOrEqual.regex)
start_time = time()
sys.setrecursionlimit(0x1000000)
threading.stack_size(256000000)  # set stack to 256mb
t = threading.Thread(target=run())
t.start()
t.join()
