from pyx import *
import profiles as pro
import shutil
import os
import sys
import csv
import qrcode
import qrcode.image.svg

def escape(str):
    replace = {"_":"\_"}

    for k,v in replace.items():
        str = str.replace(k,v)
    return str


class Badge:
    height = 74                     # Do not change this, just used for formatting
    width = 105                     # Do not change this, just used for formatting
    font = "cabin"                  # Take a font known by your LaTeX distribution (e.g. texlive)
    font_attr = "sfdefault"         # optional attributes for your font
    logo_color = color.grey(0.7)    # Fill color of your logo (just needed for some logos)
    tmp_dir = "tmp"                 # temp directory to be created and deleted while generating pdf


    def __init__(self, name, university, handle, id, profile):
        self.id = id
        self.name = escape(name)
        self.uni = escape(university)
        self.handle = escape(handle)
        self.profile = profile
        self.tmp_file = Badge.tmp_dir+"/"+str(self.id)+".svg"


    def draw(self):
        framesize = 0
        margin = 3
        name_height = 10
        name_size = 370
        name_width = 62
        handle_height = name_height + (name_height * 0.5) + 5
        handle_size = name_size * 0.5
        uni_height = handle_height + (name_height * 0.375) + 3
        uni_size = name_size * 0.375
        kif_size = name_size * 0.75
        qr_size = 40
        c = canvas.canvas()

        # create cuttinglines
        cuttingLines = path.path(path.moveto(0, 0),
                                 path.lineto(self.profile.width, 0),
                                 path.lineto(self.profile.width, self.profile.height),
                                 path.lineto(0, self.profile.height),
                                 path.closepath())
        # create frame
        frame = path.path(path.moveto(self.x(framesize), self.y(framesize)),
                          path.lineto(self.profile.width - self.x(framesize), self.y(framesize)),
                          path.lineto(self.profile.width - self.x(framesize), self.profile.height - self.y(framesize)),
                          path.lineto(self.x(framesize), self.profile.height - self.y(framesize)),
                          path.closepath())

        sticker = path.path(path.moveto(self.profile.width - self.x(framesize+margin),
                                        self.profile.height - self.y(framesize+margin)),
                            path.lineto(self.profile.width - self.x(framesize+margin),
                                        self.profile.height - self.y(framesize+margin+self.profile.sticker_size)),
                            path.lineto(self.profile.width - self.x(framesize+margin+self.profile.sticker_size),
                                        self.profile.height - self.y(framesize+margin+self.profile.sticker_size)),
                            path.lineto(self.profile.width - self.x(framesize+margin+self.profile.sticker_size),
                                        self.profile.height - self.y(framesize+margin)),
                            path.lineto(self.profile.width - self.x(framesize + margin),
                                        self.profile.height - self.y(framesize + margin)),
                            path.moveto(self.profile.width - self.x(framesize + margin),
                                        self.profile.height - self.y(framesize + margin+ self.profile.sticker_size + 2)),
                            path.lineto(self.profile.width - self.x(framesize + margin),
                                        self.profile.height - self.y(framesize + margin + self.profile.sticker_size+self.profile.sticker_size + 2)),
                            path.lineto(self.profile.width - self.x(framesize + margin + self.profile.sticker_size),
                                        self.profile.height - self.y(framesize + margin + self.profile.sticker_size+self.profile.sticker_size + 2)),
                            path.lineto(self.profile.width - self.x(framesize + margin + self.profile.sticker_size),
                                        self.profile.height - self.y(framesize + margin+self.profile.sticker_size + 2)),
                            path.closepath())

        points = (path.circle(self.profile.width-self.x(framesize+2*margin+self.profile.sticker_size+0.5*self.profile.point_size),
                             self.profile.height - self.y(framesize + margin+0.5*self.profile.point_size),
                             self.x(0.5*self.profile.point_size)),
                  path.circle(self.profile.width - self.x(framesize + 2 * margin + self.profile.sticker_size + 0.5 * self.profile.point_size),
                              self.profile.height - self.y(framesize + margin + self.profile.sticker_size + 1),
                              self.x(0.5 * self.profile.point_size)),
                  path.circle(self.profile.width - self.x(framesize + 2 * margin + self.profile.sticker_size + 0.5 * self.profile.point_size),
                              self.profile.height - self.y(framesize + margin + 2 * self.profile.sticker_size + 2 - 0.5 * self.profile.point_size),
                              self.x(0.5 * self.profile.point_size)))


        runner = text.latexrunner(texenc="utf8")
        runner.preamble(r"\usepackage{lmodern} \usepackage[" + Badge.font_attr + r"]{" + Badge.font + r"} \usepackage[utf8]{inputenc}")
        name = runner.text(0,0,
                           r"{\fontsize{" + str(name_size) + "}{0} \selectfont " + self.name +"}")
        handle = runner.text(self.x(framesize+margin),
                             self.profile.height - self.y(framesize+margin+handle_height),
                             r"{\fontsize{" + str(handle_size) + "}{0} \selectfont " + self.handle +"}")
        uni = runner.text(self.x(framesize+margin),
                          self.profile.height - self.y(framesize+margin+uni_height),
                          r"{\fontsize{" + str(uni_size) + "}{0} \selectfont " + self.uni +"}")
        kif = runner.text(self.x(framesize+margin),
                          self.y(framesize+margin),
                          r"{\fontsize{" + str(kif_size) + "}{0} \selectfont " + self.profile.conf_name +"}")

        logo = canvas.canvas()
        svg = svgfile.svgfile(self.x(framesize+margin+self.profile.logo_offset[0]),
                              self.y(framesize+self.profile.logo_offset[1]),
                              self.profile.logo,
                              height=self.profile.logo_height,
                              parsed=True,
                              fill=Badge.logo_color)
        logo.insert(svg)
        

        self.qr()
        qr = canvas.canvas()
        qr.insert(svgfile.svgfile(self.width-self.x(framesize+qr_size),
                                  self.y(framesize),
                                  self.tmp_file,
                                  height=qr_size,
                                  parsed=True))



        # draw all the paths
        c.insert(logo)

        c.stroke(frame, [style.linewidth.THICk,
                         color.rgb.black])
        if self.profile.print_sticker:
            c.stroke(sticker, [style.linestyle.dotted, style.linewidth.THICk])
            for i in range(3):
                c.stroke(points[i], [style.linewidth.THICk, style.linestyle.dotted])

        namesmultiplier = 1 if self.x(name_width) > name.bbox().width() else self.x(name_width) / unit.tocm(name.bbox().width())
        c.insert(name, [trafo.scale(namesmultiplier),
                        trafo.translate(self.x(framesize+margin),
                                        self.profile.height - self.y(framesize+margin+name_height))])
        c.insert(handle)
        c.insert(uni)
        c.insert(kif)
        if self.profile.qr:
            c.insert(qr)

        return document.page(c, centered=1, paperformat=document.paperformat.A4, bbox=cuttingLines.bbox(),  fittosize=True, rotated=True)



    def qr(self):
        factory = qrcode.image.svg.SvgPathImage
        if not os.path.exists(Badge.tmp_dir):
            os.makedirs(Badge.tmp_dir)
        code = qrcode.make(str(self.id), image_factory=factory, error_correction=qrcode.ERROR_CORRECT_H)
        code.save(self.tmp_file)


    def x(self, mm):
        return (self.profile.width / 105) * mm


    def y(self,mm):
        return self.x(mm)


