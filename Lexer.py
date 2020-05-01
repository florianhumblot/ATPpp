from enum import Enum
from functools import reduce
from typing import List, Union, Tuple, Optional
import re
import ATPTools


class RegexMap(Enum):
    VAR = "[a-zA-Z]+([a-zA-Z0-9])*"  # Starts with a letter, optionally followed by any number or letter
    VAL = "([-+]?)(\d*)(\.?\d*)"  # optional sign, followed by any amount of numbers, optionally a floating point number
    WHITESPACE = "\s+"  # One or more whitespace characters
    VAR_OR_CONST = "(" + str(VAR) + "|" + str(VAL) + ")"  # Combines the VAR and VAL regexes, matching either one.
    LABEL = "\.[a-zA-Z0-9]+"  # Starts with a dot, followed by one or more letters
    VAR_CONST_OR_STRING = "(" + str(VAR) + "|" + str(VAL) + "|\"[\w\d\s\?\.\!\,\\\/\-\+\%\#\'\@\&\^\$\~\*\(\)\_\{\}\[\]\;\:\<\>]*\")"
    COMMENT = "(\#{1}[\w\d\s\?\.\!\,\\\/\-\+\%\#\'\@\&\^\$\~\*\(\)\_\{\}\[\]\;\:\<\>]*)?"


class Instruction:
    regex = None

    def __init__(self):
        self.parameters = []

    def __str__(self) -> str:
        return "Instruction"


class Jump(Instruction):
    regex = None

    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return "Jump"


class SetSimple(Instruction):
    regex = "^SET[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self) -> str:
        return "SET {target}"


class Set(Instruction):
    regex = "^SET[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "SET {target} {value}"


class Declare(Instruction):
    regex = "^DECL[ \t]+(?P<label>\." + str(RegexMap.VAR.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["label"]

    def __str__(self) -> str:
        return "DECL {label}"


class Increment(Instruction):
    regex = "^INC[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self) -> str:
        return "INC {target}"


class Decrement(Instruction):
    regex = "^DEC[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target"]

    def __str__(self) -> str:
        return "DEC {target}"


class AddSimple(Instruction):
    regex = "^ADD[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "ADD {target} {var|value}"


class Add(Instruction):
    regex = "^ADD[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "ADD {target} {var|value} {var|value}"


class SubtractSimple(Instruction):
    regex = "^SUB[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "SUB {target} {var|value}"


class Subtract(Instruction):
    regex = "^SUB[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "SUB {target} {var|value} {var|value}"


class MultiplySimple(Instruction):
    regex = "^MUL[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "MUL {target} {var|value}"


class Multiply(Instruction):
    regex = "^MUL[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "MUL {target} {var|value} {var|value}"


class DivideSimple(Instruction):
    regex = "^DIV[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "DIV {target} {var|value}"


class Divide(Instruction):
    regex = "^DIV[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "DIV {target} {left} {right}"


class ModuloSimple(Instruction):
    regex = "^MOD[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "MOD {target} {right}"


