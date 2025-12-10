"""Test suite for Pink Morsels Sales Dash app."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app  # noqa: E402


def test_header_present():
    """Test that the app header 'Pink Morsels Sales Visualiser' is present in the layout."""
    layout = app.layout
    # Navigate through the layout structure to find the h1 element
    hero = layout.children[0]
    h1 = hero.children[0]
    assert h1.children == "Pink Morsels Sales Visualiser"


def test_visualisation_present():
    """Test that the sales graph visualization is present in the layout."""
    layout = app.layout
    chart_card = layout.children[2]
    graph = chart_card.children[0]
    assert graph.id == "sales-graph"
    assert graph.figure is not None


def test_region_picker_present():
    """Test that the region picker (radio items) is present with 5 options."""
    layout = app.layout
    controls = layout.children[1]
    control_card = controls.children[0]
    radio_items = control_card.children[1]
    assert radio_items.id == "region-radio"
    # Check for 5 radio options: all, north, east, south, west
    assert len(radio_items.options) == 5
    option_values = [opt["value"] for opt in radio_items.options]
    assert option_values == ["all", "east", "north", "south", "west"]
