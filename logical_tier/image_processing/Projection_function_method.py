from exception import Exception
import cv2
import math
from matplotlib import pyplot as plt

DOWNSCALE = 4
def detect_face_eyes(frame,miniframe,imageOperation):
    faces = imageOperation.detect_face(miniframe)
    for f in faces:
        x, y, w, h = [ v*DOWNSCALE for v in f ]
        roi_face = frame[y:y+h, x:x+w]
        eyes = imageOperation.get_eyes(roi_face,f)

        middle_face = (w / 2.0)
        for (ex,ey,ew,eh) in eyes:
            if(ew>0):
                if(eh>0):
                    print 'eye detected'
            if (ex > middle_face):
                cv2.rectangle(frame,(ex,ey),(ex+ew,ey+eh),(0,255,0))
                roi_eye = frame[(y + ey):(y + ey) + eh, (x + ex):(x + ex) + ew]
                #return [roi_eye,(x + ex),(y + ey)]
                eye_frame_gray = cv2.cvtColor(roi_eye, cv2.COLOR_BGR2GRAY)
                detect_center_eye(eye_frame_gray ,(x + ex),(y + ey),0.0,0.0)
                #detect_edges(roi_eye)

def calculate_total_ipf_vpf(gray_frame):
    result_ipf = 0.0
    result_vpf = 0.0
    y1 = (2 * (len(gray_frame) - 1)) / 4
    y2 = (3 * (len(gray_frame) - 1)) / 4
    y = y1
    x1 = 0.0
    x2 = len(gray_frame[0]) - 1
    while y < y2:
        ipf = calculate_horizontal_ipf(gray_frame,y,x1,x2)
        result_ipf += ipf
        result_vpf += calculate_horizontal_vpf(gray_frame,x1,x2,y,ipf)
        y += 1
    return [(result_ipf / (y2 - y1)),(result_vpf/(y2 - y1))]

def calculate_total_ipf_check(gray_frame):
    y1 = (2 * (len(gray_frame) - 1)) / 4
    y2 = (3 * (len(gray_frame) - 1)) / 4
    y = y1

    result = 0.0
    rij_result = 0.0
    while y < y2:
        x = 0.0
        while x < len(gray_frame[0]):
            rij_result += int(gray_frame[y][x])
            x += 1
        result += (rij_result / len(gray_frame[0]))
        rij_result = 0.0
        y += 1

    return (result / (y2 - y1))


def mark_vertical_line(frame, x,y1,y2,intensity):
    y = y1
    while y <= y2:
        frame[y][x] = intensity
        y += 1

def mark_horizontal_line(frame, y,x1,x2,intensity):
    x = x1
    while x <= x2:
        frame[y][x] = intensity
        x += 1
"""
def test(gray):
    x = 0
    y = 0

    while x < len(gray):
        y = 0
        while y < len(gray[x]):
            gray[y][x] = y
            y += 1
        x += 1
"""

