# Brainfuck Calculator Documentation

## Introduction

*"You can't write a proper calculator in an 8-bit esoteric language with only 8 commands!" - they said.*

Well, think again! This project proves that even Brainfuck - one of the most minimalistic programming languages - can be used to create a fully functional calculator capable of handling not just 8-bit operations, but also big numbers with virtually no limits.

## Project Overview

The Brainfuck Calculator is a Python application that combines the power of Brainfuck modules for basic arithmetic operations with Python's ability to handle big numbers. It demonstrates that esoteric programming languages aren't just toys - they can be integrated into practical applications.

## Architecture

### Core Components

1. **BrainfuckOrchestrator** - The main controller class that:
   - Manages Brainfuck operation modules
   - Handles big number operations (split into base-256 cells)
   - Provides both 8-bit and big number calculation modes
   - Parses mathematical expressions

2. **BrainfuckInterpreter** - A complete Brainfuck interpreter that:
   - Executes Brainfuck code with proper memory management
   - Handles I/O operations
   - Supports loops and conditional execution
   - Maintains a tape of memory cells

3. **Operation Modules** - Individual Brainfuck programs for each arithmetic operation:
   - `addition.bf` - Adds two numbers
   - `subtraction.bf` - Subtracts two numbers
   - `multiplication.bf` - Multiplies two numbers
   - `division.bf` - Divides two numbers
   - `power.bf` - Calculates power (exponentiation)

## Features

### Dual Calculation Modes

#### 1. 8-bit Mode
- Uses pure Brainfuck modules for calculations
- Results are modulo 256 (true to Brainfuck's nature)
- Great for testing and demonstration purposes
- Activated with the `--8bit` flag

#### 2. Big Number Mode (Default)
- Uses Brainfuck concepts but with Python implementation
- No practical limits on number size
- Supports arbitrarily large integers
- Maintains the "spirit" of Brainfuck operations

### Supported Operations
- **Addition (+)** - `5+3 = 8`
- **Subtraction (-)** - `10-4 = 6`
- **Multiplication (*)** - `6*7 = 42`
- **Division (/)** - `15/3 = 5`
- **Power (^)** - `2^10 = 1024`

### Big Number Implementation

The project implements a clever big number system using base-256 cells:

```python
# Example: Number 258 (256 + 2) is represented as:
# cells = [2, 1]
# Because: 2*256^0 + 1*256^1 = 2 + 256 = 258
```

Each operation is implemented with proper carry/borrow handling for multi-cell numbers.

## Installation & Setup

### Requirements
- Python 3.6+
- No external dependencies

### Project Structure
```
brainfuck-calculator/
├── src/
│   ├── __init__.py
│   ├── orchestrator.py
│   └── interpreter.py
├── bf_modules/
│   ├── addition.bf
│   ├── subtraction.bf
│   ├── multiplication.bf
│   ├── division.bf
│   └── power.bf
└── main.py
```

## Usage

### Command Line Interface

```bash
# Single expression (big number mode)
python main.py "999+999"

# Multiple expressions
python main.py "1000*500" "999^2" "123456789*10"

# 8-bit mode
python main.py --8bit "250+10"    # Result: 4 (260 mod 256)

# Interactive mode
python main.py -i

# Interactive 8-bit mode
python main.py -i --8bit
```

### Interactive Mode

```
Mode: Big numbers (no limits)
Supported operations: +, -, *, /, ^
Enter 'help' for help, 'quit' to exit

> 999+999
= 1998

> 1000*500
= 500000

> 2^10
= 1024

> help
```

## Technical Details

### Brainfuck Modules

Each operation is implemented as a standalone Brainfuck program. For example, the addition module:

```brainfuck
# addition.bf
,
> ,
< [->+<]
> .
```

This program:
1. Reads first number (`,`)
2. Moves to next cell (`>`)
3. Reads second number (`,`)
4. Moves back (`<`) and adds the second number to first (`[->+<]`)
5. Moves to result (`>`) and outputs it (`.`)

### Memory Management

The interpreter uses:
- **Tape size**: 30,000 cells (standard Brainfuck convention)
- **Cell size**: 256 values (0-255)
- **Circular tape**: Pointer wraps around at boundaries

### Error Handling

The calculator includes comprehensive error handling:
- Division by zero returns infinity (`inf`)
- Invalid expressions provide clear error messages
- Memory bounds are strictly enforced
- Unsupported operations are caught and reported

## Examples

### Big Number Calculations

```bash
# Really big numbers
python main.py "12345678901234567890+98765432109876543210"

# Large powers
python main.py "2^100"

# Complex calculations
python main.py "1000000*1000000/500000"
```

### 8-bit Calculations

```bash
# Modular arithmetic
python main.py --8bit "255+1"    # Result: 0
python main.py --8bit "300-100"  # Result: 200 (300-100=200, within 0-255)
```

## Limitations & Considerations

### Pure Brainfuck Limitations
- Only 8-bit calculations (0-255)
- No negative numbers
- Very slow for complex operations
- Limited error handling

### Hybrid Solution Benefits
- Unlimited number size
- Fast calculations
- Comprehensive error handling
- Maintains Brainfuck "spirit"

## Extending the Project

### Adding New Operations
1. Create a new Brainfuck module in `bf_modules/`
2. Add it to the `operations` dictionary in `orchestrator.py`
3. Implement the corresponding big number method

### Customizing the Interpreter
- Adjust `tape_size` for more memory
- Modify `cell_size` for different numeric bases
- Add debugging features to the interpreter

## Conclusion

This project bridges the gap between esoteric programming and practical computation. It shows that even the most minimalistic languages can be the foundation for useful applications when combined with the right architectural approach.

The Brainfuck Calculator proves that limitations are just opportunities for creative solutions. By understanding a language's constraints, we can build systems that respect its philosophy while extending its capabilities.

*"Not such a Brainfuck after all, huh?"*

## License & Credits

- **Author**: https://github.com/garantiatsverga
- **Version**: 1.0.0
- **License**: Free to use and modify
- **Note**: Brainfuck is a Turing-complete programming language created by Urban Müller in 1993

## Quick Reference

| Command | Mode | Example | Result |
|---------|------|---------|--------|
| `+` | Big Number | `999+999` | 1998 |
| `+` | 8-bit | `255+1` | 0 |
| `*` | Big Number | `1000*500` | 500000 |
| `^` | Big Number | `2^10` | 1024 |
| `/` | Both | `15/3` | 5 |

*Note: 8-bit mode results are modulo 256*