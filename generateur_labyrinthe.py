from tkinter import Canvas, Tk, Menu, Label, Button, Spinbox, Toplevel, Radiobutton, IntVar, StringVar, PhotoImage
from tkinter.messagebox import showerror, showinfo, askyesno
from module_laby import *
from module_pile import *

#-------------------------------------------------------------------------------
def affiche(laby, x, y , surface = "",jeu = False):
    def noir(x1, y1, co_x, co_y):
        surface.create_rectangle(x1, y1, x1+co_x, y1+co_y, fill=couleur_mur['text'], outline=couleur_mur_ext['text'])


    if x > 60:
        coeff_x = 1252 / (x * 2 + 1)
        len_x = 1252
    else:
        coeff_x = 10
        len_x = x * coeff_x * 2 + coeff_x + 2
    if y > 34:
        coeff_y = 683 / (y * 2 + 1)
        len_y = 683
    else:
        coeff_y = 10
        len_y = y * coeff_y * 2 + 3

    laby[1] = "-" + laby[1][1:]
    laby[len(laby) -2] = laby[len(laby) -2][:-1] + "-"
    surface = Canvas(width=len_x, height= len_y, bg=couleur_fond['text'])
    pos_y = 0

    for ligne in laby:
        pos_x = 0
        for case in ligne:
            if case == "X":
                noir(pos_x, pos_y, coeff_x, coeff_y)
            pos_x += coeff_x
        pos_y += coeff_y

    if jeu == False:
        return surface
    else:
        return surface, coeff_x, coeff_y
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
        labyrinthe = laby(x,y).construct()
        dessin = affiche(labyrinthe.schema() , x, y)
        dessin.pack()

    for c in fenetre.winfo_children():
        if c.winfo_class() == 'Canvas' or c.winfo_class() == 'Button':
            c.destroy()

    x = 0
    y = 0
    titre_x = Label(fenetre, text="Longueur du labyrinthe")
    titre_y = Label(fenetre, text="Largeur du labyrinthe")
    champ_x = Spinbox(fenetre, width=15, from_=1, to=67)
    champ_y = Spinbox(fenetre, width=15, from_=1, to=34)
    VALIDER = Button(fenetre, text="Valider", command = valid)

    titre_x.pack()
    champ_x.pack()
    titre_y.pack()
    champ_y.pack()
    VALIDER.pack()
#-------------------------------------------------------------------------------

def edit():
    showerror("Impossible", "Cette fonctionalité n'as pas encore été ajouté.")
#-------------------------------------------------------------------------------

