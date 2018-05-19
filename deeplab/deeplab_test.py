import time
import cv2
import numpy as np
from PIL import Image

from deeplab_model import DeepLabModel

# Needed to show segmentation colormap labels
import get_dataset_colormap

MODEL_PATH = "../../deeplab_model.tar.gz"

# If model is in download_path, skip downloading model.
if not os.path.isfile(MODEL_PATH):
    model_url = 'http://download.tensorflow.org/models/deeplabv3_pascal_trainval_2018_01_04.tar.gz'
    tf.gfile.MakeDirs(model_dir)

    print('downloading model to %s, this might take a while...' % download_path)
    urllib.request.urlretrieve(model_url, download_path)
    print('download completed!')


if __name__ == '__main__':
    model = DeepLabModel(MODEL_PATH)

    cap = cv2.VideoCapture(0)

    while True:
        start = time.time()
        ret, frame = cap.read()
        # From cv2 to PIL
        cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imshow('frame', frame)
        pil_im = Image.fromarray(cv2_im)

        # Run model
        resized_im, seg_map = model.run(pil_im)

        # Adjust color of mask
        seg_image = get_dataset_colormap.label_to_color_image(
            seg_map, get_dataset_colormap.get_pascal_name()).astype(np.uint8)

        cv2.imshow('seg_image', seg_image)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

        # to check fps
        print('{:.4f} fps'.format(1/(time.time() - start)))
