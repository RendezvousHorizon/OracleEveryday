import base64
import torch
from .model import model
import pandas as pd
import os
import torch
from PIL import Image
import numpy as np
from torchvision import transforms

MODEL_PATH = 'model.state_dict'
LABEL_PATH = 'label.csv'

if torch.cuda.is_available():
    model.load_state_dict(torch.load(MODEL_PATH))
else:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))


def load_image(img_path):
    pil_img = Image.open(img_path).convert('L')
    transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    image_data = transform(pil_img)
    return image_data


def predict(data, num_cands):
    data = data.unsqueeze(0)
    logits = model(data)[0]
    preds = [(i, logits[i]) for i in range(len(logits))]
    preds.sort(key=lambda x : x[1], reverse=True)
    # print('preds:', preds)
    preds = preds[0: num_cands]
    f = pd.read_csv(LABEL_PATH, header=None)
    result = [f[f[4] == pred[0]][2].values[0] for pred in preds]
    return result


def recognize(image_file, num_cands = 4):
    image_data = load_image(image_file)
    results = predict(image_data, num_cands)
    return results


def image2base64(image_path):
    with open(image_path, 'rb') as image_file:
        data = base64.b64encode(image_file.read())
        return data
