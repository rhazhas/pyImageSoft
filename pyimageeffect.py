from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from PIL import Image,ImageTk,ImageChops,ImageFilter

import os
#######################################
# Ce programme utilise les bobliothèques suivantes :
#   - PIL pour extraire et modifier les images
#   - Tkinter pour création de fenêtre,  menu, canvas, boites de messages et scroll
#   - Os pour l'accés aux fichiers et dossiers
#
# J'ai utlisé la programmation procedurale plutot que les classes pour rester simple
# ce qui a nécessiter l'utilisation de variables globales :lecourant pour l'id de l'image active et imagesdic qui est un
# dictionnaire qui contient les chemins des images, les noms, les references aux contenus des images.
#  Ce programme gère le cliquer glisser , le chargement d'images , quelques effets a appliquer sur les images et le zoom et
#  la sauvegarde des images traitées séparements(on peut sauvegarder chaque image seule).
#########################################"
################################
#    Quelques effets pour les appliquer sur les différentes images
################################
def diviser():
    """ permer de diviser l'image en deux parties et de les mettre cote à cote verticalement
    la ligne m fait reference a la ligne au milieu """

    global lecourant                        # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                   #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                         # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))     # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    m=lig//2                                # reference a la ligne
    for y in range(lig):                    # on parcours les lignes
        for x in range(col):                # on parcours les colonnes
            pix =im.getpixel((x,y))         # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            if y>m:                         # pour les ligne de valeurs >m on
                imtemp.putpixel((col-x-1,m+lig-y-1),pix)    # on prend le contenu de la ligne à partir de la fin
                                                            # (on inverse la moitié inférieure)
            else:
                imtemp.putpixel((x,y),pix)   # on garde le même contenu pour la partie supérieur
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto) # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                      # le même indice.
    canvas.itemconfig(indx,image=phto)         # on actualise le contenu de l'image correspondante dans le canvas

#############################################"
def inverser():
    """ permet de créer le négative du'une image  et de l'appliquer et ceci pour les trois composantes RGB
    pour chaque composante si v est la valeur de cette composante au point (x,y) on lui donnera la valeur 255-v """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(255-pix[0],255-pix[1],255-pix[2]))    # on donne à chaque composante la valeur 255-valeur
                                                                         # de la composante
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def effet1():
    """ Dans cet effet on change chaque ligne sur 2 par sa négative d'une manière alternée """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            if y%2==0:                       #  si la ligne est paire
                imtemp.putpixel((x,y),(255-pix[0],255-pix[1],255-pix[2]))  #on inverse les valeurs
            else:                            # sinon
                imtemp.putpixel((x,y),pix)   # on garde les valeurs comme elles sont
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def effet2():
    """ Dans cet effet on change prend le max de la valeur de la composante et celle complementaire pour chaque
    point de l'image """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            val0=max(pix[0],255-pix[0])      # on maximize la valeur de la composante (ici rouge)
            val1=max(pix[1],255-pix[1])      # on maximize la valeur de la composante (ici verte)
            val2=max(pix[2],255-pix[2])      # on maximize la valeur de la composante (ici bleu)
            imtemp.putpixel((x,y),(val0,val1,val2))  # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas

#############################################"
def echelleGris():
    """ effet niveau de Gris vu a la formation (voir pdf python_image page 19)"""
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            val0=0.2125*pix[0]               # pour le rouge
            val1=0.7154*pix[1]               # pour le vert
            val2=0.00721*pix[2]              # pour le bleu
            valpix=int(val0+val1+val2)       # calcul de la valeur resultante
            imtemp.putpixel((x,y),(valpix,valpix,valpix))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def colorationRouge():
    """ effet obtenu en saturant une composante des trois d'un point (x,y) ici la composante rouge """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(255,pix[1],pix[2]))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###########################################"
def filtreRouge():
    """ effet obtenu en filtrant une seule composante des trois d'un point (x,y) ici la composante rouge
    les autres auront la valeur 0 """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(pix[0],0,0))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def colorationVert():
    """ effet obtenu en saturant une composante des trois d'un point (x,y) ici la composante verte """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(pix[0],255,pix[2]))    # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###########################################"
def filtreVert():
    """ effet obtenu en filtrant une seule composante des trois d'un point (x,y) ici la composante verte
    les autres auront la valeur 0 """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(0,pix[1],0))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def colorationBleu():
    """ effet obtenu en saturant une composante des trois d'un point (x,y) ici la composante bleu """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(pix[0],pix[1],255))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###########################################"
