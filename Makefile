# Makefile for Raylib project

# Compiler and compiler flags
CC := g++
CFLAGS := -Wall -Wextra -std=c++17
LDFLAGS := -lraylib

# Directories
SRC_DIR := src
INC_DIR := inc
BUILD_DIR := bin

# Source files and object files
SRC_FILES := $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES := $(patsubst $(SRC_DIR)/%.cpp, $(BUILD_DIR)/%.o, $(SRC_FILES))

# Executable name
EXECUTABLE := $(BUILD_DIR)/my_program

# Main target: Build the executable and run the program
all: $(EXECUTABLE)
	@echo [MAKEFILE] Run...
	@./$(EXECUTABLE) 2> /dev/null  # Redirect stderr to /dev/null

$(EXECUTABLE): $(OBJ_FILES)
	@echo [MAKEFILE] Build...
	@$(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	@echo [MAKEFILE] Compile...
	@$(CC) $(CFLAGS) -I $(INC_DIR) -c $< -o $@

# Clean build files
clean:
	rm -rf $(BUILD_DIR)
