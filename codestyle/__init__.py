"""
Инструмент проверки качества кода.

Является обёрткой над множеством уже готовых решений для разных языков.
Точка входа описана в модуле __main__.

Для добавления новых обёрток используется модуль tool_wrappers и
переменная ENABLED_TOOLS в модуле application.
"""
from pathlib import Path

FIRST_LINE_INDEX = FIRST_ELEMENT_INDEX = 0
APPLICATION_PATH = Path(__file__).parent.absolute()


def _read_first_line_documentation(documentation: str) -> str:
    """
    Чтение первой строки из указанной документации.

    :param documentation: Документация.
    :return: Первая строка документации.
    """
    empty_lines_filter = filter(None, documentation.splitlines())
    return list(empty_lines_filter)[FIRST_LINE_INDEX]
