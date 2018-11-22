
# Mr. Theophilus Nutifafa
# Learn.pythonanywhere.com project
import os
import datetime
import time
from flask import Flask, redirect, render_template, request, url_for,session #flash
from flask_login import current_user, login_required, login_user, LoginManager, logout_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
#import random
from flask_mail import Mail,Message
import yagmail
import flask
import flask_login
from werkzeug.utils import secure_filename
from flask import send_from_directory
import random
import pyrebase
import json
#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate('/home/Learn/mysite/uploads/pywe-208616-c2124a16842b.json')
#default_app = firebase_admin.initialize_app(cred)




#from flask_wtf import FlaskForm
#from wtforms import TextField,validators,PasswordField,SubmitField


app = Flask(__name__)
app.config["DEBUG"] = True
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='pythonwithellie@gmail.com'
app.config['MAIL_PASSWORD']='learnpython22'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail = Mail(app)
UPLOAD_FOLDER = "/home/Learn/mysite/uploads"
ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


WTF_CSRF_SECRET_KEY = 'something random'
app.secret_key = "something random"
login_manager = LoginManager()
login_manager.init_app(app)





SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="Learn",
    password="independence",
    hostname="Learn.mysql.pythonanywhere-services.com",
    databasename="Learn$Users",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

app.secret_key = "SOMETHING RANDOM"
login_manager = LoginManager()
login_manager.init_app(app)


#class SignupForm(FlaskForm):
    #name = TextField("Username",[validators.DataRequired()])
    #email = TextField("Email",[validators.DataRequired(),validators.Email()])
    #password = PasswordField("Password",[validators.DataRequired()])
    #submit = SubmitField('Register')

configu = {  "apiKey": "AIzaSyAWhEZkholpo9TEDp2o12REdu8StRFqHSc",  "authDomain": "pywe-92968.firebaseapp.com",  "databaseURL": "https://pywe-92968.firebaseio.com",  "storageBucket": "pywe-92968.appspot.com",  "serviceAccount": "/home/Learn/mysite/uploads/pywe-208616-c2124a16842b.json" }
firebase = pyrebase.initialize_app(configu)

auth = firebase.auth()
fdb = firebase.database()
#store = firebase.storage()
#authenticate a user
#user = auth.sign_in_with_email_and_password("joe@gmail.com", "chaii222")
#auth.send_email_verification(user['idToken'])
#info = auth.get_account_info(user['idToken'])
#print (info)
#print(info['users'][0]['emailVerified'])
#auth.send_password_reset_email('gregeace@gmail.com')



#userToken = user['idToken']
#print (auth.get_account_info(userToken)['users'][0]['localId'])

# CRUD
# The set method
#lana = {"name": "Lana Kane", "agency": "Figgis Agency"}
#fdb.child("agents").child("Lana").set(lana, user['idToken'])
# Getting all data
#all_agents = fdb.child("agents").get(user['idToken']).val()

# Get specific data
#lana_data = fdb.child("userdata").child("-LG73hvrQXhh4Y9j2XR8").get(user['idToken']).val()
#print (lana_data)

# Updating records
#fdb.child("childname").child("sub_childname").update({"key": "New value"}, user['idToken'])

# Remove whole data
#fdb.child("childname").remove(user['idToken'])

# Remove specific data
#fdb.child("chidname").child("sub_childname").remove(user['idToken'])

# Writing real data to existing firebase
# Creates a child named New and a sub child named Gregory Peace
# And inserts the data called lana into the database
#lana = {"name": "Gregory Peace", "email": "myemail@gmail.com","password":"userpass222"}
#fdb.child("New").child("Gregory Peace").set(lana, user['idToken'])

#Reading from the database
#lana_data = db.child("New").child("Gregory Peace").get(user['idToken']).val()
#print(lana_data)

#user = auth.sign_in_with_email_and_password(email, password)
# before the 1 hour expiry:
#user = auth.refresh(user['refreshToken'])
# now we have a fresh token
#user['idToken']
#This query will return users with a score of 10.

