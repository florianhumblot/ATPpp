from enum import Enum
from functools import reduce
from typing import List, Union, Tuple
import re
import ast


class RegexMap(Enum):
    VAR = "[a-zA-Z]+([a-zA-Z0-9])*"  # Starts with a letter, optionally followed by any number or letter
    VAL = "([-+]?)(\d*)(\.?\d*)"  # optional sign, followed by any amount of numbers, optionally a floating point number
    WHITESPACE = "\s+"  # One or more whitespace characters
    VAR_OR_CONST = "(" + str(VAR) + "|" + str(VAL) + ")"  # Combines the VAR and VAL regexes, matching either one.
    LABEL = "\.[a-zA-Z]+"  # Starts with a dot, followed by one or more letters


class Instruction:
    regex = None

    def __init__(self):
        self.parameters = []

    def __str__(self):
        return "Instruction"


class Jump(Instruction):
    regex = None

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Jump"


class SetSimple(Instruction):
    regex = "^SET (?P<target>" + str(RegexMap.VAR.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self):
        return "SET {target}"


class Set(Instruction):
    regex = "^SET (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "SET {target} {value}"


class Declare(Instruction):
    regex = "^DECL (?P<label>\." + str(RegexMap.VAR.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["label"]

    def __str__(self):
        return "DECL {label}"


class Increment(Instruction):
    regex = "^INC (?P<target>" + str(RegexMap.VAR.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self):
        return "INC {target}"


class Decrement(Instruction):
    regex = "^DEC (?P<target>" + str(RegexMap.VAR.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self):
        return "DEC {target}"


class AddSimple(Instruction):
    regex = "^ADD (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "ADD {target} {var|value}"


class Add(Instruction):
    regex = "^ADD (?P<target>" + str(RegexMap.VAR.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "ADD {target} {var|value} {var|value}"


class SubtractSimple(Instruction):
    regex = "^SUB (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "SUB {target} {var|value}"


class Subtract(Instruction):
    regex = "^SUB (?P<target>" + str(RegexMap.VAR.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "SUB {target} {var|value} {var|value}"


class MultiplySimple(Instruction):
    regex = "^MUL (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "MUL {target} {var|value}"


class Multiply(Instruction):
    regex = "^MUL (?P<target>" + str(RegexMap.VAR.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "MUL {target} {var|value} {var|value}"


class DivideSimple(Instruction):
    regex = "^DIV (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "DIV {target} {var|value}"


class Divide(Instruction):
    regex = "^DIV (?P<target>" + str(RegexMap.VAR.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "DIV {target} {left} {right}"


class ModuloSimple(Instruction):
    regex = "^MOD (?P<target>" + str(RegexMap.VAR.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "MOD {target} {right}"


class Modulo(Instruction):
    regex = "^MOD (?P<target>" + str(RegexMap.VAR.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "MOD {target} {left} {right"


class JumpEqualSimple(Jump):
    regex = "^JE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JE {target} {right}"


class JumpEqual(Jump):
    regex = "^JE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "{target} {right}"


class JumpNotEqualSimple(Jump):
    regex = "^JNE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JNE {target} {left} {right}"


class JumpNotEqual(Jump):
    regex = "^JNE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "JNE {target} {left} {right}"


class JumpLessThanSimple(Jump):
    regex = "^JL (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JL {target} {right}"


class JumpLessThan(Jump):
    regex = "^JL (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "JL {target} {left} {right}"


class JumpGreaterThanSimple(Jump):
    regex = "^JG (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JG {target} {right}"


class JumpGreaterThan(Jump):
    regex = "^JG (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "JG {target} {left} {right}"


class JumpGreaterOrEqualSimple(Jump):
    regex = "^JGE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JGE {target} {right}"


class JumpGreaterOrEqual(Jump):
    regex = "^JGE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "JGE {target} {left} {right}"


class JumpLessOrEqualSimple(Jump):
    regex = "^JLE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self):
        return "JLE {target} {right}"


class JumpLessOrEqual(Jump):
    regex = "^JLE (?P<target>" + str(RegexMap.LABEL.value) + ") (?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ") (?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self):
        return "JLE {target} {left} {right}"


class Nop(Instruction):
    regex = "^(NOP|$|[ \t]*| *$)$"

    def __init__(self):
        super().__init__()
        self.parameters = []

    def __str__(self):
        return "NOP"


# strToList :: str -> [str]
def strToList(input_string: str) -> List[str]:
    if input_string.find(' ') == -1:
        return [input_string]
    return [input_string[:input_string.index(" ")]] + strToList(input_string[input_string.index(" ") + 1:])


# stringToLines :: str -> [str]
def strToLines(input_string: str) -> List[str]:
    if input_string.find('\n') == -1:
        return [input_string]
    return [input_string[:input_string.index('\n')]] + strToLines(input_string[input_string.index('\n') + 1:])


def mapDataTypes(input_dict: dict) -> dict:
    return dict(map(lambda kv: (kv[0], strToDataType(kv[1])), input_dict.items()))


# regexTest :: Instruction str -> Either dict None
def regexTest(instruction_type: Instruction, string: str) -> Union[dict, None]:
    pattern = re.compile(instruction_type.regex)
    match = re.fullmatch(pattern, string)
    return mapDataTypes(match.groupdict()) if match is not None else None


def strToDataType(input_string: str) -> Union[str, float, int]:
    try:
        float(input_string)
        return float(input_string)
    except ValueError:
        try:
            int(input_string)
            return int(input_string)
        except ValueError:
            return input_string


# matchToken :: str -> Either Tuple[Instruction, dict] None
def matchToken(input_string: str) -> Union[Tuple[Instruction, dict], None]:
    instruction_map = [
        Set, SetSimple,
        Declare, Increment, Decrement,
        Add, AddSimple,
        Subtract, SubtractSimple,
        Multiply, MultiplySimple,
        Divide, DivideSimple,
        Modulo, ModuloSimple,
        JumpEqual, JumpEqualSimple,
        JumpNotEqual, JumpNotEqualSimple,
        JumpLessThan, JumpLessThanSimple,
        JumpGreaterThan, JumpGreaterThanSimple,
        JumpGreaterOrEqual, JumpGreaterOrEqualSimple,
        JumpLessOrEqual, JumpLessOrEqualSimple,
        Nop,
    ]
    return reduce(
        lambda x, y: x if x[1] is not None else y,
        map(
            lambda x: (x, regexTest(x, input_string)),
            instruction_map
        )
    )


# lexInput :: [str] -> [Tokens]
def lexInput(input_program: List[str]):
    if len(input_program) == 0:
        return []
    return [matchToken(input_program[0])] + lexInput(input_program[1:])