def calculate_horizontal_line(alpha, gray, x1, x2,
                              y1_initial, y2_initial,fig,subplot,treshold):

    plot_y = []
    plot_pf = []
    plot_verschil = []
    hpf_horizontal = 0
    vorige_hpf_horizontal = 0
    y = y1_initial
    vorige_verschil = [0,0]
    y_kandidaten = []

    if (y2_initial > y1_initial):
        while y <= y2_initial:

            ipf_horizontal = calculate_horizontal_ipf(gray, y, x1, x2)
            vpf_horizontal = calculate_horizontal_vpf(gray, x1, x2, y, ipf_horizontal)

            vorige_hpf_horizontal = hpf_horizontal
            hpf_horizontal = (alpha * ipf_horizontal) + ((1 - alpha) * vpf_horizontal)

            if y < (y1_initial + 2):
                verschil = 0
            else:
                verschil = (hpf_horizontal - vorige_hpf_horizontal)

           # print str('y: ' + str(y) + '\t' + "verschil: " + str(verschil) + '\t' + "ipf: " + str( ipf_horizontal) + '\t' + "vpf: " + str(vpf_horizontal) + '\t' + "hpf: " + str(hpf_horizontal))
            plot_y.append(y)
            plot_pf.append(hpf_horizontal)
            plot_verschil.append(verschil)

            if verschil > treshold:
                return y
            """
           #     if verschil > vorige_verschil[0]:
           #         vorige_verschil = [verschil, y]
           # else:
           #     if vorige_verschil[0] > 0:
           #         #mark_horizontal_line(gray, vorige_verschil[1], x1, x2, 0)
           #         y_kandidaten.append(vorige_verschil[1])
                    y_kandidaten.append(y)
           #         vorige_verschil = [0, y]
            """
            y += 1
    else:
        while y >= y2_initial:

            ipf_horizontal = calculate_horizontal_ipf(gray, y, x1, x2)
            vpf_horizontal = calculate_horizontal_vpf(gray, x1, x2, y, ipf_horizontal)

            vorige_hpf_horizontal = hpf_horizontal
            hpf_horizontal = (alpha * ipf_horizontal) + ((1 - alpha) * vpf_horizontal)

            if y > (y1_initial - 2):
                verschil = 0
            else:
                verschil = (hpf_horizontal - vorige_hpf_horizontal)

            #print str('y: ' + str(y) + '\t' + "verschil: " + str(verschil) + '\t' + "ipf: " + str(ipf_horizontal) + '\t' + "vpf: " + str(vpf_horizontal) + '\t' + "hpf: " + str(hpf_horizontal))
            #plot_y.append(y)
            #plot_pf.append(vpf_horizontal)
            #plot_verschil.append(verschil)

            if verschil > treshold:
                return y
            """
           #     if verschil > vorige_verschil[0]:
           #         vorige_verschil = [verschil, y]
           # else:
           #     if vorige_verschil[0] > 0:
                    #mark_horizontal_line(gray, vorige_verschil[1], x1, x2, 0)
           #         y_kandidaten.append(vorige_verschil[1])
                    y_kandidaten.append(y)
           #         vorige_verschil = [0, y]
            """
            y -= 1
    return -1
    """
    print '==========================='
    print 'y_kandidaten'
    for item in y_kandidaten:
        print item
    print '==========================='
        #-------------------------------------------------------
    # Plot


    graph = fig.add_subplot(subplot)
    # Plot the data as a red line with round markers
    graph.plot(plot_y,plot_pf,'r-o')
    graph.plot(plot_y,plot_verschil,'g-o')



    #-------------------------------------------------------
    if(len(y_kandidaten) > 0):
        return y_kandidaten[0]
    else:
        if(vorige_verschil[0]>0):
            return vorige_verschil[1]
        else:
            return -1
    """


def calculate_vertical_lines(alpha, gray, y1, y2,treshold,x1_initial, x2_initial,fig, subplot):
    hpf_vertical = 0
    vorige_hpf_vertical = 0
    vorige_verschil = [0, 0]
    x = x1_initial
    x_kandidaten = []
    plot_x = []
    plot_pf = []
    plot_verschil = []
    teller = 0
    if(x1_initial < x2_initial):
        while x <= x2_initial:
            vorige_hpf_vertical = hpf_vertical
            ipf_vertical = calculate_vertical_ipf(gray, x, y1, y2)
            vpf_vertical = calculate_vertical_vpf(gray, y1, y2, x, ipf_vertical)
            hpf_vertical = alpha * ipf_vertical + (1 - alpha) * vpf_vertical

            if teller < 2:
                verschil = 0
            else:
                verschil = (hpf_vertical - vorige_hpf_vertical)
            teller += 1

            plot_x.append(x)
            plot_pf.append(hpf_vertical)
            plot_verschil.append(verschil)

            #print str('x: ' + str(x) + '\t' + "verschil: " + str(verschil) + '\t' + "vpf: " + str(vpf_vertical) + '\t' + "hpf: " + str(hpf_vertical))


            if verschil > treshold:
                return x
                """
                if verschil > vorige_verschil[0]:
                    vorige_verschil = [verschil,x]
            else:
                if vorige_verschil[0] > 0:
                    #mark_vertical_line(gray, vorige_verschil[1], y1, y2, 0.5)
                    x_kandidaten.append(vorige_verschil[1])
                    x_kandidaten.append(x)
                    vorige_verschil = [0, x]
                """
            x += 1
    else:
        while x >= x2_initial:
            teller += 1
            vorige_hpf_vertical = hpf_vertical
            ipf_vertical = calculate_vertical_ipf(gray, x, y1, y2)
            vpf_vertical = calculate_vertical_vpf(gray, y1, y2, x, ipf_vertical)
            hpf_vertical = alpha * ipf_vertical + (1 - alpha) * vpf_vertical

            if teller < 2:
                verschil = 0
            else:
                verschil = (hpf_vertical - vorige_hpf_vertical)

            #print str('x: ' + str(x) + '\t' + "verschil: " + str(verschil) + '\t' + "vpf: " + str(vpf_vertical) + '\t' + "hpf: " + str(hpf_vertical))


            if verschil > treshold:
                return x
            """
                if verschil > vorige_verschil[0]:
                    vorige_verschil = [verschil, x]
            else:
                if vorige_verschil[0] > 0:
                    #mark_vertical_line(gray, vorige_verschil[1], y1, y2, 0.5)
                    x_kandidaten.append(vorige_verschil[1])
                    x_kandidaten.append(x)
                    vorige_verschil = [0, vorige_verschil[1]]
            """
            x -= 1
    return -1
    """
    print "=============================="
    print "x_kandidaten:"
    for item in x_kandidaten:
        print item
    print "=============================="
            #-------------------------------------------------------
    # Plot


    graph = fig.add_subplot(subplot)
    # Plot the data as a red line with round markers
    graph.plot(plot_x,plot_pf,'r-o')
    graph.plot(plot_x,plot_verschil,'g-o')




    #-------------------------------------------------------

    if len(x_kandidaten) > 0:
        return x_kandidaten[0]
    else:
        if(vorige_verschil[0] > 0):
            return vorige_verschil[1]
        else:
            return -1
    """

