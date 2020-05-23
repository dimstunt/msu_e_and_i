# -*- coding: utf-8 -*-
__author__ = 'dimstunt'

import requests
from stem import Signal
from stem.control import Controller
import time


class ConnectionManager:
    def __init__(self, count_of_requests=50):
        self.new_ip = "0.0.0.0"
        self.old_ip = "0.0.0.0"
        self.proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/49.0.2623.87 Safari/537.36'
        }
        self.request_counter = 0
        self.count_of_requests = count_of_requests

    def _change_ip(self):
        self.old_ip = self.new_ip
        self.request_counter = 0
        tries = 0
        with Controller.from_port(port=9051) as controller:
            while self.old_ip == self.new_ip:
                print("Changing IP: {tires} try".format(tires=tries + 1))
                if tries != 0:
                    time.sleep(2)
                controller.authenticate(password='dimstunt_local')
                # print("Success!")
                controller.signal(Signal.NEWNYM)
                # print("New Tor connection processed")
                controller.close()
                self.new_ip = requests.get("http://icanhazip.com", headers=headers, proxies=proxies).text.strip()
                tries += 1
            print("Success, total {tries} tries".format(tries=tries))

    def request(self, url):
        if self.new_ip == "0.0.0.0":
            self.new_ip = requests.get("http://icanhazip.com", headers=headers, proxies=proxies).text.strip()
        if self.request_counter >= self.count_of_requests:
            print("Count of requests: {count}, changing IP".format(count=self.request_counter))
            self._change_ip()
        # http = requests.get(url, headers=headers, proxies=proxies)
        tries = 1
        while (
                (http := requests.get(url, headers=headers, proxies=proxies)).status_code != 200
                or (tries == 5)
        ):
            print("Get status_code={error}, {tries} try to solve by changing IP".format(error=http.status_code, tries=tries))
            self._change_ip()
            self.request_counter = 0
            tries += 1
        self.request_counter += 1
        return http


proxies = {'http': 'socks5://localhost:9050', 'https': 'socks5://localhost:9050'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/49.0.2623.87 Safari/537.36'
}
# r = requests.get('https://shikimori.one/animes/page/1', headers=headers, proxies=proxies)
# html = BeautifulSoup(r.content, 'html.parser')
# for el in html.select('.title'):
#     title_en = el.select_one('.name-en').text
#     title_ru = el.select_one('.name-ru')['data-text']
#     href = ''.join(['https://shikimori.one', el['href']])
#     print(title_en, title_ru, href)

# print(json.loads(requests.get("http://httpbin.org/ip", headers=headers, proxies=proxies).text)['origin'])
# time.sleep(5)
# # Connector.change_ip()
# print(json.loads(requests.get("http://httpbin.org/ip", headers=headers, proxies=proxies).text)['origin'])
# print(json.loads(requests.get("http://httpbin.org/ip").text)['origin'])

# # -*- coding: utf-8 -*-
# __author__ = 'dimstunt'
#
# import requests
# from bs4 import BeautifulSoup
# from stem import Signal
# import time
# from stem.control import Controller
#
#
# class ConnectionManager:
#     def __init__(self):
#         self.new_ip = "0.0.0.0"
#         self.old_ip = "0.0.0.0"
#         self.new_identity()
#
#     @classmethod
#     def _get_connection(cls):
#         """
#         TOR new connection
#         """
#         with Controller.from_port(port=9051) as controller:
#             controller.authenticate(password="dimstunt_local")
#             controller.signal(Signal.NEWNYM)
#             controller.close()
#
#     @classmethod
#     def _set_url_proxy(cls):
#         """
#         Request to URL through local proxy
#         """
#         proxy_support = urllib2.ProxyHandler({"http": "127.0.0.1:8118"})
#         opener = urllib2.build_opener(proxy_support)
#         urllib2.install_opener(opener)
#
#     @classmethod
#     def request(cls, url):
#         """
#         TOR communication through local proxy
#         :param url: web page to parser
#         :return: request
#         """
#         cls._set_url_proxy()
#         request = urllib2.Request(url, None, {
#             'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) "
#                           "AppleWebKit/535.11 (KHTML, like Gecko) "
#                           "Ubuntu/10.10 Chromium/17.0.963.65 "
#                           "Chrome/17.0.963.65 Safari/535.11"})
#         request = urllib2.urlopen(request)
#         return request
#
#     def new_identity(self):
#         """
#         new connection with new IP
#         """
#         # First Connection
#         if self.new_ip == "0.0.0.0":
#             self._get_connection()
#             self.new_ip = self.request("http://icanhazip.com/").read()
#         else:
#             self.old_ip = self.new_ip
#             self._get_connection()
#             self.new_ip = self.request("http://icanhazip.com/").read()
#
#         seg = 0
#
#         # If we get the same ip, we'll wait 5 seconds to request a new IP
#         while self.old_ip == self.new_ip:
#             time.sleep(5)
#             seg += 5
#             print("Waiting to obtain new IP: %s Seconds" % seg)
#             self.new_ip = self.request("http://icanhazip.com/").read()
#
#         print("New connection with IP: %s" % self.new_ip)
#     def renew_connection(self):
#         with Controller.from_port(port=9051) as controller:
#             controller.authenticate(password="dimstunt_local")
#             controller.signal(Signal.NEWNYM)
#         session = requests.session()
#         # Tor uses the 9050 port as the default socks port
#         session.proxies = {'http': 'socks5://127.0.0.1:9050',
#                            'https': 'socks5://127.0.0.1:9050'}
#         session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                                          'Chrome/49.0.2623.87 Safari/537.36'
#                            }
#         return session
#
# # oldIP = "0.0.0.0"
# # newIP = "0.0.0.0"
# #
# # session = renew_connection()
# # print(session.get("http://httpbin.org/ip").text)
# # session = renew_connection()
# # print(session.get("http://httpbin.org/ip").text)
# # session = renew_connection()
# # print(session.get("http://httpbin.org/ip").text)
# # print(requests.get("http://httpbin.org/ip").text)
