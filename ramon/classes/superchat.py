from classes.database import DDBB
from peewee import *
import decimal, json

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)

class Superchat(Model):
    id           = AutoField()    
    user         = CharField(default="justinFan", max_length=50)
    text         = CharField(max_length=256, default="Hello World!")
    avatar       = CharField(default='default', max_length=256)
    currency     = CharField(default='EUR', max_length=3)
    quantity     = DecimalField(max_digits=4, decimal_places=2)
    acknowledged = BooleanField(default=False)

    class Meta:
        database = DDBB.db

    def create(user="justinFan", text="Hello World!", avatar="default", currency='EUR', quantity=10, acknowledged=False):
        chat = Superchat(
            user = user,
            text = text,
            avatar = avatar,
            currency = currency,
            quantity = quantity,
            acknowledged = acknowledged
        )
        chat.save()

    def mark( id ):
        chat = Superchat.get( Superchat.id == id)
        chat.acknowledged = True
        chat.save()

    def getUnmarked():
        chats = [ x for x in Superchat.select().where( Superchat.acknowledged==False ).dicts()]
        return json.dumps(chats, cls=DecimalEncoder)

"""
s = Superchat(
    user = 'pepe',
    text = 'hello-world',
    avatar = '12324',
    currency = 'USD',
    quantity = 40,
    acknowledged = False,
)
s.save()
"""