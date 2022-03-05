import pydantic
from pydantic import BaseModel
from typing import List,Any
from ksuid import ksuid

RESTAURANT_PREFIX = '#RESTAURANT#'
ITEM_PREFIX = '#ITEM#'

class UserModel(BaseModel):
    email: str
    password: str

class Variation(BaseModel):
    name: str = ''
    price: str = ''
    currency: str = ''

class Menu_Item(BaseModel):
    PK: str = ''
    SK: str = ''
    restaurant_id: str 
    item_id: str
    item_name: str
    ingredients: List[str] = []
    variations: List[Variation] = []
    image: str = ''
    category: str = ''

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.PK = f"{RESTAURANT_PREFIX}{self.restaurant_id}"
        self.SK = f"{ITEM_PREFIX}{self.item_id}"

        if self.item_id == '':
            self.item_id = ksuid().__str__()
def display():
    test_variation = Variation(name= 'botella', price='33',currency='$')
    test_menuItem = Menu_Item(restaurant_id='1235',item_id='',item_name='testItem',
                ingredients=['air','water','fire','earth'],
                variations=[test_variation],image='testImage',category='Food')

    print(f"test_Model: {test_menuItem}")

if __name__ == "__main__":
    display()