def import_csv(filename, profile, count):
    pages = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=';', escapechar="\\", doublequote=False)
        for row in reader:
            badge = Badge(*row,profile)
            page = badge.draw()
            for i in range(count):
                pages.append(page)
    document.document(pages).writePDFfile(profile.filename, text_as_path=True)
    print_succ("Badges saved to '" + profile.filename + ".pdf'")


#badge = Badge(1,"Spyrko","Universität-Bremen", "@spyrko",normal)
#badge.draw()

def print_err(str):
    print("\33[91m" + str + "\33[0m")

def print_info(str):
    print("\33[93m" + str + "\33[0m")

def print_succ(str):
    print("\33[1m\33[92m" + str + "\33[0m")

def print_help():
    print_info("usage: python3 badges.py [input.csv] [args]")
    print("arguments:")
    print("    -c           : Print cutting-lines (no effect if no -m is specified)")
    print("    -h           : Print this help")
    print("    -m [count]   : Multiple badges per page")
    print("    -n [count]   : Create multiple badges per entry")
    print("    -o [filename]: Set output file (without .pdf)")
    print("    -p [profile] : Profile to use")


def further_info():
    print_info("Use -h for further information")

def command_not_known(arg):
    print_err("Command '" + arg + "' not known.")

def print_known_profiles():
    print("Known profiles are: ")
    for k in sorted(pro.dict.keys()):
        print("    " + k)



