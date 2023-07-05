# Microblogging-platform

## To run the server on localhost
* Clone the repository
* Run `pip install -r requirement.txt` to install the dependency
* Create a __.env__ file in the root directory
* Add the following details to .env
    ```javasript
    SECRET_KEY = your Django Secret key'
    NAME = database name
    USER = username
    PASSWORD = password
    HOST = host
    PORT = port
    ```
* Run `python manage.py runserver` to start the server
* Start the Redis server to use the Redis caching mechanism
  ```javascript
     redis://localhost:6379/0
  ```


# Microblogging Platform API

Welcome to the Microblogging Platform API documentation! This API provides endpoints to manage users and posts on the platform. It follows the RESTful principles and supports CRUD operations (Create, Read, Update, Delete) for users and posts.

## Users Endpoints

### 1. Add a New User

- **Endpoint**: `/api/users/`
- **Description**: Add contact details.
- **Method**: POST
- **Parameters**:
  - `username`: user's email.
  - `email`: user's phone number.
  - `password`: password
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/users/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "email": "abc@a.com",
      "username": "abc",
      "password":"password"
    }'
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "user_id": 492580241
        }
        ```
  - **Error**
    - **Status code**: 403
      - **Response body**
        ```javascript
        {
          "error": "User already exists"
        }
        ```
    - **Status code**: 400
      - **Response body**
        ```javascript
        {
          "error": "Missing required fields"
        }
        ```

### 2. Fetch User

- **Endpoint**: `/api/users/<int:user_id>`
- **Description**: fetch user details.
- **Method**: GET
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/users/1693299874/' \
    --header 'Content-Type: application/json' \
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "user_id": 492580241,
          "username": "a",
          "email": "1@a.com"
        }
        ```
  - **Error**
    - **Status code**: 405
      - **Response body**
        ```javascript
        {
          "error": "Invalid Request Method"
        }
        ```
    - **Status code**: 404
      - **Response body**
        ```javascript
        {
          "error": "User not found"
        }
        ```

### 3. Update user

- **Endpoint**: `/api/users/<int:user_id>`
- **Description**: Update specific user details
- **Method**: PUT/PATCH
- **Parameters**:
  - `username?`: user's email.
  - `password?`: password
  - `? indicated its not mandatory field`
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/users/1693299874/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "email": "abc@a.com"
    }'
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "user_id": 492580241,
          "username": "a",
          "email": "1@a.com"
        }
        ```
  - **Error**
    - **Status code**: 405
      - **Response body**
        ```javascript
        {
          "error": "Invalid Request Method"
        }
        ```
    - **Status code**: 404
      - **Response body**
        ```javascript
        {
          "error": "User not found"
        }'
        ```


## Posts Endpoints

### 1. Add a New post

- **Endpoint**: `/api/posts/`
- **Description**: Add contact details.
- **Method**: POST
- **Parameters**:
  - `user_id`: user's email.
  - `content`: user's phone number.
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/post/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "user_id": "123",
      "content": "1st post",
    }'
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "post_id": 492580241
        }
        ```
  - **Error**
    - **Status code**: 400
      - **Response body**
        ```javascript
        {
          "error": "error": "User ID and content are required."
        }
        ```
    - **Status code**: 401
      - **Response body**
        ```javascript
        {
          "error": "User is not authorized to add post."
        }
        ```
### 2. List all post

- **Endpoint**: `/api/posts/`
- **Description**: fetch post details.
- **Method**: GET
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/posts/' \
    --header 'Content-Type: application/json' \
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        [
          {
          "user_id": 492580241,
          "post_id": "123",
          "content": "1st post"
          },
          {
          "user_id": 492580242,
          "post_id": "1234",
          "content": "2nd post"
          }
        ]
        ```

### 3. Fetch post

- **Endpoint**: `/api/users/<int:post_id>`
- **Description**: fetch post details.
- **Method**: GET
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/users/1693299874/' \
    --header 'Content-Type: application/json' \
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "user_id": 492580241,
          "post_id": "123",
          "content": "1st post"
        }
        ```
  - **Error**
    - **Status code**: 404
      - **Response body**
        ```javascript
        {
          "error": "post not found'"
        }
        ```

### 4. Update Post

- **Endpoint**: `/api/post/<int:post_id>`
- **Description**: Update specific post details
- **Method**: PUT/PATCH
- **Parameters**:
  - `content`: content you want to change
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/post/169329874/' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "content": "updated 1st post"
    }'
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
          "post_id": 1388525039,
          "content": "updated 1st post "
        }
        ```
  - **Error**
    - **Status code**: 404
      - **Response body**
        ```javascript
        {
          "error": "Post not found"
        }
        ```

### 5. delete post

- **Endpoint**: `/api/post/<int:post_id>`
- **Description**: Delete specific post
- **Method**: DELETE
- **API Request**:
    ```javascript
    curl --location 'http://127.0.0.1:8000/api/post/169329874/' \
    --header 'Content-Type: application/json' \
    ```
- **Responses**:
  - **Success**
    - **Status code**: 200
      - **Response body**
        ```javascript
        {
           "message": "Post deleted."
        }
        ```
  - **Error**
    - **Status code**: 404
      - **Response body**
        ```javascript
        {
          "error": "Post not found"
        }
        ```
