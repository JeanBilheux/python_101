
import sys
import pdb

def add(num1=0, num2=0):
    return int(num1) + int(num2)
def sub(num1=0, num2=0):
    return int(num1) - int(num2)
def main():
    #Assuming our inputs are valid numbers
    print(sys.argv)
    pdb.set_trace() # <---- break point added here
    addition = add(sys.argv[1], sys.argv[2])
    print(addition)
    subtraction = sub(sys.argv[1], sys.argv[2])
    print(subtraction)
if __name__ == '__main__':
    main()
