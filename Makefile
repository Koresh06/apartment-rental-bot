# Переменные
PYTHON_CMD = python
FASTAPI_APP = app.main:app
MAIN_MODULE = app.__main__

# Запуск FastAPI
start_fastapi:
	$(PYTHON_CMD) -m uvicorn $(FASTAPI_APP) --reload

# Запуск бота и FastAPI из __main__.py
start_bot:
	$(PYTHON_CMD) -m $(MAIN_MODULE)

# Запуск обоих приложений (через __main__.py)
start_all:
	$(MAKE) start_bot