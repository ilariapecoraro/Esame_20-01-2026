import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists_list = []
        self.load_all_artists()
        self.min_artist = []

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")

    def load_artists_with_min_albums(self, min_albums):
        self.min_artist = DAO.get_all_min_artists(min_albums)

    def build_graph(self, min):

        # Pulisco il grafo e lo ricreo
        self._graph.clear()
        self.dict_artists = {}
        self.min_artist = []
        self.connessioni = []

        self.min_artist = DAO.get_all_min_artists(min)
        # creo un dizionario
        for artist in self.min_artist:
            if artist.id not in self.dict_artists:
                self.dict_artists[artist.id] = artist

        # aggiungo i nodi
        self._graph.add_nodes_from(self.min_artist)

        # prendo le connessioni
        self.connessioni = DAO.get_connections(self.dict_artists)

        # seleziono gli oggetti e il peso
        for a1_id, a2_id, in self.connessioni:
            a1 = self.dict_artists[a1_id]
            a2 = self.dict_artists[a2_id]
            # prendo il numero di generi

            lista1 = DAO.get_genere(a1_id)
            lista2 = DAO.get_genere(a2_id)
            peso = len(lista1) + len(lista2)
            for genere1 in lista1:
                for genere2 in lista2:
                    if genere1==genere2:
                        peso -=1
            # aggiungi l'arco con l'attributo
            self._graph.add_edge(a1, a2, weight=peso )

        print(self._graph)

    def get_num_of_nodes(self):
        return self._graph.number_of_nodes()

    def get_num_of_edges(self):
        return self._graph.number_of_edges()

    def get_vicino(self, artist):
        neigh = []
        if artist in self._graph.nodes():
            for neighbor in self._graph.neighbors(artist):
                attr = self._graph.get_edge_data(artist, neighbor)
                if attr:
                    peso = attr.get("weight")
                    neigh.append((neighbor, peso))
        neigh_ordinati = sorted(neigh, key=lambda x: x[1])
        return neigh_ordinati

