#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 yuvaraj <yuvaraj@eee-pc>
#
# Distributed under terms of the MIT license.
import psycopg2
from flask import g

import cookBook.datalayer.postdao as PostDAO

from cookBook import app
from config import *


def connectDB():
    return psycopg2.connect(database=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connectDB()
    return db


@app.teardown_appcontext
def close_get_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



addTagSQL = 'insert into tag values(%s)'
def addTag(tagList):
    c = get_db().cursor();
    sqlData = {(x,) for x in tagList};
    for data in sqlData:
        try:
            c.execute(addTagSQL, (data,));
            get_db().commit();
        except psycopg2.IntegrityError: #Integrity error comes when same key is being added
            print("Integrity Error!");
            get_db().rollback();
            pass;



updatePostSQL = 'update post set(post_code, post_title, post_content)=(%s, %s, %s) where post_code=%s';
insertPostSQL = 'insert into ost(post_code, post_title, post_content) values(%s, %s, %s)';
deletePostTagSQL = 'delete from posttag where post_code = %s';
tagPostSQL = 'insert into posttag(tag_code, post_code) values(%s,%s)';
def editPost(postCode, postTitle, postContent, tagList):
    c = get_db().cursor();
    sqlData= (postCode,postTitle, postContent, postCode);
    c.execute(updatePostSQL, sqlData);
    if( c.rowcount == 0 ):
        sqlData= (postCode,postTitle, postContent);
        c.execute(insertPostSQL, sqlData);
    c.execute(deletePostTagSQL, (postCode,));
    print("Rows Deleted"+str(c.rowcount));
    get_db().commit();
    addTag(tagList);
    sqlData = [];
    for tag in tagList:
        sqlData.append((tag, postCode));
    c.executemany(tagPostSQL, sqlData);
    clearZeroTag();
    get_db().commit();

clearZeroTagSQL = 'delete from tag where tag.tag_code not in (select tag_code from posttag)';
def clearZeroTag():
    c = get_db().cursor();
    c.execute(clearZeroTagSQL);


def getPost(post_code):
    post = PostDAO.get_post(get_cursor(), post_code)
    ret = {}
    ret['postTitle'] = post.get_title()
    ret['postContent'] = post.get_content()
    return ret


getAllPostSQL = 'select post_code, post_title from post';
def getAllPostCode():
    c = get_db().cursor();
    ret = [];
    c.execute(getAllPostSQL);
    for row in c:
        rowData = {};
        rowData['postCode'] = row[0];
        rowData['postTitle'] = row[1];
        ret.append(rowData);
    return ret;

getTagListSQL = 'select tag_code from posttag where post_code = %s'
def getTagList(postCode):
    c = get_db().cursor();
    c.execute(getTagListSQL, (postCode,));
    res = c.fetchall();
    ret = [x[0] for x in res];
    return ret;

getPostFromTagSQL = 'select post_code from posttag where tag_code = %s'
def getPostFromTag(tag):
    c = get_db().cursor();
    ret = [];
    c.execute(getPostFromTagSQL, (tag,));
    for row in c:
        ret.append(row[0]);
    return ret;

getAllTagSQL = 'select tag_code from tag';
def getAllTag():
    c = get_db().cursor();
    ret = [];
    c.execute(getAllTagSQL);
    for row in c:
        ret.append(row[0]);
    return ret;

deleteTagSQL = 'delete from tag where tag_code = %s'
def deleteTag(tag):
    c = get_db().cursor();
    c.execute(deleteTagSQL, (tag,));
    get_db.commit();

deletePostSQL = 'delete from post where post_code = %s'
def deletePost(postCode):
    c = get_db().cursor();
    c.execute(deletePostSQL, (postCode,));
    clearZeroTag();
    get_db.commit();

