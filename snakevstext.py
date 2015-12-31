import curses
import random
import time

pl1name = 'Player 1'
pl2name = 'Player 2'

screen = curses.initscr()
screen.keypad(1)
d = screen.getmaxyx()
dims = [d[0]-1, d[1]]
screen.nodelay(1)
nor = curses.A_NORMAL
gs1 = ord('X')
gs2 = ord('O')
ga1 = ord('x')
ga2 = ord('o')
startlength = 5
selfgrow = 3
opposegrow = 1
def game():
  loss = 0
  screen.nodelay(1)
  gameover = False
  pl1right = True
  pl1left, pl1up, pl1down = False, False, False
  pl2left = True
  pl2right, pl2up, pl2down = False, False, False
  topleft = [0, 0]
  bottomright = [dims[0]-1, dims[1]-1]
  snake1 = []
  snake2 = []
  for z in range(startlength):
    snake1.append(topleft[:])
    snake2.append(bottomright[:])
  pl1act = []
  pl2act = []
  apple1made, apple2made = False, False
  apple1, apple2 = [0, 0], [0, 0]
  while not gameover:
    act = [screen.getch(), screen.getch()]
    if ord('\n') in act:
      gameover = True
    for z in act:
      if z == ord('a') or z == ord('s') or z == ord('d') or z == ord('w'):
        pl1act.append(z)
      elif z == ord('j') or z == ord('k') or z == ord('l') or z == ord('i'):
        pl2act.append(z)
    if len(pl1act) > 0:
      if ord('a') == pl1act[0]:
        if not pl1right:
          pl1up, pl1down, pl1right, pl1left = False, False, False, True
        pl1act.remove(pl1act[0])
      elif ord('s') == pl1act[0]:
        if not pl1up:
          pl1up, pl1down, pl1right, pl1left = False, True, False, False
        pl1act.remove(pl1act[0])
      elif ord('d') == pl1act[0]:
        if not pl1left:
          pl1up, pl1down, pl1right, pl1left = False, False, True, False
        pl1act.remove(pl1act[0])
      elif ord('w') == pl1act[0]:
        if not pl1down:
          pl1up, pl1down, pl1right, pl1left = True, False, False, False
        pl1act.remove(pl1act[0])
    if len(pl2act)>0:
      if ord('j') == pl2act[0]:
        if not pl2right:
          pl2up, pl2down, pl2right, pl2left = False, False, False, True
        pl2act.remove(pl2act[0])
      elif ord('k') == pl2act[0]:
        if not pl2up:
          pl2up, pl2down, pl2right, pl2left = False, True, False, False
        pl2act.remove(pl2act[0])
      elif ord('l') == pl2act[0]:
        if not pl2left:
          pl2up, pl2down, pl2right, pl2left = False, False, True, False
        pl2act.remove(pl2act[0])
      elif ord('i') == pl2act[0]:
        if not pl2down:
          pl2up, pl2down, pl2right, pl2left = True, False, False, False
        pl2act.remove(pl2act[0])

    while not apple1made:
      apple1 = [random.randrange(dims[0]), random.randrange(dims[1])]
      if apple1 not in snake1 and apple1 not in snake2 and apple1 != apple2:
        apple1made = True
    while not apple2made:
      apple2 = [random.randrange(dims[0]), random.randrange(dims[1])]
      if apple2 not in snake1 and apple2 not in snake2 and apple2 != apple1:
        apple2made = True

    screen.clear()
    for z in snake1:
      screen.addch(z[0], z[1], gs1)
    for z in snake2:
      screen.addch(z[0], z[1], gs2)
    screen.addch(apple1[0], apple1[1], ga1)
    screen.addch(apple2[0], apple2[1], ga2)
    screen.addstr(dims[0], 3, chr(gs1)+' '+ pl1name)
    screen.addstr(dims[0], dims[1] - len(pl2name) -5, pl2name+ ' '+chr(gs2))

    for z in range(len(snake1)-1):
      snake1[z] = snake1[z+1][:]
    for z in range(len(snake2)-1):
      snake2[z] = snake2[z+1][:]

    if pl1right:
      snake1[-1][1] += 1
    if pl1left:
      snake1[-1][1] -= 1
    if pl1up:
      snake1[-1][0] -= 1
    if pl1down:
      snake1[-1][0] += 1

    if pl2right:
      snake2[-1][1] += 1
    if pl2left:
      snake2[-1][1] -= 1
    if pl2up:
      snake2[-1][0] -= 1
    if pl2down:
      snake2[-1][0] += 1

    if snake1[-1][0]<0 or snake1[-1][1]<0:
      gameover = True
      loss += 1
    if snake2[-1][0]<0 or snake2[-1][1]<0:
      gameover = True
      loss += 2
    if snake1[-1][0]>=dims[0] or snake1[-1][1]>=dims[1]:
      gameover = True
      loss += 1
    if snake2[-1][0]>=dims[0] or snake2[-1][1]>=dims[1]:
      gameover = True
      loss += 2
    if not gameover:
      if snake1[-1] in snake1[:-1] or snake1[-1] in snake2:
        gameover = True
        loss += 1
      if snake2[-1] in snake2[:-1] or snake2[-1] in snake1:
        gameover = True
        loss += 2
      if snake1[-1] == apple1:
        apple1made = False
        snake1.reverse()
        for z in range(3):
          snake1.append(snake1[-1])
        snake1.reverse()
      if snake2[-1] == apple2:
        apple2made = False
        snake2.reverse()
        for z in range(selfgrow):
          snake2.append(snake2[-1])
        snake2.reverse()
      if snake1[-1] == apple2:
        apple2made = False
        snake1.reverse()
        for z in range(opposegrow):
          snake1.append(snake1[-1])
        snake1.reverse()
      if snake2[-1] == apple1:
        apple1made = False
        snake2.reverse()
        for z in range(opposegrow):
          snake2.append(snake2[-1])
        snake2.reverse()        
    screen.refresh()
    time.sleep(0.1)
  screen.clear()
  screen.nodelay(0)
  if loss == 3:
    result = 'It\'s a tie!'
  elif loss == 2:
    result = pl1name + ' wins!'
  else:
    result = pl2name + ' wins!'
  q = 0
  while q not in [ord(' '), ord('\n'), ord('m')]:
    screen.addstr(dims[0]/2-2, (dims[1]-len(result))/2, result)
    screen.addstr(dims[0]/2, dims[1]/2-14, 'Press Spacebar to play again')
    screen.addstr(dims[0]/2+1, dims[1]/2-10, 'Press Enter to quit')
    screen.addstr(dims[0]/2+2, dims[1]/2-15 , 'Press M to go to the main menu')
    screen.refresh()
    q = screen.getch()
  if q == ord(' '):
    game()
  elif q == ord('m'):
    menu()

