from sql_alchemy import database

class ProductModel(database.Model):
    __tablename__ = 'products'

    id = database.Column(database.Integer(), primary_key = True)
    category = database.Column(database.String(1))
    value = database.Column(database.Float(precision = 2))
    

    def __init__(self, category : str, value: float):
        self.category = category.upper()
        self.value = value

    @classmethod
    def find_product(cls, id: str):
        product = cls.query.filter_by(id = id).first()
        
        if product:
            return product
        return None

    def to_json(self) -> dict:
        return {
            'id' : self.id,
            'category' : self.category,
            'value' : self.value
            }

    def save(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()


