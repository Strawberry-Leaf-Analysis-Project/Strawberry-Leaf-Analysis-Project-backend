import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
import shutil
from skimage import io

from sklearn.cluster import KMeans
from matplotlib.patches import Polygon


def leaf_kmeans(image, cluster_num, plants_colors):
    clt = KMeans(n_clusters=cluster_num) # 클러스터링 할 갯수 지정 / 3으로 지정하면 검정은 왠만하면 사라지고 잎 전체에 대해서 두 가지 평균 색상이 나오게 된다
    img_clt = clt.fit(image.reshape(-1,3))

    for i in img_clt.cluster_centers_:
        if sum(i) < 20 : # 검정색 배경에 대한 색상은 추출하지 않기 위해서
            continue
        plants_colors.append(i)

# 각 이피라에 접근하여 kmeans적용하여 검정색을 제외한 색상을 얻는다. 그 후 그것들의 평균을 리턴해 준다
# 이파리에 접근할 때 숫자로 접근하므로 수정사항 발생할 수 있다
def plants_leaves(dir_path, N):

    plant_color = [] # 이파리들의 평균 색상들의 집합
    # 각 이파리에 접근
    for i in range(N):
        leaf_image = io.imread(os.path.join(dir_path, "leaf_{0}.jpg".format(i+1)))
        leaf_img_rgb = cv2.cvtColor(leaf_image, cv2.COLOR_BGR2RGB)
        leaf_kmeans(leaf_img_rgb, 3, plant_color)

    return sum(plant_color) / len(plant_color)


# find masks point
def find_outlier(image, average_color):
    r = 0.5
    target = average_color / 256.0
    mask = np.zeros( (image.shape[0], image.shape[1]), dtype=np.float64)
    for h in range(image.shape[0]):
        for w in range(image.shape[1]):
            total = 0
            for i in range(3):
                origin = image[h,w,i] / 256.0
                total += (origin - target[i]) ** 2
                if i == 1:
                    total += 10*(origin - target[i]) ** 2
            if sum(image[h,w,:]) < 10 :
                mask[h,w] = 0.001
            elif total > r**2 :
                mask[h,w] = 1
    return mask    

# 1. 원하는 디렉토리를 입력
# 2. 그 디렉토리를 열어서 평균 색상을 얻는다
# 3. 각 이파리 별로 접근하여 이상치를 만들고 
# 4. 그것을 토대로 분류를 수행

def leaf_classification(leaf_path, average_color, percent=5):
    leaf_image = io.imread(leaf_path)
    leaf_image = cv2.cvtColor(leaf_image, cv2.COLOR_BGR2RGB)
    outlier = find_outlier(leaf_image, average_color)
    valid_area = 0
    valid_area += outlier[np.where(outlier[:,:] != 0.001)]
    radio = sum(sum(outlier)) / valid_area.shape
    if radio >= percent:
        return leaf_image, 1
    else :
        return leaf_image, 0


'''
- 비전을 적용하기 전에는 이파리들이 dir_path안에 저장되어 있어야 한다 / txt_to_seperate가 수행 완료 되어야한다
- 이파리들은 해당 디렉토리에 /leaf_n ( n = 1, 2 ...) 으로 저장되어 있다
- dir_path는 원본영상이 있는 파일로 해당 디렉토리에 이파리 이미지들도 같이 존재해야한다
# 평균 색상 추출하기
 average_color = plants_leaves(dir_path, N)
# 개별 이파리에 대한 적용
 for i in range(N):
    leaf_path = os.path.join(dir_path, "leaf_{0}.jpg".format(i+1))
    leaf, state  = leaf_classification(leaf_path, average_color) # average_color 뒤에 퍼센트를 임의로 부여하면 5프로 보다 적거나 많게 설정 가능
    if state == 0 :
        정상
    else :
        비정상

'''