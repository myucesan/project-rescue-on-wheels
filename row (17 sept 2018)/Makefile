CC=gcc
CCFLAGS=-Wall -Werror -g -I/usr/local/include


LD_LIBS= -lwiringPi -lwiringPiDev -lpthread -lm  
LD_FLAGS=-L/usr/local/lib


OUTDIR=.

all:  pr 

%:    %.c 
	$(CC) $(CCFLAGS) $(LD_FLAGS) $(LD_LIBS)  -o $(OUTDIR)/$@ $<  		


 
