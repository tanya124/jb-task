# jb-task
[![Build Status](https://travis-ci.com/tanya124/jb-task.svg?token=zf2uWSvzpsZfMbeLjp5N&branch=main)](https://travis-ci.com/tanya124/jb-task)
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
    - Response code: (200, 401)
    - Description: return a list of all users
  
* GET /v1/users/get_user/?user_id=<+/->
    - Response: user
    - Response code: (200, 400, 401)
    - Desription: if user_id parametr is given then return info for this user else return info for current user

    
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
    - Response code: (200, 400, 401)
    - Description: create friendship request

* DELETE /v1/friends/delete_friend/
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
    - Response code: (200, 400, 401)
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
    - Response code: (200, 400, 401)
    - Desription: if user_id parametr is given then return a list of friends for this user else return list of friends for current user


* GET /v1/friends/get_friends_of_friends/
    - Response: [ user ]
    - Response code: (200, 400, 401)
    - Desription: Return a list of possible friends of the current user

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








