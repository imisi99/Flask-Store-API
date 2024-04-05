# Flask-Pizza-api
This is a store api that is built with flask and postgresql
It uses jwt for user authentication and authorization
It uses redis for task queing and mailgun for sending emails
It uses Background worker for the email automation
It lets authorized users:
- Create Items, Stores and Tags
- Have total access to do things like edit and delete items,stores and tags that have already been created
Some other functions of the API are:
- It incorporates a strong database relationship that ensures  data integrity.
- It has protected routes that requires jwt_token to be able to access
- It ensures data security by the use of unique gmails for password recovery

You can run the api locally by these methods:
- To run the api you can use docker or python virtual environment 
- To run the api locally on docker you can access the command [here](https://github.com/imisi99/Flask-Store-API/blob/main/CONTRIBUTING.md)
- To run the api locally on your python virtual venv run the command (pip install -r requirements.txt)
- The swaager-ui view of the api is [here](https://flask-store-api-vvs7.onrender.com/swagger-ui)
- You can reach me for any request or issue on [gmail](mailto:isongrichard234@gmail.com)

