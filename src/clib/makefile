CC = gcc
PYTHON_INCLUDE = -I$(USERPROFILE)\AppData\Local\Programs\Python\Python313\include
PYTHON_LIB = -L$(USERPROFILE)\AppData\Local\Programs\Python\Python313\libs -lpython313

LDFLAGS = $(PYTHON_LIB)
CFLAGS = -Wall -shared -O2 -fPIC $(PYTHON_INCLUDE)

# Determine platform-specific extension
ifeq ($(OS),Windows_NT)
    EXT = .pyd
else
    EXT = .so
endif

TARGET = recycle_api$(EXT)
SRC = recycle-api.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	del -f *.o *.pyd