def detect_center_eye(eye_frame_gray,x_position,y_position,set_brightness,set_contrast):
    alpha_iris = 0.6
    treshold_x_iris = 5
    fig_x_iris = plt.figure()

    subplot = 111


    x1_initial = 0.0
    x2_initial = float(len(eye_frame_gray[0]) - 1)

    y1_initial = 0.0
    y2_initial = math.floor(len(eye_frame_gray) - 1)

    #alpha = 0
    #alpha_iris = 0

    eye_position = detect_eye_boundaries(eye_frame_gray,x_position,y_position,set_brightness,set_contrast)
    x1 = eye_position[0][0]
    x2 = eye_position[1][0]
    y1 = eye_position[0][1]
    y2 = eye_position[1][1]

    x1_iris = calculate_vertical_lines(alpha_iris, eye_frame_gray, y1, y2,treshold_x_iris,x1,x2,fig_x_iris, subplot)
    x2_iris = calculate_vertical_lines(alpha_iris, eye_frame_gray, y1, y2,treshold_x_iris,x2,x1,fig_x_iris, subplot)
    """
    print str("y1: " + str(y1) + "\t" + "y2: " + str(y2))
    print str("x1: " + str(x1) + "\t" + "x2: " + str(x2))
    print str("x1_iris: " + str(x1_iris) + "\t" + "x2_iris: " + str(x2_iris))

    print '-----------------------------------------'
    """

    #-------------------------------------------------------
    # Test
    #mark_horizontal_line(eye_frame_gray,47,0,len(eye_frame_gray)-1,0.5)
    #-------------------------------------------------------





    x_center = x2 - x1
    y_center = y2 - y1
     # mark
    mark_vertical_line(eye_frame_gray,x1_iris,y1,y2,100)
    mark_vertical_line(eye_frame_gray,x2_iris,y1,y2,100)
    cv2.imshow('test',eye_frame_gray)

    """
    result = str("\n \n x_center: " + str(x_position + x_center) + "\t" + "y_center: " + str(y_position + y_center))
    print result
    plt.show()
    """


