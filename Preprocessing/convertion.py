from PIL import Image
import os

IMG_DIR = os.path.abspath('./assets')
AIRCRAFTS_DIR = os.path.join(IMG_DIR, 'aircrafts')
PLAYER_DIR = os.path.join(AIRCRAFTS_DIR, 'player')
ENEMY_DIR = os.path.join(AIRCRAFTS_DIR, 'enemy')
ENV_DIR = os.path.join(IMG_DIR, 'environment')
CLOUDS_DIR = os.path.join(ENV_DIR, 'clouds')
LANDS_DIR = os.path.join(ENV_DIR, 'lands')
WAVES_DIR = os.path.join(ENV_DIR, 'waves')
LIGHT_WAVES_DIR = os.path.join(WAVES_DIR, 'light')
PROJECTILES_DIR = os.path.join(IMG_DIR, 'projectiles')
def convert_to_gif(img_path: str , output_path: str, resize_scale: float = 1.0):
    img = Image.open(img_path).convert("RGBA")

    new_width = int(img.width * resize_scale)
    new_height = int(img.height * resize_scale)

    img = img.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
        # Image.Resampling.BICUBIC
        # Image.Resampling.BILINEAR
    )

    # Create transparent background
    background = Image.new("RGBA", img.size, (0, 0, 0, 0))
    background.alpha_composite(img)

    # Convert to GIF
    gif = background.convert("P", palette=Image.ADAPTIVE, colors=255)

    # Find pixels that were transparent
    alpha = background.getchannel("A")

    transparent_pixels = []

    for y in range(background.height):
        for x in range(background.width):
            if alpha.getpixel((x, y)) == 0:
                transparent_pixels.append((x, y))

    # Use palette index 0 as transparent
    palette = gif.getpalette()

    # Make sure palette entry 0 is transparent/black
    palette[0:3] = [0, 0, 0]
    gif.putpalette(palette) 

    gif.save(
        output_path,
        transparency=0
    )

# pngs = [png for png in os.listdir(PLAYER_DIR) if png.endswith('.png')]

# for png in pngs:
#     input_file = os.path.join(PLAYER_DIR, png)
#     output_file = '.'.join(png.split('.')[:-1]) + '.gif'
#     output_file = os.path.join(PLAYER_DIR, output_file)
#     convert_to_gif(input_file, output_file, 0.7)

#####################################################################
# pngs = [png for png in os.listdir(ENEMY_DIR) if png.endswith('.png')]

# for png in pngs:
#     input_file = os.path.join(ENEMY_DIR, png)
#     output_file = '.'.join(png.split('.')[:-1]) + '.gif'
#     output_file = os.path.join(ENEMY_DIR, output_file)
#     convert_to_gif(input_file, output_file, 0.6)

#####################################################################
# pngs = [png for png in os.listdir(LANDS_DIR) if png.endswith('.png')]

# for png in pngs:
#     input_file = os.path.join(LANDS_DIR, png)
#     output_file = '.'.join(png.split('.')[:-1]) + '.gif'
#     output_file = os.path.join(LANDS_DIR, output_file)
#     convert_to_gif(input_file, output_file)
#####################################################################

# pngs = [png for png in os.listdir(WAVES_DIR) if png.endswith('.png')]

# for png in pngs:
#     input_file = os.path.join(WAVES_DIR, png)
#     output_file = '.'.join(png.split('.')[:-1]) + '.gif'
#     output_file = os.path.join(WAVES_DIR, output_file)
#     convert_to_gif(input_file, output_file, 0.5)

# pngs = [png for png in os.listdir(LIGHT_WAVES_DIR) if png.endswith('.png')]

# for png in pngs:
#     input_file = os.path.join(LIGHT_WAVES_DIR, png)
#     output_file = '.'.join(png.split('.')[:-1]) + '.gif'
#     output_file = os.path.join(LIGHT_WAVES_DIR, output_file)
#     convert_to_gif(input_file, output_file, 1)

pngs = [png for png in os.listdir(PROJECTILES_DIR) if png.endswith('.png')]

for png in pngs:
    input_file = os.path.join(PROJECTILES_DIR, png)
    output_file = '.'.join(png.split('.')[:-1]) + '.gif'
    output_file = os.path.join(PROJECTILES_DIR, output_file)
    convert_to_gif(input_file, output_file, 0.6)