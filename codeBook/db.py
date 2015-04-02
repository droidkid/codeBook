#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 yuvaraj <yuvaraj@eee-pc>
#
# Distributed under terms of the MIT license.


'''

Table Post
postCode text(10) pk not null
postTitle text
postContent text(10) not null

Table Tag
tagCode text(20) pk not null

Table postTag

tagCode ForeignKey
postCode ForeignKey

'''

import sqlite3
from flask import g
from codeBook import app


DATABASE = 'codeBook/db/codeBook.db';
PRAGMA_FK = 'pragma foreign_keys=on'

def connectDB():
    return sqlite3.connect(DATABASE);


def get_db():
    db = getattr(g, '_database', None);
    if db is None:
        db = g._database = connectDB();
        db.cursor().execute(PRAGMA_FK);
    return db;


@app.teardown_appcontext
def close_get_dbection(exception):
    db = getattr(g, '_database', None);
    if db is not None:
        db.close();

addTagSQL = 'insert into tag values(?)'
def addTag(tagList):
    c = get_db().cursor();
    sqlData = {(x,) for x in tagList};
    for data in sqlData:
        try:
            c.execute(addTagSQL, data);
        except sqlite3.IntegrityError:
            pass;

        

editPostSQL = 'insert or replace into post(post_code, post_title, post_content) values(?,?,?)';
tagPostSQL = 'insert into posttag(tag_code, post_code) values(?,?)';
def editPost(postCode, postTitle, postContent, tagList):
    c = get_db().cursor();
    sqlData= (postCode,postTitle, postContent);
    c.execute(editPostSQL, sqlData);
    addTag(tagList);
    sqlData = {(x,postCode) for x in tagList};
    c.executemany(tagPostSQL, list(sqlData));
    clearZeroTag();
    get_db().commit();

clearZeroTagSQL = 'delete from tag where tag.tag_code not in (select tag_code from posttag)';
def clearZeroTag():
    c = get_db().cursor();
    c.execute(clearZeroTagSQL);

getPostSQL = 'select post_title, post_content from post where post_code = ?';
def getPost(postCode):
    c = get_db().cursor();
    c.execute(getPostSQL, (postCode,));
    res = c.fetchone();
    if res is None:
        return None;
    ret = {};
    ret['postTitle'] = res[0];
    ret['postContent'] = res[1];
    return ret;

getAllPostSQL = 'select post_code, post_title from post';
def getAllPostCode():
    c = get_db().cursor();
    ret = [];
    for row in c.execute(getAllPostSQL):
        rowData = {};
        rowData['postCode'] = row[0];
        rowData['postTitle'] = row[1];
        ret.append(rowData);
    return ret;

getTagListSQL = 'select tag_code from posttag where post_code = ?'
def getTagList(postCode):
    c = get_db().cursor();
    c.execute(getTagListSQL, (postCode,));
    res = c.fetchall();
    ret = [x[0] for x in res];
    return ret;

getPostFromTagSQL = 'select post_code from posttag where tag_code = ?'
def getPostFromTag(tag):
    c = get_db().cursor();
    ret = [];
    for row in c.execute(getPostFromTagSQL, (tag,)):
        ret.append(row[0]);
    return ret;

deleteTagSQL = 'delete from tag where tag_code = ?'
def deleteTag(tag):
    c = get_db().cursor();
    c.execute(deleteTagSQL, (tag,));
    get_db.commit();

deletePostSQL = 'delete from post where post_code = ?'
def deletePost(postCode):
    c = get_db().cursor();
    c.execute(deletePostSQL, (postCode,));
    clearZeroTag();
    get_db.commit();

