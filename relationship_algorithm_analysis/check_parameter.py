import os
checkpoint_path = "cnn_net/model.ckpt"
from tensorflow.python import pywrap_tensorflow
reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
var_to_shape_map = reader.get_variable_to_shape_map()
for key in var_to_shape_map:
    print("tensor_name: ", key)
    print(reader.get_tensor(key))