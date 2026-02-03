class ModelState:
    def __init__(self,loss_history,max_epochs):
        self.loss_history = loss_history
        self.max_epochs = max_epochs

    @property
    def converged(self):
        if len(self.loss_history) < 3:
            return False
        return (
        self.loss_history[-1] >= self.loss_history[-2] >= self.loss_history[-3]
        )

    @property
    def progress(self):
        return len(self.loss_history) / self.max_epochs


state = ModelState([0.9,0.6,0.4,0.41,0.42,0.42,0.2,0.5,0.49,0.5,0.45],10)

print(state.converged)
print(state.progress)