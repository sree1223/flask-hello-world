from flask import Flask,render_template,send_file,url_for,session
import jwt
from flask import Flask, jsonify, request

app = Flask(__name__,static_folder="static",static_url_path="/static")

app.secret_key = 'super-secret'

# Secret key for JWT token encoding and decoding
SECRET_KEY = 'super-secret'  # Change this to your secret key

# Dummy user data (replace this with your actual user authentication logic)
users = {
    'user1': 'password1',
    'user2': 'password2'
}




@app.route("/")
def page1():
    return render_template("page1.html")





# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    
    if username not in users or users[username] != password:
        return jsonify({"msg": "Invalid username or password"}), 401
    
    # Generate JWT token
    token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
    session['token'] = token

    # Return the JWT token
    return jsonify(access_token=token), 200



@app.route('/logout', methods=['GET'])
def logout():
    if "token" in session:
        session.pop('token', None)

    # Return the JWT token
    return {"message":"logged out"}, 200




# Protected route that requires JWT token
@app.route('/protected', methods=['GET'])
def protected():
    # token = request.headers.get('Authorization')
    token = session.get('token')
    print(token)
    if not token:
        return jsonify({"msg": "Missing token"}), 401
    
    try:
        # Decode the token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded_token['username']
        return jsonify(logged_in_as=username), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Expired token"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"msg": "Invalid token"}), 401

@app.route('/logpage')
def page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
