def function(text, a=0, b=2):
    print(f"{text =}")
    print(f"{a =}")
    print(f"{b =}")

def function2(text, **kwargs):
    function(text, **kwargs)


my_dict = {'a': 5, 'b': 10}
function2("abc def", **my_dict)




