# First IPP 23/24 course project. Simple parser in python 3.10

Documentation of Project Implementation for IPP 2023/2024 \
Name and surname: Kirill Shchetiniuk\
Login: xshche05

# Documentation for task #1 (parse.py)
As a task we have to implement simple **IPPcode24** (assembly like language) parser. As an input we gets data from *stdin*, analyze input code according to basic syntax rules of provided language. Parser validates header in input code (got expected header and header got before instructions), validates opcodes according to opcode lexical form and existence of this particular instruction opcode in instruction set, next we validate instruction's arguments according to the described instruction's syntax. As a last thing we transform a valid code to the XML form, provided by the task, and out doc to *stdout*. In case of errors script returns exit code according to errors described in the task. 

## Getting the data
In the beginning of each script run, script reads input using the `Reader` instance, which is defined to use *stdin* as input data stream. `Reader` also provide a method to convert input to the list of particular lines of code.
## Input data parsing
After reading of all data from input stream, script initialize a `Parser` object, which accepts a list of lines during initialization. To start parsing, script calls `parse()` method provided by `Parser` class.
### Accepted instruction set
Parsing in the beginning of the module has an initializing of `InstructionSet` object, which is provided for easy  registration/addition of acceptable instructions. `register_header()` method is defines language header, `register_opcode()` defines particular instructions with their argument syntax. In general `InstructionSet` provides an easy interface to adding new instructions and editing instructions' configuration.
### Looking for a header
Each parsing run begins with looking for a header, in case of comments before the header they are just removed. In case of something except header and comments parser raises an error with code  `21`. In case of header we change `look_for_header` flag and begin a new iteration.
### Removing comments
In case of appearing of comment in some line, script remove the comment and increase comment counter by 1 and begin a new iteration
### Parsing instructions
Instruction parsing is simply validation instruction parts and building an instruction using the `InstructionBuilder`
#### Opcode parsing
In case if after the removing comment we don't get an empty line, we continue current iteration with instruction parsing. First of all, we splits opcode form instruction arguments, next check if opcode is presented in instruction set and continue current iteration, otherwise we raises an error with code `22` in case of opcode kind string and `23` otherwise. 
#### Argument parsing
Argument parsing is simply adding an argument string to argument list of instruction builder, for later validation.
#### Argument validation
After finishing instruction building (setting instruction order an running the `build()` method of `InstructionBuilder`) we simply runs `validate()` method of `Instruction` class. This method simply looks every possible type of each argument and checks if one of this types is corresponding to expected argument type. In case none corresponding types, parser raises an exception with code `23`.
#### Instruction final
After all validations, instructions is being added to instruction flow of `Program` object.

## Data output
After parsing using the `parse()` method of `Parser` class, method returns an `Program` object. `Program` object simply serializes using property `xml_string`, which is recursively gets an XML nodes of instruction and arguments.

## Extensions
Here would be described implemented extensions such as `STATP` and `NVP`

### STATP
This extension is implemented using custom argument parser and `Program` object methods. During argument parsing form different statistic groups according to user command line arguments.

During parsing, parser affects statistics counters in program object such as comment counter. Adding an instruction to instruction flow of program also affects internal counters, which changes according to instruction that was added.

Every stat group is a fishbone for statistic out, after parsing finishing, this fishbone is filled with values and prints to the provided file.

Extension could produce more than one file at the same time, but do not allow to print different stat groups to one file.

### NVP
Full script is written according to OOP principles, most of implemented classes is also use python magic methods such as `__str__`, `__eq__` for better implementing different limitations and validity checks. Script uses different module-files, where which file contains logic for corresponding thing. The main entry point is located in `parse.py` file, and from this point all other modules are called.

For implementation was used one of the design patterns such as **Builder Pattern** which is supposed to help to build complex objects such as `Instruction` (builds by using `InstructionBuilder`) and `Prorgam` (builds by using `Parser`)
