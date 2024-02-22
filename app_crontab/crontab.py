
from mailing.management.commands.start_mailing import Command



def schedule_mailing():
    """Функция для автоматической отправки рассылки"""

    Command().start_mailing()


