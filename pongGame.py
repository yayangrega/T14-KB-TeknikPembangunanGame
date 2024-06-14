from tkinter import *
import random

WIDTH = 900
HEIGHT = 300

# pengaturan raket
PAD_W = 15
PAD_H = 90

# pengaturan bola
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 40
BALL_RADIUS = 30

INITIAL_SPEED = 20
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = 0

# skor awal
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

# menambahkan variabel global untuk jarak ke tepi kanan lapangan permainan
right_line_distance = WIDTH - PAD_W


def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)


def spawn_ball():
    global BALL_X_SPEED
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2,
             HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2,
             HEIGHT / 2 + BALL_RADIUS / 2)
    BALL_X_SPEED = -(BALL_X_SPEED * -INITIAL_SPEED) / abs(BALL_X_SPEED)


def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randrange(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED


# memasang jendela
root = Tk()
root.title("Pong")

# area animasi
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#003300")
c.pack()

# elemen lapangan permainan
# garis kiri
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")

# garis kanan
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")

# garis tengah
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

# pemasangan fasilitas permainan

# membuat bola
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2,
                    HEIGHT / 2 - BALL_RADIUS / 2, WIDTH / 2 + BALL_RADIUS / 2,
                    HEIGHT / 2 + BALL_RADIUS / 2, fill="white")
# raket kiri
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, width=PAD_W, fill="Pink")

# raket yang tepat
RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, width=PAD_W, fill="Pink")

p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4, text=PLAYER_1_SCORE, font="Arial 20", fill="white")
p_2_text = c.create_text(WIDTH / 6, PAD_H / 4, text=PLAYER_2_SCORE, font="Arial 20", fill="white")

# diseluruh
BALL_X_SPEED = 10
BALL_Y_SPEED = 0

def move_ball():
    # menentukan koordinat sisi bola dan pusatnya
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # pantulan vertikal
    if ball_right + BALL_X_SPEED < right_line_distance and ball_left + BALL_X_SPEED > PAD_W:
        c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    elif ball_right == right_line_distance or ball_left == PAD_W: 
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]: 
                bounce("strike")
            else:
                update_score("left") 
                spawn_ball()
        else:
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]: 
                bounce("strike")
            else:
                update_score("right") 
                spawn_ball()
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_Y_SPEED) 
        else:
            c.move(BALL, -ball_left+PAD_W, BALL_Y_SPEED)

    # pantulan horizontal
    if ball_top + BALL_Y_SPEED < 0 or ball_bot + BALL_Y_SPEED > HEIGHT: 
        bounce("ricochet")

# mengatur variabel global untuk kecepatan raket
PAD_SPEED = 10
RIGHT_PAD_SPEED = 0
LEFT_PAD_SPEED = 0

# mengatur fungsi untuk menggerakkan raket 
def move_pads():
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED 
    LEFT_PAD_TOP = c.coords(LEFT_PAD)[1] 
    LEFT_PAD_BOTTOM = c.coords(LEFT_PAD)[3] 
    RIGHT_PAD_TOP = c.coords(RIGHT_PAD)[1]
 
    RIGHT_PAD_BOTTOM = c.coords(RIGHT_PAD)[3]

    if LEFT_PAD_TOP + LEFT_PAD_SPEED >= 0 and LEFT_PAD_BOTTOM + LEFT_PAD_SPEED <= HEIGHT:
        c.move(LEFT_PAD, 0, LEFT_PAD_SPEED)

    if RIGHT_PAD_TOP + RIGHT_PAD_SPEED >= 0 and RIGHT_PAD_BOTTOM + RIGHT_PAD_SPEED <= HEIGHT:
        c.move(RIGHT_PAD, 0, RIGHT_PAD_SPEED)

def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down": 
        RIGHT_PAD_SPEED = PAD_SPEED

def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ["w", "s"]:
        LEFT_PAD_SPEED = 0
    elif event.keysym in ["Up", "Down"]: 
        RIGHT_PAD_SPEED = 0

def quit_game(event): 
    root.destroy()

def main():
    move_ball() 
    move_pads() 
    root.after(30, main)

# memanggil fungsi utama untuk memulai permainan 
main()

# mengikat fungsi-fungsi ini ke canvas 
c.bind("<KeyPress>", movement_handler) 
c.bind("<KeyRelease>", stop_pad) 
c.bind("<Escape>", quit_game)

# menjalankan jendela 
c.focus_set() 
root.mainloop()