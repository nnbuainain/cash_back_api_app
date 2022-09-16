# CASH BACK API APP

An API application that stores an e-commerce's users, products and sales data. With the sales information (id) it is possible to register and get cashback for each sale, validating the cashback information at a third party API of a cashback company.

## How to run
**This is app is containerized**

To properly run:

```bash
docker run -p 5000:5000 -d cashback_api_app
```


## API documentation

To start using the APP, first, you need to either register a new user or use the default admin user. This user need be used in order to login and enable most of the functionalities.

## User

### Default User:

login: admin
password: 12345

### Create new user:

Method: POST

URL: http://0.0.0.0:5000/register_user

```bash
Header:
{'Content-Type' : 'application/json'}
```
```bash
Body: {
    'login' : 'admin',
    'password' : '12345' 
}
```

### Login

Method: POST

URL: http://0.0.0.0:5000/login

```bash
Header:
{'Content-Type' : 'application/json'}
```
```bash
Body: {
    'login' : 'admin',
    'password' : '12345' 
}
```

```bash
Response:
{'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2MzM0MTc4NCwianRpIjoiZmIxMzAxYTYtYTQ3Zi00ZDFhLWJkNTgtMjgzOWFkZGE4YjUwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjYzMzQxNzg0LCJleHAiOjE2NjMzNDI2ODR9.iunttkVbGRZ1sb6C1sUxuHdvsq5mNcnKcakaZXXxsgs'}
```
*You will need to copy this access token and use in your header in your future requests*

### Logout

Method: POST

URL: http://0.0.0.0:5000/logout

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'message' : 'You successfully logged out'}
```

## Costumer

### Register Costumer

Register a new costumer of the store. Costumer ID (CPF) must be numeric with 11 digits

Method: POST

URL: http://0.0.0.0:5000/register_costumer

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Body: {
    'costumer_id_cpf' : '12345678910',
    'name' : 'Charles Darwin' 
}
```

```bash
Response:
{'message': "Costumer with id '12345678910' successfully created"}
```

### GET Costumer

Method: GET
URL: http://0.0.0.0:5000/12345678910

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'costumer_id_cpf': '12345678910',
'name': 'Charles Darwin'}
```

### DELETE Costumer

Method: DELETE

URL: http://0.0.0.0:5000/12345678910

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'message': "Costumer with id '12345678910' successfully deleted"}
```

### GET ALL Costumers

Method: GET

URL: http://0.0.0.0:5000/costumers

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'costumers': [{'costumer_id_cpf': '12345678910', 'name': 'Charles Darwin'},
  {'costumer_id_cpf': '10987654321', 'name': 'Alfred Russel Wallace'},
  {'costumer_id_cpf': '66666666666', 'name': 'Richard Dawkins'},
  {'costumer_id_cpf': '10203040506', 'name': 'Ernst Mayr'}]}
```

## Product

Category: A product has to have one of the following categories: 'A', 'B', 'C'. These categories will dictate the cashback percentage over the value of the product

Value: product's value

### Register product
Method: POST
URL: http://0.0.0.0:5000/register_product

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Body: {
    'category' : 'A',
    'value' : 106.12
}
```

```bash
Response: {
'message': "Product with id '1' successfully registered"
}
```

### GET product

Method: Get
URL: http://0.0.0.0:5000/product/{id}

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'id': 12, 'category': 'B', 'value': 106.12}
```

### GET ALL products

Method: GET

URL: http://0.0.0.0:5000/products

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{
{'products': [{'id': 1, 'category': 'C', 'value': 130.3},
  {'id': 2, 'category': 'A', 'value': 11.3},
  {'id': 3, 'category': 'A', 'value': 44.3},
  {'id': 4, 'category': 'B', 'value': 130.3},
  {'id': 5, 'category': 'B', 'value': 98.4},
  {'id': 6, 'category': 'B', 'value': 17.7}
  }
```

### DELETE Product

Method: DELETE
URL: http://0.0.0.0:5000/product/{id}

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'message': "Product with id '12' successfully deleted"}
```

## Sale

#### Register Sale

Costumer_id_cpf: id number of the costumer who purchased the sale

Products and quantities: A list of dictionaries with the id and quantities of the products purchased.

Method: POST
URL: http://0.0.0.0:5000/register_sale

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Body: {
    "costumer_id_cpf" : 12345678910,
    "products_and_quantities" : [
        {"id" : 5,
        "quantity" : 10},
        {"id" : 8,
        "quantity" : 3}
    ]}
```

