from codeBook import app;
from flask import render_template,request

from codeBook.smdParser import parse;

@app.route('/')
def hello_world():
    return 'Hello World';


@app.route('/post/<postName>')
def post(postName):
    return postName;

@app.route('/add/<addName>', methods=['GET','POST'])
def add(addName):
    if request.method == 'POST':
        markDown = request.form.get('post-content');
        return render_template('./post.html', postContent=parse(markDown));
    return render_template('./add.html', title=addName);



