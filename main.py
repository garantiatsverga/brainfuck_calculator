from math import inf
import sys
import argparse
from src.orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(
        description='Brainfuck Calculator',
        epilog='Example: python main.py "999+999" "1000*500"'
    )
    
    parser.add_argument(
        'expressions',
        nargs='*',
        help='Arithmetic expressions to calculate'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    
    parser.add_argument(
        '--8bit',
        dest='force_8bit',
        action='store_true',
        help='Use 8-bit mode (for testing only)'
    )
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator()
    except Exception as e:
        print(f"Initialization error: {e}")
        return 1
    
    if args.expressions:
        print("\nResults:")
        print("-" * 40)
        
        for expr in args.expressions:
            try:
                if args.force_8bit:
                    result = orchestrator.calculate_8bit(expr)
                else:
                    result = orchestrator.calculate(expr)
                
                print(f"{expr} = {result}")
                    
            except Exception as e:
                print(f"{expr}: ERROR - {e}")
        
        print("-" * 40)
    
    if args.interactive or (not args.expressions):
        run_interactive_mode(orchestrator, args.force_8bit)
    
    return 0


def run_interactive_mode(orchestrator, force_8bit=False):
   
    if force_8bit:
        print("Mode: 8-bit (results modulo 256)")
    else:
        print("Mode: Big numbers (no limits)")
    
    print("Supported operations: +, -, *, /, ^, !")
    print("Enter 'help' for help, 'quit' to exit")
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Exiting...")
                break
            
            if not user_input:
                continue
            
            if user_input.lower() == 'help':
                print_help()
                continue
            
            try:
                if force_8bit:
                    result = orchestrator.calculate_8bit(user_input)
                else:
                    result = orchestrator.calculate(user_input)
                
                print(f"= {result}")
                    
            except ValueError as e:
                print(f"Error: {e}")
            except ZeroDivisionError:
                print(inf)
            except Exception as e:
                print(f"Error: {e}")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except EOFError:
            print("\n\nExiting...")
            break


def print_help():
    """Print help information"""
    print("\nHelp:")
    print("-" * 30)
    print("Enter expressions like:")
    print("  5+3      - Addition")
    print("  10-4     - Subtraction")
    print("  6*7      - Multiplication")
    print("  15/3     - Division")
    print("  2^10     - Power")
    print("  5!        - Factorial")
    print("-" * 30)
    print("Big number examples:")
    print("  999+999       = 1998")
    print("  1000*500      = 500000")
    print("  999^2         = 998001")
    print("  123456789*10  = 1234567890")
    print("-" * 30)


if __name__ == "__main__":
    sys.exit(main())