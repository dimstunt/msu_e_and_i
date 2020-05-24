import ConnectionManager
import logging


def main():
    module_logger = logging.getLogger("ConnectionManager")
    module_logger.setLevel(logging.INFO)
    fh = logging.FileHandler("ConnectionManager.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    module_logger.addHandler(fh)
    module_logger.info(msg="Testing changing ip")
    cm = ConnectionManager.ConnectionManager(3)
    for i in range(15):
        module_logger.info(msg="{i} ip: {ip}".format(i=i, ip=cm.request("http://icanhazip.com/").text.strip()))


if __name__ == '__main__':
    main()