#users_by_score = db.child("users").order_by_child("score").equal_to(10).get()
# Storing media in the storage
#storage.child("/home/Learn/mysite/uploads/samsung_earpiece[1].JPG")



class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    email_confirmed = db.Column(db.Integer)
    token = db.Column(db.String(128))
    reset = db.Column(db.String(128))
    security = db.Column(db.String(4096))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_user_id(self):
        return self.id

    def get_id(self):
        return self.username

    def get_email(self,username):
        return self.email

    def get_confirmed(self,email):
        return self.confirmed
    def get_token(self,email):
        return self.token
    def get_reset(self,email):
        return self.reset
    def get_security(self,email):
        return self.security

# Method to fetch all users with their details and dump into json file
def store():
    all_users = {}
    usernames = []
    passwords = []
    emails = []
    email_conf = []
    tokens = []
    resets = []
    securitys =[]
    objs = User.query.all()
    newfile = open("/home/Learn/mysite/uploads/all_users.json","w+")
    for i in objs:
        usernames.append(i.username)
        passwords.append(i.password_hash)
        emails.append(i.email)
        email_conf.append(i.email_confirmed)
        tokens.append(i.token)
        resets.append(i.reset)
        securitys.append(i.security)
    all_users['usernames'] = usernames
    all_users['passwords'] = passwords
    all_users['emails'] = emails
    all_users['email_conf'] = email_conf
    all_users['tokens'] = tokens
    all_users['resets'] = resets
    all_users['securitys'] = securitys
    all_users = json.dumps(all_users)
    newfile.write(all_users)
    newfile.close()



@login_manager.user_loader
def load_user(user_id):
    #user_id = User
    #(user_id,'password',password)
    #setattr(user_id,'email',email)

    return User.query.filter_by(username=user_id).first()




class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))
    posted = db.Column(db.DateTime, default=datetime.datetime.now)
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    commenter = db.relationship('User', foreign_keys=commenter_id)
    commenter_pic = db.Column(db.String(4096))




class Files(db.Model):

    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(4096))
    uploaded = db.Column(db.DateTime, default=datetime.datetime.now)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    uploader = db.relationship('User', foreign_keys=uploader_id)








#Homepage
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method=='GET':
        #user=load_user(request.form["lusername"])
        #if user is None:
         #   return render_template('new_home.html')
        adpics = [["samsung_earpiece[1].JPG","Samsung_AKG","GHC 15"],["charger[1].JPG","Android_charger","GHC 30"],["ofia[1].JPG","Ofia_Earpiece","GHC 10"]]
        chosen = random.choice(adpics)
        link = "/uploads/"+ chosen[0]
        name = chosen[1]
        price = chosen[2]
        upload = "/uploads/"
        adverts = {"ads": [
        {"id": 1, "adname": "phone_accessories", "details": {
        "items": [
            {"product_details": {"price": "Ghc 15", "name": "Samsung_AKG", "model": "","link":upload + "samsung_earpiece[1].JPG"}},
            {"product_details": {"price": "GHC 30", "name": "3_USB_Charger", "model": "","link":upload +"t_power_charger_set.JPG"}},
            {"product_details": {"price": "GHC 10", "name": "Ofia_Earpiece", "model": "","link":upload + "ofia[1].JPG"}}]}},
        {"id": 2, "adname": "food_products", "details": {
        "items": [
            {"product_details": {"price": "Ghc 18", "name": "Eggs", "number": "24"}},
            {"product_details": {"price": "GHC 30", "name": "Rice bag", "weight": "5kg"}},
            {"product_details": {"price": "GHC 8", "name": "Oil", "volume": "1l"}}]}}]}

        items = adverts['ads'][0]['details']['items']
        my_list = []
        for i in items:
            my_list.append(i)
        chosen2 = (random.choice(my_list)['product_details'])


        #adpics2 = [["samsung_earpiece[1].JPG","Samsung_AKG","GHC 15"],["charger[1].JPG","Android_charger","GHC 30"],["ofia[1].JPG","Ofia_Earpiece","GHC 10"]]
        #chosen2 = random.choice(adpics2)
        #link2 = "/uploads/"+ chosen2[0]
        #name2 = chosen2[1]
        #price2 = chosen2[2]

        return render_template('index.html',name = name,price=price,link=link,name2 = chosen2['name'],price2 = chosen2['price'],link2=chosen2['link'] )






        #if not current_user.is_authenticated:
         #   userip =  request.headers['X-Real-IP']
          #  return render_template("mainpage.html", comments=Comment.query.all())
        #else:
         #   return render_template("mainpage.html", comments=Comment.query.all())
    #if not current_user.is_authenticated:
     #   return redirect(url_for('index'))
    #if request.method == 'POST':


     #   comment = Comment(content=request.form["contents"], commenter=current_user)
      #  db.session.add(comment)
       # db.session.commit()
        #return render_template("mainpage.html", comments=Comment.query.all())


