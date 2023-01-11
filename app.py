from flask import Flask, render_template, request
import requests
import webbrowser
import random


app = Flask(__name__)

global search_results, article


@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/suggest', methods=['POST'])
def suggest_wikipedia_articles():
    global search_results, article
    topic = request.form['topic']
    search_url = 'https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search=' + topic + '&limit=max'
    search_results = requests.get(search_url).json()
    all_val = all(i == '' for i in search_results[1])
    if len(search_results[1]) != 0 or all_val != True:
        article = random.choice(search_results[1])
        return render_template("success.html", article=article)
    else:
        return render_template("error.html", error="No articles found for topic : "+topic)

@app.route('/read', methods=['POST'])
def open_article():
    #global search_results
    user_input = request.form['response']
    if user_input == 'yes':
        index = search_results[1].index(article)
        #webbrowser.open(search_results[3][index])
        artlink = search_results[3][index]
        return render_template("artlink.html", artlink = artlink)
    else:
        return render_template("article.html")

@app.route('/againread', methods=['POST'])
def again():
    another_input = request.form['response']
    if another_input == 'yes':
        new_article = random.choice(search_results[1])
        return render_template("success.html", article=new_article)

    else:
        return render_template("new.html")

@app.route('/newtopic', methods=['POST'])
def newpref():
    choice = request.form['response']
    if choice == 'yes':
        return render_template("index.html")
    else:
        return render_template("Home.html")




if __name__ == '__main__':
    app.run(debug=True)


