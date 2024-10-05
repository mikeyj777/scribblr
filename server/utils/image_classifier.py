import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image

model = models.inception_v3(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize(299),
    transforms.CenterCrop(299),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def classify_image(image_file):
    image = Image.open(image_file)
    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        top_probabilities, top_indices = torch.topk(probabilities, 3)
    with open('imagenet_classes.txt') as f:
        labels = [line.strip() for line in f.readlines()]
    top_predictions = [(labels[idx], prob.item()) for idx, prob in zip(top_indices, top_probabilities)]
    return top_predictions