def filtreBleu():
    """ effet obtenu en filtrant une seule composante des trois d'un point (x,y) ici la composante bleu
    les autres auront la valeur 0 """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            imtemp.putpixel((x,y),(0,0,pix[2]))   # on mets les valeurs dans l'image
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###############################################"
def countour():
    """ effet obtenu en filtrant une seule composante des trois d'un point (x,y) ici la composante bleu
    les autres auront la valeur 0 """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    imtemp=im.filter(ImageFilter.CONTOUR)
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###############################################"
def symverticale():
    """ effet de sysmetrie verticale vu en formation """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    imtemp=im.transpose(Image.FLIP_TOP_BOTTOM)
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###############################################"
def symhorizontale():
    """ effet de sysmetrie horizontale vu en formation """
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    imtemp=im.transpose(Image.FLIP_LEFT_RIGHT)
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
###############################################"
def rotation():
    """ effet de rotation d'un angle de 90 degrées vu en formation"""
    global lecourant                         # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    imtemp=im.rotate(90,Image.BICUBIC,True)
    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas
#############################################"
def  seuillage():
    """ seuillage des pixels les niveaux choisis sont 60 et 180 (on peut les modifier)"""
    global lecourant                         # variable contennant l'identifiant de l'image courante
    seuil1,seuil2=60,180
    indx=lecourant
    im=imagesdic[indx][2]                    #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                          # récupération de la taille de l'image : nombre de colonnes et de lignes
    imtemp=Image.new(im.mode,(col,lig))      # création d'une nouvelle zone image en mémoire à partir de l'ancienne
    for y in range(lig):                     # on parcours les lignes
        for x in range(col):                 # on parcours les colonnes
                                             # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            pix =im.getpixel((x,y))          # récupération dans pix le tuple triplet couleurs RGB au point (x,y)
            if pix[0]<seuil1:
                val0=0                         # pour le rouge
            elif pix[0]>seuil2:
                val0=255
            else :
                val0=pix[0]
            if pix[1]<seuil1:
                val1=0                         # pour le vert
            elif pix[1]>seuil2:
                val1=255
            else :
                val1=pix[1]
            if pix[2]<seuil1:
                val2=0                         # pour le bleu
            elif pix[2]>seuil2:
                val2=255
            else :
                val2=pix[2]
            valpix=int(val0+val1+val2)       # calcul de la valeur resultante
            imtemp.putpixel((x,y),(valpix,valpix,valpix))   # on mets les valeurs dans l'image

    phto = ImageTk.PhotoImage(imtemp)        # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],imtemp,phto)  # on sauvegarde dans le dictionnaire le nuveau contenu avec
    imagesdic[indx]=a                                       # le même indice.

    canvas.itemconfig(indx,image=phto)       # on actualise le contenu de l'image correspondante dans le canvas

################################
# affiche l'info
###############################
def infos():
    """ cette fonction affiche une boite de message de tkinter avec le texte ci dessous
    showinfo : méthode de la classe messagebox de tkinter """
    showinfo("Information: Apropos", "Petit Travail Réalisé par El rhazali \n CPGE TAZA")
