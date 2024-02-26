from flask import Flask, render_template , request , redirect 
from dotenv import load_dotenv
import pymongo
import random
import os
app=Flask(__name__)
app_path=os.path.join(os.path.dirname(__file__),".")
dotenv_path=os.path.join(app_path,".env")
load_dotenv(dotenv_path)
connectionString = os.environ.get("MONGODB_URI")
cluster = pymongo.MongoClient(connectionString)
database = cluster["mydatabase"]
collection = database["words"]


@app.route("/", methods= ["GET","POST"])
def index():
    if request.method=="POST":
        word =request.form["words"]
        word=word.lower()
        wordlist=list(word)
        random.shuffle(wordlist)
        jumbledword="".join(wordlist)
        collection.insert_one({"orginal-word":word,"jumbled-word":jumbledword})
        return redirect("/")
    else:
        return render_template("index.html")



@app.route("/play", methods=["GET","POST"])
def play():
    if request.method=="GET":
        words=list(collection.find())
        return render_template("play.html",words=words)
    else:
        count=0
        original_words=request.form.getlist("original-word")
        inputed=request.form.getlist("user-input")
        print(inputed,original_words)
        for n in range (0,len(inputed),1):
            if original_words[n]==inputed[n]:
                count=count+1
        return render_template("result.html",count=count,original_words=original_words,inputed=inputed)

if __name__=="__main__":
    app.run(debug=True) #automatically updates when saves