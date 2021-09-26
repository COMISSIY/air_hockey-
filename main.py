import pygame, socket
from math import sin, cos, atan2, sqrt
from threading import Thread
pygame.init()

w, h = 400, 600
sc = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
def find_angle(a_x, a_y, b_x, b_y):
    rel_x, rel_y = a_x - b_x, a_y - b_y
    angle = atan2(rel_y, rel_x)
    return angle

def find_dist(p1, p2):
	return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

class Data_Transfer:
	def __init__(self):
		self.client = socket.socket(

			socket.AF_INET,
			socket.SOCK_STREAM,

			)

		self.client.connect(
			("127.0.0.1", 1234)
			)
	def listen_server(self):
		print("get data...")
		data = self.client.recv(2048)
		data = data.decode("utf-8")
		print(data, 2)
		if data == '':
			data = game.players[1].pos
			print(data, 1)
		return data
	def send_server(self):
		print("send data...")
		# listen_thread = Thread(target=self.listen_server)
		# listen_thread.start()
		self.client.send(str(game.players[0].pos).encode("utf-8"))

class Game:
	def __init__(self, players=[]):
		self.players = players
		self.ball = Ball()
		self.font = pygame.font.Font(None, 60)
		self.enemy_score = 0
		self.player_score = 0

	def draw(self):
		pygame.draw.line(sc, (255, 0, 0), [0, h//2], [w//2-50, h//2])
		pygame.draw.line(sc, (0, 0, 255), [w//2+50, h//2], [w, h//2])
		pygame.draw.rect(sc, (0, 0, 255), (w//4, 0, w//4*2, self.ball.rad))
		pygame.draw.rect(sc, (255, 0, 0), (w//4, h-self.ball.rad, w//4*2, self.ball.rad))
		sc.blit(self.font.render(str(self.player_score), 1, (255, 255, 255)), (0, 0))
		sc.blit(self.font.render(str(self.enemy_score), 1, (255, 255, 255)), (0, h-40))
		for i in self.players:
			i.draw()
			i.update()
			i.ball_colision()
		pygame.draw.circle(sc, (255, 255, 255), (w//2, h//2), 45, 1)
		self.ball.draw()
		self.ball.update()
	def cheak_win(self):
		if self.ball.pos[0] > w//4 and self.ball.pos[0] < w-w//4:
			if self.ball.pos[1] < self.ball.rad:
				self.ball.pos = [w//2, h//2]
				self.ball.dx, self.ball.dy = 0, 0
				self.player_score += 1
			elif self.ball.pos[1] > h-self.ball.rad:
				self.ball.pos = [w//2, h//2]
				self.ball.dx, self.ball.dy = 0, 0
				self.enemy_score += 1

class Ball:
	def __init__(self, color=(0, 255, 0), pos=[w//2, h//2], rad = 25):
		self.pos = pos
		self.color = color
		self.rad = rad
		self.dx, self.dy = 0, 0
	def update(self):
		if self.pos[0]+self.rad > w:
			self.dx = -self.dx//2
			self.pos[0] = w-self.rad
		if self.pos[0]-self.rad < 0:
			self.dx = -self.dx//2
			self.pos[0] = self.rad
		if self.pos[1]+self.rad > h:
			self.dy = -self.dy//2
			self.pos[1] = h-self.rad
		if self.pos[1]-self.rad < 0:
			self.dy = -self.dy//2
			self.pos[1] = self.rad
		self.pos[0] += self.dx
		self.pos[1] += self.dy

	def draw(self):
		pygame.draw.circle(sc, self.color, self.pos, self.rad)

class Player:
	def __init__(self, pos=[w//2, h-h//4]):
		self.pos = pos
		self.speed = 10
		self.color = (255, 0, 0)

	def update(self):
		m_p = pygame.mouse.get_pos()
		a = find_angle(*self.pos, *m_p)
		if (self.pos[1] - 25 > h//2 or m_p[1] - 25 > h//2):
			self.pos[0] += -cos(a) * self.speed
			self.pos[1] += -sin(a) * self.speed
		# data.send_server()

	def ball_colision(self):

		dtb = find_dist(self.pos, game.ball.pos)
		if dtb - game.ball.rad*2 < 0:
			a = find_angle(*game.ball.pos, *self.pos)
			game.ball.dx += cos(a)*self.speed
			game.ball.dy += sin(a)*self.speed
			
	def draw(self):
		pygame.draw.circle(sc, self.color, self.pos, 25)

class Enemy(Player):
	def __init__(self):
		super().__init__()
		self.pos = [w//2, h//4]
		self.color = (0, 0, 255)
	def update(self):
		if game.ball.pos[1] > h//4:
			if self.pos[0] < game.ball.pos[0]:
				self.pos[0] += self.speed // 4
			else:
				self.pos[0] -= self.speed // 4

game = Game([Player(), Enemy()])
# data = Data_Transfer()
while True:
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			exit()
	clock.tick(60)
	sc.fill((0, 0, 0))
	game.draw()
	game.cheak_win()
	pygame.display.update()