#################################"
# Creation du menu
#################################
def creeMenu(fene):

    """ création du menu principal qui s'affiche dans la fenêtre
        pour créer un menu on commence par créer un menu en mémoire et l'associer à une fenetre à l'aide de la commande Menu
        puis on ajoute soit un autre menu qui sera donc un sous menu avec Menu et on l'ajoute à l'aide de add_cascade
        on ajoute une commande à l'aide de add_command, on ajoute un séparateur à l'aide de add_separator à la fin on ajoute
        à la fenetre à l'aide de config qui permet de configurer pas mal de option on ajoute l'option menu.

    """

    menubar = Menu(fene)                                            #création d'un menu en mémoire
    menu1 = Menu(menubar, tearoff=0)                                # creation d'un sous menu du menu principal
    menu1.add_command(label="Ouvrir...", command=chargerImage)      # ajouter une option commande dans ce sous menu command
     #designe la fonction callback fonction qui sera appellée lors du click. le texte affiché dans le label du menu ici c'est
     # "ouvrir"
    menu1.add_command(label="Enregistrer...", command=sauveImage)  # même chose que ici pour enregistrer
    menu1.add_separator()                                #création d'une ligne de séparation dans le sous menu
    menu1.add_command(label="Quitter", command=quitter) # ici commande pour sortir la fonction appelée est quitter(voir ci dessous)
    menubar.add_cascade(label="Fichier", menu=menu1)    # ajout du sous menu menu1 à la barre menu avec l'etiquete "fichier"

    menu2 = Menu(menubar, tearoff=0)              # Création d'un autre sous menu du menu principal
    mncouleurs=Menu(menu2,tearoff=0)                # création d'un sous menu du menu menu2  : coloration
    mnfiltre=Menu(menu2,tearoff=0)                # création d'un sous menu du menu menu2  : filtres
    menu2.add_cascade(label="Coloration", menu=mncouleurs)      #ajout de l'etiquette du sous menu couleur dans le sous menu 2
    menu2.add_separator()                      # ajout d'un séparateur dans le menu2
    menu2.add_cascade(label="filtre", menu=mnfiltre)      #ajout de l'etiquette du sous menu couleur dans le sous menu 2
    menu2.add_separator()
    menu2.add_command(label="Seuillage",command=seuillage)  # ajoute un effet de seuillage vue en formation
    menu2.add_command(label="Contour",command=countour)     # ajout l'effet de detection de contour vu en formation
    menu2.add_separator()                                   # ajout d'un séparateur dans le menu 2 : effets menu2.add_separator()
    mntransformation=Menu(menu2,tearoff=0)                  #creation du menu transformation
    menu2.add_cascade(label="Transformations",menu=mntransformation)  # ajout de l'etiquette transformations au menu 2
    menu2.add_separator()                                   #ajout d'un separateur
    menu2.add_command(label="Echelle de gris", command=echelleGris)   #  les commandes du menu 2 effets ici niveau du gris
    menu2.add_command(label="Diviser", command=diviser)                 # ici diviser l'image
    menu2.add_command(label="Négatif", command=inverser)                # negatif
    menu2.add_command(label="Effet 1", command=effet1)                  # alterner les lignes d'une image
    menu2.add_command(label="Effet 2", command=effet2)                  # max des valeurs de composante
    menu2.add_separator()                                       # ajout d'un séparateur dans le menu 2 : effets

    menu2.add_command(label="Zoom +", command=zoomPlus)         # commande zoom+
    menu2.add_command(label="Zoom -", command=zoomMoins)        # commande zoom-
    menubar.add_cascade(label="Effets", menu=menu2)             # affichage de l'etiquette effet au menu bar
    menu3 = Menu(menubar, tearoff=0)                            # creation d'un troisieme sous menu: aide
    menu3.add_command(label="A propos", command=infos)          # commande du sous menu aide
    menubar.add_cascade(label="Aide", menu=menu3)               # ajout de l'etiquette Aide au menu principal

    mncouleurs.add_command(label="Rouge",command=colorationRouge)   # commande du sous menu niveau 2 : coloration ici rouge
    mncouleurs.add_command(label="Vert",command=colorationVert)     # commande pour le vert
    mncouleurs.add_command(label="Bleu",command=colorationBleu)     # ici bleu

    mnfiltre.add_command(label="Rouge",command=filtreRouge)   # commande du sous menu niveau 2 : coloration ici rouge
    mnfiltre.add_command(label="Vert",command=filtreVert)     # commande pour le vert
    mnfiltre.add_command(label="Bleu",command=filtreBleu)     # ici bleu
    mntransformation.add_command(label="Symetrie verticale",command=symverticale)  # ajout des commandes syemtrie verticale
    mntransformation.add_command(label="Symetrie Horizontale", command=symhorizontale) # et symetrie horizontale
    mntransformation.add_command(label="Rotation", command=rotation)        # et rotation
    fene.config(menu=menubar)                                       # affectation du menu principal à la fenetre

###########################"
# quitter l'application
#########################
# def changevert():
#     pas=scvert.get()
#     canvas.yview_moveto(pas/400)
#
# def changehor():
#     pas=schoriz.get()
#     canvas.xview_moveto(pas)
def quitter():
    """ la fonction appelée à partir de la commande quitter du menu """
    if askyesno("Sortir","Voulez vous sortir"):     # on affiche une boite de confirmation avec les boutons yes no
       fen.quit()                       # si la reponse est yes on quit et
       fen.destroy()                    # detruit la fenetre de la memoire
##############################
# Zoomin plus
############################

