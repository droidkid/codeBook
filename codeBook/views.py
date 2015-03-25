from codeBook import app;
from flask import render_template,request,redirect,url_for

import codeBook.db as db;
from codeBook.smdparser import parse;


@app.route('/')
def index():
    posts = db.getAllPostCode();
    builder = '-[link %s %s]';
    
    postList = "";
    for post in posts:
        postList = postList + (builder % (post['postTitle'], url_for("post", postCode=post['postCode']))) + "\n";
    return render_template('./post.html', title='codeBook', postTitle='Your Posts', postContent=parse(postList));

@app.route('/edit/<postCode>', methods=['GET','POST'])
def edit(postCode):
    mesg = [];
    if request.method == 'POST':
        postTitle = request.form.get('postTitle');
        postContent = request.form.get('postContent');
        password = request.form.get('password');
        tags = request.form.get('tags');
        tagList = tags.split(',');
        tagList = [x.strip() for x in tagList];
        filter(None, tagList);
        postTitle = postTitle.strip();
        if not postTitle:
            e.append('Cannot Have Empty Post Title');
            return render_template('./edit.html',    title=postCode,
                                    postTitle=postTitle, postContent = postContent,
                                    password = '', mesg = mesg, 
                                    tags = tags);
        
        db.editPost(postCode, postTitle, postContent, tagList);
        return redirect(url_for('post', postCode=postCode));

    if request.method == 'GET':
        res = db.getPost(postCode);
        if res is None:
            return render_template('./edit.html', title=postCode);
        postTitle = res['postTitle'];
        postContent = res['postContent'];
        tagList = db.getTagList(postCode);
        return render_template('./edit.html',    title=postCode,
                                postTitle=postTitle, postContent = postContent,
                                password = '', mesg = mesg, 
                                tags = ",".join(tagList));

        

@app.route('/post/<postCode>')
def post(postCode):
    res = db.getPost(postCode);
    postCode = postCode;
    postTitle = 'Lost?'
    postContent = 'Add a new page at /edit/'+postCode;

    if res:
        postTitle = res['postTitle'];
        postContent = res['postContent'];


    return render_template('./post.html', title=postCode,
                           postTitle = postTitle, 
                           postContent= parse(postContent));



