import sqlite3
global sqlconnection, cur
# Подключение к базе
def sql_start():
    global sqlconnection, cur
    sqlconnection = sqlite3.connect("data.db")
    cur = sqlconnection.cursor()
    if sqlconnection:
        print('Data base connect ok!')
    sqlconnection.execute('CREATE TABLE IF NOT EXISTS profile(img TEXT, idchat INT, name TEXT, age TEXT, gender TEXT)')
    sqlconnection.commit()

# Добавление в базу нового пользователя
async def sql_add_profile (state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO profile VALUES(?, ?, ?, ?, ?)', tuple(data.values()))
        sqlconnection.commit()
# Чтение из базы короткого профиля
async def sql_read():
    res_table = cur.execute('SELECT * FROM profile').fetchall()
    return res_table
