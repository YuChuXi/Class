cc=gcc

main: main.c
	cc main.c -o main.bin

clean:
	rm *.bin