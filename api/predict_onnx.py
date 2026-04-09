import onnxruntime as ort
import numpy as np
from PIL import Image
import pickle
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, 'model', 'model.onnx')
CLASSES_PATH = os.path.join(BASE_DIR, 'model', 'classes.pkl')

with open(CLASSES_PATH, "rb") as f:
    classes = pickle.load(f)

session = ort.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name


def predict_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((224, 224))

    img = np.array(img) / 255.0
    img = np.transpose(img, (2, 0, 1))
    img = np.expand_dims(img, axis=0).astype(np.float32)

    outputs = session.run(None, {input_name: img})

    preds = outputs[0][0]
    idx = np.argmax(preds)
    conf = float(np.max(preds))

    return classes[idx], conf