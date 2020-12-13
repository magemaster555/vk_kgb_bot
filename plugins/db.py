import mariadb

conn = mariadb.connect(
    user="mabrikos",
    password="HNqR5nWG7NtlUK9W",
    host="localhost",
    database="vkbot"
)
conn.autocommit = True

cur = conn.cursor()
def exec(str):
    try:
        cur.execute(str)
        return cur
    except mariadb.Error as e:
        print(e)
        #vk_api("messages.send", peer_id= 218999719, message= f"Критическая ошибка при попытке запроса к бд:\n{e}")
        #vk.vk_r("messages.send", {"peer_id": 134918391, "random_id": random.randint(100, 10000), "message": f"Критическая ошибка при попытке запроса к бд. {e}"})