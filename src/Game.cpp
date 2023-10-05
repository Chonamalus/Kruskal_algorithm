#include <Game.h>

Game::Game() {
    // Shut Raylib up in the terminal
    SetTraceLogCallback(shutRaylibUp);
    std::cout << "Raylib is shut" << std::endl;
    // Start the game window
    InitWindow(this->screenWidth, this->screenHeight, this->screenTitle);
    SetTargetFPS(this->FPS);
    std::cout << "Window is started" << std::endl;
}

Game::~Game() {
    CloseWindow();
    std::cout << "Window is closed" << std::endl;
}

void Game::Tick() {
    BeginDrawing();
    ClearBackground(this->initBackground);
    ball_x += ball_speed_x;
    ball_y += ball_speed_y;

    if (ball_x + ball_radius >= screenWidth || ball_x - ball_radius <= 0) {
        ball_speed_x *= -1;
    }

    if (ball_y + ball_radius >= screenHeight || ball_y - ball_radius <= 0) {
        ball_speed_y *= -1;
    }

    DrawCircle(ball_x, ball_y, ball_radius, WHITE);
    EndDrawing();
}

void Game::shutRaylibUp(int /*logType*/, const char *text, va_list args) {
    static std::ofstream logFile(
        "bin/raylib_log.txt",
        std::ios_base::app); // Open the log file in append mode

    if (logFile.is_open()) {
        char buffer[1024];
        vsnprintf(buffer, sizeof(buffer), text,
                  args);   // Format the log message
        logFile << buffer; // Write the log message to the log file
        logFile
            .flush(); // Flush the stream to ensure data is written immediately
    }
}