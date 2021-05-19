#Makefile for codeforces C++ compilation

CC := g++
CPPFLAGS := -g -Wall -Wshadow -fconcepts -std=c++17
LOCAL_FLAGS := -DLOCAL
SRCS := $(wildcard *.cpp)
OBJS := $(SRCS:%.cpp=%)
OBJSF := $(SRCS:%.cpp=%.f)
SRCDIR := src
BINDIR := bin

all: $(OBJS) $(OBJSF)

final: $(OBJSF)

# FINAL
%.f: %.cpp
	@echo "Compile final ..."
	$(CC) $(CPPFLAGS) $(@:%.f=%).cpp -o $(@:%.f=%)

# LOCAL
%: %.cpp
	@echo "Compile ..."
	$(CC) $(CPPFLAGS) $(LOCAL_FLAGS) $@.cpp -o $@

generate: a.cpp
	for i in b.cpp c.cpp d.cpp e.cpp f.cpp; do \
		echo $$i; \
		cp a.cpp $$i; \
	done

.PHONY: clean
clean:
	rm -f $(OBJS) $(OBJSF)
