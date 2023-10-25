#pragma once
#include "parameters.h"
#include <iostream>
#include <raylib.h>

class Cell {
  public:
    Cell();
    ~Cell();

    void setCellColor(Color m_cellColor);
    void setCoordinates(std::pair<int, int> m_position);

    virtual void drawCell() = 0;

  protected:
    // Initialized and fixed attributes
    Color cellColor;
    static const int cellSize;
    static const int wallThickness;
    std::pair<int, int> position;
};