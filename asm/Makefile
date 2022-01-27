SOURCES := $(wildcard *.c)
ASM := $(patsubst %.c, %.s, $(SOURCES))
OUT := $(patsubst %.c, %.out, $(SOURCES))

all: $(ASM) $(OUT)

%.s: %.c
	gcc -S -fverbose-asm $< -o $@

%.out: %.c
	gcc $< -o $@

clean:
	rm -rf *.s *.out