# build python files from ui files

UI_FILES=$(wildcard *.ui)
PY_FILES=$(UI_FILES:%.ui=%.py)

all: $(PY_FILES)

%.py: %.ui
	pyuic4 -x $< -o $@

clean:
	rm -f $(PY_FILES)