#login page control
@app.route("/login/", methods=["GET", "POST"])
def login():

    if request.method == "GET":

        return render_template("login.html", error=False)

    user = load_user(request.form["username"])
    if user is None:
        return render_template("login.html", error="Incorrect Username")

    if not user.check_password(request.form["password"]):
        return render_template("login.html", error="Incorrect Password")
    if user.email_confirmed == 0:
        return render_template('login.html',error="Please confirm your email to sign in")
    url = session.get('url',None)
    login_user(user)
    flask_login.login_user(user, remember=False)



    #flask.session.permanent = True
    #app.permanent_session_lifetime = datetime.timedelta(minutes=30)
    #flask.session.modified = True
    #flask.g.user = flask_login.current_user

    if not url:
        return redirect(url_for('course'))
    else:
       return redirect(url)
    #return render_template("comment.html",user=request.form["username"],comments=Comment.query.all())
    #if request.method == "POST":

#Logs user out after 44640 minutes
@app.before_request
def before_request():
    min = 44640
    flask.session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=min)
    flask.session.modified = True
    flask.g.user = flask_login.current_user

def timeremaining(year=2018,month=8,day=17,hours=15,minutes=30,seconds=0):
    from datetime import datetime
    then = datetime(year,month,day,hours,minutes,seconds)
    now=datetime.now()
    duration = then - now
    duration_in_s = duration.total_seconds()
    days = divmod(duration_in_s,86400)
    hours = divmod(days[1],3600)
    minutes = divmod(hours[1],60)
    seconds = divmod(minutes[1],1)
    countdown = "%d Hour(s), %d Minute(s), %d Second(s)"%(hours[0],minutes[0],seconds[0])
    return countdown





List=[]
List2 = []
picList = []
idList =[]
picnidList = []
@app.route("/course", methods = ['GET','POST'])
def course():

    if request.method == "GET":



        if not current_user.is_authenticated:
            session['url'] = request.url
            return render_template('new_course.html',error="Please ",image="static/images/IMG-20180227-WA0019.jpg")


        uid = current_user.id
        ufile = Files.query.filter_by(uploader_id=uid).all()
        if len(ufile)==0:
            imagename = "PyWe.jpg"
        else:
            for each in ufile:
                List.append(each.filename)
            imagename = str(List[-1])
        rawcomments=Comment.query.all()


        return render_template("new_course.html",comments=Comment.query.all(),User=current_user.username,image ="uploads/{}".format(imagename))
    if request.method == 'POST':


        uid = current_user.id
        ufile = Files.query.filter_by(uploader_id =uid).all()


        if len(ufile) ==0:
            imagename="PyWe.jpg"

        else:
            for each in ufile:
                List.append(each.filename)
            imagename = str(List[-1])

        contents=str(request.form["contents"]).encode('utf-8')
        comment = Comment(content=contents, commenter=current_user,commenter_pic=str(imagename))
        db.session.add(comment)
        db.session.commit()
        rawcomments=Comment.query.all()




        return render_template("new_course.html", comments=rawcomments,User=current_user.username,image="uploads/{}".format(imagename),cmt=contents)





