class pile:
    """
    Une pile
    """
    def __init__(self):
        """
        On initialise la Pile comme étant vide
        """
        self.contenu = []

    def estVide(self):
        """
        Donne un booléen qui indique si la Pile est vide ou non
        """
        return self.contenu == []

    def empiler(self,x):
        """
        Prend en paramètres x, un objet qui est ajouté à la pile
        """
        self.contenu.append(x)

    def depiler(self):
        """
        Donne le dernier objet de la Pile et le supprime de la Pile
        """
        if self.estVide():
            return "La pile est vide"
        return self.contenu.pop()

    def get_depile(self):
        """
        Donne le prochain qui sera depiler
        """
        if self.estVide():
            return "La pile est vide"
        depile =  self.contenu.pop()
        self.empiler(depile)
        return depile