def main(argv):
    output = None
    profile = None
    multipage = None
    count = 1
    cutting = ""
    if len(argv) < 1:
        print_help()
        return
    else:
        skip = False
        for i in range(len(argv)):
            if i == 0:
                if argv[0][0] == '-':
                    if argv[0] == '-h':
                        print_help()
                        return
                    else:
                        print_err("First argument should be the csv.")
                        further_info()
                        return
                else:
                    continue

            if skip:
                skip = False

            elif not argv[i][0] == '-' or len(argv[i]) < 2:
                command_not_known(argv[i])
                further_info()
                return

            elif argv[i][1] == 'h':
                print_help()
                return

            elif argv[i][1] == 'c':
                cutting = "-d "
                continue

            elif argv[i][1] == 'o':
                if len(argv) <= i+1 or argv[i+1][0] == '-':
                    print_err('-o needs a filename')
                    further_info()
                    return
                output = argv[i+1]
                skip = True

            elif argv[i][1] == 'm':
                if len(argv) <= i+1 or argv[i+1][0] == '-':
                    print_err('-m needs a count')
                    further_info()
                    return
                try:
                    multipage = int(argv[i+1])
                except ValueError:
                    print_err('Given parameter for -m must be a number')
                    further_info()
                    return
                skip = True

            elif argv[i][1] == 'n':
                if len(argv) <= i+1 or argv[i+1][0] == '-':
                    print_err('-n needs a count')
                    further_info()
                    return
                try:
                    count = int(argv[i+1])
                except ValueError:
                    print_err('Given parameter for -n must be a number')
                    further_info()
                    return
                skip = True

            elif argv[i][1] == 'p':
                if len(argv) <= i+1 or argv[i+1][0] == '-':
                    print_err('-p needs a profile')
                    print_known_profiles()
                    further_info()
                    return
                try:
                    profile = pro.dict[argv[i+1]]
                except KeyError:
                    print_err("Profile '" + argv[i+1] + "' not known.")
                    print_known_profiles()
                    return
                skip = True

            else:
                command_not_known(argv[i])
                further_info()
                return



    if not profile:
        profile = pro.dict[pro.default]
        print_info("Using default profile: '" + pro.default +"'")
    if output:
        profile.filename = output

    import_csv(argv[0], profile, count)
    if multipage:
        os.system("pdf2ps " + profile.filename + ".pdf tmp/" + profile.filename + ".ps")
        os.system("psnup -q -m 1mm " + cutting + " -n " + str(multipage) + " -p a4 -P a4 -f tmp/"+ profile.filename +".ps tmp/"+ profile.filename +"-multi.ps")
        os.system("ps2pdf tmp/"+ profile.filename + "-multi.ps " + profile.filename + ".pdf")
    shutil.rmtree(Badge.tmp_dir,True)

if __name__ == "__main__":
   main(sys.argv[1:])