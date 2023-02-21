import os
import numpy as np
import torch
import torch.nn as nn
from torchvision import models
from PIL import Image


def Load_ResNet_Model(weight_path):
        
    resnet_pretrained = models.resnet18(pretrained=True)
    for param in resnet_pretrained.parameters():
        param.requires_grad = False

    # change the output layer
    num_classes = 1
    num_ftrs = resnet_pretrained.fc.in_features
    # resnet의 마지막 층에 두 가지 결과만을 나타내도록 층 추가
    resnet_pretrained.fc = nn.Sequential(nn.Linear(num_ftrs, 20), nn.Dropout(0.4), nn.Linear(20,1))

    # 존재하는 가중치를 토대로 모델사용
    resnet_pretrained.load_state_dict(torch.load(weight_path))

    return resnet_pretrained

def classification(leaf_classification, N, input_file_path):
    
    img_to_numpy = []
    for i in range(N):
        img = Image.open(os.path.join(input_file_path, "leaf_{0}.jpg".format(i+1))) # 이미지들의 크기를 128*128로서 
        img = np.array(img).transpose(2,0,1) 
        img = img / 255.0 
        img_to_numpy.append(img)    

    test_data = torch.FloatTensor(img_to_numpy)


    leaf_classification.eval()
    with torch.no_grad():
        output_prob = torch.sigmoid(leaf_classification(test_data))
        output = torch.where(output_prob > 0.5,1,0)
    
    return output