def menu():
  screen.nodelay(0)
  option = 0
  selection = - 1
  while selection < 0:
    screen.clear()
    screen.addstr(0, dims[1]/2 - 7, '2 Player Snake')
    if option == 0:
      graphics = [curses.A_BOLD, nor, nor, nor, nor]
    elif option == 1:
      graphics = [nor, curses.A_BOLD, nor, nor, nor]
    elif option == 2:
      graphics = [nor, nor, curses.A_BOLD, nor, nor]
    elif option == 3:
      graphics = [nor, nor, nor, curses.A_BOLD, nor]
    elif option == 4:
      graphics = [nor, nor, nor, nor, curses.A_BOLD]
    screen.addstr(dims[0]/2-4, dims[1]/2 - 2, 'Play', graphics[0])
    screen.addstr(dims[0]/2-2, dims[1]/2 - 6, 'Instructions', graphics[1])
    screen.addstr(dims[0]/2, dims[1]/2 - 4, 'Set Names', graphics[2])
    screen.addstr(dims[0]/2+2, dims[1]/2 - 6, 'Set Graphics', graphics[3])
    screen.addstr(dims[0]/2+4, dims[1]/2 - 2, 'Quit', graphics[4])
    screen.addstr(dims[0], dims[1]/2-21, 'Use enter and w/s or i/k to navigate menu')
    q = screen.getch()
    if q == ord('s') or q == ord('k'):
      option = (option+1) % 5
    elif q == ord('w') or q == ord('i'):
      option = (option-1) % 5
    elif q == ord('\n'):
      selection = option
  if selection == 0:
    game()
  elif selection == 1:
    instructions()
  elif selection == 2:
    namechange()
  elif selection == 3:
    graphicschange()
    
def instructions():
  q = 0
  while q != ord('\n') and q != ord(' '):
    screen.clear()
    screen.addstr(0, dims[1]/2 - 7, '2 Player Snake')
    screen.addstr(1, dims[1]/2 - 6, 'Instructions')
    screen.addstr(dims[0]/2-6, dims[1]/2-20, 'If the head of a snake runs into a wall,')
    screen.addstr(dims[0]/2-5, dims[1]/2-21, 'or the side of a snake, that player loses.')
    screen.addstr(dims[0]/2-2, dims[1]/2 - 9, 'Player 1 controls:')
    screen.addstr(dims[0]/2-1, dims[1]/2-18, 'Up: w,  Down: s,  Left: a,  Right: d')
    screen.addstr(dims[0]/2+1, dims[1]/2 - 9, 'Player 2 controls:')
    screen.addstr(dims[0]/2+2, dims[1]/2-18, 'Up: i,  Down: k,  Left: j,  Right: l')
    screen.addstr(dims[0], dims[1]/2-19, 'Press Enter or Space to return to menu')
    q = screen.getch()
  menu()