@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method=='GET':

        return render_template('signupform.html',error=False, success=False)
    user = load_user(request.form["username"])
    if request.method == "POST":
        if user is None:
            Email = request.form["email"]
            if User.query.filter_by(email=Email).first() is None:
                name = request.form["username"]
                password = generate_password_hash(request.form["password"])



                yag = yagmail.SMTP("pythonwithellie@gmail.com","learnpython22")


                Token=str(time.time()).replace(".","")
                Token=generate_password_hash(Token)


                special = "/learn.pythonanywhere.com/link/"+Token
                html_msg="""<html><body style="border:solid 3px #3bc5e6;background-color:#eee;"><center><h2 style="color:#3bc5e6;">Welcome to PythonwithEllie
                </h2><br><p>Here is your verification  <a href=%s>link.</a> If you cannot click on it then look below.
                <br>It's so exciting having you --Welcome.<br>Learning Python with this team will be exciting <br>--What are you waiting for? C'mon!</p></center>
                </body>
                </html>""" %special



                contents=[html_msg,special]
                yag.send(str(Email),"Verification link",contents)
                #msg = Message('Welcome to PythonwithEllie',sender='theophylusnhutiphapha@gmail.com',recipients=([str(Email)]))
                #msg.body = "Please use this code:" +Token+ " to complete verification"
                #mail.send(msg)
                me = User(username=name,password_hash=password,email=Email,email_confirmed=0,token=Token,reset="",security="")
                db.session.add(me)
                db.session.commit()
                #flash('A verification link has been sent to the email you provided. check now!', 'success')
                return render_template('signupform.html',success="check your email and click verification link to confirm")
            else:
                return render_template('tsignupfor.html',error="Sorry, email exists")
        else:
            return render_template('signupfor.html',error="Sorry, username exists")
    return render_template('signupfor.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    if not current_user.is_authenticated:
        session['url'] = request.url
        return redirect(url_for('login'))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template("upload_file.html",error='No file part')
            #flash('No file part')
            #return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template("upload_file.html",error='No selected file')
            #flash('No selected file')
            #return redirect(request.url)





        if file and allowed_file(file.filename):



            firstname = str(secure_filename(file.filename))

            splitted = firstname.split('.')
            fileextension = splitted[-1].lower()
            all = ['txt', 'png', 'jpg', 'jpeg', 'gif']
            if fileextension in all:

                cur = str(time.time()).replace(".","")
                filename = str(current_user)+cur+'.'+str(fileextension) #secure_filename(file.filename)

            else:
                cur = str(time.time()).replace(".","")
                filename = str(current_user)+cur+'.'+'jpg' #secure_filename(file.filename)


            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = Files(filename=filename, uploader=current_user)
            cmt = Comment.query.filter_by(commenter_id=current_user.id).all()
            for each in cmt:
                each.commenter_pic=filename
            db.session.add(file)
            db.session.commit()
            return render_template("upload_file.html",success='photo upload successful')
            #This is to show the file but will not be used now
            #return redirect(url_for('uploaded_file',
              #                      filename=filename))
    return render_template("upload_file.html")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    try:
        if not current_user.is_authenticated:
            session['url'] = request.url

            return redirect(url_for('login'))
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                                   filename)
    except:
        return render_template('forgotten.html',error="file doesn't exist")
#The following are the course pages

