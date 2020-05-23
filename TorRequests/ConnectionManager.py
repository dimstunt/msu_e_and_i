# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

import requests
from stem import Signal
from stem.control import Controller
import time


class ConnectionManager:
    """
    Класс для создания запросов через tor
    """
    def __init__(self, count_of_requests=50):
        """
        Инициализирует сессию для отправки запросов через tor
        :param count_of_requests: количество запросов, после которого будет запрошен новый ip-адрес
        """
        self.__new_ip = "0.0.0.0"
        self.__old_ip = "0.0.0.0"
        self.__proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.87 Safari/537.36'
        }
        self.__request_counter = 0
        self.count_of_requests = count_of_requests

    def _check_ip(self):
        return requests.get("http://icanhazip.com", headers=self.__headers, proxies=self.__proxies).text.strip()

    def _change_ip(self):
        """
        Функция меняет ip-адрес
        Если не удается за 10 попыток, останавливается
        """
        self.__old_ip = self.__new_ip
        self.__request_counter = 0
        tries = 0
        with Controller.from_port(port=9051) as controller:
            while self.__old_ip == self.__new_ip and tries <= 10:
                # TODO добавить логгирование
                print("Changing IP: {tires} try".format(tires=tries + 1))
                if tries != 0:
                    time.sleep(2)
                controller.authenticate(password='dimstunt_local')
                # print("Success!")
                controller.signal(Signal.NEWNYM)
                # print("New Tor connection processed")
                controller.close()
                self.__new_ip = self._check_ip()
                tries += 1
            # TODO добавить обработку неудачи смены ip
            print("Success, total {tries} tries".format(tries=tries))

    def request(self, url):
        """
        Функция возвращает http-страницу в виде класса Response
        :param url: запрашиваемый URL, sting
        :return: класс Response
        """
        if self.__new_ip == "0.0.0.0":
            self.__new_ip = self._check_ip()
        if self.__request_counter >= self.count_of_requests:
            # TODO добавить логгирование
            print("Count of requests: {count}, changing IP".format(count=self.__request_counter))
            self._change_ip()
        tries = 1
        while (
                (http := requests.get(url, headers=self.__headers, proxies=self.__proxies)).status_code != 200
                or (tries == 5)
        ):
            # TODO добавить логгирование
            print("Get status_code={error}, {tries} try to solve by changing IP"
                  .format(error=http.status_code, tries=tries))
            self._change_ip()
            self.__request_counter = 0
            tries += 1
        self.__request_counter += 1
        return http
