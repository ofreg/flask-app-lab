import sqlite3

# Підключення до бази даних
conn = sqlite3.connect('instance/data.sqlite')
cursor = conn.cursor()

# Виконання SQL-команди для видалення таблиці
cursor.execute("DROP TABLE IF EXISTS _alembic_tmp_users;")

# Збереження змін та закриття з'єднання
conn.commit()
conn.close()
