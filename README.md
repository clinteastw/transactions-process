## Test Credentials

- Admin\
  email: admin@example.com\
  password: admin\
  username: admin
- Test User \
  email: testuser@example.com\
  password: testuser\
  username: testuser
 
### Rename and edit .env-example 

- ## Docker

```python
docker-compose up --build -d
```

Go to <http://localhost:8000/docs>


- ## Without docker

Create virtualenv
```python
virtualenv venv
```

Install dependencies
```python
venv/scripts/activate
pip install -r -requirements.txt
```

Run migration
```python
alembic upgrade head
```

Run app
```python
py src/main.py
```
Go to <http://localhost:8000/docs>

## Process transaction for test user
- login with test user credentials - `auth/jwt/login`
- generate transaction_id `payments/generate-random-transaction_id`
- pass the generated transaction_id to generate signature `payments/generate-signature`
   ```python
      {
        "transaction_id": "generated transaction_id",
        "account_id": 1,
        "user_id": 1,
        "amount": 10
      }
    ```
- pass generated transaction_id and signature to create payment `payments/process`
    ```python
      {
        "transaction_id": "generated transaction_id",
        "account_id": 1,
        "user_id": 1,
        "amount": 10,
        "signature": "generated signature"
      }
    ```
