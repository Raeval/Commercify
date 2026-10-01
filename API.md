- [Products API](#products-api)

# API Documentation

## Products API

### GET Product by ID

**Endpoint**

```http
GET /products/{item_id}
```

**Example Response** -- 200 OK

```json
{
  "id": "1",
  "name": "Apple",
  "price": "2.50"
}
```

**Example Response** -- 404 Not Found

```json
{
  "message": "No product found"
}
```

### POST Create a Product

**Endpoint**

```http
POST /products
```

**Request Body**
```json
{
  "name": "Apple",
  "price": "2.50"
}
```

**Example Response** -- 201 Created
```json
{
  "id": "50",
  "name": "Apple",
  "price": "2.50"
}
```

**Error Response** -- 400 Bad Request
```json
{
  "message": "Unable to create product"
}
```

### DELETE Product by ID
```http
DELETE /products/{item_id}
```

**Example Response** -- 204 No Content
**Example Response** -- 404 Not Found

```json
{
  "message": "No product found"
}
```

### PATCH Product by ID
```http
PATCH /products/{item_id}
```

**Request Body**
```json
{
  "name": "apple",
  "price": "2.75"
}
```

**Example Response** -- 200 OK
```json
{
  "id": "1",
  "name": "apple",
  "price": "2.75"
}
```

**Example Response** -- 404 Not found
```json
{
  "message": "No product found"
}
```