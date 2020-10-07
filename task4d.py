
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

''' References
This subtask's skeleton was taken from https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
Changes/additions to skeleton:
- Replace static image with feed from video taken
- Print primary cluster center to terminal
- Run clustering only on center rectangle, marked on the frame
'''

def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture("tracking_phone_high.mov")

while True:
    frame_available, frame = cap.read()
    if not frame_available:
        break

    img = frame

    crop_img = img[int(img.shape[0]*0.4):int(img.shape[0]*0.6), int(img.shape[1]*0.4):int(img.shape[1]*0.6)]
    cv2.rectangle(frame, (int(img.shape[1]*0.4), int(img.shape[0]*0.4)), (int(img.shape[1]*0.6), int(img.shape[0]*0.6)), (255, 0, 0), 2)
    img_reshape = crop_img.reshape((crop_img.shape[0] * crop_img.shape[1],3)) #represent as row*column,channel number
    clt = KMeans(n_clusters=3) #cluster number
    clt.fit(img_reshape)
    
    hist = find_histogram(clt)
    bar = plot_colors2(hist, clt.cluster_centers_)
    print(clt.cluster_centers_[0])

    cv2.imshow('frame', frame)
    cv2.imshow('bar', bar)
    k = cv2.waitKey(50) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()