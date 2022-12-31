# translates rgb values to hex color vals
# from https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter/51592104
def fromrgb(rgb):
        return "#%02x%02x%02x" % rgb 

# translates hex to rgb
# from https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
def fromHex(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))