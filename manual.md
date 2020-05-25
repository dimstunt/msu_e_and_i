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
    * `virtualenv venv`
    * `source ./venv/bin/activate`
    * `pip install -r requiments.txt`
    * `pip install 'requests[socks]'`
* Установить `apache-spark`
    * `brew cask install homebrew/cask-versions/adoptopenjdk8`
    * `brew install apache-spark`
