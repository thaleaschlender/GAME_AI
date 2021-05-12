import random
from PIL import Image
# import numpy as np

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


def add_padding(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def pcg_clouds(noise):  # for multi-layer ds noise
    if type(noise) == list:
        width = len(noise)
        height = len(noise)
    else:
        width = noise.shape[0]
        height = noise.shape[1]

    im = Image.new("RGBA", [width, height])

    # deep = (0, 10, 80)
    # water = (65, 105, 180)
    # beach = (240, 205, 150)
    # wetlands = (60, 240, 180)
    # desert = (255, 255, 160)
    # forest = (25, 90, 15)
    # jungle = (120, 220, 10)
    # mountain = (140, 140, 140)
    # snow = (250, 250, 250)
    transparent = (0, 0, 0, 0)
    white = (255, 255, 255, 255)
    '''
    for i in range(width):
        for j in range(height):
            if noise[i][j] < 0.05:
                im.putpixel((i, j),(255, 255, 255, 200+int(noise[i][j]*100)))
            elif noise[i][j] <0.25:
                im.putpixel((i, j), (255, 255, 255, 170))
            else:
                im.putpixel((i, j), transparent)
    
    im = add_padding(im, 50, 0, 50, 0, transparent)
    '''
    im.save('pcg_clouds.png')
    return im
    # im.show()


# noise = ds_algorithm(513, 128)
# pcg_clouds(noise)
