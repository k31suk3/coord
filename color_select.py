
def rgb2colorcode(R:int, G:int, B:int, s=None) -> str:
    if s == None:
        color_code = '{:02x}{:02x}{:02x}'.format(R, G, B)
        return color_code.replace('0x', '')
    else:       
        color_code = '#{:02x}{:02x}{:02x}'.format(R, G, B)
        return color_code.replace('0x', '')

def gradation(num:int) -> list:
    """"Returns a list of color codes gradated by an arbitrary number of values specified in the argument.
        Arguments range from 1~1275.
        1~6       ["0000ff","00ffff","00ff00","ffff00","ff0000","ff00ff"]
        6~255     {"R":0,"G":0,"B":255} to {"R":0,"G":255,"B":254}
        56~510    {"R":0,"G":255,"B":255} to {"R":0,"G":255,"B":1}
        511~765   {"R":0,"G":255,"B":0} to {"R":254,"G":255,"B":0}
        766~1020  {"R":255,"G":255,"B":0} to {"R":255,"G":1,"B":0}
        1021~1275 {"R":255,"G":0,"B":0} to {"R":255,"G":0,"B":255}"""
    if num == 2:
        list_color_code = ["0000ff","00ffff",]
        return list_color_code
    elif num == 3:
        list_color_code = ["0000ff","00ffff","00ff00"]
        return list_color_code
    elif num == 4:
        list_color_code = ["0000ff","00ffff","00ff00","ffff00"]
        return list_color_code
    elif num == 5:
        list_color_code = ["0000ff","00ffff","00ff00","ffff00","ff0000"]
        return list_color_code
    elif num == 6:
        list_color_code = ["0000ff","00ffff","00ff00","ffff00","ff0000","ff00ff"]
        return list_color_code
    elif num > 1275:
        return "value Error! Enter a value of 1275 colors or less."
    else:  
        scale_range = 1275//num
        dic_color_code = {"R":0,"G":0,"B":255}
        list_color_code = []
        for i in range(1,1275,scale_range):
            if i <= 255:
                if i == 1:
                    hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                    list_color_code.append(hexcolor)
                else:
                    dic_color_code["G"] = (i)
                    hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                    list_color_code.append(hexcolor)
            elif 255 < i <= 510:
                dic_color_code["G"] = 255
                dic_color_code["B"] = 255-(i-255)
                hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                list_color_code.append(hexcolor)
            elif 510 < i <= 765:
                dic_color_code["B"] = 0
                dic_color_code["R"] = (i-510)
                hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                list_color_code.append(hexcolor)
            elif 765 < i <= 1020:
                dic_color_code["R"] = 255
                dic_color_code["G"] = 255-(i-765)
                hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                list_color_code.append(hexcolor)          
            else:
                dic_color_code["G"] = 0
                dic_color_code["B"] = (i-1020)
                hexcolor = rgb2colorcode(dic_color_code["R"],dic_color_code["G"],dic_color_code["B"])
                list_color_code.append(hexcolor)
        return list_color_code

def graation_verify(num:int):
    test_list = gradation(num)
    with open("test.html", "w")as test:
        for i, item in enumerate(test_list):
            print(i, item+"<font color="+item+">■■■■■■■</font><br>", file=test)
