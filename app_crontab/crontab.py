import schedule
import time
from mailing.services import start_mailing


def schedule_mailing():
    """Функция для автоматической отправки рассылки"""
    start_mailing()


# Определите расписание для отправки рассылок
schedule.every().hour.do(schedule_mailing)


# Запускайте планировщик в отдельном потоке
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Запустите планировщик
if __name__ == "__main__":
    run_scheduler()
