from codeBook import app;
from flask import render_template,request,redirect,url_for

import codeBook.db as db;
from codeBook.smdparser import parse;


@app.route('/')
def index():
    posts = db.getAllPostCode();
    tags = db.getAllTag();
    postBuilder = '-[link %s %s]';
    tagBuilder = '[link %s %s]';

    
    postList = "";
    tagList = "";
    for tag in tags:
        tagList = tagList + (tagBuilder % (tag, '/tag/'+tag))+ ', ';
    for post in posts:
        postList = postList + (postBuilder % (post['postTitle'], url_for("post", postCode=post['postCode']))) + "\n";

    postContent = "Tags: "+tagList[0:-2] + "\n\n" + postList;

    return render_template('./index.html', title='codeBook', postTitle='Your Posts', postContent=parse(postContent), displayTag = False);

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
                                    postTitle=postTitle, postContent = postContent.rstrip(),
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
                                postTitle=postTitle, postContent = postContent.rstrip(),
                                password = '', mesg = mesg, 
                                tags = ",".join(tagList));

        


@app.route('/post/<postCode>')
def post(postCode):
    res = db.getPost(postCode);
    postTitle = 'Lost?'
    postContent = 'Add a new page [link here /edit/'+postCode+']';
    if res:
        postTitle = res['postTitle'];
        postContent = res['postContent'];
        tagList = db.getTagList(postCode);

        return render_template('./post.html', title=postCode, postCode=postCode,
                           postTitle = postTitle, tagList = tagList,
                           postContent= parse(postContent), displayTag = True);


    else:
        return render_template('./post.html', title="Lost?", 
                           postTitle = postTitle, 
                           postContent= parse(postContent), displayTag = False);



@app.route('/tag/<tagCode>')
def tag(tagCode):
    res = db.getPostFromTag(tagCode);
    postContent = "";
    for post in res:
        postContent = postContent + "-[link "+post+" /post/"+post+"]\n";
    print(str(postContent));
    return render_template('./post.html', title="tag- "+tagCode,
                        postTitle=tagCode, displayTag = False, postContent=parse(postContent));
