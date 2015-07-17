from cookBook.datalayer.post import Post


def get_post(db, postCode):
    cursor = db.cursor()
    post = Post()
    get_post_sql = 'select post_title, post_content \
                    from post where post_code = %s'
    cursor.execute(get_post_sql, (postCode,))
    result = cursor.fetchone()
    if result is None:
        return None
    post.set_code(postCode)
    post.set_title(result[0])
    post.set_content(result[1])
    return post


def get_all_post_code(db):
    cursor = db.cursor()
    posts = []
    get_all_post_code_sql = 'select post_code, post_title from post'
    cursor.execute(get_all_post_code_sql)
    for row in cursor:
        post = Post()
        post.set_code(row[0])
        post.set_title(row[1])
        posts.append(post)
    return posts


def get_post_from_tag(db, tag):
    cursor = db.cursor()
    posts = []
    get_post_from_tag_sql = 'select posttag.post_code, \
                             post.post_title from \
                             posttag,\
                             post where tag_code = %s\
                             and posttag.post_code=post.post_code'
    cursor.execute(get_post_from_tag_sql, (tag,))
    for row in cursor:
        post = Post()
        post.set_code(row[0])
        post.set_title(row[1])
        posts.append(post)
    return posts


def update_post(db, post):
    cursor = db.cursor()
    post_code = post.get_code()
    post_title = post.get_title()
    post_content = post.get_content()
    update_post_sql = 'update post set\
                       ( post_code, post_title, post_content) =\
                       (%s, %s, %s) where post_code = %s'
    params = (post_code, post_title, post_content, post_code)
    cursor.execute(update_post_sql, params)
    db.commit()
    return cursor.rowcount


def insert_post(db, post):
    cursor = db.cursor()
    post_code = post.get_code()
    post_title = post.get_title()
    post_content = post.get_content()
    insert_post_sql = 'insert into post \
                       (post_code, post_title, post_content)\
                       values(%s, %s, %s)'
    params = (post_code, post_title, post_content)
    cursor.execute(insert_post_sql, params)
    db.commit()
    return cursor.rowcount


