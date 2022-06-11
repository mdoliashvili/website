from flask import Flask, render_template, url_for, redirect,session, request,  flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt, generate_password_hash
from pars import img

# print(img)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'films'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///films.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)



class Films(db.Model):
    description = db.Column(db.String(70), nullable=False,primary_key= True)
    genre = db.Column(db.String(40), nullable=False)
    com = db.Column(db.String(40))
    imdb = db.Column(db.String(40), nullable=False)
    img = db.Column(db.String(100))

    def __str__(self):
        return f' description: {self.description};  genre-  {self.genre}; imdb {self.imdb}'

class User(db.Model):
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(40), nullable=False,primary_key= True)
    password = db.Column(db.String(20), nullable=False)

    def __str__(self):
        return f'User First Name:{self.First_Name}; Last Name: {self.Last_Name}; Email: {self.Email}'



db.create_all()



@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')






@app.route('/login', methods= ['GET','POST'])
def login():

    if 'user' not in session:
        try:
            if request.method == 'POST' and User.query.filter_by(username=request.form['Username']).first().username == request.form['Username']:
                hashed_password = User.query.filter_by(username=request.form['Username']).first().password
                passw = request.form['Password']
                print(bcrypt.check_password_hash(hashed_password, passw))
                if bcrypt.check_password_hash(hashed_password, passw):
                    userr = request.form['Username']
                    session['user'] = userr
                    return redirect(url_for('user', user=userr))
                if not bcrypt.check_password_hash(hashed_password, passw):
                    flash('პაროლი არასწორია', 'n')
                    # return render_template('login.html')

        except AttributeError:
            flash('თქვენ არ ხართ დარეგისტრირებული', 'n')

        return render_template('login.html')
    return redirect(url_for('home'))


    # forr searchh
    # <form class="form-inline my-2 my-lg-0">
    #   <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
    #   <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    # </form>



@app.route('/logout')
def logout():
    session.pop('user',None)
    flash('you are log out', 'n')
    return redirect(url_for('home'))






@app.route('/<user>')
def user(user):
    if 'user' in session and User.query.filter_by(username=session['user']).first():
        user = User.query.filter_by(username=session['user']).first().username

        return render_template('user.html', user= user)

    return redirect(url_for('home'))



@app.route('/registration', methods= ['GET','POST'])
def registration():
    try:
        if request.method == 'POST' and User.query.filter_by(username=request.form['Username']).first().username == request.form['Username']:
            flash ('თქვენ უკვე დარეგისტრირებული ხართ','n')
            return render_template('register.html')
    except AttributeError:

        if request.method == 'POST':
            firstname = request.form['Firstname']
            lastname = request.form['Lastname']
            username = request.form['Username']
            password = request.form['Password']
            hashed_psw = bcrypt.generate_password_hash(password).decode('utf-8')
            pas = hashed_psw
            user = User(firstname=firstname, lastname=lastname, username= username,password=hashed_psw )
            db.session.add(user)
            db.session.commit()

            userr = request.form['Username']
            session['user'] = userr
            return redirect(url_for('user',user = userr))

    return render_template('register.html')







@app.route('/films')
def films():
    if 'user' in session:
        all = Films.query.all()
        return render_template('films.html',all= all, img=img)
    flash('please log in to your account', 'n')
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run(debug=True)
