

TESTS=../novos_testes/GOPR0002.MP4
.PHONY: $(TESTS)

all: $(TESTS)
	echo Tests OK

$(TESTS):
	python2 ready_for_contours.py $@ -q | diff - $@.out
