import os
import io
import uuid
import datetime
import numpy as np

from PIL import Image
import tensorflow as tf
import tensorflow_hub as hub

os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

# Declaring Constants
SAVED_MODEL_PATH = "https://tfhub.dev/captain-pool/esrgan-tf2/1"


#이미지 전처리
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

#이미지 전처리2
def preprocess_image_v2(hr_image):
  """ Loads image from path and preprocesses to make it model ready
      Args: 
        image_path: Path to the image file
  """
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.

   # PIL 이미지 객체로 변환
  image = Image.open(io.BytesIO(hr_image))
  # NumPy 배열로 변환
  hr_image = np.array(image)
  print("Successfully download image, time : " +  str(datetime.datetime.now()))
  
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

#이미지 저장
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


# 이미지 고해상도 
def i_enhance(image_path):
    hr_image = preprocess_image(image_path)
    print("done preprocess image, time: "+ str(datetime.datetime.now()))

    model = hub.load(SAVED_MODEL_PATH)
    print("done load image, time: "+ str(datetime.datetime.now()))
    fake_image = model(hr_image)
    print("done enhance image, time: "+ str(datetime.datetime.now()))

    stored_name = str(uuid.uuid4()) 
    output_path = "output/"+ stored_name 
    save_image(tf.squeeze(fake_image), filename=output_path) 
    print("save image, time: "+ str(datetime.datetime.now()))

    return output_path


