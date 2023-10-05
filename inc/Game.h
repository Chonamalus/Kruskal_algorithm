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
  
    const int screenWidth = 800;
    const int screenHeight = 600;
    const char *screenTitle = "My first RAYLIB program!";
    const int FPS = 60;
    const Color initBackground = BLACK;
    int ball_x = 100;
    int ball_y = 100;
    int ball_speed_x = 5;
    int ball_speed_y = 5;
    int ball_radius = 15;

  private:
    static void shutRaylibUp(int /*logType*/, const char *text, va_list args);
};