def zoomPlus():
    """ on agrandit les dimensions de l'image d'un facteur de 1.2 ce qui augmente la taille et ceci en largeur et hauteur  """
    global lecourant                                # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                            #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                                  # récupération de la taille de l'image : nombre de colonnes et de lignes

    ncol,nlig=int(col*1.2),int(lig*1.2)              # nouvelle largeur et hauteur calculées
    im=im.resize((ncol,nlig),Image.ANTIALIAS)        #redimensionde l'image
    phto= ImageTk.PhotoImage(im)                     # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],im,phto) # on sauvegarde dans le dictionnaire les modifications avec
    imagesdic[indx]=a                               # le même indice.
    canvas.itemconfig(indx,image=phto)              # on actualise le contenu de l'image correspondante dans le canvas
##############################
# Zoomin  moins
############################

def zoomMoins():
    """ on reduit les dimensions de l'image d'un facteur de 0.8 ce qui diminue la taille et ceci en largeur et hauteur  """
    global lecourant                                # variable contennant l'identifiant de l'image courante
    indx=lecourant
    im=imagesdic[indx][2]                            #on récupère la référence de l'image à traiter à partir du dictionnaire
    col,lig=im.size                                  # récupération de la taille de l'image : nombre de colonnes et de lignes

    ncol,nlig=int(col*0.8),int(lig*0.8)             # nouvelle largeur et hauteur calculées
    im=im.resize((ncol,nlig),Image.ANTIALIAS)        #redimensionde l'image
    phto= ImageTk.PhotoImage(im)                     # on passe cette zone sous forme d'image
    a=(imagesdic[indx][0],imagesdic[indx][1],im,phto) # on sauvegarde dans le dictionnaire les modifications avec
    imagesdic[indx]=a                               # le même indice.
    canvas.itemconfig(indx,image=phto)              # on actualise le contenu de l'image correspondante dans le canvas
#################################"
#  chargement des images
###################################
def chargerImage():
    """ fonction qui permet de  charger une nouvelle image est de l'ajouter au canvas"""
    nom_fichier=askopenfilename(title="Ouvrir une image",filetypes=[('fichiers jpg','.jpg'),('fichier gif','.gif'),('fichier png','.png'),('Tous les fichiers','.*')])
    # boite de message ouvrir un fichier qui permet de chercher une image sur l'ordinateur et de la charger
    # on filtre les images de type jpg, gif,png
    if not nom_fichier:
        return
    img1 = Image.open(nom_fichier)  #on ouvre le fichier
    nomph=  donneNom(nom_fichier)   # on récupère son nom sans extension

    phto = ImageTk.PhotoImage(img1) #on charge l'image

    indx=canvas.create_image(0,0,anchor=NW, image=phto,tag=nomph) # création dans le canvas d'un nouveau
                                                                                    #    objet image

    imagesdic[indx]=(nomph,nom_fichier,img1,phto)  #on ajoute l'image dans le dictionnaire

    canvas.move(nomph,100,100)      # on deplace la nouvelle image à la position (100,100) dans le canvas : on peut modifier
#####################################
#  sauvegarde d'une image
######################################
def sauveImage():
    """ cette fonction permet de sauver l'image courante sur le disque"""
    global lecourant  # variable contennant l'identifiant de l'image courante
    indx=lecourant
    titre = "Sauver l'image courante as" #le titre de la boite de message sauvegarder
    ftypes = [('Image jpeg', '.jpg'), ('All files', '*')] #les extensions des images à sauvegarder
    nomfichier = asksaveasfilename(filetypes=ftypes, title=titre,
                                     defaultextension='.jpg') # appel à la boite de dialogue enregistrer
    if not nomfichier:  # si le nom du fichier n'est pas donné, on fera rien
        return
    phto=imagesdic[indx][2]   #sinon on recupère l'image du dictionnaire
    phto.save(nomfichier)       # et on l'neregistre

##############################
# pour l'evenement roulette de la souris
#################################
def rollWheel(event):
    """ fonction s'éxecutant lorsqu'on defile la roulette de la souris"""
    if event.num == 4 or event.delta==-120:    # si delta la deviation de la roulette vers le haut
        canvas.xview('scroll', -1, 'units')    #on defile le canvas horizontalement vers la gauche d'une unité
    elif event.num == 5 or event.delta==120:    # sinon
        canvas.xview('scroll', 1, 'units')      # on défile le canvas horizontalement vers la droite d'une unité
