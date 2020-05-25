# Подготовка к запуску
* Установить `tor`
    * `brew install tor`
* Добавить `controlport`
    * `cp /usr/local/etc/tor/torrc.sample /usr/local/etc/tor/torrc`
    * `sublime /usr/local/etc/tor/torrc`
    * Разкомментить `ControlPort` и `HashedControlPassword`
    * `tor --hash-password "dimstunt_local"`
    * полученный хеш скопировать вместо существующего в `HashedControlPassword`
* Создать виртуальное окружение
    * `python -m venv venv`
    * `source ./venv/bin/activate`
    * `pip install -r requiments.txt`
    * `pip install 'requests[socks]'`
