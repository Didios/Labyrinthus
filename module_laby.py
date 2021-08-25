from random import choice, random

class laby():
    def __init__(self, x, y, case = [0, 0]):
        self.x = x
        self.y = y
        self.data = [[[1, 1, 1, 1] for m in range(self.x)] for n in range(self.y)]

    def construct(self):
        def maze(labyrinthe, case_courante, passer):
            def case_haut(L,case):
                if case[0] -1 == -1:
                    return [0,1,0,0]
                return L[case[0] -1][case[1]]

            def case_bas(L,case):
                if case[0] +1 == len(L):
                    return [1,0,0,0]
                return L[case[0] +1][case[1]]

            def case_droite(L,case):
                if case[1] +1 == len(L[0]):
                    return [0,0,0,1]
                return L[case[0]][case[1] +1]

            def case_gauche(L,case):
                if case[1] -1 == -1:
                    return [0,0,1,0]
                return L[case[0]][case[1] -1]

            def cor_H(case):
                return [case[0] -1, case[1]]

            def cor_B(case):
                return [case[0] +1, case[1]]

            def cor_D(case):
                return [case[0], case[1] +1]

            def cor_G(case):
                return [case[0], case[1] -1]

            def possible(case):
                mur = 0
                ok = random()
                for i in case:
                    if i == 1:
                        mur += 1
                if ok < 0.8:
                    return mur > 3
                else:
                    return mur > 2

            while possible(case_haut(labyrinthe, case_courante)) or possible(case_bas(labyrinthe, case_courante)) or possible(case_droite(labyrinthe, case_courante)) or possible(case_gauche(labyrinthe, case_courante)):

                choix = []

                if possible(case_haut(labyrinthe, case_courante)):
                    choix += ["H"]
                if possible(case_bas(labyrinthe, case_courante)):
                    choix += ["B"]
                if possible(case_droite(labyrinthe, case_courante)):
                    choix += ["D"]
                if possible(case_gauche(labyrinthe, case_courante)):
                    choix += ["G"]

                if choix == []:
                    case_destinataire = case_courante
                else:
                    case_destinataire = choice(choix)

                if case_destinataire == "H":
                    case_destinataire = cor_H(case_courante)
                    labyrinthe[case_destinataire[0]][case_destinataire[1]][1] -= 1
                    labyrinthe[case_courante[0]][case_courante[1]][0] -= 1
                elif case_destinataire == "B":
                    case_destinataire = cor_B(case_courante)
                    labyrinthe[case_destinataire[0]][case_destinataire[1]][0] -= 1
                    labyrinthe[case_courante[0]][case_courante[1]][1] -= 1
                elif case_destinataire == "D":
                    case_destinataire = cor_D(case_courante)
                    labyrinthe[case_destinataire[0]][case_destinataire[1]][3] -= 1
                    labyrinthe[case_courante[0]][case_courante[1]][2] -= 1
                elif case_destinataire == "G":
                    case_destinataire = cor_G(case_courante)
                    labyrinthe[case_destinataire[0]][case_destinataire[1]][2] -= 1
                    labyrinthe[case_courante[0]][case_courante[1]][3] -= 1

                case_courante = case_destinataire
                passer += [case_courante]

            return labyrinthe

        case_courante = [0, 0]
        passer = []
        passer += [case_courante]

        while passer != []:
            case_courante = passer[-1]
            passer = passer[:-1]
            self.data = maze(self.data, case_courante, passer)

        return self


    def __repr__(self):
        total = ""

        for i in self.data[0]:
            total +="XX"
        total += "X"

        total += '\n'

        for ligne in range(len(self.data)):
            Li = ""
            bas = ""

            for case in self.data[ligne]:

                if case[2] == 1 and case[3] == 1:
                    Li += "X-X"
                elif case[2] == 1:
                    Li += "--X"
                elif case[3] == 1:
                    Li += "X--"
                else:
                    Li += "---"

                if case[1] == 1:
                    bas += "XXX"
                else:
                    bas += "X-X"

            c = 2
            while c < len(Li) -1:
                Li = Li[:c] + Li[c+1:]
                bas = bas[:c] + bas[c+1:]
                c += 2

            total += Li + '\n'
            total += bas + '\n'
        return total

    def schema(self):
        total = ""

        for i in self.data[0]:
            total +="XX"
        total += "X"

        total += '\n'

        for ligne in range(len(self.data)):
            Li = ""
            bas = ""

            for case in self.data[ligne]:

                if case[2] == 1 and case[3] == 1:
                    Li += "X-X"
                elif case[2] == 1:
                    Li += "--X"
                elif case[3] == 1:
                    Li += "X--"
                else:
                    Li += "---"

                if case[1] == 1:
                    bas += "XXX"
                else:
                    bas += "X-X"

            c = 2
            while c < len(Li) -1:
                Li = Li[:c] + Li[c+1:]
                bas = bas[:c] + bas[c+1:]
                c += 2

            total += Li + '\n'
            total += bas + '\n'

        in_out = total.split("\n")
        return in_out[:-1]