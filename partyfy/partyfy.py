from PIL import Image
from colorsys import rgb_to_hls, hls_to_rgb
from io import BytesIO
from pathlib import posixpath


def rgb2hls(r,g,b):
    """ convert PIL-like RGB tuple (0 .. 255) to colorsys-like
    HSL tuple (0.0 .. 1.0) """
    r /= 255.0
    g /= 255.0
    b /= 255.0
    return rgb_to_hls(r,g,b)


def hls2rgb(h,l,s):
    """ convert a colorsys-like HSL tuple (0.0 .. 1.0) to a
    PIL-like RGB tuple (0 .. 255) """
    r,g,b = hls_to_rgb(h,l,s)
    r *= 255
    g *= 255
    b *= 255
    return (int(r),int(g),int(b))


def partyfy_gif(gif, party_num):
    party_frames = []
    for frame_count in range(gif.n_frames):
        gif.seek(frame_count)
        party_frames.append(partyfy_frame(gif, frame_count, party_num))
    return party_frames


def partyfy_frame(frame, frame_count, party_num):
    img = frame.convert("RGBA")
    img_data = list(img.getdata())
    for i in range(len(img_data)):
        img_data[i] = partyfy_pixel(img_data[i], frame_count, party_num)
    img.putdata(img_data)
    return img


def partyfy_pixel(pixel, frame_count, party_num):
    # Pixels should be in RGBA format
    r,g,b,a = pixel
    h,l,s = rgb2hls(r,g,b)
    # h is a number between 0 and 1 that maps to 0 and 360
    h = ((frame_count * party_num) % 360) / 360.0
    r,g,b =  hls2rgb(h,l,s)
    return int(r),int(g),int(b),a


def save_party(party_frames, gif_info, file):
    party_frames[0].save(
        file,
        format='GIF',
        append_images=party_frames[1:],
        save_all=True,
        duration=gif_info["duration"],
        loop=0, # number of times gif will loop (0 means always :shrug:)
        # transparency=gif_info["transparency"],
        transparency=0,
        disposal=2, # Restore to background color.
    )


def partyfy_to_bytes(gif_source, party_num):
    gif = Image.open(gif_source)
    party_frames = partyfy_gif(gif, party_num)
    bytes = BytesIO()
    save_party(party_frames, gif.info, bytes)
    bytes.seek(0)
    return bytes


def partyfy(gif_source, party_num):
    gif = Image.open(gif_source)
    party_frames = partyfy_gif(gif, party_num)
    basename = posixpath.basename(gif_source)
    dirname = posixpath.dirname(gif_source)
    name = posixpath.join(dirname, f"party_{basename}")
    save_party(party_frames, gif.info, name)
