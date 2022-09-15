from sql_alchemy import database

class CashBackModel(database.Model):
    __tablename__ = 'cashbacks'

    cashback_id = database.Column(database.Integer, primary_key = True)
    cashback_total = database.Column(database.Float(precision = 2), default = 0)
    api_response = database.Column(database.JSON, default = {})
    sale_id = database.Column(database.Integer, database.ForeignKey('sales.sale_id'))


    def __init__(self, cashback_total : float, api_response : dict, sale_id : int):
        self.cashback_total = cashback_total
        self.api_response = api_response
        self.sale_id = sale_id
    

    @classmethod
    def find_cashback(cls, cashback_id: int):
        cashback = cls.query.filter_by(cashback_id = cashback_id).first()
        
        if cashback:
            return cashback
        return None

    @classmethod
    def find_cashback_by_sale_id(cls, sale_id: int):
        cashback = cls.query.filter_by(sale_id = sale_id).first()
        
        if cashback:
            return cashback
        return None

    def to_json(self) -> dict:
        return {
            'cashback_id' : self.cashback_id, 
            'cashback_total' : self.cashback_total,
            'api_response' : self.api_response,
            'sale_id' : self.sale_id,
            }

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()