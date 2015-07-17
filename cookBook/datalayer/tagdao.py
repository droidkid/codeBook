import psycopg2


def add_tags(database, tags):
    cursor = database.cursor()
    add_tag_sql = 'insert into tag values (%s)'
    for tag in tags:
        try:
            cursor.execute(add_tag_sql, (tag,))
            database.commit()
        except psycopg2.IntegrityError:
            database.rollback()


def get_all_tag(database):
    cursor = database.cursor()
    get_all_tag_sql = 'select tag_code from tag'
    tags = []
    cursor.execute(get_all_tag_sql)
    for row in cursor:
        tags.append(row[0])
    return tags


def delete_tag(database, tag):
    cursor = database.cursor()
    delete_tag_sql = 'delete from post where post_code = %s'
    cursor.execute(delete_tag_sql, (tag.get_code(),))
    database.commit()


def remove_unused_tags(database):
    cursor = database.cursor()
    remove_unused_tag_sql = 'delete from tag \
                             where tag.tag_code not in \
                            (select tag_code from posttag)'
    cursor.execute(remove_unused_tag_sql)
    database.commit()
    return cursor.rowcount


def get_tag_of_post(database, post_code):
    cursor = database.cursor()
    get_tag_of_post_sql = 'select tag_code from posttag where post_code = %s'
    params = (post_code,)
    cursor.execute(get_tag_of_post_sql, params)
    tags = []
    for row in cursor:
        tags.append(row[0])
    return tags
