# AISingers

[![PyPI version](https://badge.fury.io/py/ultimate-rvc.svg)](https://badge.fury.io/py/ultimate-rvc)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/varaslaw/ultimate-rvc/blob/main/notebooks/ultimate_rvc_colab_ru.ipynb)
[![Discord Server](https://dcbadge.limes.pink/api/server/https://discord.gg/T4ejEz8HtX?style=flat&compact=true&theme=default-inverted)](https://discord.gg/https://discord.gg/T4ejEz8HtX)
[![Open In Huggingface](https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/JackismyShephard/ultimate-rvc)

AISingers — русифицированный инструмент для создания AI-каверов и TTS-озвучки на базе Ultimate RVC. Это расширение [AiCoverGen](https://github.com/SociallyIneptWeeb/AICoverGen) с улучшенным качеством конверсии голоса, RMVPE и другими методами извлечения высоты, поддержкой кастомных эмбеддеров и удобным веб-интерфейсом на Gradio.

![AISingers](images/webui_generate.png?raw=true)

## Обзор

* Готовые скрипты запуска для Windows и Debian/Ubuntu.
* Улучшенное качество и скорость конверсии голоса, опции автотюна, шумоподавления и гибкой работы с высотой тона.
* RMVPE и альтернативные алгоритмы извлечения высоты — лучший выбор по точности для большинства задач.
* Работа с моделями для генерации: каталог, скачивание по ссылке, загрузка собственных весов и удаление.
* Поддержка TTS через Edge TTS и конверсия полученной речи в выбранный голос.
* Режим «в один клик» и «по шагам» с просмотром промежуточных аудио.
* Сохранение/загрузка конфигураций интерфейса и кэш промежуточных файлов для ускорения.

## Где попробовать

* **Google Colab**: русифицированный блокнот с быстрым стартом. [Открыть](https://colab.research.google.com/github/varaslaw/ultimate-rvc/blob/main/notebooks/ultimate_rvc_colab_ru.ipynb).
* **Hugging Face Spaces**: веб-версия без GPU-ускорения. [Перейти](https://huggingface.co/spaces/JackismyShephard/ultimate-rvc).

Если у вас достаточно VRAM на NVIDIA GPU, лучше запускать локально — так быстрее и стабильнее.

## Локальный запуск

Поддерживаются Windows и Debian/Ubuntu (22.04/24.04). Команды для Windows выполняйте в **PowerShell**, для Linux — в **bash**.

### Windows: установка в два клика

Для обычного пользователя ручная установка Python и Git не требуется:

1. Скачайте ZIP проекта и полностью распакуйте его в отдельную папку.
2. Запустите `1_УСТАНОВИТЬ_AISingers.bat` и дождитесь завершения.
3. Запускайте студию через `2_ЗАПУСТИТЬ_AISingers.bat`.

Установщик скачает локальный Python 3.12, создаст изолированное окружение и
установит CUDA-версию PyTorch. Системный Python пользователя не изменяется.
Дополнительные кнопки позволяют безопасно обновить проект и создать отчёт
диагностики. Рекомендуется NVIDIA GPU и не менее 15 ГБ свободного места.

### 1. Установите Git
[Инструкция](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

### 2. (Windows) Разрешите выполнение скриптов

```console
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Клонируйте репозиторий

```console
git clone https://github.com/varaslaw/ultimate-rvc
cd ultimate-rvc
```

### 4. Установите зависимости

```console
./urvc install
```

На Linux при необходимости автоматически поставится CUDA 12.8. Если возникнут проблемы — установите CUDA вручную.

### 5. Запустите веб-интерфейс

```console
./urvc run
```

После сообщения `Running on local URL:  http://127.0.0.1:7860` откройте ссылку в браузере.

### 6. Обновление

```console
./urvc update
```

### 7. Режим разработки

```console
./urvc dev
```

Включает горячую перезагрузку при изменении кода.

## Как пользоваться

### Загрузка/выгрузка моделей

На вкладке **Модели → Скачать** выберите публичную модель или вставьте ссылку на zip с весами (`.pth` и опционально `.index`).

На вкладке **Модели → Загрузить** отправьте свои веса/архив и задайте имя. После успешного сообщения модель появится в выпадающих списках в разделе генерации.

### Генерация каверов

* Выберите **тип источника** (ссылка YouTube или локальный файл) и задайте **источник**.
* Укажите **голосовую модель**.
* При необходимости раскройте **Настройки** и настройте высоту, шумоподавление, автотюн, RMVPE и др.
* Нажмите **Сгенерировать** — готовый кавер и промежуточные стемы появятся ниже.

### Озвучка (TTS → RVC)

* Введите текст или загрузите `.txt`.
* Выберите голос Edge TTS, при желании сдвиньте высоту/скорость/громкость.
* Настройте конверсию (RMVPE, индексация, автотюн) и нажмите **Сгенерировать**.

## Пакет PyPI

Установите с поддержкой CUDA в окружении Python 3.12–3.13:

```console
pip install ultimate-rvc[cuda] --extra-index-url https://download.pytorch.org/whl/cu128
```

Команды CLI:

* `urvc` — генерация каверов из терминала.
* `urvc-web` — запуск веб-интерфейса AISingers.

## Переменные окружения

* `URVC_CONSOLE_LOG_LEVEL` — уровень логов в консоль (по умолчанию `ERROR`).
* `URVC_FILE_LOG_LEVEL` — уровень логов в файлы (по умолчанию `INFO`).
* `URVC_LOGS_DIR` — папка с логами (по умолчанию `./logs`).
* `URVC_MODELS_DIR` — папка моделей (по умолчанию `./models`).
* `URVC_AUDIO_DIR` — папка аудио (по умолчанию `./audio`).
* `URVC_TEMP_DIR` — временные файлы (по умолчанию `./temp`).
* `URVC_CONFIG_DIR` — конфигурации UI (по умолчанию `./configs`).
* `URVC_VOICE_MODELS_DIR` — директория голосовых моделей (по умолчанию `voice_models` внутри `URVC_MODELS_DIR`).
* `YT_COOKIEFILE` — путь к cookies для загрузки с YouTube.
* `URVC_ACCELERATOR` — `cuda` или `rocm` (по умолчанию `cuda`).
* `URVC_CONFIG` — имя конфигурации UI для автозагрузки.
* `NODE_PATH` — путь к кастомному Node.js для веб-интерфейса и загрузки из YouTube.

## Сообщество и поддержка

Наш Discord: [https://discord.gg/T4ejEz8HtX](https://discord.gg/T4ejEz8HtX). О проблемах и предложениях сообщайте через Issues или Discussions на GitHub.

## Ограничения и правила

Запрещено использовать конвертированные голоса для:

* оскорблений и атак на людей;
* политической/религиозной пропаганды;
* публикации шокирующего контента без соответствующей маркировки;
* продажи моделей/клипов;
* выдачи себя за владельцев голоса с целью причинить вред;
* мошенничества и кражи личности.

## Дисклеймер

Автор проекта не несёт ответственности за любые прямые или косвенные убытки, связанные с использованием или невозможностью использования программного обеспечения.
