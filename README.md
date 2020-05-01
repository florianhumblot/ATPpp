
  
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
- Printing variables  
  
This language implementation is Turing Complete, this is proven by a counter-machine implementation (which can be found at: [counter_machine.atp++](https://github.com/florianhumblot/ATPpp/blob/master/example_programs/counter_machine.atp++))  
  
## Using the language  
  
To start using the language, just write a program in ATP++ and run the file using any of the following command:  
```  
python3 main.py -i path-to-your-file.atp++  
python3 main.py --input path-to-your-file.atp++  
python3 main.py  
```  
Running the interpreter without an argument will prompt you for a path within the program.  
  
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
