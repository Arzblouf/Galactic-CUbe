import pyxel
from random import randint

pseudo=input("Entrez un pseudonyme :")
score=0
game_over=False

class Joueur():
    def __init__(self):
        self.x=pyxel.width/2
        self.y=pyxel.height/2
        self.width=18
        self.height=18
        self.vie=2
        self.score=0
        self.sprite_img=0
    def update(self):
        if pyxel.btn(pyxel.KEY_D):
            if self.x+self.width<321:
                self.x+=6
        if pyxel.btn(pyxel.KEY_Q):
            if self.x>1:
                self.x-=6
        if pyxel.btn(pyxel.KEY_S):
            if self.y+self.height<257:
                self.y+=6
        if pyxel.btn(pyxel.KEY_Z):
            if self.y>0:
                self.y-=6
    def draw(self):
        pyxel.blt(self.x,self.y,self.sprite_img,0,0,20,19)

class Munition():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.width=2
        self.height=6
        self.sprite_img=0
    def update(self):
        self.y-=5
    def draw(self):
        pyxel.blt(self.x,self.y,self.sprite_img,0,19,2,6)

class Petit_ennemi():
    def __init__(self):
        self.x=randint(0,pyxel.width-12)
        self.y=0
        self.width=12
        self.height=12
        self.vitesse=6
        self.sprite_img=0
    def update(self):
        self.y+=self.vitesse
    def draw(self):
        pyxel.blt(self.x,self.y,self.sprite_img,0,66,12,12)

class Gros_ennemi():
    def __init__(self):
        self.x=randint(0,pyxel.width-30)
        self.y=0
        self.width=30
        self.height=25
        self.vie=5
        self.vitesse=3
        self.sprite_img=0
    def update(self):
        self.y+=self.vitesse
    def draw(self):
        pyxel.blt(self.x,self.y,self.sprite_img,0,40,30,25)

class Bonus():
    def __init__(self):
        self.x=randint(0,pyxel.width-16)
        self.y=0
        self.width=16
        self.height=16
        self.sprite_img=0
    def update(self):
        self.y+=6
    def draw(self):
        pyxel.blt(self.x,self.y,self.sprite_img,0,25,15,15)

class Background():
    def __init__(self):
        self.x=randint(-2,pyxel.width+2)
        self.y=0
        self.width=2
        self.height=2
    def update(self):
        self.y+=5
    def draw(self):
        pyxel.rect(self.x,self.y,self.width,self.height,12)

