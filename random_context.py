from __future__ import print_function
import os, sys
from PIL import Image, ImageDraw, ImageFont
import math
import random
from copy import deepcopy
from G_free import *


full_path = os.path.realpath(__file__) # fulle path to this file
img_dir = os.path.dirname(full_path) #full path to directory from where this module is run
size = 260 # size of the image canvas
img_size = (size -5) # image area

"""
Coordinates of the initial pictorial form
"""

pform = [{"S": (0, 0, 1, 1)}]

pform1 = [{"L": (0, 0, 1/6, 1/6)}, {"w": (1/6, 0, 1/3, 1/6)}, {"w": (1/3, 0, 1/2, 1/6)}, {"w": (0, 1/6, 1/6, 1/3)}
         , {"B": (1/6, 1/6, 1/4, 1/4)}, {"w": (1/4, 1/6, 1/3, 1/4)}, {"w": (1/6, 1/4, 1/4, 1/3)}, {"Be": (1/4, 1/4, 1/3, 1/3)}
         , {"w": (1/3, 1/6, 1/2, 1/3)}, {"w": (0, 1/3, 1/6, 1/2)}, {"w": (1/6, 1/3, 1/3, 1/2)}, {"R": (1/3, 1/3, 1/2, 1/2)}
         , {"M": (1/2, 0, 1, 1/2)},
         {"M": (0, 1/2, 1/2, 1)}, {"M": (1/2, 1/2, 1, 1)}]

"""
This method to selects the rule randomly
"""

def get_rule(label, rules):
    rule1=[]
    for rule in rules:
        if rule[0] == label:
            rule1.append(rule)
    if len(rule1)>0:
        rule2=random.choice(rule1)
        return  rule2
    return None

"""
This method checks if forbidding context is present and enforces forbidding rule to be applied.
@:param forbidding - forbidding context
"""
def apply_forbidding_context(rule,pform1):
    forbidding_context= rule[2][1]
    current_labels=set()
    forbidding_context=set(forbidding_context)
    for sq in latest_pform:
        for label in sq:
            current_labels.update(label)
    if not forbidding_context&current_labels:
        return True



"""
This method checks if forbidding context is present, stores the forbidding rule and removes forbidding rule from rules.
@:param forbidding - forbidding context
"""
def apply_permitting_context(rule,pform1):
        current_labels=set()
        permitting_context=set()
        permitting_context.update(rule[2][0])
        for sq in latest_pform:
                for label in sq:
                    current_labels.update(label)

        if (len(permitting_context) > 0):
            if permitting_context.issubset(current_labels):
                return True
"""
This method checks if there are applicable rules.
"""

def hasApplicabeRule(rules, latest_pform):
    for rule in rules:
        square_label = rule[0]
        for sq in latest_pform:
            label = list(sq.keys())[0]
            if square_label== label:
                return True
    return False




"""
Font to be used for display labels on the squares in the images
"""
font = ImageFont.truetype("Arial Narrow.ttf", 12)

"""
@param rule1, a rule, e.g. ["B", ("E",), ("Yt", "E")]
@param pformV label and coordinates sets for the current pictorial production

:returns the set of coordinates to which the rule to be applied and
in case of multiple set of coordinates with the label, the index of the set to which the rules applies
"""
def applyRule(rule1, pformV):
    firstH = []  # all the label-coordinates pairs BEFORE the pair to which the rule1 will apply
    secondH = [] # all the label-coordinates pairs AFTER the pair to which the rule1 will apply
    middle = []  # the label-coordinates pair to which the rule1 will apply

    current_Square_label = rule1[0] # label to which the rule applies, e.g. "B" in ["B", ("E",), ("Yt", "E")]
    new_square_label = rule1[1] # the replacement squares, e.g. ("E") in ["B", ("E",), ("Yt", "E")]


    i = 0
    j =0
    for sq in pformV: # for each label-coordinates pair in pformV
        label = list(sq.keys())[0]
        value = sq[label]
        square_height = value[3] - value[1]
        if (label == current_Square_label and (square_height >= 1/200  or len(new_square_label) <2)):
            if (len(middle) < 1):
             middle = calculate_squares(sq[label], len(new_square_label), new_square_label)
        j = j+1


        if len(middle) <1:
            firstH.append(sq)
            i = i+1;
    secondH = pformV[(i+1):]  # get the remaining label-coordinates pair
    latest_pform=(firstH+middle+secondH)
    return latest_pform # return the updated set with the rule1 applied to the relevant label-coordinates pair and a count of such label-coordinate pair in the set
    ## for loop end

"""
this methods calculates the coordinates of the new squares that will replace an existing one
@:param basq - the parent square
@:param sqc - no of new squares
@:param newsqs - the new squares
@:return the new coordinates
"""

