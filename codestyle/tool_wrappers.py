"""
Набор обёрток для проверки качества кода.

Новые добавляются в константу ENABLED_TOOLS модуля application.
"""
from os import linesep
from pathlib import Path
from subprocess import PIPE, run  # noqa: S404
from typing import Sequence, Optional

from codestyle import APPLICATION_PATH
from codestyle.system_wrappers import ExitCodes, check_output

TOOL_SETTINGS_PATH = APPLICATION_PATH / 'tool_settings'


class Result:
    """Результат обработки файла."""

    def __init__(self, return_code: int, output: str = '', error: str = ''):
        """
        Создание результата обработки.

        :param return_code: Код работы программы.
        :param output: Результат работы.
        :param error: Результат работы в виде ошибки.
        """
        self.return_code = return_code
        self.output = output or ''
        self.error = error or ''
        self.is_success = self.return_code == ExitCodes.SUCCESS

    @property
    def whole_output(self) -> str:
        """Полный вывод работы используемой программы с ошибками."""
        return self.output + linesep if self.output else self.error


class ConsoleTool:
    """
    Класс для оборачивания (наследованием) консольной утилиты.

    Переменные класса ниже изменяют/расширяют поведение утилиты.
    """

    # Аргумент, передаваемый в командную строку для отображения описания
    # утилиты с набором доступным параметров.
    help_argument: str = '--help'

    # Аргумент командной строки для указания названия аргумента,
    # принимающего путь до конфигурации утилиты.
    configuration_argument: str = '--config'

    # Название конфигурационного файла.
    configuration_file_name: str = ''

    # Путь до директории, в которой располагается файл конфигурации.
    configuration_path: Optional[Path] = None

    # Дополнительные аргументы командной строки, необходимые для запуска
    # утилиты. Пример: ('--length', '79', '--skip-string-normalization')  # noqa: E800, E501
    extra_run_arguments: Sequence = ()

    # Название инструмента, которое будет использовано для его запуска
    # в командной строке; по-умолчанию - название класса в нижнем
    # начертании.
    cli_tool_name: str = ''

    # Суфиксы файлов (с точкой в начале), которые поддерживаются утилитой.
    supported_file_suffixes: tuple

    # Дополнительные аргументы командной строки, используемые для
    # исправления/форматирования файлов.
    fix_arguments: tuple = ()

    # Дополнительные аргументы командной строки, используемые для
    # проверки файлов.
    check_arguments: tuple = ()

    # Флаги ниже определяют возможности утилиты: переключение for_check
    # в True сообщает, утилита имеет возможность проверять файлы;
    # for_fix - для исправления/форматирования файлов.
    for_check: bool = False
    for_fix: bool = False

    # Флаг для выбора дополнительной проверки кода.
    optional_flag: str = ''
    optional = False

    def __init__(self, configuration_path: Path = None):
        """
        Проверка доступности приложения в запускаемой среде.

        :param configuration_path: путь до конфигурации приложения
        """
        if isinstance(configuration_path, Path):
            self.configuration_path = configuration_path

        check_output((self.get_name(), self.help_argument))

    @classmethod
    def get_name(cls) -> str:
        """Получение названия приложения с учётом cli_tool_name поля."""
        return cls.cli_tool_name if cls.cli_tool_name else cls.__name__.lower()

    def check(self, file_path: Path) -> Result:
        """Проверка файла по указанному пути."""
        return self._process_file(file_path, self.check_arguments)

    def fix(self, file_path: Path) -> Result:
        """Исправление файла по указанному пути."""
        return self._process_file(file_path, self.fix_arguments)

    def _get_extra_run_arguments(self) -> Sequence:
        """Дополнительные аргументы запуска приложения."""
        return self.extra_run_arguments if self.extra_run_arguments else ()

    def _process_file(self, file_path: Path, run_arguments: tuple) -> Result:
        """
        Обработка указанного файла.

        :param file_path: Путь до обрабатываемого файла.
        :param run_arguments: Аргументы запуска.
        :return: Результат обработки файла.
        """
        configuration = []
        if self.configuration_path and self.configuration_argument:
            configuration = [self.configuration_argument,
                             str(self.configuration_path)]

        completed_process = run(  # noqa: S603
            [self.get_name(), *configuration, *run_arguments,
             *self._get_extra_run_arguments(), file_path], stdout=PIPE,
            stderr=PIPE)
        return Result(completed_process.returncode,
                      output=completed_process.stdout.decode().rstrip(),
                      error=completed_process.stderr.decode().rstrip())


