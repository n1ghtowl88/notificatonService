import datetime as dt
import django
import logging
from logging.handlers import RotatingFileHandler
import os
import time

import requests
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notificatonService.settings')
django.setup()
from api.models import Client, Mailing, Message


load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(f'{__file__}.log', maxBytes=50000, backupCount=5)
message_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(message_format)
logger.addHandler(handler)

TOKEN = os.getenv('TOKEN')
REQUEST_URL = f'https://probe.fbrq.cloud/v1/send/'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

REQUEST_PARAMETERS = ('\nПараметры запроса:'
                      '\nтип: POST,'
                      '\nURL: {url},'
                      '\njson: {json},'
                      '\nheaders: {headers}.')
NETWORK_FAILURE = ('Произошел сбой сети:\nОписание ошибки:\n{exception}'
                   + REQUEST_PARAMETERS)
ERROR = 'В запросе вернулась ошибка:\nОписание ошибки:\n{exception}'
REQUEST_ERROR = ERROR + REQUEST_PARAMETERS
JOB_STARTED = 'Джоба запущена'
SEND_MESSAGE = 'Будет отправлено сообщение' + REQUEST_PARAMETERS


def main():
    while True:
        try:
            logger.debug(JOB_STARTED)
            messages = Message.objects.filter(status='ready')
            for message in messages:
                mailing = Mailing.objects.get(id=message.mailing.id)
                current_time = dt.datetime.now().replace(
                    tzinfo=dt.timezone.utc)
                if current_time <= mailing.start_datetime:
                    continue
                if current_time >= mailing.end_datetime:
                    message.status = 'not_sent'
                else:
                    client = Client.objects.get(id=message.client.id)
                    phone_number = ''.join(['7',
                                            client.operator_code,
                                            client.msisdn])
                    request_details = dict(url=REQUEST_URL + str(message.id),
                                           headers=HEADERS,
                                           json={'id': message.id,
                                                 'phone': phone_number,
                                                 'text': mailing.text})
                    try:
                        logger.info(SEND_MESSAGE.format(**request_details))
                        response = requests.post(**request_details)
                        if (response.status_code == 200 and
                                response.json()['code'] == 0):
                            message.status = 'sent'
                        elif response.status_code == 400:
                            print(REQUEST_ERROR.format(exception='Ошибка 400',
                                                       **request_details))
                            message.status = 'failed'
                        else:
                            print(REQUEST_ERROR.format(exception=('Неожиданный'
                                                                  ' ответ'),
                                                       **request_details))
                            message.status = 'failed'
                    except (requests.ConnectionError,
                            requests.Timeout,
                            requests.HTTPError,
                            requests.TooManyRedirects) as exception:
                        print(NETWORK_FAILURE.format(exception=exception,
                                                     **request_details))
                        message.status = 'failed'
                        time.sleep(120)
                    except requests.JSONDecodeError as exception:
                        print(REQUEST_ERROR.format(exception=exception,
                                                   **request_details))
                        message.status = 'failed'

                message.datetime = current_time
                message.save()
            time.sleep(600)
        except Exception as error:
            logger.error(error, exc_info=True)
            time.sleep(600)


if __name__ == '__main__':
    main()
