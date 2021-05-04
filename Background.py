import pygame
import numpy as np

class Background():

    def __init__(self, DISPLAYSURF):

        #self.bgimage = pygame.image.load('background.png')
        #self.bgimage = pygame.transform.scale(self.bgimage, DISPLAYSURF.get_size())
        #self.rectBGimg = self.bgimage.get_rect()

        self.bgimage = pygame.Surface(DISPLAYSURF.get_size())
        self.bgimage.fill((0,191,250))
        self.bgimage.set_alpha(255)
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0


        self.moving_speed = 5

        self.DISPLAYSURF = DISPLAYSURF

        #clouds via perlin noise!
        cloud_pixels = self.generate_fractal_noise_2d(shape=(self.rectBGimg.width+100,self.rectBGimg.height+100 ), res=(5,5), octaves=4, persistence=0.5)
        for kx in range(self.rectBGimg.width):
            for ky in range(self.rectBGimg.height ):
                c = cloud_pixels[kx][ky]
                col = self.bgimage.get_at((kx,ky))
                self.bgimage.set_at((kx, ky), (int(c*255), col[1]+(int(c*64)), col[2]+(int(c*5))))

    def update(self):
        #print(self.bgY1, self.bgY2)
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

        self.draw()

    def draw(self):
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

    def virtual_update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

    def generate_perlin_noise_2d(self,shape, res):
        '''
        :param shape: Size of the map to return
        :param res: 'cycles' along an axis
        :return: Noise Map (shape)
        Creates one layer of the Perlin Noise
        Taken and adapted from https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html.
        '''

        def f(t):
            return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3
        delta = (res[0] / shape[0], res[1] / shape[1])
        d = (shape[0] // res[0], shape[1] // res[1])
        grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1

        # Gradients
        angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
        g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
        # Ramps
        n00 = np.sum(grid * g00, 2)
        n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
        n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
        # Interpolation
        t = f(grid)
        n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
        n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
        return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

    def generate_fractal_noise_2d(self,shape, res, octaves=1, persistence=0.5):
        '''
        :param shape: Size of the map to return
        :param res: 'cycles' along an axis
        :param octaves: number of layers of perlin noise
        :param persistence: overlapping scale of the single layers
        :return: noise map of overlapping perlin noise layers
        creates fractal noise via overlap
        Taken and adapted from https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html.
        '''
        noise = np.zeros(shape)
        frequency = 1
        amplitude = 1
        totamp = 0
        for _ in range(octaves):
            noise += amplitude * self.generate_perlin_noise_2d(shape, (frequency * res[0], frequency * res[1]))
            frequency *= 2
            amplitude *= persistence
            totamp += amplitude
        min_value = min([min(x) for x in noise])
        max_value = max([max(x) for x in noise])

        for i in range(len(noise)):
            for j in range(len(noise[0])):
                noise[i][j] = (noise[i][j] - min_value) / (max_value - min_value)
        return noise