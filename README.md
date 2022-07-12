# Hamrobazaar-API

An unofficial python wrapper around [hamrobazaar.com](https://hamrobazaar.com/) API

## Install
```bash
pip install hamrobazaar-api
```

## How to use?
```python
import asyncio

from hamrobazaar.aioclient import HamrobazaarClient

async def main():
    with HamrobazaarClient(api_key) as client:

        # Get product detail with its id
        product = await client.get_product_detail("4ace7c2501964de481d4e0cf09121724")        
        
        print(product.name)
        print(product.price)
        print(product.description)
    
asyncio.run(main())
```

## 🚧 Work In Progress. 🚧 
 