import numpy as np

# Dataset names.
_CITYSCAPES = 'cityscapes'

# Max number of entries in the colormap for each dataset.
_DATASET_MAX_ENTRIES = {
    _CITYSCAPES: 19
}


def create_cityscapes_label_colormap():
  """Creates a label colormap used in CITYSCAPES segmentation benchmark.

  Returns:
    A Colormap for visualizing segmentation results.
  """
  colormap = np.asarray([
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 255],
      [0, 0, 0],
      [0, 0, 0],
      [0, 0, 0],
  ])
  return colormap


def label_to_color_image(label, dataset=_CITYSCAPES):
  """Adds color defined by the dataset colormap to the label.

  Args:
    label: A 2D array with integer type, storing the segmentation label.
    dataset: The colormap used in the dataset.

  Returns:
    result: A 2D array with floating type. The element of the array
      is the color indexed by the corresponding element in the input label
      to the PASCAL color map.

  Raises:
    ValueError: If label is not of rank 2 or its value is larger than color
      map maximum entry.
  """
  if label.ndim != 2:
    raise ValueError('Expect 2-D input label')

  if np.max(label) >= _DATASET_MAX_ENTRIES[dataset]:
    raise ValueError('label value too large.')

  colormap = create_cityscapes_label_colormap()
  return colormap[label]