class Flake8(ConsoleTool):
    """
    flake8 утилита для проверки python кода.

    .. seealso:: https://gitlab.com/pycqa/flake8
    """

    configuration_file_name = 'flake8.conf'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.py',)
    for_check = True


class Autopep8(ConsoleTool):
    """
    autopep8 утилита для форматирования python кода.

    .. seealso:: https://github.com/hhatto/autopep8
    """

    configuration_argument = ''
    extra_run_arguments = ('--in-place', '--aggressive')
    supported_file_suffixes = ('.py',)
    for_fix = True


class Autoflake(ConsoleTool):
    """
    autoflake утилита для удаления неиспользуемых импортов в python.

    .. seealso:: https://github.com/myint/autoflake
    """

    configuration_argument = ''
    extra_run_arguments = ('--in-place', '--remove-unused-variables')
    supported_file_suffixes = ('.py',)
    for_fix = True


class MyPy(ConsoleTool):
    """
    Mypy утилита для проверки типов в python коде.

    .. seealso:: https://github.com/python/mypy
    """

    configuration_file_name = 'mypy.conf'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.py',)
    for_check = True
    optional = True
    optional_flag = 'mypy'


class Black(ConsoleTool):
    """
    Black утилита для форматирования python кода.

    .. seealso:: https://black.readthedocs.io/en/stable/
    """

    configuration_file_name = 'black.cfg'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.py',)
    for_fix = True
    optional = True
    optional_flag = 'black'


class ShellCheck(ConsoleTool):
    """
    ShellCheck утилита для проверки .sh файлов.

    Файл .shellcheckrc перемещается в root директорию контейнера
    .. seealso:: https://github.com/koalaman/shellcheck
    """

    configuration_argument = ''
    configuration_file_name = '.shellcheckrc'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.sh',)
    for_check = True


class Hadolint(ConsoleTool):
    """
    Hadolint утилита для проверки Dockerfile.

    Файл .hadolint.yaml перемещается в app директорию контейнера
    .. seealso:: https://github.com/hadolint/hadolint
    """

    configuration_argument = ''
    supported_file_suffixes = ('',)
    for_check = True
    optional = True
    optional_flag = 'hadolint'


class AnsibleLint(ConsoleTool):
    """
    ansible-lint утилита для проверки playbooks, roles and collections.

    .. seealso:: https://github.com/ansible-community/ansible-lint
    """

    configuration_argument = ''
    cli_tool_name = 'ansible-lint'
    configuration_file_name = '.ansible-lint'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.yaml', '.yml')
    for_check = True
    optional = True
    optional_flag = 'ansible-lint'


class HTMLCS(ConsoleTool):
    """
    Инструмент проверки и форматирования html файлов.

    .. seealso:: https://github.com/ecomfe/htmlcs
    """

    configuration_file_name = 'htmlcs.json'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    check_arguments = ('hint',)
    fix_arguments = ('format', '--in-place')
    supported_file_suffixes = ('.html',)
    for_check = True


class Stylelint(ConsoleTool):
    """
    Инструмент проверки и форматирования css-подобных языков.

    .. seealso:: https://stylelint.io
    """

    configuration_file_name = '.stylelintsrc.json'
    configuration_path = TOOL_SETTINGS_PATH / configuration_file_name
    supported_file_suffixes = ('.css', '.html', '.md', '.sass', '.scss',
                               '.less', '.sss')
    extra_run_arguments = ('--formatter=verbose',)
    fix_arguments = ('--fix',)
    for_check = True
    for_fix = True
