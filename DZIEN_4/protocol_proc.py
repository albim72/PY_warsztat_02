from typing import Protocol

class Processor(Protocol):
    def process(self, data) -> object: ...

class TextProcessor:
    def process(self, text: str) -> str:
        return text.upper()

class NumberProcessor:
    def process(self, number: int) -> int:
        return number * 3

def run(processor:Processor, data):
    return processor.process( data)

print(run(TextProcessor(), "hello"))
print(run(NumberProcessor(), 5))

class BadProcessor:
    def process(self):
        print("....kiepsko...")

run(BadProcessor(), "hello")