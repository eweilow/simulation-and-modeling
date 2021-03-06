#include <stdbool.h>
#include "../common/grid.c"

void relax(struct Grid *grid)
{
  double **curr = grid->currentGrid;

  for (unsigned long i = 1; i < grid->points - 1; ++i)
  {
    for (unsigned long j = 1; j < grid->points - 1; ++j)
    {
      grid->nextGrid[i][j] = 0.25 * (curr[i + 1][j] + curr[i - 1][j] + curr[i][j - 1] + curr[i][j + 1]);
    }
  }

  ++(grid->relaxations);

  copyNextIntoCurrentGrid(grid, grid->nextGrid, grid->currentGrid);
}

void relaxGaussSeidel(struct Grid *grid)
{
  double **curr = grid->currentGrid;

  for (unsigned long i = 1; i < grid->points - 1; ++i)
  {
    for (unsigned long j = 1; j < grid->points - 1; ++j)
    {
      curr[i][j] = 0.25 * (curr[i + 1][j] + curr[i - 1][j] + curr[i][j - 1] + curr[i][j + 1]);
    }
  }

  ++(grid->relaxations);

  //copyNextIntoCurrentGrid(grid, grid->nextGrid, grid->currentGrid);
}

void relaxGaussSeidelCheckered(struct Grid *grid)
{
  double **curr = grid->currentGrid;

  for (unsigned long c = 0; c < 2; ++c)
  {
    for (unsigned long i = 1; i < grid->points - 1; ++i)
    {
      for (unsigned long j = 1; j < grid->points - 1; ++j)
      {
        if ((i * (grid->points + 1) + j) % 2 == c)
        {
          curr[i][j] = 0.25 * (curr[i + 1][j] + curr[i - 1][j] + curr[i][j - 1] + curr[i][j + 1]);
        }
      }
    }
  }

  ++(grid->relaxations);

  //copyNextIntoCurrentGrid(grid, grid->nextGrid, grid->currentGrid);
}

unsigned long runRelaxationsUntilAccuracy(
    char *name,
    double linearDimension,
    unsigned long points,
    double desiredAccuracy,
    void (*relaxFn)(struct Grid *grid),
    double (*initialValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*boundaryValue)(struct Grid *grid, unsigned long, unsigned long),
    double (*guessPotential)(struct Grid *grid, unsigned long, unsigned long),
    double **storeGrid)
{
  struct Grid grid = createGrid(linearDimension, points);
  setInitialValues(&grid, initialValue);
  setBoundaryConditions(&grid, boundaryValue);
  computeAccuracy(&grid, guessPotential);

  //printGrid(&grid);

  unsigned long steps = 0;
  while (grid.currentAccuracy > desiredAccuracy && (++steps) <= 1500000)
  {
    relaxFn(&grid);
    computeAccuracy(&grid, guessPotential);
  }
  //printGrid(&grid);

  if (name != NULL)
  {
    FILE *file = fopen(name, "wb");
    storeGridInFile(file, &grid);
    fclose(file);
  }

  if (storeGrid != NULL)
  {
    copyNextIntoCurrentGrid(&grid, grid.currentGrid, storeGrid);
  }

  freeGrid(&grid);

  return grid.relaxations;
}