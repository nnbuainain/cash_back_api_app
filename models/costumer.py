from sql_alchemy import database

class CostumerModel(database.Model):
    __tablename__ = 'costumers'

    costumer_id_cpf = database.Column(database.String(11), primary_key = True)
    name = database.Column(database.String(40))


    def __init__(self, costumer_id_cpf : str, name: str):
        self.costumer_id_cpf = costumer_id_cpf
        self.name = name


    @classmethod
    def find_costumer(cls, costumer_id_cpf: str):
        costumer = cls.query.filter_by(costumer_id_cpf = costumer_id_cpf).first()
        
        if costumer:
            return costumer
        return None


    def to_json(self) -> dict:
        return {
            'costumer_id_cpf' : self.costumer_id_cpf,
            'name' : self.name
            }


    def save(self):
        database.session.add(self)
        database.session.commit()


    def delete(self):
        database.session.delete(self)
        database.session.commit()