from typing import Optional
from fastapi import FastAPI
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from mongomock_motor import AsyncMongoMockClient

from beanie import Document, Indexed, init_beanie

from pymongo.server_api import ServerApi
uri = "mongodb+srv://test1:test1@testbatch.4k43ctn.mongodb.net/?retryWrites=true&w=majority&appName=testbatch"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection



class Category(BaseModel):
    name: str
    description: str
    
    
    class Meta:
        collection = "categories"
        
    async def insert(self):
        await Category.insert_one(self)
        
    async def update(self):
        await Category.update_one(self)
        
    async def delete(self):
        await Category.delete_one(self)


# This is the model that will be saved to the database
class Product(Document):
    name: str                          # You can use normal types just like in pydantic
    description: Optional[str] = None
    price: Indexed(float)              # You can also specify that a field should correspond to an index
    category: Category 
  
    class Meta:
        collection = "products"        # Specify the collection name
        indexes = [                     # Specify the indexes
            {"key": [("name", 1)], "unique": True},
            {"key": [("price", 1)]}
        ]
    class Config:
        schema_extra = {
            "example": {
                "name": "Product Name",
                "description": "Product Description",
                "price": 100.0,
                "category": {"name":"Category Name","description":"Category Description"}
            }
        }
        
    async def insert(self):
        await Product.insert_one(self)
        
   


# Call this from within your event loop to get beanie setup.
async def init():
    # Create Motor client
    client=client

    # Init beanie with the Product document class
    await init_beanie(database=client.test, document_models=[Product])
    
    
app = FastAPI()

@app.post("/products/")
async def create_product(product: Product):
    await product.insert()
    return product.Config()

@app.get("/products/")
async def get_products():
    products = await Product.find_all().to_list()
    return products
  
@app.get("/products/{product_id}")
async def get_product(product_id:str):
    product = await Product.get(product_id)
    return product.Config()
  
  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
  
  
