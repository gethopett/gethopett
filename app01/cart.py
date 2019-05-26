from app01.models import TBook
class CartItem():
    def __init__(self,book,amount):
        self.amount = amount
        self.book = book

class Cart():
    def __init__(self):
        self.save_price = 0   #节省金额
        self.total_price = 0   #总金额
        self.cartltem = []   #存书和书的数量


        # 计算金额
    def sums(self):
        self.total_price = 0
        self.save_price = 0
        for i in self.cartltem:
            self.total_price = i.book.dangdang_price*i.amount
            self.save_price = (i.book.market_price - i.book.dangdang_price)*i.amount


   #向购物车中添加书籍
    def add_book_toCart(self,book_id):
        for i in self.cartltem:
            if i.book.id == book_id:
                i.amount +=1
                self.sums()
                return
        book = TBook.objects.filter(book_id = id)
        self.cartltem.append(CartItem(book,1))
        self.sums()

    #修改商品信息
    def modify_cart(self,book_id,amount):
        for i in self.cartltem:
            if i.book.id == book_id:
                i.amount = amount
        self.sums()

    #删除购物车
    def delete_book(self,book_id):
        for i in self.cartltem:
            if i.book.id == book_id:
                self.cartltem.remove(i)
        self.sums()



