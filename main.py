from flask import Flask, render_template, request, redirect, send_file
from indeed import get_jobs as indeed_get_jobs
from so import get_jobs as so_get_jobs
from itertoolz import interleave as interleave
from exporter import save_to_file

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/report")
def report():
    word = request.args.get('word')
    location = request.args.get('location')
    searchKey = word +" in "+ location
    if searchKey:
        word = word.lower()
        location = location.lower()
        searchKey = searchKey.lower()
        existingJobs = db.get(searchKey)
        if existingJobs:
            jobs = existingJobs
        else:
            jobs = list(interleave([indeed_get_jobs(word, location),so_get_jobs(word, location)]))
            db[searchKey] = jobs
    else:
        return redirect("/")

    return render_template(
        "report.html", 
        searchingBy=searchKey, 
        word = word,
        location = location,
        resultsNumber=len(jobs),
        jobs=jobs
        )

@app.route("/export")
def export():
    try:
      word = request.args.get('word')
      if not word:
        raise Exception()
      location = request.args.get('location')
      if not location: 
        raise Exception()
      word = word.lower()
      location = location.lower()
      searchKey = word + " in " + location
      jobs = db.get(searchKey)
      if not jobs:
        raise Exception()
      save_to_file(jobs)
      return send_file(
            filename_or_fp  = f"{word}_{location}_jobs.csv",
            mimetype='application/x-csv',
            as_attachment=True,
            cache_timeout=0
            )
    except:
      return redirect("/")




# need host="0.0.0.0" b/c we are on repl.it
app.run(host="0.0.0.0")
