# Makefile pentru Tema 2 - Simulare Ferma

CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++11
TARGET = ferma
INPUT = ferma.txt
OUTPUT = ferma.out

# Găsește automat toate fișierele .cpp din directorul curent
SOURCES = $(wildcard *.cpp)
OBJS = $(SOURCES:.cpp=.o)

.SILENT:

all: test-all

build: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Regulă generală pentru compilare .cpp -> .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f *.o $(TARGET) $(OUTPUT)

run: $(TARGET)
	./$(TARGET) $(INPUT) $(OUTPUT)

test: run
	python3 teste/scripturi/verifica.py $(INPUT) $(OUTPUT)

test-all: $(TARGET)
	python3 teste/scripturi/verifica.py all
	@if [ -f .test_results.txt ]; then \
		read TRECUTE TOTAL < .test_results.txt; \
		if [ -n "$$SERVER_IP" ]; then \
			python3 teste/scripturi/trimite_rezultate.py $$TRECUTE $$TOTAL "$$SERVER_IP"; \
		fi; \
		rm -f .test_results.txt; \
	fi

test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12 test13 test14 test15 test16 test17 test18: $(TARGET)
	python3 teste/scripturi/verifica.py $(subst test,,$@)

verify: $(TARGET)
	./$(TARGET) $(INPUT) $(OUTPUT)
	python3 teste/scripturi/verifica.py $(INPUT) $(OUTPUT)

key:
	@bash teste/scripturi/genereaza_key.sh

.PHONY: all clean run test test-all test1 test2 test3 test4 test5 test6 test7 test8 test9 test10 test11 test12 test13 test14 test15 test16 test17 test18 verify key

