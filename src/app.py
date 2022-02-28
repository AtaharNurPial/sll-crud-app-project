# import pydantic
from pydantic import BaseModel
from typing import List,Dict

class IngrediantCls:
    def __init__(self, ingredient: List[str]) -> None:
        self.ingredient = ingredient

class VariationCls:
    def __init__(self,variation: Dict[str, str]) -> None:
        self.variation = variation

class Menu_Item_Cls:
    def __init__(self, restaurant_id: str, item_id: str, item_name: str, ingredients: IngrediantCls,
    variations: VariationCls, image: str, category: str) -> None:
        self.restaurant_id = restaurant_id
        self.item_id = item_id
        self.item_name = item_name
        self.ingredients = ingredients
        self.variations = variations
        self.image = image
        self.category = category

class Ingredient(BaseModel):
    ingedient: List[str]

    class Config:
        orm_mode = True

class Variation(BaseModel):
    name: str
    price:str
    currency:str
    

    class Config:
        orm_mode = True


class Menu_Item(BaseModel):
    restaurant_id: str 
    item_id: str
    item_name: str
    ingredients: Ingredient
    variations: List[Variation]
    image: str
    category: str

    class Config:
        orm_mode = True

test_ingredients = IngrediantCls(ingredient=['air','water','fire','earth'])
test_variations = VariationCls(variation={"name":"botella","price":"33","currency":"$"})
test_menuItem = Menu_Item_Cls(restaurant_id='1235',item_id='b23',item_name='testItem',
ingredients= test_ingredients,variations=test_variations,image='testImage',category='Food')

    
test_model = Menu_Item.from_orm(test_menuItem)

print("testModel: ", test_model)