class Modulo(Instruction):
    regex = "^MOD[ \t]+(?P<target>" + str(RegexMap.VAR.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "MOD {target} {left} {right"


class JumpEqualSimple(Jump):
    regex = "^JE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JE {target} {right}"


class JumpEqual(Jump):
    regex = "^JE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*(" + str(RegexMap.COMMENT.value) + "[ \t]*)$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "{target} {right}"


class JumpNotEqualSimple(Jump):
    regex = "^JNE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JNE {target} {left} {right}"


class JumpNotEqual(Jump):
    regex = "^JNE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "JNE {target} {left} {right}"


class JumpLessThanSimple(Jump):
    regex = "^JL[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JL {target} {right}"


class JumpLessThan(Jump):
    regex = "^JL[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "JL {target} {left} {right}"


class JumpGreaterThanSimple(Jump):
    regex = "^JG[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JG {target} {right}"


class JumpGreaterThan(Jump):
    regex = "^JG[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "JG {target} {left} {right}"


class JumpGreaterOrEqualSimple(Jump):
    regex = "^JGE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JGE {target} {right}"


class JumpGreaterOrEqual(Jump):
    regex = "^JGE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "JGE {target} {left} {right}"


class JumpLessOrEqualSimple(Jump):
    regex = "^JLE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "right"]

    def __str__(self) -> str:
        return "JLE {target} {right}"


class JumpLessOrEqual(Jump):
    regex = "^JLE[ \t]+(?P<target>" + str(RegexMap.LABEL.value) + ")[ \t]+(?P<left>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]+(?P<right>" + str(
        RegexMap.VAR_OR_CONST.value) + ")[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = ["target", "left", "right"]

    def __str__(self) -> str:
        return "JLE {target} {left} {right}"


class Nop(Instruction):
    regex = "^(NOP|$|[ \t]*| *$)[ \t]*" + str(RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        self.parameters = []

    def __str__(self) -> str:
        return "NOP"


class Print(Instruction):
    regex = "^PRINT[ \t]+(?P<right>" + str(RegexMap.VAR_CONST_OR_STRING.value) + ")[ \t]*" + str(
        RegexMap.COMMENT.value) + "[ \t]*$"

    def __init__(self):
        super().__init__()
        super().__init__()
        self.parameters = ["right"]

    def __str__(self) -> str:
        return "PRINT {value}"


# strToList :: str -> [str]
@ATPTools.copyParameters
def strToList(input_string: str) -> List[str]:
    if input_string.find(' ') == -1:
        return [input_string]
    return [input_string[:input_string.index(" ")]] + strToList(input_string[input_string.index(" ") + 1:])


# stringToLines :: str -> [str]
@ATPTools.copyParameters
def strToLines(input_string: str) -> List[str]:
    if input_string.find('\n') == -1:
        return [input_string]
    return [input_string[:input_string.index('\n')]] + strToLines(input_string[input_string.index('\n') + 1:])


# mapDataTypes :: dict -> dict
@ATPTools.copyParameters
def mapDataTypes(input_dict: dict) -> dict:
    return dict(map(lambda kv: (kv[0], strToDataType(kv[1])), input_dict.items()))


# regexTest :: Instruction -> str -> Either dict None
@ATPTools.copyParameters
def regexTest(instruction_type: Instruction, string: str) -> Union[dict, None]:
    pattern = re.compile(instruction_type.regex)
    match = re.fullmatch(pattern, string)
    return mapDataTypes(match.groupdict()) if match is not None else None


# strToDataType :: str -> Either str float int
@ATPTools.copyParameters
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
@ATPTools.copyParameters
def matchToken(input_string: str) -> Union[Tuple[Instruction, dict], None]:
    instruction_map = [
        SetSimple, Set,
        Declare, Increment, Decrement,
        AddSimple, Add,
        SubtractSimple, Subtract,
        MultiplySimple, Multiply,
        DivideSimple, Divide,
        ModuloSimple, Modulo,
        JumpEqualSimple, JumpEqual,
        JumpNotEqualSimple, JumpNotEqual,
        JumpLessThanSimple, JumpLessThan,
        JumpGreaterThanSimple, JumpGreaterThan,
        JumpGreaterOrEqualSimple, JumpGreaterOrEqual,
        JumpLessOrEqualSimple, JumpLessOrEqual,
        Nop, Print
    ]
    return reduce(
        lambda x, y: x if x[1] is not None else y,
        map(
            lambda x: (x, regexTest(x, input_string)),
            instruction_map
        )
    )


# lexInput :: [str] -> [Tuple[Instruction, dict]]
@ATPTools.copyParameters
def lexInput(input_program: List[str]) -> List[Tuple[Instruction, dict]]:
    if len(input_program) == 0:
        return []
    return [matchToken(input_program[0])] + lexInput(input_program[1:])
