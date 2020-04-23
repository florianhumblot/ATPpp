from functools import reduce

import Lexer
import Parser
from pprint import pprint
import re
from time import time
import sys

sys.setrecursionlimit(150000)

with open("example_programs/loop.atp++", "r") as file:
    start = time()
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
    ps = Parser.run(ps)
    print(ps)
    print("Program finished in {} seconds".format(time() - start))
