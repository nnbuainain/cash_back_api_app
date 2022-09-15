from sql_alchemy import database
from datetime import datetime

class SaleModel(database.Model):
    __tablename__ = 'sales'

    sale_id = database.Column(database.Integer, primary_key = True)
    sale_date = database.Column(database.String)
    costumer_id_cpf = database.Column(database.Integer, database.ForeignKey('costumers.costumer_id_cpf'))
    products = database.Column(database.JSON, nullable = True, default = [])
    total = database.Column(database.Float(precision = 2), default = 0)


    def __init__(self, costumer_id_cpf: int, products: list):
        self.sale_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.costumer_id_cpf = costumer_id_cpf
        self.products = products
        self.total = sum([product.get('value', 0) for product in self.products])
    

    @classmethod
    def find_sale(cls, sale_id: str):
        sale = cls.query.filter_by(sale_id = sale_id).first()
        
        if sale:
            return sale
        return None

    def to_json(self) -> dict:
        return {
            'sale_id' : self.sale_id, 
            'sale_date' : self.sale_date,
            'costumer_id_cpf' : self.costumer_id_cpf,
            'products' : self.products,
            'total' : self.total
            }

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()