def detect_eye_boundaries(eye_frame_gray,x_position,y_position,set_brightness,set_contrast):
    """
    #total_ipf_normal = 68.8214334285
    #total_ipf_normal = 60.94624643
    #total_ipf_normal = 61.1061384532
    total_ipf_normal =  123.47399829497017
    total_vpf_normal = 29.299850501006954

    #brightness_initial = 100.0
    #contrast_initial = 90.0

    brightness_initial = 40.0
    contrast_initial = 60.0
    """
    fig_y = None
    fig_x = None
    fig_x_iris = None
    subplot = 111
    """

    # plot
    fig_y = plt.figure()
    fig_x = plt.figure()

    fig_x_iris = plt.figure()
    subplot = 111
    """
    #treshold = 0.305
    #treshold_y = 9
    #treshold_x = 11

    """
    #eye_frame_gray = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)

    total_ipf_vpf_gray = calculate_total_ipf_vpf(eye_frame_gray)

    print str("total_ipf_vpf: " + str(total_ipf_vpf_gray))
    print str("total_ipf test: " + str(calculate_total_ipf_check(eye_frame_gray)))


    #brightness = brightness_initial / total_ipf_vpf_gray[0] * total_ipf_normal * 0.2
    #brightness /= (abs(brightness - brightness_initial) / brightness)

    #contrast = contrast_initial /   total_ipf_vpf_gray[0] * total_ipf_normal * 0.2
    #contrast *= (abs(contrast - contrast_initial)/ contrast)

    #brightness = 45
    #contrast = 50
    """
    brightness = 0
    contrast = 0

    #brightness = set_brightness
    #contrast = set_contrast

    treshold_x = 2
    treshold_y1 = 3
    treshold_y2 = 2




    alpha = 0.6

    """
    newGray = image_operations.update_brightcont(eye_frame_gray, brightness, contrast)

    print str("brightness: " + str(brightness) + "\t contrast: "  + str(contrast))
    """
    #newGray = change_contrast(eye_frame_gray,10.0,2.0,255.0)
    #newGray = change_contrast_3de_poging(eye_frame_gray)
    #eye_frame_gray = newGray
    gray_original = eye_frame_gray

    """
    y = 0
    result = ''
    while y < len(eye_frame_gray):
        x = 0
        result += "\n" + "\n" + "y = " + str(y) + "\n" + "\t"
        while x < len(eye_frame_gray[0]):
            result += str(eye_frame_gray[y][x]) + "\t"
            x += 1
        y += 1
    print result
    cv2.imshow('original',eye_frame_gray)
    """

    # Dit stond er oorspronkelijk, als puur ipf en vpf gebruikt worden
    """
    x1_initial = 2.0
    x2_initial = float(len(eye_frame_gray[0]) - 1)

    y1_initial = math.floor(len(eye_frame_gray) * (1.0 / 5.0))
    y2_initial = math.floor(len(eye_frame_gray) * (3.0 / 4.0))
    """

    x1_initial = 0.0
    x2_initial = float(len(eye_frame_gray[0]) - 1)

    y1_initial = 0.0
    y2_initial = math.floor(len(eye_frame_gray) - 1)




    y1 = calculate_horizontal_line(alpha, gray_original,
                                       x1_initial, x2_initial,  y1_initial, y2_initial,fig_y,subplot,treshold_y1)


    y2 = calculate_horizontal_line(alpha, gray_original,
                                       x1_initial, x2_initial,  y2_initial, y1,fig_y,subplot,treshold_y2)



    x1 =  calculate_vertical_lines(alpha, gray_original, y1, y2,treshold_x,x1_initial,x2_initial,fig_x, subplot)
    x2 =  calculate_vertical_lines(alpha, gray_original, y1, y2,treshold_x,x2_initial,x1,fig_x, subplot)

    if (y2 - y1) + (x2 - x1) == 0:
        raise Exception.NoEyesDetected('Unable to detect the eye')

    """
    print '-----------------------------------------'
    # Mark
    mark_horizontal_line(eye_frame_gray,y1,x1_initial,x2_initial,0.5)
    mark_horizontal_line(eye_frame_gray,y2,x1_initial,x2_initial,0.5)

    mark_vertical_line(eye_frame_gray,x1,y1,y2,0)
    mark_vertical_line(eye_frame_gray,x2,y1,y2,0)

    cv2.imshow('test',eye_frame_gray)
    plt.show()
    """
    return [[x1 , y1],[ x2 , y2]]

def calculate_vertical_ipf(gray_frame, x_float,y1,y2):
    ipf = 0.0
    y = int(math.floor(y1))
    x = int(x_float)
    while y <= y2:
        ipf +=  int(gray_frame[y][x])
        y += 1

    result = float(ipf / float((y2 - y1 + 1)))
    return result

def calculate_horizontal_ipf(gray_frame, y,x1,x2):
    ipf = 0.0
    x = x1
    while x <= x2:
        ipf += int(gray_frame[y][x])
        x += 1

    return  float(ipf / (x2 - x1 + 1))

def calculate_vertical_vpf(gray_frame, y1, y2, x, vertical_ipf):
    y = y1
    tussen_resultaat = 0.0
    while(y <= y2):
        intensity = int(gray_frame[y][x])
        #tussen_resultaat += math.pow((intensity - vertical_ipf),2)
        tussen_resultaat += abs(intensity - vertical_ipf)
        #tussen_resultaat += (intensity - vertical_ipf)
        y += 1

    result = float(( 1.0 / (y2 - y1 + 1)) * float(tussen_resultaat))
    return result

def calculate_horizontal_vpf(gray_frame, x1, x2, y, horizontal_ipf):
    x = x1
    tussen_resultaat = 0.0
    while(x <= x2):
        intensity = int(gray_frame[y][x])
        #tussen_resultaat += math.pow((intensity - horizontal_ipf),2)
        tussen_resultaat += abs(intensity - horizontal_ipf)
        #tussen_resultaat += (intensity - horizontal_ipf)
        x += 1

    result = float(( 1.0 / (x2 - x1 + 1)) * float(tussen_resultaat))
    return result
