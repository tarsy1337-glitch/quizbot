# Работа с гит

```sh
git init  # инициализировать гит репозиторий

git remote add origin <URL>  # установить удаленный репозиторий на имя origin
git remote set-url origin <URL>  # установить ссылку на определенный ремоут(например заменить ссылку для origin) 

git add <FILES>  # добавить файлы в stage для коммита 
git commit -m "COMMENT"  # закоммитить изменения из стейджа

git push -u origin main  # первый пуш ветки в удаленный репозиторий
git push  # последующие пуши коммитов ветки в удаленный репозиторий
```

# Работа с виртуальном окружением Python

```sh
python3 -m venv .venv  # создать виртуальное окружение в папке .venv

# активация виртуального окружения
.venv\Scripts\activate.ps1  # Windows PowerShell
.venv\Scripts\activate.bat  # Windows CMD
source .venv/bin/activate  # Unix-like(Linux, MacOS)

# Установка пакетов
pip install PyTelegramBotAPI dotenv
```