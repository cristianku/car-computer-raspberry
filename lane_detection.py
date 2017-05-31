import cv2
from os import system
import matplotlib.pyplot as plt
import numpy as np


import graph_utils

class lane_detection():
    def __init__(self, original_frame):
        self._original_frame = original_frame


    def detection(self):
        imshape = self._original_frame.shape
        image_height = imshape[0]
        image_width = imshape[1]
        vertices_left = 0
        vertices_right = image_width - vertices_left
        vertices_mid = image_width / 2
        lower = np.array([80, 80, 40])
        upper = np.array([255, 255, 80])

        hsv = cv2.cvtColor(self._original_frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only yellow colors
        mask = cv2.inRange(hsv, lower, upper)
        # show_image('mask',mask)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(self._original_frame, self._original_frame, mask=mask)
        res = cv2.addWeighted(res, 1.0, self._original_frame, 1.0, 0)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        blur_gray = cv2.GaussianBlur(res, (5, 5), 0)

        canny = cv2.Canny(blur_gray, 50, 150)

        [vertices_top, vertices_bottom] = self.top(self._original_frame)

        vertices = np.array([[(vertices_left, vertices_bottom), (vertices_left, vertices_top + 10),
                              (vertices_right, vertices_top + 10), (vertices_right, vertices_bottom)
                              ]], dtype=np.int32)


        masked_edges = self.region_of_interest(canny, vertices)


        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 180  # angular resolution in radians of the Hough grid
        threshold = 40  # 15    # minimum number of points on a line (intersections in Hough grid cell)
        min_line_len = 100  # 20  # minimum number of pixels making up a line
        max_line_gap = 160  # 20  # maximum gap in pixels between connectable line segments

        lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                                maxLineGap=max_line_gap)
        for line in lines:
            for x1, y1, x2, y2 in line:
                # print (x1,y1,x2,y2)
                cv2.line(self._original_frame , (x1, y1), (x2, y2), color=[255, 0, 0], thickness=2)

        # new_lines = self.lane_lines(masked_edges, lines)
        #
        #
        # new_lines = self.lane_lines(masked_edges, lines)
        #
        # # here we should store historic lane_lines together
        # concat_lines = new_lines
        #
        # line_img = np.zeros(masked_edges.shape, dtype=np.uint8)
        # left_lane = self.lines_to_lane(masked_edges, concat_lines[0])
        # right_lane = self.lines_to_lane(masked_edges, concat_lines[1])
        # [left_lane, right_lane] = self.are_lanes_ok([left_lane, right_lane])
        # lanes = np.array([np.array([left_lane]), np.array([right_lane])])
        #
        # # lanes = lines_to_lanes2(img,new_lines)
        # self._original_frame = self.draw_lines(self._original_frame, lanes, thickness=10)



        # hough_lines_img = graph_utils.get_houg_lines_image(self._original_frame)
        #
        # combined_image = graph_utils.mark_lanes(hough_lines_img, self._original_frame)

        # plt.imshow(combined_image, cmap='gray')

        return self._original_frame

    # my modified and new functions
    def lane_lines(self,img, lines):
        """
        `lines` should be the output of a cv2.HoughLinesP.

        Returns left lane and right lane in a list.
        """
        num_lines = lines.shape[0]
        # rlines & llines store y values corresponding top and bottom x values along with weight (length of hf line y2-y1)
        llines = []
        rlines = []
        image_height = img.shape[0]
        image_width = img.shape[1]
        [image_top, image_bottom] = self.top(img)  # top is the lowest top x value of region on interest

        # for test drawing of what lines we are selecting
        tl_lines = []
        tr_lines = []
        skip_lines = []

        # filter out all the points that have slope outside 80-100 degrees
        for line in lines:
            for x1, y1, x2, y2 in line:
                skipped = True
                if (x2 == x1):
                    continue  # skip vertical lines
                m = np.round((y2 - y1) / (x2 - x1), 1)  # round to 1/10th
                b = np.round(y2 - m * x2, 0)  # round to integer
                # if(debug):
                # print("point (x1,y1,x2,y2) ",x1,y1,x2,y2," m,b",m,b,"image_width=",image_width,"image_width",image_width)
                # ignore high slopes and intercept that are not in the image
                if (x1 > 0.3 * image_width and m > .5 and b < 0.5 * image_width and b >= -100):
                    # find where the line intercepts the image bottom,
                    x_bottom = int((image_bottom - b) / m / 10) * 10  # round it to 10 pixels
                    # find where the line intercepts the top of region of interest,
                    x_top = int((image_top - b) / m / 10) * 10  # round it to 10 pixels
                    if (x_bottom > 0.7 * image_width and x_bottom < image_width):
                        newline = [x_bottom, x_top, (y2 - y1), y2]
                        # print("right line =",newline)
                        skipped = False
                        rlines.append(newline)
                        tr_lines.append(line)
                elif (m < -.5):
                    if (b < image_width and x2 < image_width):
                        # find where the line intercepts the image bottom,
                        x_bottom = int((image_bottom - b) / m / 10) * 10  # round it to 10 pixels
                        # find where the line intercepts the top of region of interest,
                        x_top = int((image_top - b) / m / 10) * 10  # round it to 10 pixels
                        if (x_bottom > 0 and x_top < 0.7 * image_width):
                            newline = [x_bottom, x_top, (y1 - y2), y1]
                            llines.append(newline)
                            tl_lines.append(line)
                            skipped = False
                if (skipped):
                    skip_lines.append(line)
                    # print("skipping (x1,y1,x2,y2) ",x1,y1,x2,y2," slope,intercept",m,b)

        # test_lines(img, skip_lines)
        new_lines = np.array([np.array(llines), np.array(rlines)])
        # print ("new_lines shape=",new_lines.shape)
        # print ("shapes of llines,rlines=",new_lines[0].shape,new_lines[1].shape)
        return new_lines

    def top(self,img):
        """
            Define where to truncate the image. This function brings hard-coding to one place.
        """
        hardcoding = 0.6

        image_height = img.shape[0]
        image_width = img.shape[1]
        image_top = hardcoding * image_height  # top is the lowest top x value of region on interest
        image_bottom = 1.0 * image_height

        return [image_top, image_bottom]

    @property
    def original_frame(self):
        return self._original_frame


    @property
    def final_image(self):
        return self._final_image

    def lines_to_lane(self,img, lines):
        """
        convert lines to single lane based on their weights (length of lines and closeness to car)
        """
        [top_y, bottom_y] = self.top(img)
        if(len(lines) == 0):
            lane = np.array([0, 0, 0, 0], dtype=np.int32)
            # print("no lane found for image " )
            return lane

        #print (lines.size)
        #print (lines)
        #print (np.median(lines,axis=0),np.std(lines,axis=0))
        median_bottom = np.median(lines,axis=0)[0]
        std_bottom = np.std(lines,axis=0)[0]
        median_top = np.median(lines,axis=0)[1]
        std_top = np.std(lines,axis=0)[1]

        product_sum=0
        bottom_sum=0
        top_sum=0
        count=0
        for line in lines:
            #print ("line=",line)
            [x_bottom,x_top,length,proximity] = line
            #print ("np.abs(x_top-median_top)",np.abs(x_top-median_top))
            #only chose points that are withing 1 std of mean ??? should it be median?
            if( ((std_bottom/median_bottom) > .15 and np.abs(x_bottom-median_bottom) > std_bottom) or
               ((std_top/median_top) > .15 and np.abs(x_top-median_top) > std_top)):
                    print ("skipping (x_bottom,x_top,length,proximity)", x_bottom,x_top,length,proximity)
            else:
                # print ("good (x_bottom,x_top,length,proximity)", x_bottom,x_top,length,proximity)
                product=length*proximity
                #product=length
                product_sum = product_sum+product
                bottom_xp = product*x_bottom
                bottom_sum = bottom_sum+bottom_xp
                top_xp = product*x_top
                top_sum = top_sum+top_xp
                count=count+1

        if(count>0):
            bottom_x = int(bottom_sum/product_sum)
            top_x = int(top_sum/product_sum)
            lane = np.array([bottom_x, bottom_y, top_x, top_y], dtype=np.int32)
        else:
            #cv2.imwrite("test_images/noleft-"+str(image_cnt)+".jpg",img)
            lane = np.array([0, 0, 0, 0], dtype=np.int32)

        return lane


    def region_of_interest(self, img, vertices):
        """
        Applies an image mask.

        Only keeps the region of the image defined by the polygon
        formed from `vertices`. The rest of the image is set to black.
        """
        #defining a blank mask to start with
        mask = np.zeros_like(img)

        #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(img.shape) > 2:
            channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255

        #filling pixels inside the polygon defined by "vertices" with the fill color
        cv2.fillPoly(mask, vertices, ignore_mask_color)

        #returning the image only where mask pixels are nonzero
        masked_image = cv2.bitwise_and(img, mask)
        return masked_image

    def are_lanes_ok(self, lanes):
        global prev_lanes
        prev_lanes=[]
        #are we here first time?
        if(len(prev_lanes) == 0):
            prev_lanes = lanes
            return lanes

        [prev_left_lane,prev_right_lane] = prev_lanes
        [left_lane, right_lane] = lanes
        #print(prev_left_lane,left_lane)
        #print(prev_right_lane,right_lane)

        #make sure x co-ordinates are not far apart (100 points)
        allowed=100
        if(abs(left_lane[0]-prev_left_lane[0]) > allowed or
           abs(left_lane[2]-prev_left_lane[2]) > allowed):
            #too much shift, keep old lane
            # print("for image_cnt=", image_cnt, "keeping prev left lane: prev, new ",prev_left_lane, left_lane)
            left_lane = prev_left_lane

        if(abs(right_lane[0]-prev_right_lane[0]) > allowed or
           abs(right_lane[2]-prev_right_lane[2]) > allowed):
            #too much shift, keep old lane
            # print("for image_cnt=", image_cnt, "keeping prev right lane: prev, new ", prev_right_lane, right_lane)
            right_lane = prev_right_lane

        #print("prev=",prev_lanes)
        lanes = [left_lane, right_lane]
        #print("new lanes=",lanes)
        prev_lanes = lanes

        return lanes

    def draw_lines(self, img, lines, color=[255, 0, 0], thickness=2):

        for line in lines:
            for x1,y1,x2,y2 in line:
                #print (x1,y1,x2,y2)
                cv2.line(img, (x1, y1), (x2, y2), color, thickness)

        return img

