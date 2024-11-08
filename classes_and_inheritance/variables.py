class TestClass:

    variable_a = "var a"
    variable_b = "var b"

test = TestClass()
list_all_variable = dir(test)
list_variables = [var for var in list_all_variable if not var.startswith('__')]
print(list_variables)


my_dict = {_variable: getattr(TestClass, _variable) for _variable in list_variables}
print(my_dict)


my_dict = {_variable: getattr(test, _variable) for _variable in list_variables}
print(my_dict)
