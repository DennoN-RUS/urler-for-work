# coding: utf-8
import logging

# Проверка результата запроса
def check_request(r):
    logging.debug("url: {}".format(r.url))
    if not r.ok:
        logging.error(r.text)
        exit (1)