class Game():
    def __init__(self):
        pyxel.init(320,256,fps=32,title='Shooter Ultimate Remastrered 2.0')
        self.etoile_liste=[]
        self.perso=Joueur()
        self.missile_liste=[]
        self.petit_liste=[]
        self.gros_liste=[]
        self.bonus_liste=[]
        self.etat_jeu=0
        pyxel.load("Images.pyxres")
        pyxel.run(self.update,self.draw)
    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            pyxel.quit()
        if pyxel.frame_count%4==0 and len(self.etoile_liste)<=200:
            self.etoile_liste.append(Background())
        for etoile in self.etoile_liste:
            etoile.update()
            if etoile.y>pyxel.height:
                etoile.y-=pyxel.height
        if self.etat_jeu==0:
            self.update_start()
        elif self.etat_jeu==1:
            self.update_jeu()
        elif self.etat_jeu==2:
            self.update_game_over()
    def update_start(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.etat_jeu=1
    def update_jeu(self):
        if self.perso.vie<=0:
            self.etat_jeu=2
        else:
            self.perso.update()
            if pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count%8==0:
                missile=Munition((self.perso.x+self.perso.width/2),self.perso.y)
                self.missile_liste.append(missile)
            for missile in self.missile_liste:
                missile.update()
                if missile.y+missile.height<0:
                    self.missile_liste.remove(missile)
            if pyxel.btn(pyxel.KEY_B)+pyxel.btn(pyxel.KEY_N):
                self.perso.vie+=10000
                for gros_mechant in self.gros_liste:
                    gros_mechant.vitesse=(-3)
                    gros_mechant.y=pyxel.height
                for petit_mechant in self.petit_liste:
                    petit_mechant.vitesse=(-6)
                    petit_mechant.y=pyxel.height
            if pyxel.frame_count%600==0:
                self.bonus_liste.append(Bonus())
            for bonus in self.bonus_liste:
                bonus.update()
                if bonus.y>pyxel.height:
                    self.bonus_liste.remove(bonus)
            for bonus in self.bonus_liste:
                if self.perso.x<=bonus.x+bonus.width\
                and self.perso.x+self.perso.width>=bonus.x\
                and self.perso.y<=bonus.y+bonus.height\
                and self.perso.y+self.perso.height>=bonus.y:
                    self.perso.score+=200
                    self.bonus_liste.remove(bonus)
            if pyxel.frame_count%8==0:
                self.petit_liste.append(Petit_ennemi())
            for petit_mechant in self.petit_liste:
                petit_mechant.update()
                if petit_mechant.y > pyxel.height:
                    self.petit_liste.remove(petit_mechant)
            for petit_mechant in self.petit_liste:
                for missile in self.missile_liste:
                    if petit_mechant.y+petit_mechant.height>=missile.y\
                    and petit_mechant.y<=missile.y+missile.height\
                    and petit_mechant.x+petit_mechant.width>=missile.x\
                    and petit_mechant.x<=missile.x+missile.width:
                        self.petit_liste.remove(petit_mechant)
                        self.missile_liste.remove(missile)
                        self.perso.score+=20
            for petit_mechant in self.petit_liste:
                if self.perso.x<=petit_mechant.x+petit_mechant.width\
                and self.perso.x+self.perso.width>=petit_mechant.x\
                and self.perso.y<=petit_mechant.y+petit_mechant.height\
                and self.perso.y+self.perso.height>=petit_mechant.y:
                    self.perso.vie-=1
                    self.petit_liste.remove(petit_mechant)
            if pyxel.frame_count%64==0:
                self.gros_liste.append(Gros_ennemi())
            for gros_mechant in self.gros_liste:
                gros_mechant.update()
                if gros_mechant.y>pyxel.height:
                    self.gros_liste.remove(gros_mechant)
            for gros_mechant in self.gros_liste:
                if self.perso.x<=gros_mechant.x+gros_mechant.width\
                and self.perso.x+self.perso.width>=gros_mechant.x\
                and self.perso.y<=gros_mechant.y+gros_mechant.height\
                and self.perso.y+self.perso.height>=gros_mechant.y:
                    self.perso.vie-=1
                    self.gros_liste.remove(gros_mechant)
            for gros_mechant in self.gros_liste:
                for missile in self.missile_liste:
                    if missile.x<=gros_mechant.x+gros_mechant.width\
                    and missile.x+missile.width>=gros_mechant.x\
                    and missile.y<=gros_mechant.y+gros_mechant.height\
                    and missile.y+missile.height>=gros_mechant.y:
                        gros_mechant.vie-=1
                        self.missile_liste.remove(missile)
                        self.perso.score+=50
                        if gros_mechant.vie<=0:
                            self.gros_liste.remove(gros_mechant)
    def update_game_over(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.etat_jeu=1
            self.perso.vie+=3

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5,pyxel.height-10,"Appuyez sur A pour quitter",3)
        for etoile in self.etoile_liste:
            etoile.draw()
        if self.etat_jeu==0:
            self.draw_start()
        elif self.etat_jeu==1:
            self.draw_jeu()
        elif self.etat_jeu==2:
            self.draw_game_over()
    def draw_start(self):
        pyxel.text((pyxel.width/2)-35,pyxel.height/2,"APPUYEZ SUR ENTREE",pyxel.frame_count%12)
        pyxel.text((pyxel.width/2)-35,pyxel.height/2+20,"Bienvenue "+str(pseudo),8)
        game_over=False
    def draw_jeu(self):
        pyxel.text(pyxel.width-50,10,'Score :'+str(self.perso.score),7)
        pyxel.text(10,10,'Vies :'+str(self.perso.vie),7)
        self.perso.draw()
        for missile in self.missile_liste:
            missile.draw()
        for gros_mechant in self.gros_liste:
            gros_mechant.draw()
        for petit_mechant in self.petit_liste:
            petit_mechant.draw()
        for bonus in self.bonus_liste:
            bonus.draw()
    def draw_game_over(self):
        pyxel.text(pyxel.width/2-20,pyxel.height/2-12,'GAME OVER',7)
        pyxel.text(pyxel.width/2-70,pyxel.height/2,"Appuyez sur ENTREE pour recommencer",14)
        score=self.perso.score
        game_over=True

Game()