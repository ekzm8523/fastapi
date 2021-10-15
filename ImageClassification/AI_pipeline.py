import timm
from timm.models.layers.classifier import ClassifierHead
import torch.nn as nn
import torch
from torchvision import transforms
from torchvision.transforms import *
from PIL import Image
import random
import os

class MaskLabels:
    mask = 0
    incorrect = 1
    normal = 2


class GenderLabels:
    male = 0
    female = 1


class AgeGroup:
    map_label = lambda x: 0 if int(x) < 30 else 1 if int(x) < 58 else 2


class custom_resnet50(nn.Module): # mask, age, gender 클래스 별 분류
    def __init__(self):
        super(custom_resnet50, self).__init__()

        model = timm.create_model('resnet50', pretrained=True)
        self.backbone = nn.Sequential(*(list(model.children())[:-2]))
        self.mask_classifier = ClassifierHead(2048, 3)
        self.gender_classifier = ClassifierHead(2048, 2)
        self.age_classifier = ClassifierHead(2048, 3)

    def forward(self, x):
        x = self.backbone(x)
        z = self.age_classifier(x)
        y = self.gender_classifier(x)
        x = self.mask_classifier(x)
        return x, y, z


def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_model():
    device = get_device()
    model = custom_resnet50().to(device)
    model.eval()
    return model


def get_transform():
    transform = transforms.Compose([
        Resize((224, 224), Image.BILINEAR),
        ToTensor(),
        Normalize(mean=(0.548, 0.504, 0.479), std=(0.237, 0.247, 0.246)),
    ])
    return transform

def get_image():
    device = get_device()
    transform = get_transform()

    image_dir = os.path.join(os.getcwd(), 'static/image')
    image_list = os.listdir(image_dir)
    image_path = os.path.join(image_dir, random.choice(image_list))

    image = Image.open(image_path)
    image = transform(image).unsqueeze(0).to(device)

    return image, image_path


# pred = model(image)

# mask_pred = int(pred[0].argmax(dim=-1))
# gender_pred = int(pred[1].argmax(dim=-1))
# age_pred = int(pred[2].argmax(dim=-1))
#
#
# decode_mask_label = ['mask', 'incorrect', 'normal']
# decode_gender_label = ['mail', 'female']
# decode_age_label = ['0-30', '30-60', '60-']
#
# print(decode_mask_label[mask_pred])
# print(decode_gender_label[gender_pred])
# print(decode_age_label[age_pred])