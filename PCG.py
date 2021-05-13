import random
from PIL import Image
import numpy as np

################ Diamond Square ################


def ds_algorithm(size, randomness):
    noise_map = []

    # create noise_amp with 0s
    noise_map = [[0]*size for i in range(size)]

    # set the corner points to the same random value
    rand = random.randint(0, 256)
    noise_map[0][0] = rand
    noise_map[size - 1][0] = rand
    noise_map[0][size - 1] = rand
    noise_map[size - 1][size - 1] = rand

    # set the randomness bounds, higher values mean rougher landscapes
    # randomness = 128

    # starting size
    size -= 1

    # we make a pass over the noise_map
    # each time we decrease the side length by 2
    while size > 1:
        halfSide = size // 2

        # set the diamond values (the centers of each tile)
        for x in range(0, len(noise_map) - 1, size):
            for y in range(0, len(noise_map) - 1, size):
                cornerSum = noise_map[x][y] + noise_map[x + size][y] + \
                    noise_map[x][y + size] + noise_map[x + size][y + size]

                avg = cornerSum / 4
                avg += random.randint(-randomness, randomness)

                noise_map[x + halfSide][y + halfSide] = avg

        # set the square values (the midpoints of the sides)
        for x in range(0, len(noise_map) - 1, halfSide):
            for y in range((x + halfSide) % size, len(noise_map) - 1, size):
                avg = noise_map[(x - halfSide + len(noise_map) - 1) % (len(noise_map) - 1)][y] + \
                    noise_map[(x + halfSide) % (len(noise_map) - 1)][y] + \
                    noise_map[x][(y + halfSide) % (len(noise_map) - 1)] + \
                    noise_map[x][(y - halfSide + len(noise_map) - 1) % (len(noise_map) - 1)]

                avg /= 4.0
                avg += random.randint(-randomness, randomness)

                noise_map[x][y] = avg

                # because the values wrap round, the left and right edges are equal, same with top and bottom
                if x == 0:
                    noise_map[len(noise_map) - 1][y] = avg
                if y == 0:
                    noise_map[x][len(noise_map) - 1] = avg

        # reduce the randomness in each pass, making sure it never gets to 0
        randomness = max(randomness // 2, 1)
        size //= 2

        # normalize noise_map
    min_value = min([min(x) for x in noise_map])
    max_value = max([max(x) for x in noise_map])

    for i in range(len(noise_map)):
        for j in range(len(noise_map[0])):
            noise_map[i][j] = (noise_map[i][j] - min_value)/(max_value - min_value)
    return noise_map


################ Perlin Noise ################

def generate_perlin_noise_2d(shape, res):
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


def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
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
        noise += amplitude * \
            generate_perlin_noise_2d(shape, (frequency * res[0], frequency * res[1]))
        frequency *= 2
        amplitude *= persistence
        totamp += amplitude
    min_value = min([min(x) for x in noise])
    max_value = max([max(x) for x in noise])

    for i in range(len(noise)):
        for j in range(len(noise[0])):
            noise[i][j] = (noise[i][j] - min_value) / (max_value - min_value)
    return noise

################ Background ################


def pcg_bg(e, m):  # for multi-layer ds noise
    if type(e) == list:
        width = len(e)
        height = len(e)
    else:
        width = e.shape[0]
        height = e.shape[1]

    im = Image.new("RGB", [width, height])

    deep = (0, 10, 80)
    water = (65, 105, 180)
    # beach = (240, 205, 150)
    # wetlands = (60, 240, 180)
    # desert = (255, 255, 160)
    # forest = (25, 90, 15)
    jungle = (120, 220, 10)
    # mountain = (140, 140, 140)
    # snow = (250, 250, 250)

    for i in range(width):
        for j in range(height):
            if e[i][j] < 0.3:
                im.putpixel((i, j), deep)
            elif e[i][j] < 0.7:
                im.putpixel((i, j), water)
            # elif e[i][j] < 0.35:
            #     im.putpixel((i, j), beach)
            # elif e[i][j] < 0.4 and m[i][j] > 0.7:
            #     im.putpixel((i, j), wetlands)
            # elif e[i][j] < 0.6 and m[i][j] < 0.15:
            #     im.putpixel((i, j), desert)
            # elif e[i][j] < 0.6 and m[i][j] < 0.5:
            #     im.putpixel((i, j), forest)
            # elif e[i][j] < 0.6:
            #     im.putpixel((i, j), jungle)
            # elif e[i][j] < 0.75 and m[i][j] < 0.35:
            #     im.putpixel((i, j), mountain)
            # elif e[i][j] < 0.75:
            #     im.putpixel((i, j), forest)
            # elif e[i][j] < 0.9 and m[i][j] < 0.35:
            #     im.putpixel((i, j), snow)
            else:
                im.putpixel((i, j), jungle)

    im.save('pcg_background.png')
    return im

################ Clouds ################

# this isn't used in the latest version

# def add_padding(pil_img, top, right, bottom, left, color):
#     width, height = pil_img.size
#     new_width = width + right + left
#     new_height = height + top + bottom
#     result = Image.new(pil_img.mode, (new_width, new_height), color)
#     result.paste(pil_img, (left, top))
#     return result


# def pcg_clouds(noise):  # for multi-layer ds noise
#     if type(noise) == list:
#         width = len(noise)
#         height = len(noise)
#     else:
#         width = noise.shape[0]
#         height = noise.shape[1]
#
#     im = Image.new("RGBA", [width, height])
#
#     # deep = (0, 10, 80)
#     # water = (65, 105, 180)
#     # beach = (240, 205, 150)
#     # wetlands = (60, 240, 180)
#     # desert = (255, 255, 160)
#     # forest = (25, 90, 15)
#     # jungle = (120, 220, 10)
#     # mountain = (140, 140, 140)
#     # snow = (250, 250, 250)
#     transparent = (0, 0, 0, 0)
#     # cloud = (255, 255, 255, 255*noise[i][j])
#
#     for i in range(width):
#         for j in range(height):
#             if noise[i][j] < 0.25:
#                 transparency = 255 - int(255*float(noise[i][j]))
#                 im.putpixel((i, j), (255, 255, 255, transparency))
#             else:
#                 im.putpixel((i, j), transparent)
#
#     im = add_padding(im, 50, 0, 50, 0, transparent)
#
#     im.save('pcg_clouds.png')
#     return im
#     # im.show()

################ Tests ################


# elevation = ds_algorithm(513, 128)
# moisture = ds_algorithm(513, 128)
# bg = pcg_bg(elevation, moisture)
#
#
# im = Image.new("RGBA", [512, 512])
#
# noise = ds_algorithm(513, 128)
# im = pcg_clouds(noise)
#
# elevation = ds_algorithm(513, 128)
# moisture = ds_algorithm(513, 128)
# im = pcg_bg(elevation, moisture)
# im.show()
#
# cloud_pixels = generate_fractal_noise_2d(shape=(512, 512), res=(4, 4), octaves=8, persistence=0.5)
# for kx in range(len(cloud_pixels)):
#     for ky in range(len(cloud_pixels[0])):
#         c = int(cloud_pixels[kx][ky] * 255)
#         col = im.getpixel((kx, ky))
#         im.putpixel((kx, ky), (col[0], col[1], col[2], c))
#
#
# im.show()
