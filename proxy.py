import sqlite3
import random

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

conn = sqlite3.connect("proxy.db")
cs = conn.cursor()


def crawl():
    ua = UserAgent()

    cs.execute(
        """create table if not exists proxy(
		host varchar(20),
		port varchar(10),
		unique (host, port)
		)"""
    )

    headers = {"user-agent": ua.random}

    r = requests.get("http://cn-proxy.com/", headers=headers)

    if r.status_code == 200:
        print("crawl cn-proxy secessfully!")

    soup = BeautifulSoup(r.text, "lxml")

    for tbody in soup.find_all("tbody"):
        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")
            host = tds[0].text
            port = tds[1].text
            cs.execute(
                "insert or ignore into proxy (host, port) values (?, ?)", (host, port)
            )
            conn.commit()

    cs.close()
    conn.close()


def get():
    cs.execute("select * from proxy")
    record = random.choice(cs.fetchall())

    proxies = {
        "http": "{}:{}".format(record[0], record[1]),
        "https": "{}:{}".format(record[0], record[1]),
    }

    try:
        r = requests.get("https://processon.com/", proxies=proxies)
    except Exception:
        cs.execute("delete from proxy where host=?", (record[0],))
        conn.commit()
        return get()

    return proxies


if __name__ == "__main__":
    crawl()
