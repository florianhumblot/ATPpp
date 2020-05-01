


  
# ATP++  
an assembly-lookalike language for the Advanced Technical Programming course.  
  
## Language features  
This simple language supports the following features:  
  
- (unlimited) named variables  
- simple mathematics (not chained)  
   - addition  
   - subtraction  
   - multiplication  
   - division  
   - modulo  
   - increment  
   - decrement  
- Jumps  
   - using comparison operators  
   - labels  
- Printing
   - variables
   - strings
   - immediate values
  
This language implementation is Turing Complete, this is proven by a counter-machine implementation (which can be found at: [counter_machine.atp++](https://github.com/florianhumblot/ATPpp/blob/master/example_programs/counter_machine.atp++))  
  
## Using the language  
  
To start using the language, just write a program in ATP++ and run the file using any of the following command:  
```  
python3 main.py -i path-to-your-file.atp++  
python3 main.py --input path-to-your-file.atp++  
python3 main.py  
```  
Running the interpreter without an argument will prompt you for a path within the program.  

### Example programs
There are a few example programs that are ready to run, you can find all of them in [the example_programs folder](https://github.com/florianhumblot/ATPpp/blob/master/example_programs/)
  
  
## Syntax  
  
|  Keyword  |  Description  | Simple variant |  
| -- | -- | -- |  
|  `NOP` |  No-op instruction  | N |  
|  `SET` |  Declares a variable and sets it to the specified value or 0 if no value is specified  | Y |  
|  `DECL` |  Declares a label  | N |  
|  `INC` |  Increments a variable  | N |  
|  `DEC` |  Decrements a variable  | N |  
|  `ADD` |  Addition of variable with a given value/variable  | Y |  
|  `SUB` |  Subtraction of a variable with a given value/variable  | Y |  
|  `MUL` |  Multiplication of a variable with a given value/variable  | Y |  
|  `DIV` |  Division of a variable with a given value/variable  | Y |  
|  `MOD` |  Modulus of a variable with a given value/variable  | Y |  
|  `JE` |  Jumps to specified label if variable/value is equal to given | Y |  
|  `JNE` |  Jumps to specified label if variable/value is not equal to given variable/value | Y |  
|  `JL` |  Jums to specified label if variable is less than given variable/value | Y |  
|  `JG` |  Jumps to specified label if variable is greater than given variable/value | Y |  
|  `JGE` |  Jumps to specified label if variable is greater than or equal to given variable/value | Y |  
|  `JLE` |  Jumps to specified label if variable is less than or equal to given variable/value | Y |  
|  `PRINT` |  Prints the given variable/value  | N |  
  
Commands that have a "Simple" variant (annotated with a `Y` in the above table) have two possible signatures, a complex and a simple one.  
The complex signature of such an instruction is as follows (except for jumps):  
  
`KEYWORD target_variable left right`  
  
This means that the value in `target_variable` will be overwritten by the result of the operation. i.e.:  
`ADD my_var 5 10`  
  
Will result in `my_var` having a value of `15` irrespective of it's starting value.  
  
The simple signature of such an instruction is as follows:  
`KEYWORD target_variable right`  
  
This means that the value in `target_variable` is both the receiver of the computed value and the left operand for the selected operation. i.e.:  
  
`ADD myvar 20`  
  
If the value in `myvar` is `10` when running this instruction, the value stored in `myvar` after the instruction will be `30`.

For jumps the rule for the simple variant is that the left-operand is the value `0` and the syntax is as follows:

`KEYWORD label right` 

where `right` is a value or a variable.

The table below describes the formats for the different tokens (variables, immediate values and labels). If the casing of a character is not specified, both upper- and lowercase characters are allowed. Letters are any letter from the ASCII character set (a-z)

|token| pattern | Examples |
|--|--| -- | 
| label | A dot (`.`) followed by at least one letter optionally followed by any number of letters and numbers | `.myLabel`<br>`.a10label`<br>`.a`<br>`.MyLabel`<br>`.MYLABEL` |
| variable | at least one letter followed by any number of letters and/or numbers| `var`<br>`var10`<br>`VAR`<br>`my10thVar`|
|Immediate value|Starts with an optional sign (`+/-`), followed by any number of numbers, optionally followed by a dot (`.`), optionally followed by any number of numbers |`1`<br>`20`<br>`+5`<br>`-10`<br>`1.5`<br>`-23.42`<br>`+35.104`|
|String | Starts and ends with `"` and can contain any of the following characters: letters, numbers, spaces, and the following special characters: `.!,\/-+%#'@&^$~*()_{}[];:<>` | `"My string!"`<br>`"Hello World!"`<br>`"This is a test string 123.!@#$%^&(*)%^*){}{[][]"` |
| Comments | Comments must start with exactly one `#` followed by any number of characters, including letters, numbers and the following special characters: `.!,\/-+%#'@&^$~*()_{}[];:<>` | `# This is a comment`<br>`# This is a comment 122340 !@#$%#$%^&*(`|

The following restrictions apply to the language:
 - Comments can be placed at the end of any line of code and on any blank line of code.
 - String can __only__ be used with the `PRINT` function.
 - Division and modulo by `0` will lead to an error and the interpreter stopping early.
 - Calling functions/jumps on non-existent variables and/or labels will lead to an error and the interpreter stopping early.
 - All simple-variants of functions will assume the left parameter to be `0` if no third argument is given except in the case of arithmetic functions, in which case it will use the current value of the target as the left operand.
 - There is a system-dependent limit on the size of the program (iterations count as additional lines of code for the purposes of this limitation), this is due to stack limits imposed on us by the operating system.
 - The fact that immediate values are allowed to use a sign (`+-`) means that your mathematics can have unexpected results!
	 - i.e.: `ADD myvar 10 -5` will result in `myvar` having the value `5` because `(10) + (-5) = 5`
	 - i.e.: `SUB myvar 5 -10` will result in `myvar` having the value `15` because `(5)-(-10) = 15` 

## Extending the language

Adding new commands / functions is quite easy. While this is not supported within the language itself (except by the use of labels, but we lack branching so they aren't quite functions) adding features to the core language can be done as follows:

1. Add a class that is a subclass of `Instruction` (or `Jump`) to `Lexer.py`
2. Add the regular expression that matches the pattern of your instruction to the class as a static member
	- Tip: use named groups in your regular expression to easily get the right group in your function. 
		- Named groups are created as follows: `r"(?P<my_named_group>\w+)"` 
3. Add the name of your class to the `instruction_map` variable in the `matchToken` function in `Lexer.py` 
4. Add a function that will execute your instruction to `Parser.py`.
	- Make sure to use the `@ATPTools.copyParameters` decorator to get all your parameters by-value instead of by-reference
	- Return the program state at the end of your function
	- If anything causes your instruction to not be able to execute properly, append an error message to `program_state.errors`. The interpreter will stop the program execution as soon as this field is populated. 
5. Add a case for your instruction to the if/elif chain to the `runProgram` function in `Parser.py` that executes the function you created in step 4
6. Add your new instruction to the table above!
