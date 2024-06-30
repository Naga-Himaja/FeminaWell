from flask import Flask, request, render_template, redirect, url_for, session, g
import pickle
from user import User
from query import Query
from admin import Admin, AdminUSER
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from datetime import timedelta, date, datetime

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'JoeCare_801')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = u"Login to access this page." ##Added

model = pickle.load(open('model.pkl', 'rb'))

class CurrUser(UserMixin):
    def __init__(self, userId):
        self.userId = userId

    def get_id(self):
        return self.userId
    
    def is_active(self):
        return True

class event_login:
    def user_in(self):
        self.login = True
    def user_out(self):
        self.login = False
    def get_user(self):
        return self.login
    
class Local_User:
    def __init__(self):
        self.login = self.id = self.name = self.dob = self.age = self.phno = self.email = self.pwd = self.login = False
    def get_curr_user_name(self):
        return self.name
    def check_passowrd(self, pwd):
        return self.pwd == pwd

def set_user(record):
    session['user_id'] = record[0]
    session['name'] = record[1]
    session['email'] = record[2]
    session['phno'] = record[3]
    session['dob'] = record[4]
    session['age'] = calc_age(record[4])
    session['password'] = record[5]
    

def calc_age(dob):
     x = datetime.strptime(dob, '%Y-%m-%d')
     today = date.today()
     one_or_zero = ((today.month, today.day) < (x.month, x.day))
     year_difference = today.year - x.year
     y = 1 if one_or_zero else 0
     curr_age = year_difference - y
     return curr_age

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('user_email')
        pwd = request.form['pwd']
        if User.check_email_exists(email) == False:
            return render_template('login.html', info='Email Does Not Exist!!!')
        record = User.get_user_details(email)
        if record[5] != pwd:
            return render_template('login.html', info='Invalid Password!!!')
        else:
            user = CurrUser(record[0])
            set_user(record)
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        phno = request.form['phno']
        email = request.form['user_email']
        pwd = request.form['pwd']
        conf_pwd = request.form['conf_pwd']
        if User.check_email_exists(email):
            return render_template("login.html", info = "Email already Exits!!!")
        if pwd != conf_pwd:
            return render_template("login.html", info = "Password and Confirm Password doesn't Match")
        User.add_new_user(name,email, phno, dob, pwd)
        record = User.get_user_details(email)
        set_user(record)
        logged_user = CurrUser(record[0])
        login_user(logged_user)
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/home')
@login_required
def index():
    return render_template("home.html",logged = current_user.is_active)

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))


@app.route('/mental_health', methods=['POST', 'GET'])
def mental_health():
    return render_template('mental_health.html')

@app.route('/pregnancy', methods=['POST', 'GET'])
def pregnancy():
    return render_template('pregnancy.html')

@app.route('/period', methods=['POST', 'GET'])
def period():
    return render_template('period.html')

@app.route('/sex_ed', methods=['POST', 'GET'])
def sex_ed():
    return render_template('sex_ed.html')

@app.route('/lifestyle', methods=['POST', 'GET'])
def lifestyle():
    return render_template('lifestyle.html')

@app.route('/profile', methods=['POST','GET'])
def profile():
    return render_template('profile.html', name=session['name'])

@app.route('/community', methods=['POST','GET'])
def community():
    records = Query.get_app_post()
    return render_template('community.html', records=records)

@app.route('/communityPostAdd', methods=['POST','GET'])
def communityPostAdd():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['msg']
        anony = request.form.get('anony')
        if anony != "True":
            anony = "False"
        Query.add_new_post(session.get('user_id'), title, desc, anony, session.get('name'), session.get('email'), session.get('age'))
        return render_template("communityPostAdd.html", info = "You post have been sent to moderation. It will be approved in 24 hours.")
    return render_template('communityPostAdd.html')

@app.route("/communityPost/<int:postid>", methods = ['POST', 'GET'])
@login_required
def communityPost(postid):
    records = Query.get_post_postid(postid)
    comments = Query.get_comments(postid)
    return render_template("communityPost.html", records = records, comments = comments)