def calculate_squares (parent_square, new_square_length, new_squares):

    # no of rows within the parent square to fit the new squares
    rows = int(math.sqrt(new_square_length))

    #coordinates of the parent square, e.g. x1,y1, x2, y2
    ox1 = parent_square[0]
    oy1 = parent_square[1]
    ox2 = parent_square[2]
    oy2 = parent_square[3]
    # an empty list to hold the coordinates for the new squares
    new_square_list = []

    for r in range(0, rows): # for each row
        column_start = r*rows #start column
        column_end = column_start+rows; #end column
        i = 0;
        for c in range (column_start, column_end): # for each column in row r
            newsq = new_squares[c] # label for the new square
            dx = abs(ox2 - ox1)/rows #width of the new square
            dy = abs (oy2 - oy1)/rows #height of the new square
            nx1 = ox1+ (i*dx)
            ny1 =  oy1 + (r*dy)
            nx2 =  ox2 - (dx*(rows-(i+1)))
            ny2 =  oy2 - (dy*(rows-(r+1)))
            new_square_coordinates = {newsq:(nx1,ny1,nx2,ny2)}
            new_square_list.append(new_square_coordinates)
            i = i+1
    return new_square_list

"""
This method draws a given set of squares on the image canvas
@:param im - the image canvas
@:param pformV - coordinates of the squares to be drawn
"""

def drawPictorialForm(im, pformV):
    for sq in pformV:
        ##print (sq);
        for label in sq.keys():
            x1 = sq[label][0]
            y1 = sq[label][1]
            x2 = sq[label][2]
            y2 = sq[label][3]
            x1 = x1*img_size
            y1= 255 - (y1*img_size)
            x2 = x2*img_size
            y2 = img_size - (y2*img_size)
            fill = None

            if (label == "a"):
                fill = "green"
            if (label == "c"):
                fill = "brown"
            if (label == "o"):
                fill = "orange"
            if (label == "j"):
                fill = "magenta"
            if (label == "l"):
                fill = "blue"
            if (label == "k"):
                fill = 255 - 20 - 147
            if (label == "u"):
                fill = 208 - 32 - 14
            if (label == "e"):
                fill = "grey"
            if (label == "v"):
                fill = 255 - 105 - 180
            draw.rectangle((x1, y1, x2, y2), "grey")

            if (label == "w"):
                draw.ellipse((x1, y2, x2, y1), fill="white", )
            if (label == "b"):
                draw.ellipse((x1, y2, x2, y1), fill="black", )
            if (label == "g"):
                draw.ellipse((x1, y2, x2, y1), fill="white", )
            tx1 = x1 + ((x2 - x1) / 2)
            ty1 = y1 + ((y2 - y1) / 2)
            ##print (tx1, ty1)
            if label != "w":
                if label != "b":
                    if label != "g":
                        if label != "d":
                            if label != "c":
                                if label != "y":
                                    if label != "l":
                                        if label != "o":
                                            if label != "j":
                                                if label != "k":
                                                    if label != "i":
                                                        if label != "u":
                                                            if label != "e":
                                                                if label != "v":
                                                                    draw.text((tx1 - 5, ty1 - 5), label, font=font,
                                                                              fill="black")


"""
This method handles user inputs form the command line
"""
def userInput(q):
    while True:
        ip = input(q)
        if (ip.lower() == "y"):
            break
        elif ip.lower() == "n":
            print("Good bye")
            sys.exit(0)

"""
The main method that goes through rules list and creates images as prompted by the user.
"""
if __name__ == "__main__":
    rules = control_bag

    ## Draw the initial production
    im = Image.new("RGB", (size,size), "white")
    draw = ImageDraw.Draw(im)

    drawPictorialForm(im, pform)

    im.save(os.path.join(img_dir,"initial.png"), "PNG")
    print ("Saved initial file to "+os.path.join(img_dir,"initial.png"))
    ## delete the draw object and prepare for next production
    del draw

    ## i to keep track of number of images producted
    i = 1
    latest_pform = pform #copies the coordiantes of the initial production into rform

    while hasApplicabeRule(rules, latest_pform):

        current_labels=[]
        for sq in latest_pform:
            for label in sq:
                current_labels.append(label)
        print("Current labels: ",current_labels)
        #current_labels=random.shuffle(current_labels)
        selected_rule= random.choice(current_labels)
        print("selected_label: ",selected_rule)
        rule=get_rule(selected_rule,rules)
        if rule != None:
                    print("rule:",rule)
                    permitting=rule[2][0]
                    forbidding=rule[2][1]

                    if len(permitting)==0 and len(forbidding)==0:
                        latest_pform = applyRule(rule, latest_pform) # apply the current rule
                    elif len(permitting)>0 and len(forbidding)>0:
                            if (apply_permitting_context(rule,latest_pform)==True) and (apply_forbidding_context(rule,latest_pform) ==True):
                                latest_pform = applyRule(rule, latest_pform) # apply the current rule
                    elif (len(permitting)>0) and (len(forbidding)==0):
                                    if apply_permitting_context(rule,latest_pform):
                                        latest_pform = applyRule(rule, latest_pform) # apply the current rule
                    elif (len(permitting)==0) and (len(forbidding)>0):
                                if apply_forbidding_context(rule,latest_pform)==True:
                                    latest_pform = applyRule(rule, latest_pform) # apply the current rule

                    else:
                                    print("cant apply rule")

                    im = Image.new("RGB", (size,size), "white")
                    draw = ImageDraw.Draw(im)

                    #print("printing..", rule)
                    drawPictorialForm(im, latest_pform)
                    del draw
                    name = os.path.join(img_dir,"image"+str(i))
                    #im.show()
                    im.save(name+".png", "PNG")
                    print("Saved to ", name+".png")
                    previous_rule=rule[0]
                    next_rule=rule[0]
                    i = i+1

       #else:
                #print("rule not applicable: ", rule)

