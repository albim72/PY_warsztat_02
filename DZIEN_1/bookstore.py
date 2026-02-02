class Book:
    def __init__(self, id, title, author, price=30):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.oprawa = "miękka"
        print(self.create_book())

    def create_book(self):
        return f"utworzono książkę typu Book"

    def rabat(self,procent):
        return self.price*procent/100



bk = Book(45,"Lidia w ogrodzie","Joanna Hulik",price=44)
print(bk)
print(bk.rabat(10))
