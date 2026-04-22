# Инструкция по настройке окружения для лабораторной работы BigARTM

---

## Краткое содержание

BigARTM — мощная библиотека для тематического моделирования, но она **не работает на Python 3.9+**.
Нам нужно создать изолированное виртуальное окружение с **Python 3.8**, установить туда BigARTM
и зарегистрировать его как ядро Jupyter.

---

## Шаг 1. Установите Python 3.8

BigARTM поддерживает Python до версии 3.8 включительно.

### Windows

1. Скачайте Python 3.8 с официального сайта:
   https://www.python.org/downloads/release/python-3813/
   → выбирайте **Windows installer (64-bit)**
2. При установке **обязательно отметьте**: `Add Python 3.8 to PATH`
3. Проверьте установку:
   ```
   py -3.8 --version
   ```

### macOS (через pyenv — рекомендуется)

```bash
# 1. Установите pyenv
brew install pyenv

# 2. Установите Python 3.8
pyenv install 3.8.18

# 3. Проверка
pyenv versions
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y python3.8 python3.8-venv python3.8-dev
python3.8 --version
```

---

## Шаг 2. Создайте виртуальное окружение

Откройте терминал / командную строку и перейдите в папку проекта:

```bash
cd /путь/к/вашей/папке
```

### Windows

```bat
py -3.10 -m venv bigartm_env
bigartm_env\Scripts\activate
```

### macOS / Linux

```bash
python3.8 -m venv bigartm_env
source bigartm_env/bin/activate
```

После активации в начале строки терминала появится `(bigartm_env)`.

---

## Шаг 3. Установите зависимости

Убедитесь, что окружение активировано, затем выполните:

```bash
# Обновить pip
pip install --upgrade pip

# Основные зависимости
pip install numpy==1.23.5
pip install scipy==1.9.3
pip install pandas==1.5.3
pip install pyarrow==11.0.0
pip install scikit-learn==1.2.2
pip install matplotlib==3.7.1
pip install tqdm

# Для обработки русского текста
pip install pymorphy2==0.9.1
pip install nltk

# Jupyter
pip install jupyter ipykernel
```

---

## Шаг 4. Установите BigARTM

BigARTM устанавливается через pip — для Windows и Linux есть готовые wheel-файлы.

### Вариант A — pip (самый простой, рекомендуется)

```bash
pip install bigartm
```

> Если команда выше не работает — см. Вариант Б.

### Вариант Б — готовый wheel с GitHub

Скачайте wheel для вашей платформы со страницы релизов BigARTM:
https://github.com/bigartm/bigartm/releases

Установите командой:

```bash
# Пример для Windows 64-bit Python 3.8:
pip install bigartm-0.10.0-cp38-cp38-win_amd64.whl

# Пример для Linux:
pip install bigartm-0.10.0-cp38-cp38-linux_x86_64.whl
```

### Вариант В — через conda (альтернатива)

Если у вас установлена Anaconda/Miniconda:

```bash
# Создать окружение с Python 3.8
conda create -n bigartm_env python=3.8
conda activate bigartm_env

# Установить BigARTM из conda-forge
conda install -c conda-forge bigartm

# Дополнительные пакеты
pip install pymorphy2 tqdm pyarrow
```

### Проверка установки BigARTM

```bash
python -c "import artm; print('BigARTM version:', artm.version())"
```

---

## Шаг 5. Зарегистрируйте окружение как ядро Jupyter

```bash
# Окружение должно быть активировано!
python -m ipykernel install --user --name=bigartm_env --display-name="Python 3.8 (BigARTM)"
```

---

## Шаг 6. Запустите Jupyter и откройте ноутбук

```bash
jupyter notebook
```

1. В браузере откроется Jupyter.
2. Откройте файл `bigartm_lab.ipynb`.
3. В меню **Kernel → Change kernel** выберите **"Python 3.8 (BigARTM)"**.
4. Запускайте ячейки последовательно: **Shift+Enter**.

---

## Шаг 7. Скачайте данные (если не скачались автоматически)

Ноутбук сам скачает данные через `urllib`, но если нет интернета или скачивание
зависло — скачайте вручную:

- **Обучающая выборка** → сохранить как `train_0000.parquet`  
  https://huggingface.co/datasets/mlsum/resolve/refs%2Fconvert%2Fparquet/ru/train/0000.parquet?download=true

- **Тестовая выборка** → сохранить как `test_0000.parquet`  
  https://huggingface.co/datasets/mlsum/resolve/refs%2Fconvert%2Fparquet/ru/test/0000.parquet?download=true

Оба файла должны лежать в **той же папке**, что и ноутбук `bigartm_lab.ipynb`.

---

## Возможные проблемы и решения

| Проблема | Решение |
|---|---|
| `ModuleNotFoundError: No module named 'artm'` | Убедитесь, что активировано окружение `bigartm_env`, а не системный Python |
| `ImportError: libartm.so not found` (Linux) | `export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH` или переустановите BigARTM |
| `DLL load failed` (Windows) | Установите Visual C++ Redistributable 2019: https://aka.ms/vs/16/release/vc_redist.x64.exe |
| Ядро умирает при импорте artm | Проверьте версию Python: `python --version` — должна быть 3.8.x |
| `pymorphy2` работает медленно | Это нормально — лемматизация 10 000 документов займёт 5–15 минут |
| Нет файлов parquet | Скачайте вручную по ссылкам выше, переименуйте как указано |
| `artm.version()` возвращает ошибку | Попробуйте: `conda install -c conda-forge bigartm` (Anaconda) |

---

## Структура файлов проекта

```
папка_проекта/
│
├── bigartm_lab.ipynb      ← Jupyter-ноутбук (основная работа)
├── SETUP_GUIDE.md         ← эта инструкция
├── train_0000.parquet     ← обучающая выборка (скачать)
├── test_0000.parquet      ← тестовая выборка (скачать)
│
├── batches_train/         ← создаётся автоматически (BigARTM батчи)
├── batches_test/          ← создаётся автоматически
│
└── bigartm_env/           ← виртуальное окружение Python 3.8
    └── ...
```

---

## Деактивация окружения

После окончания работы:

```bash
# Windows
bigartm_env\Scripts\deactivate

# macOS / Linux
deactivate
```