Lesson = ['introduction','operations','identifiers','strings','numbers','lists','booleans','tuples','dictionaries','conditions','functions','loops','modules','storage','exceptions','oop','regex','cgi','dba','networking','emails','multithreading','gui','extensions','utilities']
intro ={'introduction':"""""",'operations':"",'identifiers':"",'strings':"""Strings are always chain of characters bounded by triple, double quotes or single quotes in Python,
a string can also be just a character""",'numbers':"""Number data types store numeric values. They are immutable data types,
which means that changing the value of a number data type results in a newly allocated object...""",'lists':"""Python's list is another datatype that can be used
to keep other basic datatypes
in a fairly organised manner. This is because members of a list...""",'booleans':"""One of the simplest but powerful datatypes is the boolean.
Holding only two values...""",'tuples':"""A tuple is a sequence of immutable Python objects. Tuples are sequences, just like lists.
The only difference is that tuples can't be changed i.e., tuples are
immutable and tuples use parentheses and lists use...""",'dictionaries':"""""",'conditions':"",'functions':"""The idea of functions from Maths has been extended in
programming. Functions are used as switches to performing actions, the
name of the function representing""",'loops':"",'modules':"""A module allows you to logically organize your
Python code. Grouping related code into a module makes the code easier to...""",'storage':"",'exceptions':"""The most annoying part of programming may
be encountering errors. This is because sometimes errors are hard to understand
in some languages but Python's errors are...""",'oop':"",'regex':"",'cgi':"",'dba':"""
""",'networking':"",'emails':"",'multithreading':"",'gui':"",'extensions':"",'utilities':""}
image = []
@app.route('/<lesson>',methods=['GET','POST'])
def lesson(lesson):
    if request.method == 'GET':
        if not current_user.is_authenticated:
            session['url'] = request.url

            return redirect(url_for('login'))
        try:
            curindex = Lesson.index(lesson)
        except:
            return redirect(url_for("four"))
        else:
            if curindex==0:
                Prev = Lesson[24]
                currentlesson = Lesson[curindex]
                next = Lesson[curindex+1]
            if curindex<=5:
                Kesson = Lesson[0:6]
            if curindex<=10 and curindex>4:
                Kesson = Lesson[5:11]
            if curindex>6 and curindex <=16 :
                Kesson = Lesson[10:18]
            if curindex>15 and curindex<=20:
                Kesson = Lesson[16:25]
            if curindex>20:
                Kesson = Lesson[0:6]
            if curindex == len(Lesson)-1:
                Prev = Lesson[23]
                currentlesson = Lesson[curindex]
                next = Lesson[0]

            if curindex <=23 and curindex !=0:
                Prev = Lesson[curindex-1]
                currentlesson = Lesson[curindex]
                next = Lesson[curindex+1]




        try:
            prevpic = Prev+".jpg"
            send_from_directory(app.config['UPLOAD_FOLDER'],
                                   prevpic)
        except:
            prevpic = "/uploads/"+Prev+".png"
        else:
            prevpic = "/uploads/"+Prev+".jpg"
        try:
            curpic = lesson+".jpg"
            send_from_directory(app.config['UPLOAD_FOLDER'],
                                   curpic)
        except:
            curpic = "/uploads/"+lesson+".png"
        else:
            curpic = "/uploads/"+lesson+".jpg"
        try:
            nextpic=next+".jpg"

            send_from_directory(app.config['UPLOAD_FOLDER'],
                                   nextpic)
        except:
            nextpic="/uploads/"+next+".png"
        else:
            nextpic="/uploads/"+next+".jpg"



        prevtext = intro[Prev]
        nxttext = intro[next]
        adpics = ["samsung_earpiece[1].JPG","ofia[1].JPG","t_power_charger_set.JPG"]
        adpics2 = ["samsung_earpiece[1].JPG","ofia[1].JPG","t_power_charger_set.JPG"]
        width = 330
        height = 300
        upload = "/uploads/"
        whatsappl = "https://api.whatsapp.com/"
        adverts = {"ads": [
            {"id": 1, "adname": "phone_accessories", "details": {
            "items": [
            {"product_details": {"price": "Ghc 15", "name": "Samsung_AKG", "model": "","link":upload + "samsung_earpiece[1].JPG"}},
            {"product_details": {"price": "GHC 30", "name": "Android_charger", "model": "","link":upload +"t_power_charger_set.JPG"}},
            {"product_details": {"price": "GHC 10", "name": "Ofia", "model": "","link":upload + "ofia[1].JPG"}}]}},
            {"id": 2, "adname": "food_products", "details": {"items": [
            {"product_details": {"price": "Ghc 18", "name": "Eggs", "number": "24"}},
            {"product_details": {"price": "GHC 30", "name": "Rice bag", "weight": "5kg"}},
            {"product_details": {"price": "GHC 8", "name": "Oil", "volume": "1l"}}]}}]}

        items = adverts['ads'][0]['details']['items']
        img = [items[0]['product_details']['link'], items[0]['product_details']['name'],items[0]['product_details']['price']]
        img1 = [items[1]['product_details']['link'], items[1]['product_details']['name'],items[1]['product_details']['price']]
        img2 = [ items[2]['product_details']['link'],items[2]['product_details']['name'],items[2]['product_details']['price']]




        return render_template(Lesson[curindex]+'.html',nxtlesson = next,prevlesson=Prev,curlesson=currentlesson,Lesson=Kesson,nxtpic=nextpic,curpic=curpic,prevpic=prevpic,prevtext=prevtext,nxttext=nxttext,daysmore=timeremaining(),adpic ="/uploads/"+ random.choice(adpics),width=width,height=height,adpic2 ="/uploads/"+ random.choice(adpics2),images = [img,img1,img2])








