#projet code huffman
import os







def lirecara(fichier):
    """
    fonction qui regarde tout les caractère du fichier et en fait un dictionnaire associant à chaque caractère sa fréquence 
    """
    with open(fichier,"r") as file:
            dicocara={}
            text=file.read()
            for k in range(0,len(text)):
                if  text[k] in dicocara.keys() :
                    dicocara[text[k]]=dicocara[text[k]]+1
                else:
                    dicocara[text[k]]=1
            
            return dicocara
    

def triaski(dico):
    """
    prend argument le dictionnaire de caractère 
    et en fait un nouveau avec les caractère triés dans l'ordre askii 

    """
    dicoaskii={}
    for cara,freq in dico.items():
        """
        transforme les le dictionnaire de caractere en dictionnaire askii
        """
        dicoaskii[ord(cara)]=freq
    keyaskii=dicoaskii.keys()
    keyaskiitrie=sorted(keyaskii)  #retourne une liste askii triée 
    keyaskiitrie.reverse() 
    
    dicoaskiitriee={}
    for k in keyaskiitrie:
        """
        transforme la liste en nouveau dictionnaire
        """
        dicoaskiitriee[k]=dicoaskii[k]
    dicofinal={}
    for caraaskii,freq in dicoaskiitriee.items():
        """
        repasse avec des caractère et non pas en code askii
        """
        dicofinal[chr(caraaskii)]=freq
    return dicofinal 
    
    

    
def code(fichier):
    """
    prend en argument le fichier et retourne la liste des caractère avec leur fréquence triée par frequence  et code askii si même fréquence 
    utilise les fonction lire cara et triaskii
    """
    dic=lirecara(fichier)
    dictriaski=triaski(dic)
    
    listefinal=sorted(dictriaski.items(), key=lambda t: t[1]) #tri par rapport aux frequence 
    listefinal.reverse()
    return listefinal
    
    
class arbre:
    """
    class arbre permettant de faire des arbre (ici binaire )
    """
    def __init__(self,cara,frequence,FD,FG) :
        """
        un arbre a besoin d'un caractere d'une frequence d'un fils gauche et droit qui peuvent être nul 
        """
        
        self.cara=cara
        self.frequence=frequence
        self.FD=FD
        self.FG=FG
    def get_frequence(self):
        return self.frequence
    def get_cara(self):
        return self.cara
    def get_FD(self):
        return self.FD
    def get_FG(self):
        return self.FG
    
    
        
    
    def parcours(self):
        """
        fonction qui parcours l'arbre en profondeur et qui associe un code binaire à chaque noeux
        """
        listcode=[] #liste qui garde le code de chaque caractère
        listeparcours=[[self,'0']]#on commence par la racine de l'arbre on lui associe  0 comme code binaire  
        while listeparcours!=[]:# temps qu'on a pas traité tout la liste il nous reste des noeux à parcourire 
            """
             on traite le premier terme de la liste   
            """
            if listeparcours[0][0].get_FG()!=None:# si le fils gauche n'est pas nul on lui donne le code de son père+0 et on le place dans la liste a traiter juste apres son père
                listeparcours=[listeparcours[0]]+[[listeparcours[0][0].get_FG(),listeparcours[0][1]+'0']]+listeparcours[1:] 
                
                
            if listeparcours[0][0].get_FD()!=None: # de meme que le fils gauche juste le code est 1 et pas 0 et on le place apres le fils gauche dans la liste si il existe 
                listeparcours=listeparcours[0:2]+[[listeparcours[0][0].get_FD(),listeparcours[0][1]+'1']]+listeparcours[2:]
            
            
            listcode.append(listeparcours.pop(0)) #le premier terme a été traité on peut le supprimer mais on garde son code dans une autre liste     
            
            
        return listcode





    def __str__(self):
        return self.cara
    
    def __repr__(self):
        return self.__str__()
    
    
        







def feuille(liste):
    """
    fait la liste des feuille qui serons presente dans l'arbre a partir de la liste des caractère et leur frequence
    """
    listfeuille=[]
    
    
    for k in range(0,len(liste)):
       
        listfeuille.append(arbre(liste[k][0],liste[k][1],None,None))
    return listfeuille 
    

