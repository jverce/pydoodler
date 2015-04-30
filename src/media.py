import pygame


COL_White = (255, 255, 255)
COL_Black = (0, 0, 0)
COL_Pink = (255, 127, 255)
COL_Red = (255, 0, 0)
COL_Wine = (127, 0, 63)
COL_LightBlue = (0, 127, 255)
COL_Blue = (0, 0, 255)
COL_Yellow = (255, 255, 0)
COL_LightGreen = (127, 255, 0)
COL_DarkGreen = (0, 127, 0)
COL_LightGray = (191, 191, 191)
COL_DarkGray = (127, 127, 127)
COL_Orange = (255, 127, 0)
COL_Purple = (127, 0, 127)
COL_LightBrown = (191, 127, 0)
COL_DarkBrown = (127, 63, 0)
COL_Skin = (255, 127, 127)



class ImageManager:
    _images = {}
    IMG_MenuCursor = "../data/images/cursor/HandSmall.png"
    NUM_MenuCursorTip = 25
    IMG_DoodleCursor = "../data/images/cursor/fatpencilsmall.png"
    NUM_DoodleCursorTip = 0
    
    TTF_Title = "../data/fonts/Another_.ttf"
    TTF_MenuItem = "../data/fonts/Another_.ttf"
    
    @staticmethod    
    def image(name):
        try:
            image = ImageManager._images[name]
        except KeyError:
            image = pygame.image.load(name).convert_alpha()
            ImageManager._images[name] = image
        return image
    
    @staticmethod
    def text(text, font, color=(255, 255, 255), size=40):
        try:
            image = ImageManager._images[(text, font, color, size)]
        except KeyError:
            f = pygame.font.Font(font, size)
            image = f.render(text, True, color).convert_alpha()
            ImageManager._images[(text, font, color, size)] = image
        return image
    
    
class AudioManager:
    _sounds = {}
    _music = {}
    _play_state = True
    _current_sound = None
    SND_MenuItem = "../data/sounds/22267__zeuss__The_Chime.wav"
    SND_MenuMusic = "../data/sounds/GameBoardMusic.wav"
    SND_ColorSelect = "../data/sounds/70236_gdzxpo_bulle2.wav"
    SND_Pencil = "../data/sounds/66137__theta4__scribble.wav"
    
    @staticmethod
    def play(name):
        if AudioManager._play_state:
            try:
                AudioManager._current_sound.stop()
            except AttributeError:
                pass
            try:
                sound = AudioManager._sounds[name]
            except KeyError:
                sound = pygame.mixer.Sound(name)
                AudioManager._sounds[name] = sound
            AudioManager._current_sound = sound
            sound.play()  
        
    @staticmethod
    def play_music(name):
        if AudioManager._play_state:
            try:
                music = AudioManager._music[name]
            except KeyError:
                music = pygame.mixer.music.load(name)
                AudioManager._music[name] = music
            pygame.mixer.music.play(-1)
    
    @staticmethod
    def stop_music():
        if AudioManager._play_state:
            pygame.mixer.music.stop()
    
    @staticmethod
    def off():
        AudioManager.stop_music()
        AudioManager._current_sound.stop()
        AudioManager._play_state = False
    
    @staticmethod
    def on():
        AudioManager._play_state = True
            


pygame.mixer.init()
pygame.font.init()