@app.route("/appreciation",methods=['GET','POST'])
def appreciation():
    if request.method=='GET':
        return render_template('appreciation.html')



@app.route("/forgotten",methods=['GET','POST'])
def forgotten():
    if request.method=='GET':
        return render_template('forgotten.html',error=False,success=False)
    if request.method=='POST':
        Email = request.form["email"]
        user = User.query.filter_by(email=Email).first()
        if user is None:
            return render_template('forgotten.html',error="Your Account does not exist")
        yag = yagmail.SMTP("pythonwithellie@gmail.com","learnpython22")

        Token=str(time.time())
        Token = generate_password_hash(Token.replace(".",""))


        special = "learn.pythonanywhere.com/link/"+ Token

        html_msg = """<html><body style="border:solid 3px #3bc5e6;background-color:#eee;"><h2><center style="color:#3bc5e6;">Reset your password</center></h2>
        <center><p> Please, click this <a href=%s> link </a>to reset password. If you cannot click the link then look below</a> to reset your password</p></center>
        </body>
        </html> """ %special
        contents=[html_msg,special]
        yag.send(str(Email),"Reset your password",contents)
        #setattr(user, 'reset', Token)
        #db.session.commit()
        user.reset=Token
        db.session.commit()

        return render_template('forgotten.html',success="Check your mail for link to reset password")
    return render_template('forgotten.html')











@app.route("/link/<link>",methods=['GET','POST'])
def speciallink(link):
    if request.method=='GET':
    #First check to see if the link is a token
        user=User.query.filter_by(token=link).first()
        if user is None:
            #user = User.query.filter_by(reset=link).first()
            user = User.query.filter_by(reset=link).first()
            if user is None:
                return redirect(url_for("four"))
            return redirect(url_for("reset",u_id=user.id))

        if user.email_confirmed==0:
            user.email_confirmed=1
            db.session.commit()
            Email = user.email
            return render_template('email_confirmation.html',email=Email)
        else:
            return render_template("forgotten.html",success="You have already confirmed your email")
    return render_template('forgotten.html')




@app.route("/404",methods=["GET","POST"])
def four():
    if request.method=="GET":
        return render_template("404.html")





@app.route("/reset<u_id>",methods=["GET","POST"])
def reset(u_id):
    if request.method=="get":

        user = User.query.filter_by(id=u_id).first()
        if user is None:
            return render_template("reset_pass.html",error="User does not exist")
        return render_template("reset_pass.html",error=False,success=False)


    user = User.query.filter_by(id=u_id).first()

    #db.session.commit()
    #return request.form["password"]
    session['my_var'] = u_id
    return redirect(url_for('treset'))

    #return redirect(url_for("treset"))
    #return render_template("reset_pass.html")

        #return redirect(url_for("forgotten",success="password has been successfully reset"))
    #return render_template("reset_pass.html",user1='',success="password reset successful",u_id=user.id)
    #return render_template('reset_pass.html',u_id=user.id)

