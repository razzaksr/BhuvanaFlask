from flask import Flask,render_template

app=Flask(__name__)

@app.route("/")
def check():
    return "Zealous Academy"

@app.route("/skills")
def mike():
    return "<ul><li>Python</li><li>Django</li></ul>"

@app.route("/pages")
def fight():
    return render_template('first.html',data="Razak Mohamed S")

@app.route("/stat")
def play():
    return render_template('second.html')

@app.route("/mine/<data>")
def params(data):
    return render_template('first.html',data=data)

@app.route("/mn/<int:dt>")
def paramss(dt):
    return render_template('first.html',data=dt*dt)

if __name__=="__main__":
    app.run(debug=True,port=2000)