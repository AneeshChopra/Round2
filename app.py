from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort,session
from flask_login import login_user,login_required,logout_user
from myproject.models import User,ToDo
from myproject.forms import LoginForm, RegistrationForm,ToDoForm
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome_user():

    form=ToDoForm()

    items = ToDo.query.filter_by(username=session['user']).order_by(ToDo.duedate.desc()).all()
    print(items)

    if form.validate_on_submit():
        username=session['user']
        title=form.Title.data()
        desc=form.Desc.data()
        cat=form.Category.data()
        date=form.Date.data()
        item=ToDo(username,title,desc,cat,date)
        db.session.add(item)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')


        return render_template('welcome_user.html', form=form,items=items)

    return render_template('welcome_user.html', form=form,items=items)





@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')
            session['user']=str(User.username)

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
