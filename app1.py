from flask import Flask, request,  render_template, url_for,session, redirect, flash
from pymongo import MongoClient
from  passlib.hash import sha256_crypt

app = Flask(__name__)
client = MongoClient('127.0.0.1',27017)
db = client["logindb"]

@app.route('/')
def home():
	image =["http://jinja.pocoo.org/docs/2.10/_static/jinja-small.png","http://jinja.pocoo.org/docs/2.10/_static/jinja-small.png","http://jinja.pocoo.org/docs/2.10/_static/jinja-small.png","http://jinja.pocoo.org/docs/2.10/_static/jinja-small.png"]
	name = ["tractor1","tractor2","tractor3","tractor4","tractor5","tractor6"]
	price = [4000,5000,9000,8000,7000,6000]
	return render_template('index.html',i = image,n = name,p = price)

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        users = db.users
        
        first_name = request.form["first_name"]
        middle_name = request.form["middle_name"]
        last_name = request.form["last_name"]
        phone = request.form["number"]
        password = request.form["password"]
        confirm = request.form["confirmpassword"]
        
        existing_user = users.find_one({"Phone":phone})
        
        if existing_user is  None:
            if password == confirm:
                secure_password = sha256_crypt.encrypt(str(password))
                users.insert({"First_name":first_name, "Middle_name":middle_name, "Last_name":last_name,"Phone":phone,"Password":secure_password})
                flash("You are registered and can login","success")
                return redirect(url_for("login"))
            else:
                flash("Passsword does not match","danger")
                return render_template('register.html')
            
        return "Username already exist!!!"
    
    return render_template('register.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        
        phone = request.form["number"]
        password = request.form["password"]
        
        users = db.users
        login_user = users.find_one({"Phone":phone})
        login_password = login_user["Password"]
        
        print(login_user)
        
        if login_user is None:
            flash("No Username Found","danger")
            return render_template("login.html")
        else:
            if sha256_crypt.verify(password,login_password):
                session["log"]=True
                flash("You are now log in","success")
                return redirect(url_for("secretpage"))
            else:
                flash("Password is incorrect","danger")
                return render_template("login.html")
        
    return render_template('login.html')

@app.route('/secretpage')
def secretpage():
    return render_template('secretpage.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You are now log out","success")
    return redirect(url_for("login"))
	
 
if __name__ == '__main__':
    app.secret_key = "secret key"
    app.run(debug=True) 