def solo():
    def play():
        def deplacement(opt = ""):
            def jonction(y, x, direction):
                if direction == "DG":
                    return schema[y+1][x] == "-" or schema[y-1][x] == "-"
                else:
                    return schema[y][x+1] == "-" or schema[y][x-1] == "-"

            def droite(event, enregistrer = "oui"):
                x = int((int(cor_x['text'])) // float(coeffx['text']))
                y = int(int(cor_y['text']) // float(coeffy['text']))

                if enregistrer == "oui" and ((jonction(y,x,"DG") and (x != int(croisementx['text']) or y != int(croisementy['text']))) or schema[y][x+1] == "X" or mouvement.get_depile() != "droite"):
                    croisementx['text'] = str(x)
                    croisementy['text'] = str(y)
                    mouvement.empiler("droite")

                if vitesse['text'] == "0":
                    fin = False
                    sup_x = x
                    if schema[y][sup_x +1] == "-" and jonction(y,sup_x, "DG"):
                        sup_x += 1
                    if y == len(schema) -2 and sup_x == len(schema[0]) -1:
                        fin = True
                    while fin == False and (schema[y][sup_x +1] == "-" and not jonction(y,sup_x, "DG")):
                        sup_x += 1
                        if y == len(schema) -2 and sup_x == len(schema[0]) -1:
                            fin = True
                    deplacement = (sup_x - x) * int(coeffx['text'])
                elif vitesse['text'] == "-1":
                    deplacement = int(coeffx['text'])
                else:
                    deplacement = int(vitesse['text'])

                if schema[y][int((int(cor_x['text']) + deplacement) // float(coeffx['text']))] == "-":
                    surface.move(perso, + deplacement, 0)
                    cor_x['text'] = str(int(cor_x['text']) + deplacement)

            def gauche(event, enregistrer = "oui"):
                x = int((int(cor_x['text'])) // float(coeffx['text']))
                y = int(int(cor_y['text']) // float(coeffy['text']))

                if enregistrer == "oui" and ((jonction(y,x,"DG") and (x != int(croisementx['text']) or y != int(croisementy['text']))) or schema[y][x-1] == "X" or mouvement.get_depile() != "gauche"):
                    croisementx['text'] = str(x)
                    croisementy['text'] = str(y)
                    mouvement.empiler("gauche")

                if vitesse['text'] == "0":
                    sup_x = x
                    if schema[y][sup_x -1] == "-" and jonction(y,sup_x, "DG"):
                        sup_x -= 1
                    while schema[y][sup_x -1] == "-" and not jonction(y,sup_x, "DG"):
                        sup_x -= 1
                    deplacement = (x - sup_x) * int(coeffx['text'])
                elif vitesse['text'] == "-1":
                    deplacement = int(coeffx['text'])
                else:
                    deplacement = int(vitesse['text'])

                if schema[y][int((int(cor_x['text']) - deplacement) // float(coeffx['text']))] == "-":
                    surface.move(perso, - deplacement, 0)
                    cor_x['text'] = str(int(cor_x['text']) - deplacement)

            def haut(event, enregistrer = "oui"):
                x = int(int(cor_x['text']) // float(coeffx['text']))
                y = int(int(cor_y['text']) // float(coeffy['text']))

                if enregistrer == "oui" and ((jonction(y,x,"HB") and (x != int(croisementx['text']) or y != int(croisementy['text']))) or schema[y-1][x] == "X" or mouvement.get_depile() != "haut"):
                    croisementx['text'] = str(x)
                    croisementy['text'] = str(y)
                    mouvement.empiler("haut")

                if vitesse['text'] == "0":
                    sup_y = y
                    if schema[sup_y -1][x] == "-" and jonction(sup_y,x, "HB"):
                        sup_y -= 1
                    while schema[sup_y -1][x] == "-" and not jonction(sup_y,x, "HB"):
                        sup_y -= 1
                    deplacement = (y - sup_y) * int(coeffy['text'])
                elif vitesse['text'] == "-1":
                    deplacement = int(coeffy['text'])
                else:
                    deplacement = int(vitesse['text'])

                if schema[int((int(cor_y['text']) - deplacement) // float(coeffy['text']))][x] == "-":
                    surface.move(perso, 0, - deplacement)
                    cor_y['text'] = str(int(cor_y['text']) - deplacement)

            def bas(event, enregistrer = "oui"):
                x = int((int(cor_x['text'])) // float(coeffx['text']))
                y = int(int(cor_y['text']) // float(coeffy['text']))

                if enregistrer == "oui" and ((jonction(y,x,"HB") and (x != int(croisementx['text']) or y != int(croisementy['text']))) or schema[y+1][x] == "X" or mouvement.get_depile() != "bas"):
                    croisementx['text'] = str(x)
                    croisementy['text'] = str(y)
                    mouvement.empiler("bas")

                if vitesse['text'] == "0":
                    sup_y = y
                    if schema[sup_y +1][x] == "-" and jonction(sup_y,x, "HB"):
                        sup_y += 1
                    while schema[sup_y +1][x] == "-" and not jonction(sup_y,x, "HB"):
                        sup_y += 1
                    deplacement = (sup_y - y) * int(coeffy['text'])
                elif vitesse['text'] == "-1":
                    deplacement = int(coeffy['text'])
                else:
                    deplacement = int(vitesse['text'])

                if schema[int((int(cor_y['text']) + deplacement) // float(coeffy['text']))][x] == "-":
                    surface.move(perso, 0, + deplacement)
                    cor_y['text'] = str(int(cor_y['text']) + deplacement)

            def verif_fini():
                if int(cor_y['text']) // int(coeffy['text']) == len(schema) -2 and int(cor_x['text']) // int(coeffx['text']) == len(schema[0]) -1:
                    if coeffy['text'] != "1":
                        showinfo("FIN", "Bravo, vous avez fini le labyrinthe")
                        if askyesno("REJOUER ?", "Voulez vous recommencer ?"):
                            solo()
                    else:
                        for c in fenetre.winfo_children():
                            if c.winfo_class() == 'Canvas' or c.winfo_class() == 'Button':
                                c.destroy()
                else:
                    fenetre.bind("<Right>", droite)
                    fenetre.bind("<Left>", gauche)
                    fenetre.bind("<Up>", haut)
                    fenetre.bind("<Down>", bas)
                    fenetre.bind("<space>", repere)
                    fenetre.bind("<Escape>", stop)
                    surface.grid(row=0, column=0)
                    fenetre.after(20,deplacement)

            def repere(event):
                cx = int(cor_x['text'])
                cy = int(cor_y['text'])
                while cx % int(coeffx["text"]) != 0:
                    cx -= 1
                while cy % int(coeffy["text"]) != 0:
                    cy -= 1
                surface.create_oval(cx +1, cy +1, cx + int(coeffx["text"]) -1, cy + int(coeffy["text"]) -1, fill = couleur_repere['text'], outline = couleur_repere_ext['text'], tags="repere")

            def stop(event):
                cor_y['text'] = str(len(schema) -2)
                coeffy['text'] = "1"
                cor_x['text'] = str(len(schema[0]) -1)
                coeffx['text'] = "1"

            if opt == "droite":
                V1 = vitesse['text']
                vitesse['text'] = "0"
                gauche('<Left>', "non")
                vitesse['text'] = V1
            elif opt == "gauche":
                V1 = vitesse['text']
                vitesse['text'] = "0"
                droite('<Right>', "non")
                vitesse['text'] = V1
            elif opt == "haut":
                V1 = vitesse['text']
                vitesse['text'] = "0"
                bas('<Down>', "non")
                vitesse['text'] = V1
            elif opt == "bas":
                V1 = vitesse['text']
                vitesse['text'] = "0"
                haut('<Up>', "non")
                vitesse['text'] = V1
            else:
                verif_fini()
                pass

        def retour():
            back = mouvement.depiler()
            if back == "droite":
                deplacement("droite")
            elif back == "gauche":
                deplacement("gauche")
            elif back == "haut":
                deplacement("haut")
            elif back == "bas":
                deplacement("bas")

        def retour_plus():
            surface.move(perso, -int(cor_x['text'])+int(coeff_x // 2), -int(cor_y['text'])+ 3 * int(coeff_y // 2))
            cor_x['text'] = str(int(coeff_x // 2))
            cor_y['text'] = str(int(coeff_y // 2 + coeff_y))
            surface.delete("repere")
            mouvement = pile()

        x = int(champ_x.get())
        y = int(champ_y.get())
        champ_y.destroy()
        champ_x.destroy()
        titre_x.destroy()
        titre_y.destroy()
        VALIDER.destroy()
        labyrinthe = laby(x,y).construct()
        surface = ""
        schema = labyrinthe.schema()
        surface, coeff_x, coeff_y = affiche(schema , x, y, surface, True)
        cor_x = Label(fenetre, text=str(int(coeff_x // 2)))
        cor_y = Label(fenetre, text=str(int(coeff_y // 2 + coeff_y)))
        coeffx = Label(fenetre, text=str(int(coeff_x)))
        coeffy = Label(fenetre, text=str(int(coeff_y)))
        perso = surface.create_rectangle(1, coeff_y +1, coeff_x -1, coeff_y * 2 -1, fill=couleur_perso['text'], outline=couleur_perso_ext['text'])
        croisementx = Label(fenetre, text=str(int(cor_x['text']) // int(coeffx['text'])))
        croisementy = Label(fenetre, text=str(int(cor_y['text']) // int(coeffy['text'])))
        mouvement = pile()
        Button(fenetre, text="Retour",bg="gold", command=retour, width=10, height=10).grid(row=0, column=1, sticky="n")
        Button(fenetre, text="Depart",bg="gold",  command=retour_plus, width=10, height=10).grid(row=0, column=1, sticky="s")
        deplacement()

    for c in fenetre.winfo_children():
        if c.winfo_class() == 'Canvas' or c.winfo_class() == 'Button':
            c.destroy()

    x = 0
    y = 0
    titre_x = Label(fenetre, text="Longueur du labyrinthe")
    titre_y = Label(fenetre, text="Largeur du labyrinthe")
    champ_x = Spinbox(fenetre, width=15, from_=1, to=60)
    champ_y = Spinbox(fenetre, width=15, from_=1, to=34)
    VALIDER = Button(fenetre, text="Valider", command = play)

    titre_x.pack()
    champ_x.pack()
    titre_y.pack()
    champ_y.pack()
    VALIDER.pack()

#-------------------------------------------------------------------------------
def vitesse():
    def low():
        vitesse['text'] = "1"

    def default():
        vitesse['text'] = "2"

    def high():
        vitesse['text'] = "5"

    def block():
        vitesse['text'] = "-1"

    def auto():
        vitesse['text'] = "0"


    speed = Toplevel(fenetre)
    speed.title("Vitesse")
    speed.iconbitmap('images/vitesse.ico')

    value = IntVar()
    Radiobutton(speed, text="lent", variable=value, value=1, command=low).grid(row=0, column=0, sticky="w")
    Radiobutton(speed, text="Par défaut", variable=value, value=2, command=default).grid(row=1, column=0, sticky="w")
    Radiobutton(speed, text="rapide", variable=value, value=3, command=high).grid(row=2, column=0, sticky="w")
    Radiobutton(speed, text="block", variable=value, value=4, command=block).grid(row=3, column=0, sticky="w")
    Radiobutton(speed, text="automatique", variable=value, value=5, command=auto).grid(row=4, column=0, sticky="w")
    Button(speed, text="Valider", command=speed.destroy).grid(row=5, column=0,)

#-------------------------------------------------------------------------------
def couleur():
    def palette(objet, can, obj_can=None, e="B"):
        def appliquer():
            objet['text'] = value1.get()
            if obj_can == None:
                can.configure(bg = value1.get())
            elif e == "E":
                can.itemconfigure(obj_can, outline = value1.get())
            else:
                can.itemconfigure(obj_can, fill = value1.get())

        palette = Toplevel(color)
        palette.title("palette de couleur")
        palette.iconbitmap('images/palette.ico')

        value1 = StringVar()
        Radiobutton(palette, text="       ", bg="#FF8080", variable = value1, value = "#FF8080", command = appliquer).grid(row=0, column=0)
        Radiobutton(palette, text="       ", bg="#FFFF80", variable = value1, value = "#FFFF80", command = appliquer).grid(row=0, column=1)
        Radiobutton(palette, text="       ", bg="#80FF80", variable = value1, value = "#80FF80", command = appliquer).grid(row=0, column=2)
        Radiobutton(palette, text="       ", bg="#00FF80", variable = value1, value = "#00FF80", command = appliquer).grid(row=0, column=3)
        Radiobutton(palette, text="       ", bg="#80FFFF", variable = value1, value = "#80FFFF", command = appliquer).grid(row=0, column=4)
        Radiobutton(palette, text="       ", bg="#0080FF", variable = value1, value = "#0080FF", command = appliquer).grid(row=0, column=5)
        Radiobutton(palette, text="       ", bg="#FF80C0", variable = value1, value = "#FF80C0", command = appliquer).grid(row=0, column=6)
        Radiobutton(palette, text="       ", bg="#FF80FF", variable = value1, value = "#FF80FF", command = appliquer).grid(row=0, column=7)

        Radiobutton(palette, text="       ", bg="#FF0000", variable = value1, value = "#FF0000", command = appliquer).grid(row=1, column=0)
        Radiobutton(palette, text="       ", bg="#FFFF00", variable = value1, value = "#FFFF00", command = appliquer).grid(row=1, column=1)
        Radiobutton(palette, text="       ", bg="#80FF00", variable = value1, value = "#80FF00", command = appliquer).grid(row=1, column=2)
        Radiobutton(palette, text="       ", bg="#00FF40", variable = value1, value = "#00FF40", command = appliquer).grid(row=1, column=3)
        Radiobutton(palette, text="       ", bg="#00FFFF", variable = value1, value = "#00FFFF", command = appliquer).grid(row=1, column=4)
        Radiobutton(palette, text="       ", bg="#0080C0", variable = value1, value = "#0080C0", command = appliquer).grid(row=1, column=5)
        Radiobutton(palette, text="       ", bg="#8080C0", variable = value1, value = "#8080C0", command = appliquer).grid(row=1, column=6)
        Radiobutton(palette, text="       ", bg="#FF00FF", variable = value1, value = "#FF00FF", command = appliquer).grid(row=1, column=7)

        Radiobutton(palette, text="       ", bg="#804040", variable = value1, value = "#804040", command = appliquer).grid(row=2, column=0)
        Radiobutton(palette, text="       ", bg="#FF8040", variable = value1, value = "#FF8040", command = appliquer).grid(row=2, column=1)
        Radiobutton(palette, text="       ", bg="#00FF00", variable = value1, value = "#00FF00", command = appliquer).grid(row=2, column=2)
        Radiobutton(palette, text="       ", bg="#008080", variable = value1, value = "#008080", command = appliquer).grid(row=2, column=3)
        Radiobutton(palette, text="       ", bg="#004080", variable = value1, value = "#004080", command = appliquer).grid(row=2, column=4)
        Radiobutton(palette, text="       ", bg="#8080FF", variable = value1, value = "#8080FF", command = appliquer).grid(row=2, column=5)
        Radiobutton(palette, text="       ", bg="#800040", variable = value1, value = "#800040", command = appliquer).grid(row=2, column=6)
        Radiobutton(palette, text="       ", bg="#FF0080", variable = value1, value = "#FF0080", command = appliquer).grid(row=2, column=7)

        Radiobutton(palette, text="       ", bg="#800000", variable = value1, value = "#800000", command = appliquer).grid(row=3, column=0)
        Radiobutton(palette, text="       ", bg="#FF8000", variable = value1, value = "#FF8000", command = appliquer).grid(row=3, column=1)
        Radiobutton(palette, text="       ", bg="#008000", variable = value1, value = "#008000", command = appliquer).grid(row=3, column=2)
        Radiobutton(palette, text="       ", bg="#008040", variable = value1, value = "#008040", command = appliquer).grid(row=3, column=3)
        Radiobutton(palette, text="       ", bg="#0000FF", variable = value1, value = "#0000FF", command = appliquer).grid(row=3, column=4)
        Radiobutton(palette, text="       ", bg="#0000A0", variable = value1, value = "#0000A0", command = appliquer).grid(row=3, column=5)
        Radiobutton(palette, text="       ", bg="#800080", variable = value1, value = "#800080", command = appliquer).grid(row=3, column=6)
        Radiobutton(palette, text="       ", bg="#8000FF", variable = value1, value = "#8000FF", command = appliquer).grid(row=3, column=7)

        Radiobutton(palette, text="       ", bg="#400000", variable = value1, value = "#400000", command = appliquer).grid(row=4, column=0)
        Radiobutton(palette, text="       ", bg="#804000", variable = value1, value = "#804000", command = appliquer).grid(row=4, column=1)
        Radiobutton(palette, text="       ", bg="#004000", variable = value1, value = "#004000", command = appliquer).grid(row=4, column=2)
        Radiobutton(palette, text="       ", bg="#004040", variable = value1, value = "#004040", command = appliquer).grid(row=4, column=3)
        Radiobutton(palette, text="       ", bg="#000080", variable = value1, value = "#000080", command = appliquer).grid(row=4, column=4)
        Radiobutton(palette, text="       ", bg="#000040", variable = value1, value = "#000040", command = appliquer).grid(row=4, column=5)
        Radiobutton(palette, text="       ", bg="#400040", variable = value1, value = "#400040", command = appliquer).grid(row=4, column=6)
        Radiobutton(palette, text="       ", bg="#400080", variable = value1, value = "#400080", command = appliquer).grid(row=4, column=7)

        Radiobutton(palette, text="       ", bg="#000000", variable = value1, value = "#000000", command = appliquer).grid(row=5, column=0)
        Radiobutton(palette, text="       ", bg="#808000", variable = value1, value = "#808000", command = appliquer).grid(row=5, column=1)
        Radiobutton(palette, text="       ", bg="#808040", variable = value1, value = "#808040", command = appliquer).grid(row=5, column=2)
        Radiobutton(palette, text="       ", bg="#808080", variable = value1, value = "#808080", command = appliquer).grid(row=5, column=3)
        Radiobutton(palette, text="       ", bg="#408080", variable = value1, value = "#408080", command = appliquer).grid(row=5, column=4)
        Radiobutton(palette, text="       ", bg="#C0C0C0", variable = value1, value = "#C0C0C0", command = appliquer).grid(row=5, column=5)
        Radiobutton(palette, text="       ", bg="#400040", variable = value1, value = "#400040", command = appliquer).grid(row=5, column=6)
        Radiobutton(palette, text="       ", bg="#FFFFFF", variable = value1, value = "#FFFFFF", command = appliquer).grid(row=5, column=7)

        Button(palette, text="Valider", command=palette.destroy).grid(row=6, column=3)

    def paint_perso():
        palette(couleur_perso, P1, P)

    def paint_repere():
        palette(couleur_repere, R1, R)

    def paint_mur():
        palette(couleur_mur, M1, M)

    def paint_perso_ext():
        palette(couleur_perso_ext, P1, P, "E")

    def paint_repere_ext():
        palette(couleur_repere_ext, R1,  R, "E")

    def paint_mur_ext():
        palette(couleur_mur_ext, M1, M, "E")

    def paint_fond():
        palette(couleur_fond, F)


    color = Toplevel(fenetre)
    color.title("Couleurs")
    color.iconbitmap('images/couleur.ico')

    Button(color, text="couleur du personnage", width=20, height=2, command=paint_perso).grid(row=0, column=0)
    Button(color, text="couleur du contour du personnage", width=20, height=2, command=paint_perso_ext).grid(row=0, column=1)
    P1 = Canvas(color, bg='white', width=150, height=40)
    P = P1.create_rectangle(55, 10, 75, 30, fill=couleur_perso['text'], outline=couleur_perso_ext['text'])
    P1.grid(row=0, column=2)

    Button(color, text="couleur des reperes", width=20, height=2, command=paint_repere).grid(row=1, column=0)
    Button(color, text="couleur du contour du reperes", width=20, height=2, command=paint_repere_ext).grid(row=1, column=1)
    R1 = Canvas(color, bg='white', width=150, height=40)
    R = R1.create_oval(55, 10, 75, 30, fill=couleur_repere['text'], outline=couleur_repere_ext['text'])
    R1.grid(row=1, column=2)

    Button(color, text="couleur des murs", width=20, height=2, command=paint_mur).grid(row=2, column=0)
    Button(color, text="couleur des contours de murs", width=20, height=2, command=paint_mur_ext).grid(row=2, column=1)
    M1 = Canvas(color, bg='white', width=150, height=40)
    M = M1.create_rectangle(55, 10, 75, 30, fill=couleur_mur['text'], outline=couleur_mur_ext['text'])
    M1.grid(row=2, column=2)

    Button(color, text="couleur de fond", width=20, height=2, command=paint_fond).grid(row=3, column=0)
    F = Canvas(color, bg=couleur_fond['text'], width=150, height=40)
    F.grid(row=3, column=2)

    Button(color, text="Valider", width=20, height=2, command=color.destroy).grid(row=4, column=0)

#-------------------------------------------------------------------------------
fenetre = Tk()
menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=create)
menu1.add_command(label="Editer", command = edit)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.destroy)
menubar.add_cascade(label="Labyrinthe", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Solo", command=solo)
menubar.add_cascade(label="Jouer", menu=menu2)

menu3 = Menu(menubar,tearoff=0)
menu3.add_command(label="Vitesse du personnage", command=vitesse)
menu3.add_command(label="Couleurs", command=couleur)
menubar.add_cascade(label="Options", menu=menu3)

couleur_perso = Label(fenetre, text="red")
couleur_perso_ext = Label(fenetre, text="red")
couleur_repere = Label(fenetre, text="green")
couleur_repere_ext = Label(fenetre, text="black")
couleur_mur = Label(fenetre, text="black")
couleur_mur_ext = Label(fenetre, text="black")
couleur_fond = Label(fenetre, text="white")
vitesse = Label(fenetre, text = "2")

fenetre.title("Labyrinthus")
fenetre.iconbitmap('images/icon_laby.ico')
fenetre.config(menu=menubar)
fenetre.geometry('1352x683')
fenetre.mainloop()