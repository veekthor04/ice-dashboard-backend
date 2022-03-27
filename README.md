# ice-dashboard-backend

This an app that will be used to keep record of customers payments.

## Endpoints

### Authentication

#### Signup

`POST ​/signup​/`

Adds a new user.

#### Login

`POST ​/login/`

Login to user's account

#### Profile (Get)

`GET ​/profile​/`

Gets Logged in user details

#### Profile (Put)

`PUT ​/profile​/`

Complete detail update for the logged in user.

#### Profile (Patch)

`PATCH ​/profile​/`

Partial detail update for the logged in user.

### Customer

Manages Customers.

#### Customer Create

`POST /customer/`

Adds a new customer to the platform.

#### Customer List

`GET ​/customer/`

Returns a list of register customers.

#### Customer GET

`GET ​/customer/{customer_id}/`

Retrieves a customer's detail.

#### Customer Put

`PUT ​/customer/{customer_id}/`

Completely updates a customer's detail.

#### Customer Patch

`PATCH ​/customer/{customer_id}/`

Partially updates a customer's detail.

#### Customer Delete

`DELETE /customer/{customer_id}/`

Deletes a customer.

### Payment

Manages Customers Payment.

#### Payment Create

`POST /payment/`

Adds new customer's payment.

#### Payment List

`GET ​/payment/`

List all available payments.

#### Payment GET

`GET ​/payment/{payment_ref}/`

Returns the detail of a payment.

#### Customer Payment

Manage a customer's payments.

#### Payment List

`GET ​/customer/{customer_id}/payment/`

Lists all payments for a given customer.


## Running

Create a .env file using the .env.sample file as a template

To run the app you can use docker-compose:

```
docker-compose up --build -d
```

To stop the app:

```
docker-compose down
```

To run tests:

```
docker-compose run --rm app sh -c "python manage.py test"
```

The app will be accessed at `localhost:8000`.

## API Documentation

Postman at `https://www.getpostman.com/collections/e58c49da6ea183cf4e2c`

ReDoc at `localhost:8000/redoc/`

Swagger-ui at  `localhost:8000/swagger/`
