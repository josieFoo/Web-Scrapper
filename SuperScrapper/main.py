from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
#from scrapper2 import get_jobs2
from exportCSV import save_to_file

app = Flask("SuperScrapper")
db = {}


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact")
def contact():
    return "josiepark@zedat.fu-berlin.de"

@app.route("/report")
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        from_db=db.get(word)
        if from_db:
          jobs=from_db
        else:
          jobs = get_jobs(word)#+get_jobs2(word)
          db[word] = jobs    
    else:
        return redirect("/")
    return render_template(
      "report.html", 
      searchBy=word, 
      result_number=len(jobs),
      jobs=jobs
      )

@app.route("/export")
def export():
  try:
    word=request.args.get('word')
    if not word:
      raise Exception()
    word=word.lower()
    jobs=db.get(word)
    if not jobs:
      raise Exception()
    save_to_file(jobs)
    return send_file(filename="job.csv", mimetype="text/csv")
  except:
    return redirect("/")

#@app.route("/<username>")
#def greeting(username):
#    return f"Hello, {username}, let's start!"
#<!-- for flask: \{{variables}} \{% codes%} -->
app.run(host="0.0.0.0")
