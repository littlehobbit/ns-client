init:
	pip install -r requirements.txt

test:
	python3 -m unittest

res:
	pyrcc5 client/res/resources.qrc -o client/res/resources.py