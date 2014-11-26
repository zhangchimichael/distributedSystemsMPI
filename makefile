all: test

test:
	chmod a+x test_script.sh
	./test_script.sh

clean:
	rm -rf *.pyc
	rm -rf *.txt