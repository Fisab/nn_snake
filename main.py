import pygame
import random
import time

class Block():
	def __init__(self, direction, difference, pos, game):
		self.size = 25
		self.difference = difference

		self.pos = {'x': pos[0], 'y': pos[1]}

		self.direction = direction

		self.game = game

	def move(self):
		global state
		if self.direction == 'up':
			if self.pos['y'] > 0:
				self.pos['y'] -= self.size
				return True
			else:
				self.game.restart_game()
				return False
		elif self.direction == 'down':
			if self.pos['y'] < self.game.screen_size[1] - self.size:
				self.pos['y'] += self.size
				return True
			else:
				self.game.restart_game()
				return False
		elif self.direction == 'left':
			if self.pos['x'] > 0:
				self.pos['x'] -= self.size
				return True
			else:
				self.game.restart_game()
				return False
		elif self.direction == 'right':
			if self.pos['x'] < self.game.screen_size[0] - self.size:
				self.pos['x'] += self.size
				return True
			else:
				self.game.restart_game()
				return False

class Apple():
	def __init__(self, screen_size):
		self.color = (0, 178, 0)

		self.size = 25
		self.difference = 6

		self.pos = {
			'x': random.randint(0, screen_size[0]),
			'y': random.randint(0, screen_size[1])
		}
		while self.pos['x'] % 25 != 0:
			self.pos['x'] = random.randint(0, screen_size[0] - self.size)
		while self.pos['y'] % 25 != 0:
			self.pos['y'] = random.randint(0, screen_size[1] - self.size)

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, [self.pos['x'] + self.difference / 2, self.pos['y'] + self.difference / 2, self.size - self.difference, self.size - self.difference])

class Snake():
	def __init__(self, game):
		self.color = (0, 0, 255)

		self.size = 25
		self.difference = 6

		self.direction = 'right'
		self.length = 3

		self.blocks = []

		self.game = game

		self.start_pos = {
			'x': random.randint(0, self.game.screen_size[0]),
			'y': random.randint(0, self.game.screen_size[0])
		}
		while self.start_pos['x'] % 25 != 0:
			self.start_pos['x'] = random.randint(0, self.game.screen_size[0] - self.size * 5)
		while self.start_pos['y'] % 25 != 0:
			self.start_pos['y'] = random.randint(0, self.game.screen_size[1] - self.size * 5)


		for i in range(self.length):
			self.blocks.append(Block(self.direction, self.difference, [self.start_pos['x']-i*self.size, self.start_pos['y']], self.game))

	def draw(self):
		for i in range(self.length):
			pygame.draw.rect(self.game.screen, self.color, [self.blocks[i].pos['x'] + self.blocks[i].difference / 2, self.blocks[i].pos['y'] + self.blocks[i].difference / 2, self.size - self.difference, self.size - self.difference])

	def move(self, direction):
		for i in range(self.length):
			proceed = self.blocks[i].move()
			if not proceed:
				break

	def check_collision(self, index):
		if type(index) != type(1):
			for i in range(self.length):
				block_pos = {
					'x': self.blocks[i].pos['x'],
					'y': self.blocks[i].pos['y']
				}
				if index.pos['x'] == block_pos['x']:
					if index.pos['y'] == block_pos['y']:
						return True
		else:
			for i in range(self.length):
				block_pos = {
					'x': self.blocks[i].pos['x'],
					'y': self.blocks[i].pos['y']
				}
				pos = {
					'x': self.blocks[index].pos['x'],
					'y': self.blocks[index].pos['y'],
				}
				if i == index:
					continue
				if pos['x'] == block_pos['x']:
					if pos['y'] == block_pos['y']:
						return True
		return False

	def change_direction(self, new_direction=None):
		for i in range(self.length-1, 0, -1):
			self.blocks[i].direction = self.blocks[i-1].direction
		if new_direction != None:
			self.blocks[0].direction = new_direction
			self.direction = new_direction
		return True
	def add_block(self):
		direction = self.blocks[len(self.blocks)-1].direction
		pos = [self.blocks[len(self.blocks)-1].pos['x'], self.blocks[len(self.blocks)-1].pos['y']]
		if direction == 'up':
			pos[1] += self.size
		elif direction == 'down':
			pos[1] -= self.size
		elif direction == 'right':
			pos[0] -= self.size
		elif direction == 'left':
			pos[0] += self.size
		self.blocks.append(Block(direction, self.difference, pos, self.game))
		self.length += 1


