import sys
import tempfile
from unittest.mock import MagicMock

# Create MagicMock for PySide6
mock_qt = MagicMock()

# Return a real temporary path when QStandardPaths.writableLocation is called
mock_qt.QtCore.QStandardPaths.writableLocation.return_value = tempfile.gettempdir()

# Optional: QDir().mkpath(path) should return True (success)
mock_qt.QtCore.QDir.return_value.mkpath.return_value = True

# Install into sys.modules so the import in Config.py doesn't fail
#sys.modules["PySide6"] = mock_qt
#sys.modules["PySide6.QtCore"] = mock_qt.QtCore
#sys.modules["PySide6.QtWidgets"] = mock_qt.QtWidgets
#sys.modules["PySide6.QtGui"] = mock_qt.QtGui
