import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt
import metodos_GUI


@pytest.fixture
def app(qtbot):
    application = QApplication([])
    qtbot.addWidget(metodos_GUI.MisMetodos())
    return application


def test_validar_producto(app, qtbot):
    # Simular la entrada de datos en la interfaz gráfica
    qtbot.keyClicks(app.Aplicacion.app.txt_nom_prod, "NombreProducto")
    qtbot.keyClicks(app.Aplicacion.app.txt_precio_prod, "10.5")
    qtbot.keyClicks(app.Aplicacion.app.txt_stock_prod, "20")
    qtbot.keyClicks(app.Aplicacion.app.txt_cat_prod, "Categoria")
    qtbot.keyClicks(app.Aplicacion.app.des_prod, "Descripción del producto")

    # Ejecutar la validación del producto (simula hacer clic en el botón)
    qtbot.mouseClick(app.Aplicacion.app.btn_agre, Qt.MouseButton.LeftClick)

    # Verificar que el mensaje de error esté vacío después de la validación
    assert app.Aplicacion.app.lbl_msj_error.text() == ""


if __name__ == "__main__":
    pytest.main(["-v", "test_gui.py"])