```bash
Response: {'sale_id': 4,
 'sale_date': '16/09/2022 10:11:42',
 'costumer_id_cpf': 12345678910,
 'products': [{'id': 5, 'category': 'B', 'value': 98.4, 'quantity': 10},
  {'id': 8, 'category': 'C', 'value': 15.1, 'quantity': 3}],
 'total': 1029.3}
}
```


### GET Sale

Method: GET
URL: http://0.0.0.0:5000/sales/{sale_id}

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'sale_id': 3,
 'sale_date': '15/09/2022 12:53:25',
 'costumer_id_cpf': 12345678910,
 'products': [{'id': 9, 'category': 'C', 'value': 15.9, 'quantity': 7},
  {'id': 1, 'category': 'C', 'value': 130.3, 'quantity': 3}],
 'total': 502.2}
```

### GET ALL Sales

Method: GET

URL: http://0.0.0.0:5000/sales

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{
{'sales': [{'sale_id': 1,
   'sale_date': '15/09/2022 12:50:58',
   'costumer_id_cpf': 66666666666,
   'products': [{'id': 1, 'category': 'C', 'value': 130.3, 'quantity': 2},
    {'id': 3, 'category': 'A', 'value': 44.3, 'quantity': 4}],
   'total': 437.8},
  {'sale_id': 2,
   'sale_date': '15/09/2022 12:51:58',
   'costumer_id_cpf': 66666666666,
   'products': [{'id': 4, 'category': 'B', 'value': 130.3, 'quantity': 5},
    {'id': 6, 'category': 'B', 'value': 17.7, 'quantity': 2}],
   'total': 686.9}
   }
   ```

### DELETE Sale

Method: DELETE
URL: http://0.0.0.0:5000/sales/{sale_id}

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'message': "Product with id '12' successfully deleted"}
```

## CASHBACK (FINALLY!)

Cashback id: Unique id number automatically generated
Cashback total: Total received in cashback
api_response: Api generated by the third party api responsible for oficially registering the cashback

### Register Cashback

Method: POST
URL: http://0.0.0.0:5000/register_cashback

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Body: {
    "sale_id" : 2
    ]}
```

```bash
Response: {'cashback_id': 1,
 'cashback_total': 17.837999999999997,
 'api_response': {'createdAt': '2022-09-15T13:03:00.816Z',
  'message': 'Cashback criado com sucesso!',
  'id': '32',
  'document': 12345678910,
  'cashback': 17.837999999999997},
 'sale_id': 2}
```


### GET CASHBACK

Method: GET
URL: http://0.0.0.0:5000/cashbacks/{cashback_id}

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{'cashback_id': 1,
 'cashback_total': 31.38,
 'api_response': {'createdAt': '2022-09-14T21:11:02.539Z',
  'message': 'Cashback criado com sucesso!',
  'id': '38',
  'document': 66666666666,
  'cashback': 31.38},
 'sale_id': 1}```

### GET ALL Cashbacks

Method: GET

URL: http://0.0.0.0:5000/cashbacks

```bash
Header:
{'Content-Type' : 'application/json',
'Authentication': Bearer access_token}
```

```bash
Response:
{
{'cashbacks': [{'cashback_id': 1,
   'cashback_total': 31.38,
   'api_response': {'createdAt': '2022-09-14T21:11:02.539Z',
    'message': 'Cashback criado com sucesso!',
    'id': '38',
    'document': 66666666666,
    'cashback': 31.38},
   'sale_id': 1},
  {'cashback_id': 2,
   'cashback_total': 34.35,
   'api_response': {'createdAt': '2022-09-14T23:19:24.363Z',
    'message': 'Cashback criado com sucesso!',
    'id': '39',
    'document': 66666666666,
    'cashback': 34.35},
   'sale_id': 2}
   }
   ```

## Further examples

For further examples, please access the test notebook: https://github.com/nnbuainain/cash_back_api_app/blob/master/consume_api_tests.ipynb
