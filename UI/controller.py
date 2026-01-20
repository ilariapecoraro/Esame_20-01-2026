import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        """ Handler per gestire creazione del grafo """
        try:
            n_alb = int(self._view.txtMinDuration.value)
        except ValueError:
            self._view.show_alert("non valido")
            return
        self._model.build_graph(n_alb)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(
                f"Grafo creato: {self._model.get_num_of_nodes()}(artisti),"
                f" {self._model.get_num_of_edges()} archi"))

        self._view.update_page()

    def _populate_dd_products(self):
        try:
            n_alb = int(self._view.txtMinDuration.value)
        except ValueError:
            self._view.show_alert("non valido")
            return
        all_nodes = self._model.load_all_artists(n_alb)
        self._view.ddArtist.options = [ft.dropdown.Option(key=a.name, data=a) for a in all_nodes]
        self._view.update_page()





