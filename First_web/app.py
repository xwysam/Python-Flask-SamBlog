from flask import Flask,render_template,g,session,request,redirect,url_for
from models import User,Article,Comment
from exts import db
from sqlalchemy import or_
import config
import utils
from flask_cache import Cache
from decoriters import login_reguired

cache = Cache()
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




@app.route('/')
def index():
    context = {
        'articles' : Article.query.order_by('-time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            #save cookie
            session['user_id'] = user.id
            # save for 31 days
            remember = request.form.get('remember')
            if remember:
                session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'username or password wrong!'

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':

        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check email
        user = User.query.filter(User.email == email).first()
        if user:
            return u'already have the email'
        else:
            if password1 != password2:
                return u'password wrong'
            else:
                user = User(email= email,username = username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    #del session['user_id']
    session.clear()
    return redirect(url_for('login'))



@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        return {'user' : user}
    return {}



@app.route('/blog/',methods=['GET','POST'])
@login_reguired
def blog():
    if request.method == 'GET':
        return render_template('blog.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        article = Article(title= title, content= content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        article.author = user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<article_id>/')
def detail(article_id):
    article_model = Article.query.filter(Article.id==article_id).first()
    return render_template('detail.html', article = article_model)

@app.route('/add_comment/', methods=['POST'])
@login_reguired
def add_comment():
    content = request.form.get('comment')
    article_id = request.form.get('article_id')


    comment = Comment(content=content)

    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    comment.author = user

    article = Article.query.filter(Article.id == article_id ).first()
    comment.article = article

    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail',article_id= article_id))

@app.route('/search/',methods=['GET','POST'])
def search():
    keyword = request.args.get('keyword')
    result = Article.query.filter(or_(Article.title.contains(keyword),
                                    Article.content.contains(keyword))).order_by(
                                    Article.time.desc()).all()
    if result:
        return render_template('index.html',articles=result)
    else:
        return render_template('warn.html')



if __name__ == '__main__':
    app.run(debug=True)