@app.route("/comment/<int:postid>", methods = ['POST'])
@login_required
def comment(postid):
    if request.method == "POST":
        comment = request.form["comment"]
        anony = request.form.get("anony")
        if anony != "True":
            anony = "False"
        Query.add_comment(postid, session.get('user_id'), session.get('name'), session.get('email'), comment, anony)
        return redirect(url_for("communityPost", postid = postid))
    return redirect(url_for("communityPost", postid = postid))

@app.route("/expert", methods=['POST', 'GET'])
@login_required
def expert():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form['email']
        phno = request.form["phno"]
        msg = request.form["msg"]
        res = request.form['res']
        Query.add_expert(session.get("user_id"), name, email, phno, msg, res, "False")
        return render_template("expert.html", info="You request have been sent to moderation. You will be contacted in 24 hours.")
    return render_template("expert.html")

admin_user = AdminUSER()
@app.route("/adminlogin")
@login_required
def adminLogin():
    records = Admin.get_admin()
    for record in records:
        if session.get('user_id') in record:
            admin_user.set_login()
            return redirect("admin")
    return redirect(url_for("index"))

@app.route("/approve/<int:postid>", methods = ["POST"])
@login_required
def approve(postid):
    if request.method == "POST":
        ageres = request.form.get('ageres')
        if ageres != "True":
            ageres = "False"
        Admin.post_approve(postid, "False", "True", ageres)
        return redirect(url_for('admin'))
    return redirect(url_for("admin"))

@app.route("/disapprove/<int:postid>")
@login_required
def disapprove(postid):
    Admin.post_approve(postid, "False", "False", "False")
    return redirect(url_for('admin'))

@app.route("/reqdone/<int:reqid>", methods = ["POST"])
@login_required
def reqdone(reqid):
    if request.method == 'POST':
        done = request.form.get('done')
        if done != "True":
            done = "False"
        Admin.req_completed(reqid, done)
        return redirect(url_for("admin"))
    return redirect(url_for("admin"))

@app.route("/admin")
@login_required
def admin():
    if admin_user.get_status():
        records = Admin.get_posts()
        req = Query.get_expert_req()
        return render_template("admin.html", records = records, req = req)
    else:
        return redirect(url_for('index'))

@app.route("/adminlogout")
@login_required
def adminLogout():
    admin_user.set_logout()
    return redirect(url_for("index"))


@app.route("/query")
@login_required
def query():
    records = Query.get_app_post()
    return render_template("query.html", records = records)


@app.route('/pcos_prediction',methods=['POST', 'GET'])
def pcos_pred():
    diagnosis = 0
    if request.method == 'POST':
        x1 = int(request.form.get('periodLen',False))
        print(x1)
        x2 = int(request.form.get('cycleLen',False))
        x3 = int(request.form.get('age',False))
        x4 = int(request.form.get('overweight',False))
        x5 = int(request.form.get('weightLossGain',False))
        x6 = int(request.form.get('missedPeriod',False))
        x7 = int(request.form.get('diffConceive',False))
        x8 = int(request.form.get('chinHair',False))
        x9 = int(request.form.get('cheekHair',False))
        x10 = int(request.form.get('breastHair',False))
        x11 = int(request.form.get('lipHair',False))
        x12 = int(request.form.get('armHair',False))
        x13 = int(request.form.get('thighHair',False))
        x14 = int(request.form.get('acne',False))
        x15 = int(request.form.get('hairLoss',False))
        x16 = int(request.form.get('darkPatch',False))
        x17 = int(request.form.get('tired',False))
        x18 = int(request.form.get('mood',False))
        x19 = int(request.form.get('exercise',False))
        x20 = int(request.form.get('junk',False))
        x21 = int(request.form.get('canned',False))
        
        diagnosis = model.predict([[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,
                                    x12,x13,x14,x15,x16,x17,x18,x19,x20,x21]])
        
    return render_template('pcos_prediction.html', diagnosis= diagnosis)

@login_manager.user_loader
def load_user(userid):
    return CurrUser(userid)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    session.modified = True
    g.user = current_user

if __name__=='__main__':
    app.run(debug=True)