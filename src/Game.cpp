#include "Game.h"

Game::Game() {
    // Shut Raylib up in the terminal
    SetTraceLogCallback(Game::shutRaylibUp);
    std::cout << "Raylib is shat" << std::endl;
    // Start the game window
    InitWindow(this->screenWidth, this->screenHeight, this->screenTitle);
    SetTargetFPS(this->FPS);
    std::cout << "Window is started" << std::endl;
}

// Get the values from parameters.h
const int Game::screenWidth = screenWidth;
const int Game::screenHeight = screenHeight;
const char *Game::screenTitle =
    screenTitle; // char* for the string, it is a pointer
const int Game::FPS = FPS;
const Color Game::initBackground = initBackground;

Game::~Game() {
    CloseWindow();
    std::cout << "Window is closed" << std::endl;
}

void Game::Tick() {
    BeginDrawing();
    ClearBackground(this->initBackground);

    DrawCircle(100, 100, 10, WHITE);

    EndDrawing();
}

void Game::shutRaylibUp(int /*logType*/, const char *text, va_list args) {
    if (shutMyRaylib) {
        /* Here the function do not output the rylib in terminal, or in logfile
         */
    } else {
        static std::ofstream logFile(
            "bin/raylib_log.txt",
            std::ios_base::app); // Open the log file in append mode

        if (logFile.is_open()) {
            char buffer[1024];
            vsnprintf(buffer, sizeof(buffer), text,
                      args);   // Format the log message
            logFile << buffer; // Write the log message to the log file
            logFile.flush();   // Flush the stream to ensure data is written
                               // immediately
        }
    }
}