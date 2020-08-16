import pygame
from joblib import dump, load
from sklearn.neural_network import MLPClassifier


ar = []
X_train = load('X_train.joblib')
y_train = load('y_train.joblib') 
counter = len(y_train)
model = load('model.joblib')

pygame.init()
pygame.font.init()
    
for y in range(20):
    for x in range(20):
        ar.append([(x * 20, y * 20, 20, 20), 0])        
     
screen = pygame.display.set_mode((500, 400))
screen.fill((0, 0, 0))
pygame.display.set_caption("Digit recognizer")
running = True

def drawComponents():
    #control panel
    pygame.draw.rect(screen, (180, 180, 180), (400, 0, 100, 400))
    
    #clear button
    pygame.draw.rect(screen, (255, 0, 255), (410, 10, 80, 30))
    myfont = pygame.font.SysFont('Comic Sans MS', 28)
    textsurface = myfont.render('Clear', False, (0, 0, 0))
    screen.blit(textsurface,(413, 6))
    
    #predict button
    pygame.draw.rect(screen, (255, 255, 0), (410, 50, 80, 30))
    myfont = pygame.font.SysFont('Comic Sans MS', 22)
    textsurface = myfont.render('Predict', False, (0, 0, 0))
    screen.blit(textsurface,(413, 48))
    
    pygame.display.update()
    for rec_col in ar:
        c = rec_col[1]
        r = rec_col[0]
        pygame.draw.rect(screen, (c * 255, c * 255, c * 255), r)

def showResult(y):
    myfont = pygame.font.SysFont('Comic Sans MS', 22)
    textsurface = myfont.render('I think', False, (0, 0, 0))
    screen.blit(textsurface,(413, 90))
    textsurface = myfont.render('it is', False, (0, 0, 0))
    screen.blit(textsurface,(413, 120))
    pygame.display.update()
    
    
def clear():
    for x in range(20 * 20):
        ar[x][1] = 0
      
def predict():
    #preparing input data
    X_train.append([])
    global counter
    for t in ar:
        X_train[counter].append(t[1])
    counter += 1
    
    #predicting
    y = model.predict([X_train[-1]])
    print('I think it is', y[0])
    s = input("Am I right? (y/n)\n")
    if s[0] == 'n' or s[0] == 'N':
        y[0] = int(input('Please, input correct answer: '))
    y_train.append(y[0])
    model.fit(X_train, y_train)
    clear()
    
"""
def correct():
    model.fit(X_pred, y)
    saveModel()
def wrong():
    model.fit(X_pred, y_input)
    saveModel()
"""
  
while running:
    drawComponents()
    for event in pygame.event.get():
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            x, y = pygame.mouse.get_pos()
            if x < 400 and y < 400 and x > 0 and y > 0:
                #fill pixel
                index = x // 20 + y // 20 * 20
                ar[index][1] = 1
            elif x >= 410 and y >= 10 and x <= 490 and y <= 40:
                clear()
            elif x >= 410 and y >= 50 and x <= 490 and y <= 80:
                #drawing_blocked = True
                y = predict()
                showResult(y)
                
        if event.type == pygame.QUIT:
            running = False
    
dump(model, 'model.joblib')
dump(X_train, 'X_train.joblib')
dump(y_train, 'y_train.joblib')            
pygame.quit()         
            


