from cookBook import app
from flask import render_template, request, redirect, url_for

import cookBook.datalayer.db as db
from cookBook.smdparser import parse
import cookBook.datalayer.postdao as PostDAO
import cookBook.datalayer.posttagdao as PostTagDAO
import cookBook.datalayer.tagdao as TagDAO
import cookBook.datalayer.tagdao as TagDAO
from cookBook.datalayer.post import Post
from cookBook.datalayer.tag import Tag

PASS = 'ninefuck'


def get_list_of_posturl(posts):
    list_of_posturl = ""
    post_link_builder = '-[link %s %s]'
    for post in posts:
        params = (post.get_title(), url_for("post", post_code=post.get_code()))
        list_of_posturl = list_of_posturl + (post_link_builder % params) + "\n"
    return list_of_posturl


def get_list_of_tagurl(tags):
    list_of_tagurl = ""
    tag_link_builder = '[link %s %s]'
    for tag in tags:
        params = (tag, url_for("tag", tagCode=tag))
        list_of_tagurl = list_of_tagurl + (tag_link_builder % params) + ', '
    return "Tags: " + list_of_tagurl[0:-2]


@app.route('/')
def index():
    posts = PostDAO.get_all_post_code(db.get_db())
    tags = TagDAO.get_all_tag(db.get_db())
    list_of_post = get_list_of_posturl(posts)
    list_of_tag = get_list_of_tagurl(tags)
    content = parse(list_of_tag + "\n\n" + list_of_post)
    return render_template('./index.html',
                           title='cookBook',
                           postTitle='Posts',
                           postContent=content,
                           displayTag=False)


def edit_post(post_code, post_title, post_content, tag_list):
    post = Post()
    post.set_code(post_code)
    post.set_title(post_title)
    post.set_content(post_content)
    rows_changed = PostDAO.update_post(db.get_db(), post)
    if rows_changed == 0:
        PostDAO.insert_post(db.get_db(), post)
    TagDAO.add_tags(db.get_db(), tag_list)
    PostTagDAO.delete_tags_of_post(db.get_db(), post.get_code())
    PostTagDAO.update_tags_of_post(db.get_db(), post.get_code(), tag_list)
    TagDAO.remove_unused_tags(db.get_db())


@app.route('/edit/<post_code>', methods=['GET', 'POST'])
def edit(post_code):
    post_title = ''
    post_content = ''
    messages = []
    tags = ''
    if request.method == 'POST':
        post_title = request.form.get('postTitle').strip()
        post_content = request.form.get('postContent')
        tags = request.form.get('tags')
        tag_list = [tag for tag in tags.split(",")]
        filter(None, tag_list)
        password = request.form.get('password')
        if(password != PASS):
            messages.append('Wrong Password')
        elif not post_title:
            messages.append('Cannot Have Empty Post Title')
        else:
            edit_post(post_code, post_title, post_content, tag_list)
            return redirect(url_for('post', post_code=post_code))
    if request.method == 'GET':
        post = PostDAO.get_post(db.get_db(), post_code)
        tag_list = TagDAO.get_tag_of_post(db.get_db(), post_code)
        if post:
            post_code = post.get_code()
            post_title = post.get_title()
            post_content = post.get_content()
            tags = ",".join(tag_list)
    return render_template('./edit.html',
                           title=post_code,
                           postTitle=post_title,
                           postContent=post_content.rstrip(),
                           password='',
                           mesg=messages,
                           tags=tags)


@app.route('/post/<post_code>')
def post(post_code):
    post = PostDAO.get_post(db.get_db(), post_code)
    title = 'Lost?'
    content = 'Add a new page [link here /edit/'+post_code+']'
    displayTag = False
    if post:
        title = post.get_title()
        content = post.get_content()
        tagList = TagDAO.get_tag_of_post(db.get_db(), post_code)
        displayTag = True
    return render_template('./post.html',
                           title=post_code,
                           postCode=post_code,
                           postTitle=title, tagList=tagList,
                           postContent=parse(content),
                           displayTag=displayTag)


@app.route('/tag/<tagCode>')
def tag(tagCode):
    posts = PostDAO.get_post_from_tag(db.get_db(), tagCode)
    list_of_posturl = get_list_of_posturl(posts)
    return render_template('./post.html',
                           title="tag- "+tagCode,
                           postTitle=tagCode,
                           displayTag=False,
                           postContent=parse(list_of_posturl))
