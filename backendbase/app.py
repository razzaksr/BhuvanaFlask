from dataclasses import fields
from flask import Flask, jsonify, make_response, redirect,render_template, request,Response, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app=Flask(__name__)

#db configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/bhuvana'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
buvana=SQLAlchemy(app)
marsh=Marshmallow(app)
CORS(app)
app.secret_key="bhuvana"

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
    

class ProfileSchema(marsh.Schema):
    class Meta:
        fields=('id','person','role','experience','ctc','expected')
        

# schema object for one profile object to serialize and deserialize
profile_scheme=ProfileSchema()
# schema object for many profiles object to serialize and deserialize
profiles_schemes=ProfileSchema(many=True)


# rest api>> json, jsonify

@app.route("/rest/",methods=['GET'])
def toAll():
    all=profiles.query.all()
    obj=profiles_schemes.dump(all)
    return jsonify(obj)







# jinja response
@app.route("/short",methods=['GET','POST'])
def shorting():
    if not session.get('who'):
        return render_template("login.html")
    else:
        if request.method=="POST":
            e=request.form['exp']
            #print(e)
            pro=profiles.query.filter_by(experience=e)
            print(type(pro),pro)
            ha=[]
            ha.append(pro)
            return render_template('listing.html',every=pro)
        else:
            return render_template('short.html')
    
@app.route("/logout",methods=['GET'])
def out():
    session['who']=None
    return render_template('login.html',info="logged out successfully")

@app.route("/",methods=['GET','POST'])
def log():
    if request.method=="POST":
        if request.form['username']=="zealous" and request.form['password']=="buvanaflask":
            session['who']=request.form['username']
            return redirect("/home")
        else:
            return render_template('login.html',info="login failed")
    return render_template('login.html')

@app.route("/home",methods=['GET'])
def traverse():
    if not session.get('who'):
        return render_template("login.html")
    else:
        hai=profiles.query.all()
        #return render_template('listing.html',every=hai)
        #return Response(render_template('listing.html',every=hai))
        res=make_response(render_template('listing.html',every=hai))
        return res

@app.route("/delete/<int:key>",methods=['GET'])
def delete(key):
    if not session.get('who'):
        return render_template("login.html")
    else:
        obj=profiles.query.filter_by(id=key).first()
        print(obj)
        buvana.session.delete(obj)
        buvana.session.commit()
        return redirect("/home")

@app.route("/update/<int:key>",methods=['GET','POST'])
def update(key):
    if not session.get('who'):
        return render_template("login.html")
    else:
        obj=profiles.query.filter_by(id=key).first()
        if request.method=="POST":
            obj.person=request.form['person']
            obj.role=request.form['role']
            obj.experience=request.form['experience']
            obj.ctc=request.form['ctc']
            obj.expected=request.form['expected']
            buvana.session.add(obj)
            buvana.session.commit()
            return redirect("/home")
        return render_template('edit.html',object=obj)
    
@app.route("/new",methods=['GET','POST'])
def process():
    if not session.get('who'):
        return render_template("login.html")
    #buvana.create_all() # to create table
    else:
        if request.method=="GET":
            return render_template('newone.html')
        else:
            pro=profiles(request.form['person'],request.form['experience'],request.form['role'],request.form['ctc'],request.form['expected'])
            buvana.session.add(pro)
            buvana.session.commit()
            return redirect('/home')
        
        

if __name__=="__main__":
    app.run(debug=True)