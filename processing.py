import cv2
import numpy as np
import pytesseract
import solver
nolist = []
concenterlist = []


def resizeimage(img):
    scale_percent = 50  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def filtercontours(contours):
    filterlist = []
    for c in contours[1::]:
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        area = cv2.contourArea(box)
        if area > 4000:
            filterlist.append(c)
    return filterlist


def findcontourcenter(contour):
    M = cv2.moments(contour)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    return (cx, cy)


def main():
    while len(nolist) != 81:
        image = cv2.imread("sudoku.png")
        resizedimage = resizeimage(image)
        gray = cv2.cvtColor(resizedimage, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (11, 11), 3)
        returns, thresh = cv2.threshold(
            gray, 125, 255, cv2.THRESH_BINARY_INV)
        contours, hierachy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        getfilteredcontour = filtercontours(contours)
        for con in getfilteredcontour[::-1]:
            area = cv2.contourArea(con)
            if area > 4000:
                rect = cv2.boundingRect(con)
                concenterlist.append(str(findcontourcenter(
                    con)[0])+"-"+str(findcontourcenter(con)[1]))
                cv2.drawContours(resizedimage, [con], 0, (0, 255, 0), 2)
                getroi = gray_blur[rect[1]:rect[1] +
                                   rect[3], rect[0]:rect[0]+rect[2]]
                text = pytesseract.image_to_string(
                    getroi, lang="eng",
                    config='--psm 7 -c tessedit_char_whitelist=0123456789.%')
                if str(text).splitlines()[0] == "":
                    nolist.append(0)
                else:
                    nolist.append(int(str(text).splitlines()[0].split(".")[0]))
            cv2.imshow("Wait I am Reading", resizedimage)
            if cv2.waitKey(1) == 27:
                break


def solve(bo):
    find = solver.find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if solver.valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0
    return False


def get_tuple_coordinates(stringvalue):
    (x, y) = stringvalue.split("-")
    return (int(x)-1, int(y)+1)


main()
board = np.array(nolist).reshape(9, 9)
print(board)
concenterlist = np.asanyarray(concenterlist).reshape(9, 9)
print(concenterlist)
forverification = board.copy()
solve(board)
print(board)
while True:
    image = cv2.imread("sudoku.png")
    resizedimage = resizeimage(image)
    for i in range(len(forverification)):
        for j in range(len(forverification[0])):
            if forverification[i][j] == 0:
                cv2.putText(resizedimage, str(board[i][j]), get_tuple_coordinates(concenterlist[i][j]),
                            cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0),
                            2)
    cv2.imshow("OK it's Over See the Result", resizedimage)
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
