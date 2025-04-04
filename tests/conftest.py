import sys
from unittest.mock import MagicMock

# Apply before Pytest collects anything
mock = MagicMock()
sys.modules["PySide6"] = mock
sys.modules["PySide6.QtWidgets"] = mock.QtWidgets
sys.modules["PySide6.QtCore"] = mock.QtCore
sys.modules["PySide6.QtGui"] = mock.QtGui