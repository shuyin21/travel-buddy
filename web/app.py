
from flask import Flask, redirect, render_template, url_for, request, session
from datetime import timedelta
import sqlite3 as sql
import time


app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(days=5)

def databaseCon():
    conn = sql.connect("web/travel-db.db")
    
    conn.row_factory = sql.Row
    return conn

def searchEmail(email):
    conn = databaseCon()
    mycursor = conn.cursor()
    mycursor.execute("SELECT email FROM members")
    time.sleep(1)
    myresult = mycursor.fetchall()
    

    counter = 0

    for x in myresult:

        if x[0] == email:
            counter += 1

    if counter > 0:

        return 'exsist'

    else:
        return 'not exsist'

def checkPassword(email,password):
    conn = databaseCon()
    mycursor = conn.cursor()

    email = "'" + email + "'"
    mycursor.execute(
        "SELECT password FROM members WHERE email = " + email)
    time.sleep(1)
    myresult = mycursor.fetchall()
    

    for x in myresult:
        not_match = True
        while not_match:
            
            if password == x[0]:
                not_match = False
                return 'match'

            else:
                return 'wrong'


def getAll():
    allConn = databaseCon()
    cursor = allConn.cursor()
    cursor.execute("SELECT * FROM members")
    getMembers = cursor.fetchall()
    
    return getMembers
def getSingleData(email):
    allConn = databaseCon()
    cursor = allConn.cursor()
    email = "'" + email + "'"
    cursor.execute("SELECT * FROM members WHERE email = " + email)
    getMember = cursor.fetchall()
    
    return getMember

def getUserData(email):
    conn = databaseCon()
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM members WHERE email=?",(email,))
    time.sleep(1)
    myresult = mycursor.fetchall()
    return myresult
    
    
@app.route("/")
@app.route("/home")
def home():
    logged = False
    if "user" in session:
        logged = True
    return render_template("index.html", logged_in=logged)

# login
@app.route("/login", methods=["POST", "GET"])
def login():
    logged = False
    if "user" in session:
        logged = True
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        uPass = request.form["pass"]
        login_email = searchEmail(user)
        
        if login_email == 'exsist':
            user_pass = checkPassword(user,uPass)
            if user_pass == 'match':
                session["user"] = user
                logged = True
                
                return redirect(url_for("user"))
            else:
                logged = False
                return render_template("login.html", message = 'Incorrect password',logged_in=logged)
        else:
            if "user" in session:
                return redirect(url_for("user"))
            else:
                logged = False
                return render_template("login.html", message = 'Email is not in database',logged_in=logged)
    return render_template("login.html", logged_in=logged)

        
@app.route("/register",methods=["POST","GET"])
def register():
    conn = databaseCon()
    cursor = conn.cursor()
    members = []
    if request.method == "POST":
        fname = request.form['fname'].title()
        lname = request.form['lname'].title()
        email = request.form['email']
        valid = searchEmail(email)
        if valid == 'exsist':
            return render_template("register.html", message = 'The email already been used, please login!!')
        gender = request.form['gender'].title()
        country_from = request.form['cFrom'].title()
        country_to = request.form['cTo'].title()
        info = request.form['info']
        date = request.form['date']
        
        
        password = request.form['pass']
        
            
        members.append(fname)
        members.append(lname)
        members.append(email)
        members.append(gender)
        members.append(country_from)
        members.append(country_to)
        members.append(info)
        members.append(date)
        members.append(password)

        # insert data to members table
        cursor.execute(
            """INSERT INTO members VALUES(NULL, ?,?,?,?,?,?,?,?,?)""", members)       
            
        conn.commit()
        print(f"{fname} added to members table")
        return redirect(url_for("login"))
    return render_template("register.html", logged_in = False)
# after login redirect to the user page



@app.route("/user", methods=("GET", "POST",))
def user():
    if "user" in session:
        user = session["user"]
        
        data = getUserData(user)
        
        return render_template("user.html", name=user, data=data)
    else:
        return redirect(url_for("login"))
    
    
    
    
    
@app.route("/<int:memberID>/update", methods=("GET", "POST",))
def update(memberID):
    conn = databaseCon()
    cursor = conn.cursor()
    if "user" in session:
        user = session["user"]
        
        data = getUserData(user)
    
    if request.method == "POST":
        
        fname = request.form['fname'].title()
        lname = request.form['lname'].title()
        gender = request.form['gender'].title()
        country_from = request.form['cFrom'].title()
        country_to = request.form['cTo'].title()
        info = request.form['info']
        date = request.form['date']

       
        cursor.execute("UPDATE members SET firstname = ?, lastname = ?, gender = ?, country_from = ?,country_to = ?,info = ?, date = ?" "WHERE Member_ID= ?",
                       (fname,lname, gender, country_from, country_to,info,date,memberID),)
        conn.commit()
        conn.close()
        # redirect to songs page after delete
        return redirect(url_for("user"))
    return render_template("update.html", data= data)



@app.route("/travelers", methods=("GET", "POST",))
def allTraveler():
    conn = databaseCon()
    cursor = conn.cursor()
    if "user" in session:
        data=getAll()

    return render_template("travelers.html", data= data)
    
    
@app.route("/<int:memberID>/traveler")
def travelerData(memberID):
    conn = databaseCon()
    cursor = conn.cursor()
    if "user" in session:
        user = session["user"]
        cursor.execute("SELECT * FROM members WHERE Member_ID=?",(memberID,))
        time.sleep(1)
        myresult = cursor.fetchall()
        return render_template("traveler.html", data = myresult)
    
    return render_template("traveler.html")


@app.route("/<email>/addTraveler",methods=("GET", "POST",))
def addTraveler(email):
    conn = databaseCon()
    cursor = conn.cursor()
    user = session['user'] 
    data = getSingleData(user)
    
    for x in data:
        
        if x[10] == None :
            cursor.execute("UPDATE members SET saved_travelers = ?" "WHERE email= ?",
                    (email,user),)
        else:
            if x[11] == None :
                cursor.execute("UPDATE members SET saved_travelers2 = ?" "WHERE email= ?",
                    (email,user),)
            else:
                if x[12] == None :
                   cursor.execute("UPDATE members SET saved_travelersTwo = ?" "WHERE email= ?",
                    (email,user),)
                else:
                    emessage= 'You cannot save more than 3 travelers. Please remove one to save a new one!!'
                    session['emessage'] = emessage
                    return redirect(url_for('user',emessage = emessage) )
        print(x[11])
    
    
    conn.commit()
    conn.close()
    return redirect(url_for("user"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))
































if __name__ == "__main__":
    app.run(debug=True)


