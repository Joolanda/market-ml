"""Shared fixtures: every test runs on seeded sample data, never on data/raw/ or the network."""

import pytest

from src.data import data_loader, sources


@pytest.fixture(autouse=True, scope="session")
def _sample_data_only(tmp_path_factory):
    empty = tmp_path_factory.mktemp("raw")
    original = sources.RAW_DIR
    sources.RAW_DIR = empty
    data_loader.clear_cache()
    yield
    sources.RAW_DIR = original
    data_loader.clear_cache()
