# Simple Graphs

A small Python project focused on making data visualization and data loading simpler and more convenient.

The main idea is to create reusable utilities that reduce repetitive code when working with **Matplotlib** and **Pandas**.

This project is also being developed as a learning project for Python packaging, automated testing, and eventually publishing a package to **PyPI**.

## Features

### `make_plot()`

A helper function for quickly creating and configuring Matplotlib plots.

It currently supports:

* X and Y axis labels;
* plot titles;
* horizontal reference lines;
* vertical reference lines;
* grid;
* legends;
* figure size;
* X and Y axis limits;
* optional automatic display of the plot.

Example:

```python
import numpy as np

from simple_graphs import make_plot

x = np.linspace(0, 10, 100)
y = x**2

make_plot(
    x,
    y,
    xlabel="Time (s)",
    ylabel="Position (m)",
    title="Position over Time",
)
```

### `load_data_automatically()`

A utility for loading data into a Pandas DataFrame without having to manually choose the appropriate Pandas reader.

The function can currently work with:

* CSV files;
* Excel files (`.xlsx` and `.xls`);
* JSON files;
* Parquet files;
* file-like objects and in-memory buffers.

The file format can be deter
