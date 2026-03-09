import os # Unused import (should trigger a warning)
import sys

def my_function(name):
    # Poor indentation and missing whitespace around operators
    print("Hello "+name)
    x = 10; # Trailing semicolon (un-pythonic)
    return x

# Too many blank lines below (PEP8 usually wants 2 between functions)



def another_function():
  print("This has inconsistent indentation")
  if True:
    pass