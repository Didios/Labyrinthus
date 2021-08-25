from random import choice
from tkinter import *

#-------------------------------------------------------------------------------
def make_laby(x,y):
    def case_haut(laby,case):
        if case[0]-1 == -1:
            return [0,1,0,0]
        return laby[case[0]-1][case[1]]

    def case_bas(laby,case):
        if case[0]+1 == len(laby):
            return [1,0,0,0]
        return laby[case[0]+1][case[1]]

    def case_droite(laby,case):
        if case[1]+1 == len(laby[0]):
            return [0,0,0,1]
        return laby[case[0]][case[1]+1]

    def case_gauche(laby,case):
        if case[1]-1 == -1:
            return [0,0,1,0]
        return laby[case[0]][case[1]-1]

    def cor_H(case):
        return [case[0]-1,case[1]]

    def cor_B(case):
        return [case[0]+1,case[1]]

    def cor_D(case):
        return [case[0],case[1]+1]

    def cor_G(case):
        return [case[0],case[1]-1]

    def possible(case):
        mur = 0
        for i in case:
            if i == 1:
                mur += 1
        return mur > 2

    def maze(laby,case_courante,passer):
        while possible(case_haut(laby,case_courante)) or possible(case_bas(laby,case_courante)) or possible(case_droite(laby,case_courante)) or possible(case_gauche(laby,case_courante)):
            choix = []
            if possible(case_haut(laby,case_courante)):
                choix += ["H"]
            if possible(case_bas(laby,case_courante)):
                choix += ["B"]
            if possible(case_droite(laby,case_courante)):
                choix += ["D"]
            if possible(case_gauche(laby,case_courante)):
                choix += ["G"]

            case_destinataire = choice(choix)

            if case_destinataire == "H":
                case_destinataire = cor_H(case_courante)
                laby[case_destinataire[0]][case_destinataire[1]][1] -= 1
                laby[case_courante[0]][case_courante[1]][0] -=1
            elif case_destinataire == "B":
                case_destinataire = cor_B(case_courante)
                laby[case_destinataire[0]][case_destinataire[1]][0] -= 1
                laby[case_courante[0]][case_courante[1]][1] -=1
            elif case_destinataire == "D":
                case_destinataire = cor_D(case_courante)
                laby[case_destinataire[0]][case_destinataire[1]][3] -= 1
                laby[case_courante[0]][case_courante[1]][2] -=1
            else:
                case_destinataire = cor_G(case_courante)
                laby[case_destinataire[0]][case_destinataire[1]][2] -= 1
                laby[case_courante[0]][case_courante[1]][3] -=1

            case_courante = case_destinataire
            passer += [case_courante]
        return laby

    def affiche(laby,x,y):
        def noir(x1, y1, co_x, co_y):
            surface.create_rectangle(x1, y1, x1+co_x, y1+co_y, fill="black")

        coeff_x = 5
        coeff_y = 10
        if x > 50:
            coeff_x = (1020 / (x + 1)) / 4
        if y > 30:
            coeff_y = (620 / (y + 1)) / 2

        surface = Canvas(width=x*coeff_x*4, height=y*coeff_y*2 +1, bg='white')
        surface.create_rectangle(0, 0, x*21, coeff_y, fill='black')
        pos_y = -coeff_y
        for ligne in range(len(laby)):
            pos_y += (coeff_y * 2)
            pos_x = 0

            for case in laby[ligne]:
                if case[3] == 1:
                    noir(pos_x, pos_y, coeff_x, coeff_y)
                pos_x += coeff_x * 2

                if case[2] == 1:
                    noir(pos_x + coeff_x, pos_y, coeff_x, coeff_y)
                pos_x += coeff_x * 2

                if case[1] == 1:
                    noir(pos_x - coeff_x * 3, pos_y + coeff_y, coeff_x, coeff_y)
                    noir(pos_x - coeff_x * 2, pos_y + coeff_y, coeff_x, coeff_y)
                noir(pos_x - coeff_x * 4, pos_y + coeff_y, coeff_x, coeff_y)
                noir(pos_x - coeff_x, pos_y + coeff_y, coeff_x, coeff_y)
            noir(pos_x, pos_y, coeff_x, coeff_y)
            noir(pos_x, pos_y + coeff_y, coeff_x, coeff_y)
        surface.create_rectangle(0, coeff_y + 1, coeff_x *2, coeff_y * 2 -1, fill="white", outline="white")
        surface.create_rectangle(pos_x - coeff_x * 2, pos_y + 1, pos_x + coeff_x * 2, pos_y + coeff_y-1, fill="white", outline="white")
        surface.pack()

    laby = [[[1,1,1,1] for m in range(x)] for n in range(y)]
    case_courante = [0,0]
    passer = []
    passer += [case_courante]

    while passer != []:
        case_courante = passer[-1]
        passer = passer[:-1]
        laby = maze(laby,case_courante,passer)
    return affiche(laby,x,y)
#-------------------------------------------------------------------------------

def create():
    def valid():
        x = int(champ_x.get())
        y = int(champ_y.get())
        champ_y.destroy()
        champ_x.destroy()
        titre_x.destroy()
        titre_y.destroy()
        VALIDER.destroy()
        make_laby(x,y)

    for c in fenetre.winfo_children():
        if c.winfo_class() == 'Canvas':
            c.destroy()

    x = 0
    y = 0
    titre_x = Label(fenetre, text="Longueur du labyrinthe")
    titre_y = Label(fenetre, text="Largeur du labyrinthe")
    champ_x = Spinbox(fenetre, width=15, from_=5, to=50)
    champ_y = Spinbox(fenetre, width=15, from_=5, to=30)
    VALIDER = Button(fenetre, text="Valider", command = valid)

    titre_x.pack()
    champ_x.pack()
    titre_y.pack()
    champ_y.pack()
    VALIDER.pack()

fenetre = Tk()
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=create)
menu1.add_command(label="Editer")
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.destroy)
menubar.add_cascade(label="Labyrinthe", menu=menu1)

fenetre.title("Générateur de Labyrinthe")
fenetre.iconbitmap('icon_laby.ico')
fenetre.config(menu=menubar)
fenetre.geometry('1020x620')
fenetre.mainloop()



