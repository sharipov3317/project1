from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Мы создаем объект на основе класса Falsk и основным файлом будет ap.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db' #Мы использовали базу данных SQLAlchemy 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False        # и создали объект под названием db
db = SQLAlchemy(app)#В этом файле сохраняются все наши информации. 

#В этом классе есть пять полей и каждая поля она будет отвечат за определенный поля в табличке
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), primary_key=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, primary_key=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/') #Первая страница
@app.route('/home')
def index():
    return render_template("home.html")


@app.route('/2home') #Вторая страница
def about():
    return render_template("2home.html")


@app.route('/3home') #Третья страница
def about2():
    return render_template("3home.html")


@app.route('/posts') #В этом файле хранятся данные, которые мы записали
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>') #в этом файле мы можем удалить или редактировать данные, которые мы записали
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/del') # Если мы нажмем (редактировать), мы получим доступ к этому файлу 
def post_delete(id):              # и сможем редактировать введенную информацию
    article = Article.query.get_or_404(id)
 
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удаление статьи произашла ошибка"
    


@app.route('/posts/<int:id>/update', methods=['POST','GET']) #В этом файле обновляем записанные данные
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произашла ошибка"

    else:
        return render_template("post_update.html", article=article)



@app.route('/create-article', methods=['POST','GET']) # Файл, в который будет вставлена основная информация
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавление статьи произашла ошибка"

    else:
        return render_template("create-article.html") 


if __name__ == "__main__":
    app.run(debug=True)