import enum


class Status(enum.Enum):
    CREATED = "Создано"
    DONE = "Завершено"
    DELETED = "Удалено"


class Priority(enum.Enum):
    URGENT = "Срочно сделать"
    HIGH = "Важно сделать как можно быстрее"
    MEDIUM = "Необходимо сделать"
    LOW = "Не к спеху"
