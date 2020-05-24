import ConnectionManager
import logging


def main():
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('log/main.log', mode='w')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(msg='Testing changing ip')
    cm = ConnectionManager.ConnectionManager(3)
    for i in range(15):
        logger.info(msg='{i} ip: {ip}'.format(i=i, ip=cm.request("http://icanhazip.com/").text.strip()))


if __name__ == '__main__':
    main()
