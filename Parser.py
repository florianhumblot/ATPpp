from typing import List, Union, Tuple
import Lexer
import copy
import ATPTools


class ProgramState:
    def __init__(self):
        self.variables = {}
        self.current_pos = -1
        self.warnings = []
        self.errors = []
        self.instructions = []
        self.labels = {}

    def __str__(self):
        return "ProgramState: [\n\tcurrent line: {line}\n\tvariables: {vars}\n\tlabels: {labels}\n\twarnings: {warn}\n\terrors: {err}\n]\n".format(
            vars=self.variables, labels=self.labels,
            warn=self.warnings,
            err=self.errors, line=self.current_pos)


# setVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def setVariable(ps: ProgramState, parameters: dict):
    if "right" in parameters.keys():
        ps, right = checkVariable(ps, "right", parameters)
    else:
        right = 0
    if type(right) == str:
        ps.variables[parameters["target"]] = right
    else:
        ps.variables[parameters["target"]] = right
    return ps


# checkVariable :: ProgramState -> str -> dict -> Either Tuple[ProgramState, Either str float int None] ProgramState
@ATPTools.copyParameters
def checkVariable(ps: ProgramState, key: str, parameters: dict) -> Union[
    Tuple[ProgramState, Union[str, float, int, None]], ProgramState]:
    var = parameters[key]
    if type(var) == str:
        if var in ps.variables.keys():
            return ps, ps.variables[var]
        else:
            ps.errors.append("Unknown variable {0} on line {1}".format(var, ps.current_pos))
            return ps, None
    else:
        return ps, var


# checkPrintParameters :: ProgramState -> dict -> Tuple[ProgramState, Either int float str]
@ATPTools.copyParameters
def checkPrintParameters(ps: ProgramState, parameters: dict):
    if parameters["right"] not in ps.variables.keys():
        if parameters["right"][0] == '"' and parameters["right"][-1] == '"':
            right = parameters["right"]
        else:
            right = checkVariable(ps, "right", parameters)
    else:
        right = ps.variables[parameters["right"]]
    return ps, right


# checkFuncArguments :: ProgramState -> dict -> str -> Tuple(ProgramState, Union[float, int None], Union[float, int None])
@ATPTools.copyParameters
def checkFuncArguments(ps: ProgramState, parameters: dict, instruction: str):
    if "target" not in parameters.keys() or parameters["target"] in ("", None):
        ps.errors.append("{1} expects a name on line {0}".format(ps.current_pos, instruction))
        return ps, None, None
    if parameters["target"] not in ps.variables.keys():
        print("parameters")
        ps.errors.append(
            "Unknown variable {0} on line {1} for instruction {2}".format(parameters["target"], ps.current_pos,
                                                                          instruction))
        return ps, None, None
    if len(parameters) >= 2:
        ps, right = checkVariable(ps, "right", parameters)
        ps, left = checkVariable(ps, "target", parameters)
        if len(parameters) == 3:
            ps, left = checkVariable(ps, "left", parameters)
        return ps, left, right
    ps.errors.append(
        "Invalid parameter count for {2} function. Got {0} parameters, expected {1}.".format("[2,3]",
                                                                                             len(parameters),
                                                                                             instruction))
    return ps, None, None


# checkJumpArguments :: ProgramState -> dict -> str -> Tuple(ProgramState, Union[float, int None], Union[float, int None])
@ATPTools.copyParameters
def checkJumpArguments(ps: ProgramState, parameters, instruction: str):
    if "target" not in parameters.keys() or parameters["target"] in ("", None):
        ps.errors.append("{1} expects a label on line {0}".format(ps.current_pos, instruction))
        return ps, None, None
    if parameters["target"] not in ps.labels.keys():
        ps.errors.append("Unknown label {0} on line {1}".format(parameters["target"], instruction))
        return ps, None, None
    if len(parameters) >= 2:
        ps, right = checkVariable(ps, "right", parameters)
        ps, left = ps, 0
        if len(parameters) == 3:
            ps, left = checkVariable(ps, "left", parameters)
        return ps, left, right
    ps.errors.append(
        "Invalid parameter count for {2} function. Got {0} parameters, expected {1}.".format("[2,3]",
                                                                                             len(parameters),
                                                                                             instruction))
    return ps, None, None


# incrementVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def incrementVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    if "target" not in parameters.keys():
        ps.errors.append("target must be specified for increment on line {0}".format(ps.current_pos))
    ps.variables[parameters["target"]] = ps.variables[parameters["target"]] + 1
    return ps


# decrementVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def decrementVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    if "target" not in parameters.keys():
        ps.errors.append("target must be specified for decrement on line {0}".format(ps.current_pos))
    ps.variables[parameters["target"]] = ps.variables[parameters["target"]] - 1
    return ps


# addToVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def addToVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkFuncArguments(ps, parameters, "ADD")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left + right
    return ps


# subtractFromVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def subtractFromVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkFuncArguments(ps, parameters, "SUB")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left - right
    return ps


# multiplyByVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def multiplyByVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkFuncArguments(ps, parameters, "MUL")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left * right
    return ps


# divideByVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def divideByVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkFuncArguments(ps, parameters, "DIV")
    if left is None or right is None:
        return ps
    if right == 0:
        ps.errors.append("Division by zero on line {0}".format(ps.current_pos))
    else:
        ps.variables[parameters["target"]] = left / right
    return ps


# modulo :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def modulo(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkFuncArguments(ps, parameters, "DIV")
    if left is None or right is None:
        return ps
    if right == 0:
        ps.errors.append("Division by zero on line {0}".format(ps.current_pos))
    else:
        ps.variables[parameters["target"]] = left % right
    return ps


# jump_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JE")
    if left is None or right is None:
        return ps
    if left == right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_not_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_not_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JNE")
    if left is None or right is None:
        return ps
    if left != right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_less_than :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_less_than(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JL")
    if left is None or right is None:
        return ps
    if left < right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_greater_than :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_greater_than(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JG")
    if left is None or right is None:
        return ps
    if left > right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_less_or_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_less_or_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JLE")
    if left is None or right is None:
        return ps
    if left <= right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_greater_or_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_greater_or_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, left, right = checkJumpArguments(ps, parameters, "JGE")
    if left is None or right is None:
        return ps
    if left >= right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# ATPPrint :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def ATPPrint(ps: ProgramState, parameters: dict) -> ProgramState:
    ps, right = checkPrintParameters(ps, parameters)
    if right is None:
        ps.errors.append("Incorrect parameter for PRINT on line {0}".format(ps.current_pos))
        return ps
    print("> {}".format(right))
    return ps


# parseLabels :: List[Tuple[Instruction, dict]] -> int -> dict
@ATPTools.copyParameters
def parseLabels(tokens: List[Tuple[Lexer.Instruction, dict]], counter: int = 0) -> dict:
    if len(tokens) == 0:
        return {}
    if tokens[0][0] == Lexer.Declare:
        return dict(**{tokens[0][1]["label"]: counter}, **parseLabels(tokens[1:], counter + 1))
    else:
        return parseLabels(tokens[1:], counter + 1)


# runProgram :: ProgramState -> ProgramState
@ATPTools.copyParameters
def runProgram(ps: ProgramState):
    if ps.current_pos == len(ps.instructions) - 1:
        return ps
    ps.current_pos += 1
    current_token, current_parameters = ps.instructions[ps.current_pos]
    if current_token == Lexer.SetSimple or current_token == Lexer.Set:
        ps = setVariable(ps, current_parameters)
    elif current_token == Lexer.Increment:
        ps = incrementVariable(ps, current_parameters)
    elif current_token == Lexer.Decrement:
        ps = decrementVariable(ps, current_parameters)
    elif current_token == Lexer.AddSimple or current_token == Lexer.Add:
        ps = addToVariable(ps, current_parameters)
    elif current_token == Lexer.SubtractSimple or current_token == Lexer.Subtract:
        ps = subtractFromVariable(ps, current_parameters)
    elif current_token == Lexer.MultiplySimple or current_token == Lexer.Multiply:
        ps = multiplyByVariable(ps, current_parameters)
    elif current_token == Lexer.DivideSimple or current_token == Lexer.Divide:
        ps = divideByVariable(ps, current_parameters)
    elif current_token == Lexer.ModuloSimple or current_token == Lexer.Modulo:
        ps = modulo(ps, current_parameters)
    elif current_token == Lexer.JumpEqualSimple or current_token == Lexer.JumpEqual:
        ps = jump_equal(ps, current_parameters)
    elif current_token == Lexer.JumpNotEqualSimple or current_token == Lexer.JumpNotEqual:
        ps = jump_not_equal(ps, current_parameters)
    elif current_token == Lexer.JumpLessThanSimple or current_token == Lexer.JumpLessThan:
        ps = jump_less_than(ps, current_parameters)
    elif current_token == Lexer.JumpGreaterThanSimple or current_token == Lexer.JumpGreaterThan:
        ps = jump_greater_than(ps, current_parameters)
    elif current_token == Lexer.JumpLessOrEqualSimple or current_token == Lexer.JumpLessOrEqual:
        ps = jump_less_or_equal(ps, current_parameters)
    elif current_token == Lexer.JumpGreaterOrEqualSimple or current_token == Lexer.JumpGreaterOrEqual:
        ps = jump_greater_or_equal(ps, current_parameters)
    elif current_token == Lexer.Print:
        ps = ATPPrint(ps, current_parameters)
    if len(ps.errors) > 0:
        return ps
    return ps
