#include "Cell.h"

Cell::Cell() { std::cout << "Cell created" << std::endl; }

// Get the values from parameters.h
const int Cell::cellSize = cellSize;
const int Cell::wallThickness = wallThickness;

Cell::~Cell() { std::cout << "Cell killed" << std::endl; }

void Cell::setCellColor(Color m_cellColor) { cellColor = m_cellColor; }

void Cell::setCoordinates(std::pair<int, int> m_position) {
    position = m_position;
}