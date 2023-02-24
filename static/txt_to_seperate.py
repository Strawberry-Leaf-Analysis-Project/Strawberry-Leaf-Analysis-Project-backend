import numpy as np
import os
import cv2
from skimage import io

def check_true(str):
    return str=="1"

def background_remove(image, mask):
    for c in range(3):
        image[:, :, c] = np.where(mask == 1, image[:, :, c] , 0)
    return image


def txt_to_seperate(dir_path):
    '''
    입력 : 파일결로
     이미지도 해당 파일 내에 /input_image.jpg로 저장되어 있기 때문에 이를 활용하여 접근
    출력 : 따로 할게 없다
     저장시킬 이미지들은 /leaf_n.jpg로 저장된다
    
    텍스트 파일의 이름은 /leaves_information.txt
    텍스트 파일은 n개의 결과, 바운딩 박스 좌표, 마스크 정보들이 들어간다
    '''

    image = io.imread(os.path.join(dir_path, "input_image.jpg"))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    f = open(os.path.join(dir_path,'leaves_information.txt'),'r')
    N = int(f.readline())
    for i in range(N):
        y1, x1, y2, x2 = map(int, f.readline().split())
        
        mask = []
        for j in range(y2-y1):
            tmp = f.readline()
            tmp2 = list(map(check_true ,tmp.split()))
            mask.append(tmp2)
        mask = np.array(mask)

        seg_image = image.copy()
        seg_image = cv2.cvtColor(seg_image, cv2.COLOR_BGR2RGB)
        seg_image = background_remove(seg_image[y1:y2, x1:x2], mask)
        seg_image = cv2.resize(seg_image, (300, 300)) # 이파리 분할된 사진의 크기를 변경
        
        file_name = "leaf_" + str(i+1) + ".jpg"
        result_path = '{}/{}'.format(dir_path, file_name)

        retval, buffer = cv2.imencode('.bmp', seg_image)
        if (retval):
            with open(result_path, 'wb') as f_writer:
                f_writer.write(buffer)

    f.close()
    return N