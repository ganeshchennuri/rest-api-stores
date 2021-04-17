# FLASK REST API

## The following endpoints are implemented in this project

---
- /register     => POST         - user register
- /login        => POST         - authentication and Token Generation
- /logout       => POST         - logout user
- /refresh      => POST         - obtaining access token using refresh token
- /user/id      => GET,DELETE   - Querying and deleting user
- /stores       => GET          - querying all stores
- /store/name   => GET,POST,DELETE - querying, creating and deleting stores with name
- /items        => GET          - querying all item details
- /item/name    => GET,POST,PUT,DELETE - CRUD Operations on items
---

### /register

```
endpoint : /register
method : POST

payload
{
    "username" : "bob",
    "password" : "hash"
}

Response:
    {
    "message": "User Created Successfully"
    }
```
### /login
```
endpoint : /login
method : POST

payload
{
    "username" : "bob",
    "password" : "hash"
}

Response:
    {"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjE4NjYyNzI5LCJqdGkiOiIyNjk3YWIyYy1iYjY3LTQzZDAtOTE0Ni0wYzA3NTBhMDEyNmYiLCJuYmYiOjE2MTg2NjI3MjksInR5cGUiOiJhY2Nlc3MiLCJzdWIiOjEsImV4cCI6MTYxODY2MzYyOSwiaXNfYWRtaW4iOnRydWV9.50UPuFElihuTdxMsP2uUVb5iBFkDKfid3MnJS6O__uU"
    "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxODY2MjcyOSwianRpIjoiYzEzODQwZGItOTA3Ny00MjBmLWE1ZjYtNWNlY2I5OWU5NDdmIiwibmJmIjoxNjE4NjYyNzI5LCJ0eXBlIjoicmVmcmVzaCIsInN1YiI6MSwiZXhwIjoxNjIxMjU0NzI5LCJpc19hZG1pbiI6dHJ1ZX0.qtC4z8g7gtFkd5HuRfVU_FtpNkj7GYfk0QRGtDkV13o"}
```

### /logout
```
endpoint : /logout
method : POST

Headers:
Authorization: Bearer access_token

Response:
    {
    "message": "User successfully logged out"
    }
```
### /refresh
```
endpoint : /refresh
method : POST

Headers:
Authorization: Bearer refresh_token

Response:
{
    "access_token": token
}
```
### /user/id
```
endpoint : /user/1
method : GET

Response
{
    "id": 1,
    "username": "bob"
}
```
```
endpoint : /user/1
method : DELETE

Headers:
Authorization: Bearer access_token

Response
{
    "message": "User deleted Successfully"
}
```
### /stores
```
endpoint : /stores
method : GET

Headers:
Authorization: Bearer access_token

Response
{
    "stores": []
}
```
### /store/name
```
endpoint : /store/laptops
method : POST

Headers:
Authorization: Bearer access_token

Response
{
    "id": 1,
    "name": "laptops",
    "items": []
}
```
```
endpoint : /store/laptops
method : GET

Headers:
Authorization: Bearer access_token

Response
{
    "id": 1,
    "name": "laptops",
    "items": [
        {
            "id": 1,
            "name": "macbook",
            "price": 1799.0,
            "store_id": 1
        }
    ]
}
```
```
endpoint : /store/laptops
method : DELETE

Headers:
Authorization: Bearer access_token

Response
{
    "message": "Store Deleted"
}
```
### /items
```
endpoint : /items
method : GET

Headers:
Authorization: Bearer access_token

Response
{
    "items": [
        {
            "id": 1,
            "name": "macbook",
            "price": 1799.0,
            "store_id": 1
        }
        ]
}
```
### /item/name
```
endpoint : /item/macbook
method : POST

Headers:
Authorization: Bearer access_token

payload:
    {
        "store_id": 1,
        "price": 1799.0
    }

Response
    {
        "id": 1,
        "name": "macbook",
        "price": 1799.0,
        "store_id": 1
    }
```
```
endpoint : /item/macbook
method : GET

Headers:
Authorization: Bearer access_token

Response
{
    "id": 1,
    "name": "macbook",
    "price": 1799.0,
    "store_id": 1
}
```
```
endpoint : /item/iphone12
method : PUT

Headers:
Authorization: Bearer access_token

payload:
    {
        "price": 899.0,
        "store_id": 2
    }

Response
    {
        "id": 2,
        "name": "iphone12",
        "price": 899.0,
        "store_id": 2
    }
```
```
endpoint : /item/iphone12
method : DELETE

Headers:
Authorization: Bearer access_token

Response
{
    "message": "item deleted successfully"
}
```


