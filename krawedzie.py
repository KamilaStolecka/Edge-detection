#
#
# Python 3.7
#
# Pillow version 6.0.0
#
# picture used: https://www.archdaily.com/889344/grove-at-grand-bay-big


from PIL import Image
import sys

def colour_channel(colour, lista, filtr):

    colours_dict = {

        'R' : 0,
        'G' : 1,
        'B' : 2
    }

    par = colours_dict[colour]

    wynik = 0
    for ii in range(3):
        for jj in range(3):
            wynik += lista[ii][jj][par] * filtr[ii][jj]


    return wynik


def normalization(lista:list):

    new_pixel = list()
    min_ = min(lista)
    max_ = max(lista)


    for i in lista:
        j = int(abs(2*(i-min_)/(max_ - min_) - 1)*255)
        new_pixel.append(j)

    return new_pixel


def edges(image, filter):
    """
    Function detects edges by using Prewitt filter

    :param image:
    :param filter: '---', '|', '/', '\'
    :return: 
    """
    # Should work for non-RGB modes as wel (eg. "L")
    if image.mode != 'RGB':
        image = image.convet('RGB')

    # Dictionary which provides matrixes based on user's choice of filtration

    Prewitt = {

        '---' : [[-1,-1,-1],[0,0,0],[1,1,1]],
        '|' : [[-1,0,1],[-1,0,1],[-1,0,1]],
        '\\' : [[0,1,1],[-1,0,1],[-1,-1,0]],
        '/' : [[-1,-1,0],[-1,0,1],[0,1,1]]

    }

    try:
        filtr = Prewitt[filter]
    except KeyError:
        sys.exit('Filter not found')

    new_pic = Image.new('RGB', (image.width , image.height), color=0)

    R_channel = list()
    G_channel = list()
    B_channel = list()

    for i in range(image.width - 2):
        for j in range(image.height -2):

            all_channels_list = list()
            for k in range(3):
                pixel_value = list()
                for z in range(3):

                    colour = image.getpixel((i+k, j + z))
                    pixel_value.append(colour)
                all_channels_list.append(pixel_value)

            # No need to write the same logic for each colour channel, so additional function was made

            R_channel.append(colour_channel('R',all_channels_list, filtr))
            G_channel.append(colour_channel('G', all_channels_list, filtr))
            B_channel.append(colour_channel('B', all_channels_list, filtr))

    # Pixel value cannot exceed 255, so they should be normalized

    R_channel = normalization(R_channel)
    G_channel = normalization(G_channel)
    B_channel = normalization(B_channel)


    # new picture is drawn
    m = 0
    for i in range(image.width - 2):
        for j in range(image.height - 2):
            coordinate = (i, j)

            new_pic.putpixel(coordinate, (R_channel[m], G_channel[m], B_channel[m]))
            m += 1



    return new_pic



if __name__ == '__main__':

    picture = Image.open("miami.jpg")

    # all filters are used on the spectacular example
    edges_horizontal = edges(picture, '---')
    edges_vertical = edges(picture, '|')
    edges_left = edges(picture, '\\')
    edges_right = edges(picture, '/')


    edges_horizontal.show()
    edges_vertical.show()
    edges_left.show()
    edges_right.show()
    