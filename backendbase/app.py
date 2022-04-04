from flask import Flask,render_template, request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

#db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/bhuvana'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
buvana=SQLAlchemy(app)

#model
class profiles(buvana.Model):
    id=buvana.Column(buvana.Integer,primary_key=True)
    person=buvana.Column(buvana.String(255),nullable=False)
    experience=buvana.Column(buvana.Integer,nullable=False)
    role=buvana.Column(buvana.String(255),nullable=False)
    ctc=buvana.Column(buvana.Float,nullable=False)
    expected=buvana.Column(buvana.Float,nullable=False)
    
    def __init__(self,nm="",exp=0,r="",ct=0.0,ex=0.0):
        self.person=nm
        self.experience=exp
        self.role=r
        self.ctc=ct
        self.expected=ex

    def __repr__(self) -> str:
        return f"{self.person} - {self.role}"
    
@app.route("/new",methods=['GET','POST'])
def process():
    if request.method=="GET":
        return render_template('newone.html')
    else:
        pro=profiles(request.form['person'],request.form['experience'],request.form['role'],request.form['ctc'],request.form['expected'])
        buvana.session.save(pro)
        buvana.session.commit()
        return render_template('newone.html',info="Object saved")

if __name__=="__main__":
    app.run(debug=True)