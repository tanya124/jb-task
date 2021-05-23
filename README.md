# jb-task

***
## API Documentation

**Definitions:**

- <> - string 
- [ ... ] - list of
- (..., ..., ...) - tuple
- +/- - optional
-  user: 
```json
{ 
  "id": "<>", 
  "username": "<>", 
  "email": "<>" 
}
```

**Headers:**

- Content-Type: application/json
- Authorization: Token \<Token> (*NOTE: DO NOT include header with /auth/*)

**Requests:**

* GET /v1/users/user_list
    - Response: [ user ]
    - Response code: (200,...)
    - Description: return a list of all users
  
* GET /v1/users/get_user/?user_id=<+/->
    - Response: user
    - Response code: (200, ...)
    - Desription: if user_id parametr is given then return info for this user else return info for current user **ПОФИКСИТЬ**

    
* POST /v1/friends/add_friend/
    - Request:
    ```json
    { 
      "user_id": "<>"
    }
    ```
    - Response:
    ```json
    {
      "status": "<>",
      "message": "<>"
    }
    ```
    - Response code: (200, 400, ...)
    - Description: create friendship request

* POST /v1/friends/delete_friend/
    - Request:
    ```json
    { 
      "user_id": "<>"
    }
    ```
    - Response:
    ```json
    {
      "status": "<>",
      "message": "<>"
    }
    ```
    - Response code: (200, 400, ...)
    - Description: delete friendship request

* GET /v1/friends/get_friends/?user_id=<+/->
    - Response: 
    ```json
    [
      {
        "to_user": "user",
        "created_date": "<>"
      }
    ]
    ```
    - Response code: (200, ...)
    - Desription: if user_id parametr is given then return a list of friends for this user else return list of friends for current user **ПОФИКСИТЬ**


* GET /v1/friends/get_friends/?user_id=<+/->
    - Response: 
    ```json
    [
      {
        "to_user": "user",
        "created_date": "<>"
      }
    ]
    ```
    - Response code: (200, ...)
    - Desription: if user_id parametr is given then return a list of friends for this user else return list of friends for current user **ПОФИКСИТЬ**

* POST /v1/auth/registration/
    - Request:
    ```json
    {
      "username": "",
      "email": "",
      "password1": "",
      "password2": ""
    }
    ```
    - Response:
    ```json
    {
      "key": "",
    }
    ```
    - Response code: (200, 400)

* GET /v1/auth/login/
    - Request:
    ```json
    {
      "username": "",
      "email": "",
      "password": ""
    }
    ```
    - Response:
    ```json
    {
      "key": "",
    }
    ```
    - Response code: (200, 400)








