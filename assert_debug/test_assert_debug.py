# testing assert and debug statement

if __debug__:
    print("we are in debug mode")

a = 0
assert a == 0 
    
print("outside debug!")


#python -O test_assert_debug.py
# to turn off the debugging mode