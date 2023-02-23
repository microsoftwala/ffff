from flask import Flask,render_template,request,redirect
import os
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///prakhar.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# postgres://prakhar_user:zhJXuJzkjBPirI0XopW9mAITVsHA5fMy@dpg-cfq74e9gp3jo0b5um0v0-a.singapore-postgresql.render.com/prakhar
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime(200), default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.content} - {self.desc}"
    
def create_app():
    with app.app_context():    
        @app.route('/', methods = ['GET','POST'])
        def hello_world():
            if request.method=='POST':
                content = request.form["content"]
                desc = request.form["desc"]
                todo = Todo(content = content , desc = desc)
                db.session.add(todo)
                db.session.commit()
            alltodo = Todo.query.all()
            return render_template("index.html",alltodo=alltodo)
                # return "Hello bhai sahab"
                
        @app.route('/show')
        def products():
            alltodo = Todo.query.all()
            print(alltodo)
            return "This is prduct page"
        
        @app.route('/delete/<int:sno>')
        def delete(sno):
            todo = Todo.query.filter_by(sno=sno).first()
            db.session.delete(todo)
            db.session.commit()
            return redirect("/")
        
        @app.route('/update/<int:sno>',methods = ['GET','POST'])
        def update(sno):
            if request.method=='POST':
                content = request.form["content"]
                desc = request.form["desc"]
                todo = Todo.query.filter_by(sno=sno).first()
                todo.content = content
                todo.desc = desc
                db.session.commit()
                return redirect("/")
            todo = Todo.query.filter_by(sno=sno).first()
            return render_template("update.html",todo=todo)
            # return "This is after update"
        
        return app