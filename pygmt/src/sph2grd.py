"""
sph2grd - Compute grid from spherical harmonic coefficients
"""
from pygmt.clib import Session
from pygmt.helpers import (
    GMTTempFile,
    build_arg_string,
    fmt_docstring,
    kwargs_to_strings,
    use_alias,
)
from pygmt.io import load_dataarray


@fmt_docstring
@use_alias(
    G="outgrid",
    I="spacing",
    R="region",
    V="verbose",
    b="binary",
    h="header",
    i="incols",
    r="registration",
    x="cores",
)
@kwargs_to_strings(I="sequence", R="sequence", i="sequence_comma")
def sph2grd(data, **kwargs):
    r"""
    Create spherical grid files in tension of data.

    Reads a spherical harmonics coefficient table with records of L, M,
    C[L,M], S[L,M] and evaluates the spherical harmonic model on the
    specified grid.

    Full option list at :gmt-docs:`sph2grd.html`

    {aliases}

    Parameters
    ----------
    data : str or {table-like}
        Pass in data with L, M, C[L,M], S[L,M] values by
        providing a file name to an ASCII data table, a 2D
        {table-classes}.
    outgrid : str or None
        The name of the output netCDF file with extension .nc to store the grid
        in.
    {I}
    {R}
    {V}
    {b}
    {h}
    {i}
    {r}
    {x}

    Returns
    -------
    ret: xarray.DataArray or None
        Return type depends on whether the ``outgrid`` parameter is set:

        - :class:`xarray.DataArray` if ``outgrid`` is not set
        - None if ``outgrid`` is set (grid output will be stored in file set by
          ``outgrid``)
    """
    with GMTTempFile(suffix=".nc") as tmpfile:
        with Session() as lib:
            file_context = lib.virtualfile_from_data(check_kind="vector", data=data)
            with file_context as infile:
                if "G" not in kwargs:  # if outgrid is unset, output to tempfile
                    kwargs.update({"G": tmpfile.name})
                outgrid = kwargs["G"]
                arg_str = " ".join([infile, build_arg_string(kwargs)])
                lib.call_module("sph2grd", arg_str)

        return load_dataarray(outgrid) if outgrid == tmpfile.name else None
