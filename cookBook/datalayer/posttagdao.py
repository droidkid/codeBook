def update_tags_of_post(db, post_code, tags):
    cursor = db.cursor()
    update_tags_of_post_sql = 'insert into posttag(post_code, tag_code)\
                                                            values(%s,%s)'
    for tag in tags:
        params = (post_code, tag)
        cursor.execute(update_tags_of_post_sql, params)
        db.commit()


def delete_tags_of_post(db, post_code):
    cursor = db.cursor()
    delete_tags_of_post_sql = 'delete from posttag where post_code = %s'
    cursor.execute(delete_tags_of_post_sql, (post_code,))
    db.commit()