####################################"
# extraction du nom du fichier image sans extension
######################################
def donneNom(path):
      return path.split("/")[-1].split(".")[0]   # on recupère le nom du fichier sans extension à partir de son chemin complet
#####################################
# slection d'une image du canvas
####################################"
def selectionne(event):
    """ Fonction lancée au click sur une image qu'elle soit en avant plan ou en arrière plan"""
    global lecourant   # variable contennant l'identifiant de l'image courante
    ind=canvas.find_closest(event.x,event.y,halo=5) # recupération de l'id de l'image sur laquelle on clique
    if ind!=None:    # si on a l'id
        indx=ind[0]

        lecourant=indx   # on l'affecte a la variable lecourant
        #print(lecourant)
        canvas.tag_raise(indx,ALL)  # on met cette image en avant plan
        canvas.tag_bind(indx,"<B1-Motion>",picmove) #on lui attache l'evenement cliquer glisser avec action :appel
                                                        # à la fonction picmove
        canvas.tag_bind ( indx, "<Button-3>", relache ) # on attache aussi l'actionde relacher le bouton à relache

 #################################
 # deplacement d'une image
 ##################################
def picmove(event):
    """  fonction attachée à l'evenement cliquer glisser et qui permet de deplacer l'image avec la souris"""
    x,y=event.x,event.y   # recupération des coordonnées x,y de la souris
    canvas.coords(CURRENT,x,y) # affectation de la position de l'objet dont l'id est dans la variable CURRENT la position (x,y)
#############################
# fonction s'executnt au relachement du bouton de la souris
################################
def relache(event):
    """ lorsqu'on relache le bouton droit de la souris, on affiche la pile des ID des images qui sont dans le canvas """
    print(canvas.find_all())
#################################"
#  initialisation de l'application
#############################"##
def initialisation():
   """ initialisation de l'application creation de la fenetre, dimensionnement, titre, defilement,  etc"""
   fen= Toplevel()  #modification ***************                    # creation d'une fenetre en mémoire
   fen.size=(1200,500)          # dimension de la fenetre 1200,500
   fen.title("Gestionnaire d'images") # titre de la fenetre
   creeMenu(fen)                        # création du menu : appel à la fonction creemenu definie en haut
   canvas = Canvas(fen, width =500, height = 400,cursor="hand1",borderwidth=2, relief=GROOVE,scrollregion=(0,0,500,500),bg ="dark orange") # création d'un canvas avec les dimension et le type de curseur et la bordure et la couleur de fond
        # et la region defilable
   sbarV = Scrollbar(fen, orient=VERTICAL) # définition de la barre de défilement verticale
   sbarH = Scrollbar(fen, orient=HORIZONTAL) # definition de la barre de défilement horizontale
   sbarV.config(command=canvas.yview)   #configuration de la commande a utiliser
   sbarH.config(command=canvas.xview)
   canvas.config(yscrollcommand=sbarV.set) #affectation de la barre de defilement vertical à celle du canva
   canvas.config(xscrollcommand=sbarH.set) #affectation de la barre de defilement horizontal à celle du canva

   sbarV.pack(side=RIGHT, fill=Y)  # actualisation de la barre verticale
   sbarH.pack(side=BOTTOM, fill=X)  # actualisation de la barre horizontale
   fen.bind("<MouseWheel>", rollWheel)  #affectation de l'evenement defilement de la souris(la roulette de la souris) à la fenêtre
   canvas.pack(side=LEFT, expand=YES, fill=BOTH)        # actualisation du canvas : disposition

   return fen,canvas  # recuperation des references de la fenetre et du canvas

##############################################
#Programme principal
#############################################"
lecourant=None    # variable contennant l'identifiant de l'image courante
imagesdic={}     # creation d'un dictionnaire vide
fen,canvas=initialisation()   #initialisation
largeur,hauteur=800,600         # dimensions nouvelles pour la zone de défilement
canvas.config(scrollregion=(0,0,largeur,hauteur)) # affectation de cette zone au canvas
text_id = canvas.create_text(20, hauteur//3, anchor="nw") # creation d'un element texte qui sera ajouter au canvas
                                        # position : 20, hauteur//3
canvas.itemconfig(text_id, text="Programme python pour la gestion des images avec quelques effets, enjoy:)") # affectation du texte
canvas.bind("<Button-1>", selectionne) # on affecte le click gauche sur le canvas à la fonction selectionne définie en haut
fen.mainloop()       # boucle principale d'execution de l'application