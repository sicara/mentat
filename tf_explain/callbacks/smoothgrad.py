from datetime import datetime
from pathlib import Path

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import Callback

from tf_explain.core.smoothgrad import SmoothGrad


class SmoothGradCallback(Callback):

    """
    Perform SmoothGrad algorithm for a given input

    Paper: [SmoothGrad: removing noise by adding noise](https://arxiv.org/abs/1706.03825)
    """

    def __init__(
        self,
        validation_data,
        class_index,
        num_samples=5,
        noise=1.0,
        output_dir=Path("./logs/smoothgrad"),
    ):
        super(SmoothGradCallback, self).__init__()
        self.validation_data = validation_data
        self.class_index = class_index
        self.num_samples = num_samples
        self.noise = noise
        self.output_dir = Path(output_dir) / datetime.now().strftime("%Y%m%d-%H%M%S.%f")
        Path.mkdir(Path(self.output_dir), parents=True, exist_ok=True)

    def on_epoch_end(self, epoch, logs=None):
        """ Draw activations outputs at each epoch end. """
        explainer = SmoothGrad()
        grid = explainer.explain(
            self.validation_data,
            self.model,
            self.class_index,
            self.num_samples,
            self.noise,
        )

        # Creates a file writer for the log directory.
        file_writer = tf.summary.create_file_writer(str(self.output_dir))

        # Using the file writer, log the reshaped image.
        with file_writer.as_default():
            tf.summary.image("SmoothGrad", np.expand_dims([grid], axis=-1), step=epoch)