def namechange():
  global pl1name
  global pl2name
  screen.nodelay(0)
  option = 0
  selection = - 1
  while selection < 2:
    selection = - 1
    screen.clear()
    screen.addstr(0, dims[1]/2 - 7, '2 Player Snake')
    if option == 0:
      graphics = [curses.A_BOLD, nor, nor]
    elif option == 1:
      graphics = [nor, curses.A_BOLD, nor]
    elif option == 2:
      graphics = [nor, nor, curses.A_BOLD]
    screen.addstr(dims[0]/2 - 3, dims[1]/2-len(pl1name)/2, pl1name)
    screen.addstr(dims[0]/2 - 2, dims[1]/2-3, 'Change', graphics[0])
    screen.addstr(dims[0]/2, dims[1]/2-len(pl2name)/2, pl2name)
    screen.addstr(dims[0]/2+1, dims[1]/2-3, 'Change', graphics[1])
    screen.addstr(dims[0]/2+3, dims[1]/2-6, 'Back to Menu', graphics[2])
    q = screen.getch()
    if q == ord('s') or q == ord('k'):
      option = (option+1) % 3
    elif q == ord('w') or q == ord('i'):
      option = (option-1) % 3
    elif q == ord('\n'):
      selection = option
    if selection == 0:
      screen.clear()
      screen.addstr(0, 0, 'Enter name for player 1: ')
      pl1name = screen.getstr()
    elif selection == 1:
      screen.clear()
      screen.addstr(0, 0, 'Enter name for player 2: ')
      pl2name = screen.getstr()
  menu()

def graphicschange():
  global gs1, gs2, ga1, ga2  
  screen.nodelay(0)
  option = 0
  selection = - 1
  page = 0
  while selection < 4:
    selection = -1
    screen.clear()
    screen.addstr(0, dims[1]/2 - 7, '2 Player Snake')
    if option == 0:
      graphics = [curses.A_BOLD, nor, nor, nor, nor, nor]
    elif option == 1:
      graphics = [nor, curses.A_BOLD, nor, nor, nor, nor]
    elif option == 2:
      graphics = [nor, nor, curses.A_BOLD, nor, nor, nor]
    elif option == 3:
      graphics = [nor, nor, nor, curses.A_BOLD, nor, nor]
    elif option == 4:
      graphics = [nor, nor, nor, nor, curses.A_BOLD, nor]
    elif option == 5:
      graphics = [nor, nor, nor, nor, nor, curses.A_BOLD]
    if page == 0:
      screen.addstr(dims[0]/2-5, dims[1]/2-9, 'Player 1 Snake: ' + chr(gs1), graphics[0])
      screen.addstr(dims[0]/2-3, dims[1]/2-9, 'Player 2 Snake: ' + chr(gs2), graphics[1])
      screen.addstr(dims[0]/2-1, dims[1]/2-9, 'Player 1 Apple: ' + chr(ga1), graphics[2])
      screen.addstr(dims[0]/2+1, dims[1]/2-9, 'Player 2 Apple: ' + chr(ga2), graphics[3])
      screen.addstr(dims[0]/2+3, dims[1]/2-6, 'More Options', graphics[4])
      screen.addstr(dims[0]/2+5, dims[1]/2-6, 'Back to Menu', graphics[5])
    q = screen.getch()
    if q == ord('s') or q == ord('k'):
      option = (option+1) % 6
    elif q == ord('w') or q == ord('i'):
      option = (option-1) % 6
    elif q == ord('\n'):
      selection = option
    if page == 0:
      if selection == 0:
        screen.addch(dims[0]/2-5, dims[1]/2+7, ord('>'), curses.A_BLINK)
        gs1 = screen.getch()   
      elif selection == 1:
        screen.addch(dims[0]/2-3, dims[1]/2+7, ord('>'), curses.A_BLINK)
        gs2 = screen.getch()   
      elif selection == 2:
        screen.addch(dims[0]/2-1, dims[1]/2+7, ord('>'), curses.A_BLINK)
        ga1 = screen.getch()   
      elif selection == 3:
        screen.addch(dims[0]/2+1, dims[1]/2+7, ord('>'), curses.A_BLINK)
        ga2 = screen.getch()
    if selection == 4:
      page = (page+1)%2
  menu()

menu()
curses.endwin()
