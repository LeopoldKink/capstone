Fitness Api Documentation

Motivation for project:

My motivation for this project is to be able to put all my new skills to the test.


Getting Started / Authentication
- The 2 JWTs are located in the .env file.
    - Base URL: https://fitness4711.herokuapp.com/exercices, retruns a list of all exercices.
    - This app requires authentication for the post, patch and delte endpoints. And for the endpoint to show a specific instructor.
    - There a two roles:
        --> Admin: can perform anything: patch:workout, post:workout, delete:workout, get:instructor
        --> Instructor: can see a specific instructor: get:instructor

Error Handling 
    - Errors are returned as JSON objects like the following:
        {
            "success" : False,
            "error" : 404,
            "message" : recource not found
        }
    - The API will return four error types:
        1. 404: Recource Not Found
        2. 405: Method not allowed
        3. 401: Unauthorized
        4. 403: Forbidden


Endpoints

    1. GET /exercices
    - General: Returns a list of exercices
    - Sample: curl http://127.0.0.1:5000/exercices

        {"exercices":[{"difficulty":1,"id":9,"likes":0,"muscles":"chest","name":"push ups","requirements":"nothing","video_path":"https://youtube.com"},{"difficulty":1,"id":3,"likes":0,"muscles":"chest","name":"push ups","requirements":"nothing","video_path":"https://youtube.com"},{"difficulty":1,"id":11,"likes":0,"muscles":"chest","name":"push ups","requirements":"nothing","video_path":"https://youtube.com"}]}


    2. GET /instructors
    - General: Returns a list of instructors
    - Sample: curl http://127.0.0.1:5000/instructors

        {"instructors":[{"age":25,"id":10,"name":"Vin Diesel","profile_pic_path":"https://n-cdn.serienjunkies.de/hq/100176.jpg"},{"age":30,"id":1,"name":"The Rock","profile_pic_path":"https://qph.fs.quoracdn.net/main-qimg-cbd43fb5a668f4b6731e9b566244149d"}]}

    3. GET /instructors/<int:inst_id>
    - General: Returns one instructor
    - Sample: 

        {"age":30,"id":1,"name":"The Rock","profile_pic_path":"https://qph.fs.quoracdn.net/main-qimg-cbd43fb5a668f4b6731e9b566244149d"}


    4. POST /create/exercice
    - General: Creates a new exercice
    - Sample:
        {
            'success' : True,
            'created' : 11,
            'exercice name' : "Push Ups" 
        }


    5.DELETE /delete/exercice/<int:ex_id>
    - General: deletes a certain exercice 
    - Sample:
        {
            'success' : True,
            'deleted' : 10
        }

    6. PATCH /patch/exercice/<int:ex_id>
    - General: Updates a certain exercice
    - Sample: 
        {
            'success' : True,
            'updated' : 11,
            'exercice name' : "Push Ups"
        }