@app.route('/rset',methods=['GET','POST'])
def treset():
    if request.method=="GET":
        my_vari = session.get('my_var', None)
        user = User.query.filter_by(id=my_vari).first()
        name = user.email

        return render_template("reset_pass.html",my_user=name)
    my_vari = session.get('my_var', None)
    user = User.query.filter_by(id=my_vari).first()


    np = request.form["password"]
    user.password_hash = generate_password_hash(np)
    user.reset=''
    db.session.commit()
    login_user(user)

    return redirect(url_for('course'))
    #return render_template("reset_pass.html",success="Reset Successful")
    #user = User.query.filter_by(security='reset').first()
    #newpass = request.form["password"]
    #user.security='resetdone'
    #db.session.commit()
    #return render_template("reset_pass.html",success="success")

#Google search verification page
@app.route("/google5551350abd40a242.html",methods=['Get','Post'])
def hello():
    if request.method=='GET':
        return render_template('google5551350abd40a242.html')





@app.route("/datatypes",methods=['GET','POST'])
def datatypes():


    if request.method=='GET':
        if not current_user.is_authenticated:
            session['url'] = request.url
            return render_template('data_types.html',error="please")
        uid = current_user.id
        ufile = Files.query.filter_by(uploader_id =uid).all()


        if len(ufile) ==0:
            imagename="PyWe.jpg"

        else:
            for each in ufile:
                List.append(each.filename)
                imagename = str(List[-1])


        return render_template("data_types.html",User=current_user.username,image ="uploads/{}".format(imagename))









@app.route("/image",methods=['GET','POST'])
def image():
    if request.method=='GET':
        if not current_user.is_authenticated:
            session['url'] = request.url
            return render_template('data_types.html',error="please")
        return render_template("course.html",User=current_user.username,image="Screenshot_20180217-170846.png")

imgList = []

@app.route("/slides",methods=['GET','POST'])
def slides():
    if request.method=='GET':
        if not current_user.is_authenticated:
            session['url'] = request.url
            return redirect(url_for('login'))

        ufile = Files.query.all()

        length= len(ufile)

        number=1
        return render_template('slides.html',ufile=ufile,num = number,length=length,imgnamelist=ufile)
    return redirect(url_for('login'))


imgList = []

@app.route("/user",methods=['GET','POST'])
def user():


    if request.method=='GET':

        if not current_user.is_authenticated:
            session['url'] = request.url
            return redirect(url_for('login'))
        ufile = Files.query.filter_by(uploader_id=current_user.id).all()

        length= len(ufile)

        number=1
        imagename = current_user.username


        return render_template('slides.html',ufile=ufile,num = number,length=length,imgname=imagename,error=True)
    return redirect(url_for('login'))










#Send mail to myself from user
@app.route("/mail",methods=["GET","POST"])
def mail():
    yag = yagmail.SMTP("pythonwithellie@gmail.com","learnpython22")
    name = request.form['name1']
    email = request.form["email1"]
    message1 = request.form["message"]

    html_msg = """<html><body style="border:solid 3px #3bc5e6;background-color:#eee;"><center><h3 style="color:#3bc5e6">Message from user</h3></center><center><p>Message: %(my_str1)s <br> From: %(my_str3)s<br>Reply to %(my_str2)s</p></center></body></html>""" %{"my_str1":message1,"my_str2":email,"my_str3":name}
    #msg = Message('Message from user', sender = "pythonwithellie@gmail.com", recipients = [email])
    #msg.body = str(message)
    #mail.send(msg)
    contents = [html_msg]

    yag.send("pythonwithellie@gmail.com","Message from user",contents)
    return redirect(url_for('index',success="Your message was sent"))


#Logging out a user
@app.route("/logout/")

@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



if __name__=="__main__":
    app.run()