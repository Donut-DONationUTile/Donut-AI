import os
import time
from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

# Declaring Constants
IMAGE_PATH = "/Users/kang/Documents/Github/donut-AI/asset/choco_banana.png"
SAVED_MODEL_PATH = "https://tfhub.dev/captain-pool/esrgan-tf2/1"


def preprocess_image(image_path):
  """ Loads image from path and preprocesses to make it model ready
      Args: 
        image_path: Path to the image file
  """
  hr_image = tf.image.decode_image(tf.io.read_file(image_path))
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)


def save_image(image, filename):
  """
    Saves unscaled Tensor Images.
    Args:
      image: 3D image tensor. [height, width, channels]
      filename: Name of the file to save.
  """
  if not isinstance(image, Image.Image):
    image = tf.clip_by_value(image, 0, 255)
    image = Image.fromarray(tf.cast(image, tf.uint8).numpy())
  image.save("%s.jpg" % filename)
  print("Saved as %s.jpg" % filename)

def i_enhance():
    hr_image = preprocess_image(IMAGE_PATH)
    print("done preprocess image")
    model = hub.load(SAVED_MODEL_PATH)
    fake_image = model(hr_image)
    fake_image = tf.squeeze(fake_image)
    return print("done image enhancement")


