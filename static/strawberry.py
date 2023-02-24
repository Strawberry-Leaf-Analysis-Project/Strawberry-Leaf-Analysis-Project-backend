"""
Mask R-CNN
Train on the Strawberry Leaves dataset and implement color splash effect.

Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla

------------------------------------------------------------

Usage: import the module (see Jupyter notebooks for examples), or run from
       the command line as such:

    # Train a new model starting from pre-trained COCO weights
    python3 strawberry.py train --dataset=/path/to/strawberry/dataset --weights=coco

    # Resume training a model that you had trained earlier
    python3 strawberry.py train --dataset=/path/to/strawberry/dataset --weights=last

    # Train a new model starting from ImageNet weights
    python3 strawberry.py train --dataset=/path/to/strawberry/dataset --weights=imagenet

    # Apply color splash to an image
    python3 strawberry.py splash --weights=/path/to/weights/file.h5 --image=<URL or path to file>
"""

import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import keras.backend as K

# Root directory of the project -> Mask_RCNN
ROOT_DIR = os.path.abspath("../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from static.Mask_RCNN.mrcnn.config import Config
from static.Mask_RCNN.mrcnn import model as modellib, utils
from static.Mask_RCNN.mrcnn import visualize

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = os.path.join(ROOT_DIR, "logs")

############################################################
#  Configurations
############################################################


class StrawberryConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "strawberry"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + strawberry

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9


############################################################
#  Dataset
############################################################

class StrawberryDataset(utils.Dataset):

    def load_strawberry(self, dataset_dir, subset):
        """Load a subset of the Strawberry dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        self.add_class("strawberry", 1, "strawberry")

        # Train or validation dataset?
        assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)
        annotations = json.load(open(os.path.join(dataset_dir, "_annotations.coco.json")))
        for i in range(len(annotations['annotations'])):
            polygons = []  # segmentaion을 x, y 좌표 나누어서 저장
            all_points_x = list(map(int, annotations['annotations'][i]['segmentation'][0][0::2]))
            all_points_y = list(map(int, annotations['annotations'][i]['segmentation'][0][1::2]))
            polygons.append({'name':'polygon','all_points_x':all_points_x, 'all_points_y':all_points_y}) # 각 폴리곤에 해당하는 파일 이름을 할당 시킨다

            image_id = annotations['annotations'][i]['image_id']
            file_name = annotations['images'][image_id]['file_name']
            image_path = os.path.join(dataset_dir, file_name)
            image = skimage.io.imread(image_path)
            height, width = 1024, 1024

            self.add_image( "strawberry",
                            image_id=file_name,
                            path=image_path,
                            width=width,
                            height=height,
                            polygons=polygons)


    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a strawberry dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "strawberry":
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)
        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        return mask.astype(np.bool), np.ones([mask.shape[-1]], dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "strawberry":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


def train(model):
    """Train the model."""
    # Training dataset.
    dataset_train = StrawberryDataset()
    dataset_train.load_strawberry(args.dataset, "train")
    dataset_train.prepare()

    # Validation dataset
    dataset_val = StrawberryDataset()
    dataset_val.load_strawberry(args.dataset, "val")
    dataset_val.prepare()

    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=50,
                layers='heads')

def check_true(str):
    return str=="True"

def detect_and_color_splash(model, image_path=None):
    assert image_path

    if image_path:
        # Run model detection and generate the color splash effect
        input_image = os.path.join(image_path,"input_image.jpg")
        # Read image
        image = skimage.io.imread(input_image)
        # Detect objects
        results = model.detect([image], verbose=1)[0]

        # 이미지 세그먼트한 결과를 보여주는 기능
        r = results
        labels_to_names = {0: 'BG', 1: 'strawberry'}
        class_names = [value for value in labels_to_names.values()]
        output_img, state = visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'],
                                    class_names, image_path)
        return output_img, state

############################################################
#  Training
############################################################

if __name__ == '__main__':
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Train Mask R-CNN to detect strawberry leaves.')
    parser.add_argument("command",
                        metavar="<command>",
                        help="'train' or 'splash'")
    parser.add_argument('--dataset', required=False,
                        metavar="/path/to/strawberry/dataset/",
                        help='Directory of the Strawberry dataset')
    parser.add_argument('--weights', required=True,
                        metavar="/path/to/weights.h5",
                        help="Path to weights .h5 file or 'coco'")
    parser.add_argument('--logs', required=False,
                        default=DEFAULT_LOGS_DIR,
                        metavar="/path/to/logs/",
                        help='Logs and checkpoints directory (default=logs/)')
    parser.add_argument('--image', required=False,
                        metavar="path or URL to image",
                        help='Image to apply the color splash effect on')
    args = parser.parse_args()

    # Validate arguments
    if args.command == "train":
        assert args.dataset, "Argument --dataset is required for training"
    elif args.command == "splash":
        assert args.image,\
               "Provide --image to apply color splash"

    print("Weights: ", args.weights)
    print("Dataset: ", args.dataset)
    print("Logs: ", args.logs)

    # Configurations
    if args.command == "train":
        config = StrawberryConfig()
    else:
        class InferenceConfig(StrawberryConfig):
            # Set batch size to 1 since we'll be running inference on
            # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
            GPU_COUNT = 1
            IMAGES_PER_GPU = 1
        config = InferenceConfig()
    config.display()

    # Create model
    if args.command == "train":
        model = modellib.MaskRCNN(mode="training", config=config,
                                  model_dir=args.logs)
    else:
        model = modellib.MaskRCNN(mode="inference", config=config,
                                  model_dir=args.logs)

    # Select weights file to load
    if args.weights.lower() == "coco":
        weights_path = COCO_WEIGHTS_PATH
        # Download weights file
        if not os.path.exists(weights_path):
            utils.download_trained_weights(weights_path)
    elif args.weights.lower() == "last":
        # Find last trained weights
        weights_path = model.find_last()
    elif args.weights.lower() == "imagenet":
        # Start from ImageNet trained weights
        weights_path = model.get_imagenet_weights()
    else:
        weights_path = args.weights

    # Load weights
    print("Loading weights ", weights_path)
    if args.weights.lower() == "coco":
        # Exclude the last layers because they require a matching
        # number of classes
        model.load_weights(weights_path, by_name=True, exclude=[
            "mrcnn_class_logits", "mrcnn_bbox_fc",
            "mrcnn_bbox", "mrcnn_mask"])
    else:
        model.load_weights(weights_path, by_name=True)

    # Train or evaluate
    if args.command == "train":
        train(model)
    elif args.command == "splash":
        output_img = detect_and_color_splash(model, image_path=args.image)

def segmentation(weights):
    '''
    weights = 가중치 파일의 경로
    '''
    class InferenceConfig(StrawberryConfig):
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
    config = InferenceConfig()

    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=weights)
    weights_path = weights

    model.load_weights(weights_path, by_name=True)
    K.clear_session()
    return model