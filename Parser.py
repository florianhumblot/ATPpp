from typing import List, Union, Tuple

import ATPTools
import Lexer


class ProgramState:
    """
    Container for our program state, Abstract Data Type that does not contain any methods apart from string
    representation.
    """

    def __init__(self):
        self.variables = {}
        self.current_pos = -1
        self.warnings = []
        self.errors = []
        self.instructions = []
        self.labels = {}

    def __str__(self) -> str:
        return "ProgramState: [\n\tcurrent line: {line}\n\tvariables: {vars}\n\tlabels: {labels}\n\twarnings: {warn}\n\terrors: {err}\n]\n".format(
            vars=self.variables, labels=self.labels,
            warn=self.warnings,
            err=self.errors, line=self.current_pos + 1)


# setVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def setVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Sets a variable to the correct value in the program state
    :param ps: Current program state
    :param parameters: parameters for the operation
    :return: new program state after the transformation
    """
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
    """
    Checks that a variable is either the correct type (float/int) or if it is an existing variable in the program state
    :param ps: current program state
    :param key: variable name or immediate value
    :param parameters: parameters for the operation
    :return: Either str/float/int or None if there is an error.
    """
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
def checkPrintParameters(ps: ProgramState, parameters: dict) -> Tuple[ProgramState, Union[int, float, str]]:
    """
    Checks whether the parameters for the PRINT instruction are valid.
    :param ps: current program state
    :param parameters: the parameters for the instruction
    :return: ProgramState with an int, float or str
    """
    if parameters["right"] not in ps.variables.keys():
        if parameters["right"][0] == '"' and parameters["right"][-1] == '"':
            right = parameters["right"]
        else:
            right = checkVariable(ps, "right", parameters)
    else:
        right = ps.variables[parameters["right"]]
    return ps, right


# checkFuncArguments :: ProgramState -> dict -> str -> Tuple(ProgramState, Union[float, int, None], Union[float, int, None])
@ATPTools.copyParameters
def checkFuncArguments(ps: ProgramState, parameters: dict, instruction: str) -> Tuple[
    ProgramState, Union[float, int, None], Union[float, int, None]]:
    """
    Checks the arguments for a function and corrects them for the 2-argument versions of the functions by replacing the
    left operand with the value of the target
    :param ps: current program state
    :param parameters: parameters for the function
    :param instruction: which instruction is being checked for error messaging
    :return: ProgramState, Left (either float, int or none on error) and Right (either float, int or None on error)
    """
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


# checkJumpArguments :: ProgramState -> dict -> str -> Tuple(ProgramState, Union[float, int, None], Union[float, int, None])
@ATPTools.copyParameters
def checkJumpArguments(ps: ProgramState, parameters, instruction: str) -> Tuple[
    ProgramState, Union[float, int, None], Union[float, int, None]]:
    """
    Checks the arguments for jump instructions. These are different from the arguments for normal functions which is why
    they have their own check functions.
    :param ps: current program state
    :param parameters: parameters for the jump
    :param instruction: which instruction for debug information
    :return: program state, Left (either float, int or None on error), Right (either float, int or None on error)
    """
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
    """
    Increments a variable
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after incrementing
    """
    if "target" not in parameters.keys():
        ps.errors.append("target must be specified for increment on line {0}".format(ps.current_pos))
    ps.variables[parameters["target"]] = ps.variables[parameters["target"]] + 1
    return ps


# decrementVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def decrementVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Decrement a variable
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after decrementing
    """
    if "target" not in parameters.keys():
        ps.errors.append("target must be specified for decrement on line {0}".format(ps.current_pos))
    ps.variables[parameters["target"]] = ps.variables[parameters["target"]] - 1
    return ps


# addToVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def addToVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Adds two values or variables and stores the result in the target
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after addition
    """
    ps, left, right = checkFuncArguments(ps, parameters, "ADD")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left + right
    return ps


# subtractFromVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def subtractFromVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Subtract two values or variables and stores the result in the target
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after subtraction
    """
    ps, left, right = checkFuncArguments(ps, parameters, "SUB")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left - right
    return ps


# multiplyByVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def multiplyByVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Multiplies two values or variables and stores the result in the target
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after multiplication
    """
    ps, left, right = checkFuncArguments(ps, parameters, "MUL")
    if left is None or right is None:
        return ps
    ps.variables[parameters["target"]] = left * right
    return ps


# divideByVariable :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def divideByVariable(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Divides two values or variables and stores the result in the target
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after division
    """
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
    """
    computes the modulo of two values or variables and stores the result in the target
    :param ps: current program state
    :param parameters: parameters for the function
    :return: program state after modulo operation
    """
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
    """
    Jumps to the target label if right is equal to left
    :param ps: current program state
    :param parameters: parameters for the function
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JE")
    if left is None or right is None:
        return ps
    if left == right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_not_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_not_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Jumps to the target label if right is not equal to left
    :param ps: current program state
    :param parameters: parameters for the function
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JNE")
    if left is None or right is None:
        return ps
    if left != right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_less_than :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_less_than(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Jumps to the target label if left is less than right
    :param ps: current program state
    :param parameters: parameters for the jump
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JL")
    if left is None or right is None:
        return ps
    if left < right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_greater_than :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_greater_than(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Jumps to the target label if left is greater than right
    :param ps: current program state
    :param parameters: parameters for the jump
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JG")
    if left is None or right is None:
        return ps
    if left > right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_less_or_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_less_or_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Jumps to the target label if left is less than or equal to right
    :param ps: current program state
    :param parameters: parameters for the jump
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JLE")
    if left is None or right is None:
        return ps
    if left <= right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# jump_greater_or_equal :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def jump_greater_or_equal(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Jumps to the target label if left is greater than or equal to right
    :param ps: current program state
    :param parameters: parameters for the jump
    :return: modified program state
    """
    ps, left, right = checkJumpArguments(ps, parameters, "JGE")
    if left is None or right is None:
        return ps
    if left >= right:
        ps.current_pos = ps.labels[parameters["target"]]
    return ps


# ATPPrint :: ProgramState -> dict -> ProgramState
@ATPTools.copyParameters
def ATPPrint(ps: ProgramState, parameters: dict) -> ProgramState:
    """
    Prints the given value, variable or string
    :param ps: current program state
    :param parameters: parameters for the print
    :return: program state
    """
    ps, right = checkPrintParameters(ps, parameters)
    if right is None:
        ps.errors.append("Incorrect parameter for PRINT on line {0}".format(ps.current_pos))
        return ps
    print("> {}".format(right))
    return ps


# ATPDump :: ProgramState -> ProgramState
@ATPTools.copyParameters
def ATPDump(ps: ProgramState) -> ProgramState:
    """
    Dumps the program state to stdio
    :param ps: current program state
    :return: program state
    """
    print("-------------DUMPING PROGRAM STATE-------------")
    print(ps)
    print("-----------END DUMPING PROGRAM STATE-----------")
    return ps


# parseLabels :: List[Tuple[Instruction, dict]] -> int -> dict
@ATPTools.copyParameters
def parseLabels(tokens: List[Tuple[Lexer.Instruction, dict]], counter: int = 0) -> dict:
    """
    Parse the labels we find in the program so that we can jump to them.
    This adds the labels to a dict with the key being the label and the value being the position
    :param tokens: List of instructions
    :param counter: current line number
    :return: dict of labels with their position
    """
    if len(tokens) == 0:
        return {}
    if tokens[0][0] == Lexer.Declare:
        # Je kunt dicts niet samenvoegen, dus we maken een nieuwe dict aan met de vorige dict en de return waarde van
        # de recursieve function-call
        return dict(**{tokens[0][1]["label"]: counter}, **parseLabels(tokens[1:], counter + 1))
    else:
        return parseLabels(tokens[1:], counter + 1)


@ATPTools.copyParameters
def runProgram(ps: ProgramState) -> ProgramState:
    """
    Advances the program counter by one and executes the instruction at the program counter.
    :param ps: current program state
    :return: program state after execution of the current instruction
    """
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
    elif current_token == Lexer.Dump:
        ps = ATPDump(ps, current_parameters)
    if len(ps.errors) > 0:
        return ps
    return ps
