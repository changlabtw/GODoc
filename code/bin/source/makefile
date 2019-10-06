.KEEP_STAT:

all: psssm2tfpssm

Compiler	= g++-5
#FLAGS		= -Wall -fopenmp -D NDEBUG -O2 -I/soft/general/gsl-1.12/include/ -L/soft/general/gsl-1.12/lib/
FLAGS		= -Wall -fopenmp -D NDEBUG -O2
LIB		= -lgsl -lgslcblas -lm

OBJECT4psssm2tfpssm	= pssm2tfpssm.o term.o pssm.o

psssm2tfpssm:	$(OBJECT4psssm2tfpssm)
			$(Compiler) $(FLAGS) $(OBJECT4psssm2tfpssm) -o pssm2tfpssm $(LIB)
			mv -f pssm2tfpssm ../.

%.o:		%.cpp
			$(Compiler) $(FLAGS) -c $<

clean:
			rm -f *.o
