class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def __call__(self, *args):
        child = Node(f"{self.name}({', '.join(map(str, args))})")
        self.children.append(child)
        return child

    def show(self,level=0):
        print("  "*level+self.name)
        for child in self.children:
            child.show(level+1)


pipeline = Node("START")

step1 = pipeline("load data", "clean data") #() -> szukanie wskaźnik : tp_call
step2 = step1("train model", "evaluate model")
step3 = step2("save model")
step4 = step3("serve model")
step5 = step4("monitor model")
step6 = step5("POST-monitor model")

pipeline.show()

print(id(step1), id(step2), id(step3), id(step4))
