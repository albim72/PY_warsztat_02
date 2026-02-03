class Book:
    __kolor = "czarny"

    def __init__(self, title, author, price, pages, bookstor_nb):
        self.title = title #self -> zmienna: argument
        self.author = author
        self.price = price
        self.pages = pages
        self.bookstor_nb = bookstor_nb
        self.binding = "miękka"

    def __repr__(self):
        return f"Book({self.title}, {self.author}, {self.price}, {self.pages}, {self.bookstor_nb})"

    def __call__(self,procent):
        return f"Rabat {procent}% z ceny: {self.price}PLN = {self.price * procent / 100:.2f} PLN"

    def get_bind(self):
        return self.binding

    def set_bind(self,bind):
        self.binding = bind


    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,newtitle):
        self._title = newtitle



b = Book("ABC Kulturysty", "Jan Nowak", 56.6,456,34)
print(b)
print(b.get_bind())
print(b(12))

b.set_bind("twarda")
print(b.get_bind())

print(b.title)
b.title = "ABC Kulturysty 2"
print(b.title)

print(b._title)

