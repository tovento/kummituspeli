#Pelissä ohjataan ystävällistä kummitusta nuolinäppäimillä (oik/vas).
#Tavoitteena on pelastaa mahdollisimman monta putoavaa robottia.
#Peli loppuu, kun kymmenen robottia on menetetty.

import pygame
import random

class Robotti:
    maxnopeus = 1

    def __init__(self, peli: 'Kummituspeli'):
        self.x = random.randint(0,640-Kummituspeli.robo_leveys)
        self.y = 0 - Kummituspeli.robo_korkeus
        self.pelastunut = False
        self.peli = peli
        self.nopeus = self.laske_nopeus()

    def liike(self):
        if self.pelastunut:
            self.pelastu()
        else:
            self.putoaminen()

    def putoaminen(self):
        self.y +=self.nopeus

    def pelastu(self):
        #robotin liikkeet pelastumisen jälkeen: 
        if self.y > 480-Kummituspeli.robo_korkeus:
            self.y-=self.nopeus
        elif self.y < 480-Kummituspeli.robo_korkeus:
            self.y+=self.nopeus
        else:
            if self.x <320-Kummituspeli.robo_leveys:
                self.x -= self.nopeus
            elif self.x >=320-Kummituspeli.robo_leveys:
                self.x += self.nopeus

    def laske_nopeus(self):
        #robottien liikkumisnopeus vaihtelee, lasketaan kullekin robolle nopeus:
        return random.randint(1, Robotti.maxnopeus)

    @classmethod
    #lisätään maksiminopeutta joka 5. pelastetun robotin jälkeen:
    def laske_max_nopeus(cls, peli):
        if peli.pelastuneet_laskuri() > peli.menetetyt_laskuri():
            Robotti.maxnopeus = peli.pelastuneet_laskuri()//5 + 1
                

class Kummituspeli:
    robo = pygame.image.load("robo.png")
    kummitus = pygame.image.load("hirvio.png")
    robo_korkeus = robo.get_height()
    robo_leveys = robo.get_width()
    kummitus_korkeus = kummitus.get_height()
    kummitus_leveys = kummitus.get_width()

    def __init__(self):
        pygame.init()
        self.naytto = pygame.display.set_mode((640,480))
        self.kummitus_x = 320-Kummituspeli.kummitus_leveys//2
        self.kummitus_y = 480-Kummituspeli.kummitus_korkeus
        pygame.display.set_caption("Kummituspeli")
        self.kello = pygame.time.Clock()
        self.roboja = []
        self.fontti = pygame.font.SysFont("Arial", 24)

        self.silmukka()
    

    def putoavat_robotit(self):
        #arvotaan, putoaako uusi robotti, nro 1 pudottaa:
        roboarvonta = list(range(1,105))
        putoaako = random.choice(roboarvonta)
        if putoaako == 1:
            uusirobo = Robotti(self)
            self.roboja.append(uusirobo)
        Robotti.laske_max_nopeus(self)
        for robotti in self.roboja:
            robotti.liike()
            self.naytto.blit(Kummituspeli.robo,(robotti.x,robotti.y))           

    def silmukka(self):
        oikealle = False
        vasemmalle = False
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = True
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = True
                    if tapahtuma.key == pygame.K_ESCAPE:
                        exit()
                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikealle = False
                    if tapahtuma.key == pygame.K_LEFT:
                        vasemmalle = False

            if oikealle:
                self.kummitus_oikealle()
            if vasemmalle:
                self.kummitus_vasemmalle()
            
            self.naytto.fill((255,204,153))
            
            self.putoavat_robotit()
            self.piirra_tilastot()
            if self.game_over():
                while True:
                    self.game_over_ruutu()
                    for tapahtuma in pygame.event.get():
                        if tapahtuma.type == pygame.QUIT:
                            exit()

            self.naytto.blit(Kummituspeli.kummitus,(self.kummitus_x,self.kummitus_y))
            pygame.display.flip()
            self.tarkista_osumat()
            self.kello.tick(60)       

    def kummitus_oikealle(self):
        if self.kummitus_x < 640-Kummituspeli.kummitus_leveys:
            self.kummitus_x+=2

    def kummitus_vasemmalle(self):
        if self.kummitus_x > 0:
            self.kummitus_x-=2

    def tarkista_osumat(self):
        #tarkistetaan, koskettaako kummitus robotteja:
        for robotti in self.roboja:
            for i in range(self.kummitus_x, self.kummitus_x+Kummituspeli.kummitus_leveys+1):
                if i in range(robotti.x, robotti.x+Kummituspeli.robo_leveys+1):
                    for j in range(self.kummitus_y, self.kummitus_y+Kummituspeli.kummitus_korkeus+1):
                        if j in range(robotti.y, robotti.y+Kummituspeli.robo_korkeus+1):
                            robotti.pelastunut = True

    def game_over(self):
        if self.menetetyt_laskuri() >=10:
            return True

    def game_over_ruutu(self):
        self.naytto.fill((0,51,102))
        fontti2 = pygame.font.SysFont("Arial", 50)
        teksti1 = fontti2.render("GAME OVER", True,(255,0,0))
        teksti2 = fontti2.render("Pelastit " + str(self.pelastuneet_laskuri()) + " robottia", True,(255,0,0))
        teksti3 = fontti2.render("Pelastit 1 robotin", True,(255,0,0))
        self.naytto.blit(teksti1,(320-teksti1.get_width()/2,100))
        if self.pelastuneet_laskuri() == 1:
            self.naytto.blit(teksti3,(320-teksti3.get_width()/2,200))
        else:
            self.naytto.blit(teksti2,(320-teksti2.get_width()/2,200))
        pygame.display.flip()

    def pelastuneet_laskuri(self):
        return len([robo for robo in self.roboja if robo.pelastunut])
    
    def menetetyt_laskuri(self):
        return len([robo for robo in self.roboja if not robo.pelastunut and robo.y >=480])

    def piirra_tilastot(self):
        #tilastoikkuna, johon lisätty hieman läpinäkyvyyttä:
        s = pygame.Surface((640,70))
        s.set_alpha(210)
        s.fill((96,96,96))
        self.naytto.blit(s,(0,0))
        teksti = self.fontti.render("Pelastuneita: " + str(self.pelastuneet_laskuri()) + " Menetettyjä: " + str(self.menetetyt_laskuri()), True, (255,102,102))
        self.naytto.blit(teksti,(20,20))


Kummituspeli()