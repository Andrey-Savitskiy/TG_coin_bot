import sqlite3


def insert(value: str):
    sql = f"""
        INSERT INTO user(password) VALUES ('{value}');
        """
    db = sqlite3.connect('sqlite.db')
    db.execute(sql)
    db.commit()
    db.close()


def main():
    with open('pass.txt', 'r', encoding='utf-8') as file:
        for password in file.read().split('\n'):
            insert(password)

    print('Пароли добавлены!')


if __name__ == '__main__':
    main()
