class Timeblock:
    def __init__(self,start,end,function):
        self.start = start
        self.end = end
        self.interval = list(3**function(x) for x in range(end-start))
        
