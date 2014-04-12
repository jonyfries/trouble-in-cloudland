import utility
import pygame
import actor
import text
import vector
import animation
import copy
import infoBubble

from actor import *

def loadData():
    Balloon.pickupSound = utility.loadSound("pop")
    Bonus250.MasterAnimationList.buildAnimation("Idle","balloonblue")
    Bonus500.MasterAnimationList.buildAnimation("Idle","balloongreen")

    BonusX2.MasterAnimationList.buildAnimation("Idle","balloonred")
    BonusX2.pickupSound = utility.loadSound("doublePoints")
    BonusCombo.MasterAnimationList.buildAnimation("Idle","balloonyellow")
    BonusCombo.pickupSound = utility.loadSound("combo")


class Balloon(actor.Actor):
    def __init__(self):
        actor.Actor.__init__(self)
        self.actorType = ACTOR_TYPE_PICKUP
        self.boundStyle = BOUND_STYLE_KILL
        self.bounds = [-32,-32,SCREEN_WIDTH + 32, SCREEN_HEIGHT + 32]
        
        """    MOVEMENT VARIABLES    """
        self.wave = 0
        self.moveRight = True
        self.XMovement = 1
        self.velocity = vector.vector2d.zero

    def actorUpdate(self):
        self.active = True
        
        if self.moveRight:
            self.wave -= 1
            if self.wave < -0.20 * FRAMES_PER_SECOND:
                self.moveRight = False
        else:
            self.wave += 1
            if self.wave > FRAMES_PER_SECOND:
                self.moveRight = True

        self.XMovement = (self.wave / (FRAMES_PER_SECOND)) * 1.5
        self.velocity = vector.vector2d(self.XMovement,-3)

    def collide(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            utility.playSound(self.pickupSound)
            self.die()
 
class Bonus250(Balloon):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):
        Balloon.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle") 

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0,0,60,60)
        self.hitrectOffsetY = -5
        
        self.textGroup = textGroup
        self.position = vector.vector2d(position)

    def die(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.incrementScore(250, self.position, self.textGroup)
        
        self.active = False
        self.kill()
        del self

class Bonus500(Balloon):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):
        Balloon.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle") 

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0,0,60,60)
        self.hitrectOffsetY = -5
        
        self.textGroup = textGroup
        self.position = vector.vector2d(position)

    def die(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.incrementScore(500, self.position, self.textGroup)
        
        self.active = False
        self.kill()
        del self

class BonusX2(Balloon):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):
        Balloon.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle") 

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0,0,60,60)
        self.hitrectOffsetY = -5
        
        self.position = vector.vector2d(position)
        self.textGroup = textGroup



    def die(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.pointBonus += 5 * FRAMES_PER_SECOND
            tempImage = text.Text(FONT_PATH, 30, FONT_COLOR, "Double Points!", 1).image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.objectCollidedWith,1.5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            self.textGroup.add(helpBubble)
        
        self.active = False
        self.kill()
        del self

class BonusCombo(Balloon):
    MasterAnimationList = animation.Animation()
    def __init__(self, position, textGroup):
        Balloon.__init__(self)
        
        self.animationList = copy.copy(self.MasterAnimationList)
        self.animationList.setParent(self)
        self.animationList.play("Idle") 

        self.rect = self.image.get_rect()        
        self.hitrect = pygame.Rect(0,0,60,60)
        self.hitrectOffsetY = -5
        
        self.position = vector.vector2d(position)
        self.textGroup = textGroup



    def die(self):
        if self.objectCollidedWith.actorType == ACTOR_PLAYER:
            self.objectCollidedWith.comboBonus += 5 * FRAMES_PER_SECOND
            tempImage = text.Text(FONT_PATH, 30, FONT_COLOR, "Combo Time!", 1).image
            
            helpBubble = infoBubble.infoBubble(tempImage, self.objectCollidedWith,1.5 * FRAMES_PER_SECOND)
            helpBubble.offSet = vector.vector2d(0.0, -100.0)
            self.textGroup.add(helpBubble)
        
        self.active = False
        self.kill()
        del self