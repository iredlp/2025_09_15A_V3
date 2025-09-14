import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMapA= {}

    def getAllYears(self):
        return DAO.getAllYears()

    def creaGrafo(self, anno1, anno2):
        self._grafo.clear()
        self._idMapA.clear()

        piloti = DAO.getAllNodes(anno1, anno2)
        for a in piloti:
            self._idMapA[a.driverId] = a
            self._grafo.add_node(a)
            # aggiungo i nodi
        print("2 - Nodi aggiunti")

        for a in piloti:
           # a.clientiPerArtista = set(DAO.getClientiPerArtista(a.ArtistId))
            a.partecipazioni = DAO.getSquadrePerPilota(a.driverId, anno1, anno2)
           # a.popolarita = DAO.getPopolarita(a.ArtistId)
        print("3 - Informazioni recuperate")

        for i in range(len(piloti)):
            a1 = piloti[i]
            for j in range(i + 1, len(piloti)):
                a2 = piloti[j]
                peso = 0

                for gara1, squadra1 in a1.partecipazioni:
                    for gara2, squadra2 in a2.partecipazioni:
                        if gara1 == gara2 and squadra1 == squadra2:
                            peso += 1
                if   peso > 0:

                    self._grafo.add_edge(a1, a2, weight=peso)
        print("4 - Archi aggiunti")


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def get_num_nodes(self) -> int:
        return self._grafo.number_of_nodes()

    def get_num_edges(self) -> int:
        return self._grafo.number_of_edges()

    def getTop3Archi(self):
        # return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:10]
        archi = self._grafo.edges(data=True)
        return sorted(
            archi,
            key=lambda x: x[2]["weight"],
            reverse=True
        )[:3]

    def getConnessaInfo(self):
        # lo trasformo in non orientato pk richiesto di ignorare
        grafo_non_orientato = self._grafo.to_undirected()
        components = list(nx.connected_components(grafo_non_orientato))

        # Se il grafo è vuoto
        if len(components) == 0:
            return 0, set(), []

        # components = list(nx.connected_components(self._grafo))  # TROVO LE COMP CONNESSE e ci faccio una lista
        largest = max(components, key=len)  # trova la + grande

        # b. Film con maggior numero di archi uscenti
        #film_max_out = max(self._grafo.nodes, key=lambda n: self._grafo.out_degree(n))
        # relativo numero archi usenti
        #max_out = self._grafo.out_degree(film_max_out)

        # ORDINO PER  GRADO!!
        ordered_nodes = sorted(largest, key=lambda n: grafo_non_orientato.degree(n), reverse=True)  # ordine decrescente
        details = [(n, len(n.partecipazioni)) for n in ordered_nodes]

        return len(components), largest, details

    def getGruppoPiloti(self,  k):
        self._best_group = []
        self._best_score = float("inf")

        self._creaMappaComponenti()

        piloti= list(self._grafo.nodes)
        self._ricorsione([], piloti, k, 0)
        # Il percorso parziale parte con il nodo selezionato
       # parziale = [start_node]
       # self._ricorsione(parziale, k)

        return self._best_group, self._best_score

    def _ricorsione(self, parziale,piloti, k,pos):
        # CASO BASE: ho trovato K piloti
        if len(parziale) == k:
            score = self._score(parziale)
           # score = sum(len(a.movies) for a in parziale)

            if score <self._best_score:
                self._best_score = score
                self._best_group = list(parziale)
            return

        # POTATURA: non ci sono abbastanza piloti per completare il gruppo
        # Se non restano abbastanza costruttori, termino
        if len(piloti) - pos < k - len(parziale):
            return
        # PROVO I PILOTI A PARTIRE DALLA POSIZIONE pos
        # Provo i costruttori a partire dalla posizione pos
        for i in range(pos, len(piloti)):
            candidato = piloti[i]


            # Controllo che non ci sia già un costruttore
            # della stessa componente nella soluzione parziale
            stessa_componente = False

            for costruttore in parziale:
                if (self._mappaComponenti[candidato]
                        == self._mappaComponenti[costruttore]):
                    stessa_componente = True
                    break

            if stessa_componente:
                continue
            # AGGIUNGO IL PILOTA
            parziale.append(candidato)
            # Chiamata ricorsiva passando il nuovo arco come riferimento
            self._ricorsione(parziale, piloti, k, i + 1)
            # BACKTRACKING: annullo l'ultima mossa
            parziale.pop()

    def _score(self, parziale):
        date_nascita = []

        for pilota in parziale:
            dob = pilota.dob
            if dob is None:
                return float("inf")
            date_nascita.append(dob)

        data_piu_vecchia = min(date_nascita)
        data_piu_recente = max(date_nascita)
        scarto = (data_piu_recente - data_piu_vecchia).days

        return scarto

    def _creaMappaComponenti(self):
        self._mappaComponenti = {}

        grafoNonOrientato = self._grafo.to_undirected()
        componenti = list(nx.connected_components(grafoNonOrientato))

        for i, componente in enumerate(componenti):
            for costruttore in componente:
                self._mappaComponenti[costruttore] = i


