import sys
import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True, scope="session")
def mock_pyside_modules():
    """Automatically mock PySide6 modules in all tests."""
    mock = MagicMock()

    sys.modules["PySide6"] = mock
    sys.modules["PySide6.QtWidgets"] = mock.QtWidgets
    sys.modules["PySide6.QtCore"] = mock.QtCore
    sys.modules["PySide6.QtGui"] = mock.QtGui

    # Add more submodules if needed:
    # sys.modules["PySide6.QtSvg"] = mock.QtSvg
    # sys.modules["PySide6.QtOpenGL"] = mock.QtOpenGL

    yield
