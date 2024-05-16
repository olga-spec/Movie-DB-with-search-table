from tabulate import tabulate
from preparation import *

def search_by_name(dbconfig_amazon, dbconfig_ich, arg):
    connection_amazon, cursor_amazon = connection_db(dbconfig_amazon)
    connection_ich, cursor_ich = connection_db(dbconfig_ich)

    cursor_amazon.execute(f'''select title, year, cast, `imdb.rating`, plot
                    from movies 
                    where title like "%{arg}%"
                    order by `imdb.rating` DESC
                    limit 10''')
    result = cursor_amazon.fetchall()

    print(tabulate(result, headers=['Title', 'Year', 'Actors', 'Rating', 'Description']))

    if len(result) ==0:
        print('No data avaliable')
    else:
        insert_into_table(cursor_ich, connection_ich, arg)
    disconnect_connection(connection_amazon, cursor_amazon)
    disconnect_connection(connection_ich, cursor_ich)



def search_by_year_genre(dbconfig_amazon, dbconfig_ich, genre, year):
    connection_amazon, cursor_amazon = connection_db(dbconfig_amazon)
    connection_ich, cursor_ich = connection_db(dbconfig_ich)

    cursor_amazon.execute(f'''select title, year, cast, `imdb.rating`, plot
                        from movies 
                        where genres like "%{genre}%"
                        and year = "{year}"
                        order by `imdb.rating` DESC
                        limit 10''')
    result = cursor_amazon.fetchall()

    print(tabulate(result, headers=['Title', 'Year', 'Actors', 'Rating', 'Description']))

    if len(result) ==0:
        print('No data avaliable')
    else:
        arg = ', '.join(map(str, (genre, year)))
        insert_into_table(cursor_ich, connection_ich, arg)
    disconnect_connection(connection_amazon, cursor_amazon)
    disconnect_connection(connection_ich, cursor_ich)



def search_by_actor(dbconfig_amazon, dbconfig_ich, arg):
    connection_amazon, cursor_amazon = connection_db(dbconfig_amazon)
    connection_ich, cursor_ich = connection_db(dbconfig_ich)

    cursor_amazon.execute(f'''select title, year, cast, `imdb.rating`, plot
                        from movies 
                        where cast like "%{arg}%"
                        order by `imdb.rating` DESC
                        limit 10''')
    result = cursor_amazon.fetchall()

    print(tabulate(result, headers=['Title', 'Year', 'Actors', 'Rating', 'Description']))

    if len(result) ==0:
        print('No data avaliable')
    else:
        insert_into_table(cursor_ich, connection_ich, arg)
    disconnect_connection(connection_amazon, cursor_amazon)
    disconnect_connection(connection_ich, cursor_ich)



def insert_into_table(cursor_ich, connection_ich, arg):
    cursor_ich.execute(f'''select id, count
                        from searched_info
                        where searched_key_word = "{arg}"''')
    result = cursor_ich.fetchall()

    if len(result) == 0:
        cursor_ich.execute(f'''insert into searched_info (searched_key_word, count)
                            values ('{arg}', 1)''')
        print('Data inserted')
        connection_ich.commit()
    elif len(result) == 1:
        id, count = result[0]
        count += 1
        cursor_ich.execute(f'''update searched_info 
                            set count = {count}
                            where id = {id}''')
        print('Data updated')
        connection_ich.commit() 
    else:
        print('Error. Check manualy, your program does not working properly')



def get_common(dbconfig_ich):
    connection_ich, cursor_ich = connection_db(dbconfig_ich)
    cursor_ich.execute('''select searched_key_word, count
                    from searched_info
                    order by count DESC''')
    result = cursor_ich.fetchall()
    print(tabulate(result, headers=['Searched by', 'Total count']))
    disconnect_connection(connection_ich, cursor_ich)
