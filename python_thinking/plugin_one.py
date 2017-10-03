class Plugin:
    
    def __init__(self, *args, **kwargs):
        print("plugi int (one): ", args, kwargs)
        
    def execute(self, a, b):
        return a+b