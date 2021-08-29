"""
Отдельный модуль с набором параметров для ArgumentationTool.

Подробнее о параметрах:
https://docs.python.org/3/library/argparse.html#the-add-argument-method
https://pypi.org/project/ConfigArgParse/
"""
from pathlib import Path

from codestyle import __version__ as application_version
from codestyle.tool_wrappers import (Flake8, HTMLCS,
                                     Stylelint, TOOL_SETTINGS_PATH,
                                     MyPy, Black, Hadolint, AnsibleLint)

PARAMETERS: tuple = (
    (
        ('target',),
        {
            'metavar': 'target',
            'type': Path,
            'nargs': '+',
            'help': 'Путь до проверяемых файлов или директорий',
        },
    ),
    (
        ('-f', '--fix'),
        {
            'dest': 'fix',
            'action': 'store_true',
            'help': 'Исправить ошибки по возможности',
        },
    ),
    (
        ('-c', '--compact'),
        {
            'dest': 'compact',
            'action': 'store_true',
            'help': 'Включить компактный вывод процесса работы приложения',
        },
    ),
    (
        ('-q', '--quiet'),
        {
            'dest': 'quiet',
            'action': 'store_true',
            'help': 'Включить тихий режим работы приложения '
            '(показывать только ошибки)',
        },
    ),
    (
        ('-d', '--debug'),
        {
            'dest': 'debug',
            'action': 'store_true',
            'help': 'Включить режим отладки',
        },
    ),
    (
        ('-s', '--settings'),
        {
            'dest': 'settings',
            'type': Path,
            'default': TOOL_SETTINGS_PATH,
            'help': 'Путь до директории с настройками инструментов '
            f'(по умолчанию: {TOOL_SETTINGS_PATH})',
        },
    ),
    (
        ('--file_suffix',),
        {
            'dest': 'file_suffix',
            'metavar': '<file suffix>',
            'help': 'Проверяемое расширение файлов (.py, .js и так '
            'далее; по-умолчанию: все расширения)',
        },
    ),
    (
        ('-x', '--exclude'),
        {
            'dest': 'exclude',
            'metavar': '<globbing шаблон>',
            'help': 'Исключить по указанному globbing шаблону',
            'nargs': '+',
            'default': (),
        },
    ),
    (
        ('--stylelint-configuration_name',),
        {
            'dest': 'stylelint_configuration',
            'default': Stylelint.configuration_file_name,
            'help': 'Имя файла конфигурации для stylelint утилиты '
            '(по-умолчанию: '
            f'{Stylelint.configuration_file_name})',
        },
    ),
    (
        ('--flake8-configuration_name',),
        {
            'dest': 'flake8_configuration',
            'default': Flake8.configuration_file_name,
            'help': 'Имя файла конфигурации для flake8 утилиты '
            '(по-умолчанию: '
            f'{Flake8.configuration_file_name})',
        },
    ),
    (
        ('-al', '--ansible-lint'),
        {
            'dest': AnsibleLint.optional_flag,
            'action': 'store_true',
            'help': 'Имя файла конфигурации для ansible-lint утилиты '
                    '(по-умолчанию: '
                    f'{AnsibleLint.configuration_file_name})',
        },
    ),
    (
        ('-m', '--mypy'),
        {
            'dest': MyPy.optional_flag,
            'action': 'store_true',
            'help': 'Имя файла конфигурации для mypy утилиты '
                    '(по-умолчанию: '
                    f'{MyPy.configuration_file_name})',
        },
    ),
    (
        ('-hl', '--hadolint'),
        {
            'dest': Hadolint.optional_flag,
            'action': 'store_true',
            'help': 'Имя файла конфигурации для hadolint утилиты '
                    '(по-умолчанию: '
                    f'{Hadolint.configuration_file_name})',
        },
    ),
    (
        ('-b', '--black'),
        {
            'dest': Black.optional_flag,
            'action': 'store_true',
            'help': 'Имя файла конфигурации для mypy утилиты '
                    '(по-умолчанию: '
                    f'{Black.configuration_file_name})',
        },
    ),
    (
        ('--htmlcs-configuration_name',),
        {
            'dest': 'htmlcs_configuration',
            'default': HTMLCS.configuration_file_name,
            'help': 'Имя файла конфигурации для htmlcs утилиты '
            '(по-умолчанию: '
            f'{HTMLCS.configuration_file_name})',
        },
    ),
    (
        ('-v', '--version'),
        {'action': 'version', 'version': application_version},
    ),
)
