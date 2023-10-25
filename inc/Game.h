#pragma once
#include "parameters.h"
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
    static const int screenWidth;
    static const int screenHeight;
    static const char *screenTitle;
    static const int FPS;
    static const Color initBackground;

  private:
    static const bool shutMyRaylib = true;
    static void shutRaylibUp(int /*logType*/, const char *text, va_list args);
};