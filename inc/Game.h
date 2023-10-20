#pragma once
#include <fstream>
#include <iostream>
#include <raylib.h>

class Game {
  public:
    Game();
    ~Game();

    void Tick();

  private:
    // Windows parameters
    const int screenWidth = 800;
    const int screenHeight = 600;
    const char *screenTitle = "My first RAYLIB program!";
    const int FPS = 60;
    const Color initBackground = BLACK;

  private:
    static const bool shutMyRaylib = true;
    static void shutRaylibUp(int /*logType*/, const char *text, va_list args);
};