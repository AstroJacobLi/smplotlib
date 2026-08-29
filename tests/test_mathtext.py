# -*- coding: utf-8 -*-
"""Regression tests for MathText rendering with smplotlib.

Matplotlib 3.11 redefined ``mathtext.default``: the value that keeps letters
italic while leaving digits upright (classic TeX behaviour) changed from
``'it'`` to ``'normal'``.  With the old value, numbers inside ``$...$`` are
now rendered in the italic font.  smplotlib picks the right value per
Matplotlib version; these tests lock that behaviour in.
"""
import logging

import matplotlib

matplotlib.use("Agg")

import pytest
from matplotlib import _mathtext, rcParams
from matplotlib.font_manager import FontProperties

import smplotlib  # noqa: F401  (import applies the style)

try:  # matplotlib >= 3.10
    from matplotlib.ft2font import LoadFlags as _LoadFlags

    _NO_HINTING = _LoadFlags.NO_HINTING
except ImportError:  # older matplotlib
    from matplotlib.ft2font import LOAD_NO_HINTING as _NO_HINTING


def _glyph(sym):
    """Return (font_family, slanted) for *sym*, as the math parser would ask it.

    Uses the same ``custom`` fontset path smplotlib configures.  Skips the test
    if this Matplotlib exposes a different internal signature.
    """
    try:
        fontset = _mathtext.UnicodeFonts(FontProperties(), _NO_HINTING)
        font, _num, slanted = fontset._get_glyph(
            rcParams["mathtext.default"], "it", sym
        )
    except (AttributeError, TypeError) as exc:  # pragma: no cover
        pytest.skip(f"mathtext internals differ on this Matplotlib: {exc}")
    return font.family_name, slanted


@pytest.mark.parametrize("digit", list("0123456789"))
def test_digits_are_upright_in_mathtext(digit):
    family, slanted = _glyph(digit)
    assert family.startswith("AVHershey"), family
    assert slanted is False, f"digit {digit!r} should not be italic"


@pytest.mark.parametrize("sym", [r"x", r"M", r"\alpha", r"\sigma"])
def test_letters_are_italic_in_mathtext(sym):
    family, slanted = _glyph(sym)
    assert family.startswith("AVHershey"), family
    assert slanted is True, f"symbol {sym!r} should be italic"


def test_mathtext_default_is_version_appropriate():
    from smplotlib import _mpl_version_ge

    expected = "normal" if _mpl_version_ge(3, 11) else "it"
    assert rcParams["mathtext.default"] == expected


def test_font_weight_warning_is_filtered(caplog):
    """The cosmetic 'Failed to find font weight' log line must be suppressed."""
    fp = FontProperties(family="AVHershey Complex", weight="normal")
    with caplog.at_level(logging.WARNING, logger="matplotlib.font_manager"):
        from matplotlib.font_manager import findfont

        findfont(fp)
    assert not any(
        "Failed to find font weight" in rec.getMessage() for rec in caplog.records
    )


def test_end_to_end_render_smoke(tmp_path):
    """A figure full of numeric MathText renders without raising."""
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.set_title(r"$M_{200} = 3.5 \times 10^{12}\ M_\odot$, $z = 0.1234$")
    ax.set_xlabel(r"$\log_{10}(M_\star/M_\odot)$")
    ax.plot([1e-5, 2e-5, 3e-5], [1, 2, 3])  # forces sci-notation mathtext ticks
    fig.savefig(tmp_path / "smoke.png", dpi=80)
    plt.close(fig)
