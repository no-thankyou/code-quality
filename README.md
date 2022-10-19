
Code Quality Checker
========================

Supports multiple languages (checks or fix):

-   Python (flake8, autopep8, autoflake, mypy, black)
-   CSS (stylelint)
-   HTML (htmlcs)
-   Bash (shellcheck)
-   Dockerfile (hadolint)
-   Ansible (ansible-lint)

Args
-------------------------------

 Arg | Description
--- | ---
`-h, --help` | Отобразить вспомогательное сообщение и завершить работу программы
`-f, --fix` | Исправить ошибки по возможности
`-c, --compact` | Включить компактный вывод процесса работы приложения
`-q, --quiet` | Включить тихий режим работы приложения (показывать только ошибки)
`-d, --debug` | Включить режим отладки
`-s SETTINGS, --settings SETTINGS` | Путь до директории с настройками инструментов (по умолчанию: ./tool_settings)
`--file_suffix <file_suffix>` | Проверяемое расширение файлов (.py, .js и так далее; по-умолчанию: все расширения)
`-m, --mypy` |  Опциональная проверка типизации при помощи mypy
`-b, --black` | Опциоанльное форматирование при помощи black, только после флага -f
`-hl, --hadolint` |  Опциональная проверка Dockerfile`ов, в файле .hadolint.yaml указать: ignored: - <номер ошибки>
`-al, --ansible-lint` |  Опциональная проверка Ansible playbooks и roles
`-x <globbing шаблон>, --exclude <globbing шаблон>` | Исключить по указанному globbing шаблону, для файла необходимо указывать список exclude = [file1, file2, ...]
`--stylelint-configuration_name STYLELINT_CONFIGURATION` | Имя файла конфигурации для stylelint утилиты (по-умолчанию: .stylelintsrc.json)
`--flake8-configuration_name FLAKE8_CONFIGURATION` | Имя файла конфигурации для flake8 утилиты (по-умолчанию: flake8.conf) В этом же файле пишется конфигурация darglint - линтер документации (игнорирование ошибки <ignore=номер_ошибки>)
`--htmlcs-configuration_name HTMLCS_CONFIGURATION` | Имя файла конфигурации для htmlcs утилиты (по-умолчанию: htmlcs.json
`-v, --version` | Отобразить версию приложения и завершить работу программы

Порядок использования консольных аргументов приложения
------------------------------------------------------

``` {.sourceCode .console}
codestyle [-h] [-f] [-c] [-q] [-d] [-s SETTINGS] [--file_suffix <file suffix>]
          [-x <globbing шаблон> [<globbing шаблон> ...]] 
          [--stylelint-configuration_name STYLELINT_CONFIGURATION]
          [--flake8-configuration_name FLAKE8_CONFIGURATION] [--htmlcs-configuration_name HTMLCS_CONFIGURATION]

```

### Использование в качестве устанавливаемого приложения

В процессе

#### Обновление документации для Sphinx (вне контейнера)

``` {.sourceCode .console}
python -m install sphinx
sphinx-apidoc --force --separate --no-toc --module-first --output-dir docs/pages codestyle codestyle/tool_settings
```
