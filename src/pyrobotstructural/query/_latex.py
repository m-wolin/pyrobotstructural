CASE_NATURE_MAP = {
    0: "Permanent",
    1: "Live",
    2: "Wind",
    3: "Snow",
    4: "Temperature",
    5: "Accidental",
    6: "Seismic",
}

_LATEX_SPECIAL = str.maketrans({
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
})


def escape(text: str) -> str:
    return str(text).translate(_LATEX_SPECIAL)


COMB_TYPE_MAP = {
    0: "ULS",
    1: "SLS",
    2: "ALS",
    3: "SPC",
}


def format_factors(case_factors) -> str:
    parts = []
    for i in range(1, case_factors.Count + 1):
        cf = case_factors.Get(i)
        factor_str = f"{cf.Factor:.4g}".rstrip("0").rstrip(".")
        parts.append(f"{cf.CaseNumber}\\cdot{factor_str}")
    return "$" + " + ".join(parts) + "$"