class Game():
	def __init__(self):
		pygame.init()

		self.screen_size = [800, 600]
		self.screen = pygame.display.set_mode(self.screen_size)

		self.RUNNING, self.PAUSE, self.RESTART = 0, 1, 2
		self.state = self.RUNNING

		self.pause_text = pygame.font.SysFont('Consolas', 32).render('Pause', True, (255, 255, 255))
		self.game_over_text = pygame.font.SysFont('Consolas', 32).render('Game Over', True, (255, 255, 255))

		self.apple = None

	def run_game(self):
		self.state = self.RUNNING

	def pause_game(self):
		self.state = self.PAUSE

	def restart_game(self):
		self.state = self.RESTART

	def draw_grid(self, block_size):
		x_range = int(self.screen_size[0] / block_size)
		for x in range(x_range):
			pygame.draw.line(self.screen, (220,220,220), [x * block_size, 0], [x * block_size, self.screen_size[1]], 1)
		y_range = int(self.screen_size[1] / block_size)
		for y in range(y_range):
			pygame.draw.line(self.screen, (220,220,220), [0, y * block_size], [self.screen_size[0], y * block_size], 1)

	def control(self, sn):
		pressed = pygame.key.get_pressed()
		already_changed = False


		if pressed[pygame.K_r]:
			self.restart_game()
		if pressed[pygame.K_SPACE]:
			self.pause_game()

		if pressed[pygame.K_v]:
			sn.add_block()
		if pressed[pygame.K_w]:
			if sn.direction != 'down':
				already_changed = sn.change_direction('up')
		elif pressed[pygame.K_s]:
			if sn.direction != 'up':
				already_changed = sn.change_direction('down')
		elif pressed[pygame.K_a]:
			if sn.direction != 'right':
				already_changed = sn.change_direction('left')
		elif pressed[pygame.K_d]:
			if sn.direction != 'left':
				already_changed = sn.change_direction('right')
		if already_changed == False:
			sn.change_direction()
		sn.move(sn.direction)
		for i in range(sn.length):
			collision = sn.check_collision(i)
			if collision == True:
				self.restart_game()
				return
		if self.apple != None:
			collision = sn.check_collision(self.apple)
			if collision == True:
				self.apple = None
				sn.add_block()

	def create_apple(self):
		self.apple = Apple(self.screen_size)

	def main(self):
		pygame.display.set_caption("Snake by FISUBUS")

		done = False
		clock = pygame.time.Clock()
		
		sn = Snake(self)

		while not done:
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True

			if self.state == self.RUNNING:
				if self.apple == None:
					self.create_apple()

				self.control(sn)

				self.screen.fill((202,202,202))
				self.draw_grid(sn.size)
				if self.apple != None:
					self.apple.draw(self.screen)
				sn.draw()

			elif self.state == self.PAUSE:
				self.screen.blit(self.game_over_text, (self.screen_size[0]/2-30, self.screen_size[1]/2-25))
				pressed = pygame.key.get_pressed()

				if pressed[pygame.K_r]:
					self.restart_game()
				elif pressed[pygame.K_SPACE]:
					self.run_game()

			elif self.state == self.RESTART:
				return True
			pygame.display.flip()
			clock.tick(10)
		
		pygame.quit()

if __name__ == '__main__':
	play = True
	while play:
		g = Game()
		play = g.main()