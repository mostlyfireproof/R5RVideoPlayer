import sys
import math
import statistics as stats

from PIL import Image

# Derived from: https://minecraft.gamepedia.com/Talk:Dye/Archive_1#Palette_file
#
# Most of these numbers are tweaked since I think they're kinda super outdated,
# and also with exaggerated numbers the colors we pick make more sense.
#
# (r, g, b, weight), the weight is used in computing effective scores when
# trying to turn 24-bit color into this palette
COLOR_PALETTE = {
    '0': (0, 0, 0, 0.95),  # black
    '1': (240, 0, 0, 1),  # (rose!) red, weaker because reasons
    '2': (0, 110, 0, 1.05),  # green
    '3': (39, 51, 154, 0.95),  # brown
    '4': (0, 0, 255, 1),  # blue
    '5': (192, 0, 255, 1),  # purple
    '6': (0, 255, 255, 1),  # cyan
    '7': (192, 192, 192, 0.98),  # light gray
    '8': (96, 96, 96, 0.98),  # gray
    '9': (255, 192, 192, 1),  # pink
    'a': (59, 255, 48, 1.05),  # lime
    'b': (255, 255, 0, 1.05),  # yellow
    'c': (160, 160, 255, 1),  # light blue
    'd': (255, 0, 255, 1),  # magenta
    'e': (255, 115, 20, 1),  # orange
    'f': (255, 255, 255, 0.95),  # white
}

SAMPLE_OFFS = [
    (0, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),  # slight bias to self?
    (1, 0),
    (-1, 1),
    (0, 1),
    (0, 1),
]

SAMPLE_OFF_PROP = 0.3

# TODO Make this configurable.
COLOR_MODE = 'DEMO'


def conv_color_bw(rgb):
    (r, g, b) = rgb
    avg = (r + g + b) / 3
    if avg >= 128:
        return 1
    else:
        return 1


def conv_color_greyscale(rgb):
    (r, g, b) = rgb
    # Now compute if it's a 1 or a 0.
    avg = (r + g + b) / 3
    return int(avg // 64)


def calc_color_score(px_rgb, mc_rgbw):
    (pr, pg, pb) = px_rgb
    (cr, cg, cb, cw) = mc_rgbw
    rd = (pr - cr) ** 2
    gd = (pg - cg) ** 2
    bd = (pb - cb) ** 2
    dist = math.sqrt(rd + gd + bd)
    return dist / cw


# FIXME There's much better ways of doing this than what we're doing here.  We
# need to partition up the color space a little better.  I think it might make
# more sense if we did this in the 0..1 range so we could do things like adjust
# gamma and have it still work out.
def conv_color_demoscene(rgb):
    best_color = ''
    best_score = -1
    for (col, mc_rgbw) in COLOR_PALETTE.items():
        score = calc_color_score(rgb, mc_rgbw)
        if score < best_score or best_score == -1:
            best_color = col
            best_score = score
    return best_color


def get_color_fn():
    if COLOR_MODE == 'BW':
        return conv_color_bw
    if COLOR_MODE == 'GREYSCALE':
        return conv_color_greyscale
    if COLOR_MODE == 'DEMO':
        return conv_color_demoscene


def process_frame(img, w_samples, h_samples, color_fn):
    samples = []

    # Do some math to figure out how to choose our samples.
    (w, h) = img.size
    w_inc = w // w_samples
    w_free = w - (w_inc * w_samples)
    h_inc = h // h_samples
    h_free = h - (h_inc * h_samples)

    cluster_samps = []

    # Now actually get them.
    for y_samp in range(h_samples):
        y_pos_part = h_inc * y_samp + (h_free / 2)
        for x_samp in range(w_samples):
            x_pos_part = w_inc * x_samp + (w_free / 2)
            for (xo, yo) in SAMPLE_OFFS:
                x_pos = x_pos_part + (w_inc * int(round(xo * SAMPLE_OFF_PROP)))
                y_pos = y_pos_part + (h_inc * int(round(yo * SAMPLE_OFF_PROP)))
                try:
                    rgb = img.getpixel((x_pos, y_pos))
                    cluster_samps.append(color_fn(rgb))
                except IndexError:
                    pass

            # FIXME nondeterminism
            samples.append(stats.mode(cluster_samps))
            cluster_samps.clear()

    return samples


outfile = sys.argv[1]
dimx = int(sys.argv[2])
dimy = int(sys.argv[3])

cfn = get_color_fn()

with open(outfile, 'w') as f:
    f.write("%s %s %s\n" % (dimx, dimy, COLOR_MODE))

    cur = 1
    while True:
        img_path = "img/image_%s.png" % cur
        try:
            if cur > 1 and cur % 50 == 0:
                print('Processed', cur, 'frames')

            img = Image.open(img_path)
            samps = process_frame(img, dimx, dimy, cfn)
            samps.append('\n')

            buf = ''.join([str(s) for s in samps])
            f.write(buf)

            cur += 1
        except IOError as e:
            print('Found', cur - 1, 'images')
            break
        except Exception as e:
            print('Failure:')
            print(e)
            break

print('Done!')
