import io
import os
from pathlib import Path

import pandas as pd


def make_plot(
    x,
    y,
    *,
    xlabel=None,
    ylabel=None,
    title=None,
    hline=None,
    vline=None,
    grid=True,
    legend=None,
    figsize=(8, 5),
    xlim=None,
    ylim=None,
    show=True,
):
    """
    Quickly and flexibly generate a plot.

    Parameters
    ----------
    x, y : array-like
        Data for the X and Y axes.

    xlabel : str, optional
        X-axis label.

    ylabel : str, optional
        Y-axis label.

    title : str, optional
        Plot title.

    hline : dict or list of dicts, optional
        Configuration for plt.axhline().
        Example:
            {"y": 10, "color": "red", "linestyle": "--"}

    vline : dict or list of dicts, optional
        Configuration for plt.axvline().
        Example:
            {"x": 5, "color": "green", "linestyle": "--"}

    grid : bool
        Whether to display the grid.

    legend : bool
        Whether to display the legend when elements have a label.

    figsize : tuple
        Figure size.

    xlim : tuple, optional
        X-axis limits. Example: (0, 10)

    ylim : tuple, optional
        Y-axis limits. Example: (-5, 20)

    show : bool
        If True, plt.show() is called automatically.

    Returns
    -------
    fig, ax
        Matplotlib Figure and Axes objects.
    """

    import matplotlib.pyplot as plt

    # Create the figure and axes
    fig, ax = plt.subplots(figsize=figsize)

    # Main plot
    ax.plot(x, y, label="Data")

    # Axis labels
    if xlabel is not None:
        ax.set_xlabel(xlabel)

    if ylabel is not None:
        ax.set_ylabel(ylabel)

    # Title
    if title is not None:
        ax.set_title(title)

    # Horizontal line(s)
    if hline is not None:
        if isinstance(hline, dict):
            hline = [hline]

        for config in hline:
            ax.axhline(**config)

    # Vertical line(s)
    if vline is not None:
        if isinstance(vline, dict):
            vline = [vline]

        for config in vline:
            ax.axvline(**config)

    # Axis limits
    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    # Grid
    if grid:
        ax.grid(True, alpha=0.3)

    # Legend
    if legend:
        ax.legend()

    # Automatically adjust the spacing
    fig.tight_layout()

    # Display the plot
    if show:
        plt.show()

    return fig, ax


def load_data_automatically(file_or_buffer, **kwargs) -> pd.DataFrame:
    """
    Automatically load data from files or buffers into a Pandas DataFrame.

    Dynamically identifies the file format based on its extension or content
    and applies the appropriate Pandas reading function (CSV, Excel, JSON,
    or Parquet).

    Parameters
    ----------
    file_or_buffer : str, Path, or file-like object
        File path (e.g. 'data.csv') or an in-memory file-like object.

    **kwargs :
        Additional arguments passed directly to Pandas reading functions.

        Useful examples:
        - nrows=100
            Reads only the first 100 rows.
        - usecols=['Name', 'Age']
            Loads only specific columns.
        - sheet_name='Sheet1'
            Specifies the Excel sheet.
        - sep=';'
            Changes the default CSV separator.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing the loaded data.
    """

    # --- CASE 1: The user provided a physical file path (String or Path) ---
    if isinstance(file_or_buffer, (str, Path)):
        path = Path(file_or_buffer)
        extension = path.suffix.lower()

        if extension == ".csv":
            # Avoids an error if the user accidentally passes an Excel parameter
            kwargs.pop("sheet_name", None)
            return pd.read_csv(path, **kwargs)

        elif extension in [".xlsx", ".xls"]:
            return pd.read_excel(path, **kwargs)

        elif extension == ".json":
            kwargs.pop("sheet_name", None)
            return pd.read_json(path, **kwargs)

        elif extension == ".parquet":
            kwargs.pop("sheet_name", None)
            return pd.read_parquet(path, **kwargs)

        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    # --- CASE 2: The user provided an in-memory file (Upload/Web) ---
    elif hasattr(file_or_buffer, "read"):
        # Try to get the uploaded file name from the browser/system
        file_name = getattr(file_or_buffer, "name", "")

        if file_name:
            _, extension = os.path.splitext(file_name.lower())

            if extension == ".csv":
                kwargs.pop("sheet_name", None)
                return pd.read_csv(file_or_buffer, **kwargs)

            elif extension in [".xlsx", ".xls"]:
                return pd.read_excel(file_or_buffer, **kwargs)

            elif extension == ".json":
                kwargs.pop("sheet_name", None)
                return pd.read_json(file_or_buffer, **kwargs)

            elif extension == ".parquet":
                kwargs.pop("sheet_name", None)
                return pd.read_parquet(file_or_buffer, **kwargs)

        # --- CASE 3: Raw buffer without a name (e.g. io.StringIO or io.BytesIO in tests) ---
        try:
            if isinstance(file_or_buffer, io.BytesIO):
                content = (
                    file_or_buffer.getvalue()
                    .decode("utf-8", errors="ignore")
                    .strip()
                )
            else:
                content = file_or_buffer.read()

                if hasattr(file_or_buffer, "seek"):
                    file_or_buffer.seek(0)
                    # Reset the pointer so Pandas can read from the beginning

            # Simple heuristic: if the text starts with braces or brackets,
            # it is probably JSON
            if content.startswith("{") or content.startswith("["):
                kwargs.pop("sheet_name", None)
                return pd.read_json(file_or_buffer, **kwargs)
            else:
                kwargs.pop("sheet_name", None)
                return pd.read_csv(file_or_buffer, **kwargs)

        except Exception as e:
            raise TypeError(
                "Could not determine the type of the provided buffer."
            ) from e

    else:
        raise TypeError(
            "The argument must be a file path (str/Path) or a file-like object."
        )
