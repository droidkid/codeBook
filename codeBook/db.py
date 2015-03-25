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

conn = sqlite3.connect('codeBook/db/codeBook.db');
c = conn.cursor();

f = open('codeBook/db/schema.sql');
s = f.read();
c.executescript(s);
conn.commit();


addTagSQL = 'insert into tag values(?)'
def addTag(tagList):
    sqlData = [(x,) for x in tagList];
    for data in sqlData:
        try:
            c.execute(addTagSQL, data);
        except sqlite3.IntegrityError:
            pass;

        

editPostSQL = 'insert or replace into post(post_code, post_title, post_content) values(?,?,?)';
tagPostSQL = 'insert into posttag(tag_code, post_code) values(?,?)';
def editPost(postCode, post_title, postContent, tagList):
    sqlData= (postCode,post_title, postContent);
    c.execute(editPostSQL, sqlData);
    addTag(tagList);
    sqlData = [(x,postCode) for x in tagList];
    c.executemany(tagPostSQL, sqlData);
    clearZeroTag();
    conn.commit();

clearZeroTagSQL = 'delete from tag where tag.tag_code not in (select tag_code from posttag)';
def clearZeroTag():
    c.execute(clearZeroTagSQL);

getPostSQL = 'select post_title, post_content from post where post_code = ?';
def getPost(postCode):
    c.execute(getPostSQL, (postCode,));
    res = c.fetchone();
    if res is None:
        return None;
    ret = {};
    ret['post_title'] = res[0];
    ret['post_content'] = res[1];
    return ret;

getAllPostSQL = 'select post_code, post_title from post';
def getAllPostCode():
    ret = [];
    for row in c.execute(getAllPostSQL):
        rowData = {};
        rowData['post_code'] = row[0];
        rowData['post_title'] = row[1];
        ret.append(rowData);
    return ret;

getTagListSQL = 'select tag_code from posttag where post_code = ?'
def getTagList(postCode):
    c.execute(getTagListSQL, (postCode,));
    res = c.fetchall();
    ret = [x[0] for x in res];
    return ret;

deleteTagSQL = 'delete from tag where tag_code = ?'
def deleteTag(tag):
    c.execute(deleteTagSQL, (tag,));
    conn.commit();

deletePostSQL = 'delete from post where post_code = ?'
def deletePost(postCode):
    c.execute(deletePostSQL, (postCode,));
    clearZeroTag();
    conn.commit();