def arbretotal(listfeuille):
    """
    crée l'arbre a partir de la liste des feuille qu'on a fait avant la liste des feuille est trié par frequence décroissance 
    """
    lf=listfeuille.copy()
    
   
    while len(lf)>1 :
        """
        on prend les 2 terme de plus basse frequence et on les remplace par un nouvelle arbre qui les prend pour fils gauche et fils droit et qui a pour frequence la somme de ces 2 termes  
        """
        t1=lf.pop()
        
        t2=lf.pop()
        t1freq=t1.get_frequence()
        t2freq=t2.get_frequence()
      
        
        t=t1freq+t2freq
        
        
        nouvelle=(arbre('t'+str(t),t,t1,t2 ))
        
        for i in range(0,len(lf)):#pour savoir ou integrer le nouvelle arbre dans la liste des feuilles 
            if nouvelle.get_frequence()<lf[i].get_frequence():
                ifi=i
                    
        lf.insert(ifi,nouvelle)

        

   
    return lf[0] # retourne la racine de l'arbre 


def recupcodecara(listefeuille,listeparcours):
    """ 
    focntion qui recupere un dictionnaire avec les caractère d'origine et leur code binaire associé 

    """
    
    caracode={}
    for k in listefeuille: 
        for i in range(0,len(listeparcours)):
            if k==listeparcours[i][0]: # recupere la liste de feuille d'origine present dans liste des noeux parcouru
                caracode[listeparcours[i][0].get_cara()]=listeparcours[i][1]
    return caracode


def codage(dico,fichier):
    """
    regarde tout les caractère du fichier et fait un nouveau texte en les remplacant par leur code 
    """
    
    with open(fichier,"r") as file:
        text=file.read()
        newtext=''
        for k in  text: #code le caractère par son nouveau code et l'ajoute au précèdent 
            newtext=newtext+dico[k]
    return newtext
            
            
def octet(textcode):
    """
    code en octet le texte binaire
    """
    inttext=int(textcode,2)
    
    
    longeur = (inttext.bit_length() + 7) // 8 #nombre octet nécessaire
    octets = inttext.to_bytes(longeur, byteorder='big') #code en octet
    
    return octets
    
def stockfichier(chemincomp,octet):
    """
    ecrit le fichier compressé dans un nouveau fichier 
    """
    with open(chemincomp,'wb') as fichiercompr:
        fichiercompr.write(octet)
    

def tauxcompression(text,textcompr):
    """
    retourne le taux de compression en comparant la taille du fichier compressé et original
    """
    
    tailletext = os.path.getsize(text)
    tailletextcompr = os.path.getsize(textcompr)
    return(1-tailletextcompr/tailletext)

    
def bitcara(chemin,textcoder):
    """
    determine le nombre de bit moyen pour coder un caractère du fichier
    """
    with open(chemin,'r') as file:
        text=file.read()
        n=len(text) #nombre caractère original
    nbit=len(textcoder)#nombre bit quand le texte et codé
    return nbit/n

        


 


    
   

def codagefinal(chemin,chemincomp):
    """
    utilise les fonction précèdentes pour a partir d'un fichier crée un nouveau fichier avec le contenu compressé et affiche le taux de compression et le nombre de bit moyen par caractère
    """


    liste=(code(chemin))
    print(liste)

    listefeuilles=feuille(liste)

    arbree=arbretotal(listefeuilles)




    listeparcours=arbree.parcours()

    dicoletrecode=recupcodecara(listefeuilles,listeparcours)

    codagee=codage(dicoletrecode,chemin)
    

    octets=octet(codagee)
    stockfichier(chemincomp,octets)
    print(tauxcompression(chemin,chemincomp))
    print(bitcara(chemin,codagee))

chemintext="C:/Users/Lois/Desktop/projet info 631/textesimple.txt"
cheminalice="C:/Users/Lois/Desktop/projet info 631/alice.txt"
chemintextcomp="C:/Users/Lois/Desktop/projet info 631/textesimplecomp.txt"
cheminalicecomp="C:/Users/Lois/Desktop/projet info 631/alicecomp.txt"
chemin=cheminalice
chemincomp=cheminalicecomp
codagefinal(chemin,chemincomp)
