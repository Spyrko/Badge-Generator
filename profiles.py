class Profile:
    def __init__(self,
                 filename,
                 conf_name,
                 logo,
                 logo_offset,
                 logo_height,
                 point_size,
                 sticker_size,
                 print_sticker,
                 qr):
        self.filename = filename
        self.height = 74
        self.width = self.height * 1.41
        self.conf_name = conf_name
        self.logo = logo
        self.logo_offset = logo_offset
        self.logo_height = logo_height
        self.point_size = point_size
        self.sticker_size = sticker_size
        self.print_sticker = print_sticker
        self.qr = qr


example = Profile(filename = 'example',         # without -o result will be saved as 'example.pdf'
                  conf_name = "Conference",     # name of the conference (lower left corner)
                  logo = "img/tux.svg",         # path to logo (must be svg)
                  logo_offset = (0, 0),         # offset of logo from lower left corner of border (x,y)
                  logo_height = 50,             # height of logo (width will be calculated)
                  point_size = 8,               # diameter of points in upper right corner
                  sticker_size = 13,            # size of squares in upper right corner
                  print_sticker = True,         # print points and squares in upper right corner
                  qr = True)                    # print ID as qrcode

default = "example"

dict = {"example":example}