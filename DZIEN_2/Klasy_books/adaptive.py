class AdaptiveThreshold:
    def __init__(self,start=0.5, alpha=0.1):
        self.threshold = start
        self.alpha = alpha
        self.history = []

    def __call__(self,value):
        decision = value > self.threshold
        self.history.append(value)

        #adaptacja progu(uczenie online)
        error = value - self.threshold
        self.threshold += self.alpha * error

        return decision

gate = AdaptiveThreshold(start=10)

# gate(12)
#
# print(gate.history)
#
# gate(4)
# print(gate.history)
#
# gate(56)
# print(gate.history)

for x in [8,9,11,34,5,78,14,3,24,88,6]:
    print(x,gate(x),round(gate.threshold,2))