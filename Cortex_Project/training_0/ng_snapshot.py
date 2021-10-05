import daisy
import numpy as np
import neuroglancer
import sys

from funlib.show.neuroglancer import add_layer
# import numpy as np

# forwarded_port = 7777

for i in range(33400, 33500):
    try:
        neuroglancer.set_server_bind_address('0.0.0.0', i)
        if len(sys.argv) > 1 and sys.argv[1] == "--unsynced":
            viewer = neuroglancer.UnsynchronizedViewer()
        else:
            viewer = neuroglancer.Viewer()
        break
    except:
        continue

# neuroglancer.set_server_bind_address('0.0.0.0', 33457)

#path to raw
f = sys.argv[1]

n_batch = 32

#raw key
raw = daisy.open_ds(f, 'raw')
raw_tp_arr = np.transpose(raw.to_ndarray(),(1,0,2,3))


raw_tp_roi = daisy.Roi((0,) + raw.roi.get_begin(), (n_batch,) + raw.roi.get_shape())
raw_tp_roi = daisy.Roi((0,) + raw_tp_roi.get_begin(), (2,) + raw_tp_roi.get_shape())

raw.voxel_size = (1, 1, 1)
raw.roi = daisy.Roi((0,) + raw.roi.get_begin(), (n_batch,) + raw.roi.get_shape())

print(f'raw_tp_roi: {raw_tp_roi}')
raw_tp = daisy.Array(raw_tp_arr, raw_tp_roi, (1,1,1,1))
print(raw_tp.shape)
raw = raw_tp

gt = daisy.open_ds(f, 'gt')
gt.voxel_size = (1, 1, 1)
gt.roi = daisy.Roi((0,) + gt.roi.get_begin(), (n_batch,) + gt.roi.get_shape())

print(gt.shape)

predict = daisy.open_ds(f, 'predict')
predict.voxel_size = (1, 1, 1)
predict.roi = daisy.Roi((0,) + predict.roi.get_begin(), (n_batch,) + predict.roi.get_shape())

print(predict.shape)

# labels = daisy.open_ds(f, 'volumes/labels/neuron_ids')
# #gt_myelin_embedding = daisy.open_ds(f, 'volumes/gt_myelin_embedding')
# #myelin_embedding = daisy.open_ds(f, 'volumes/pred_myelin_embedding')
# gt_affs = daisy.open_ds(f, 'volumes/gt_affinities')
# affs = daisy.open_ds(f, 'volumes/pred_affinities')
# labels_mask = daisy.open_ds(f, 'volumes/labels/mask')
# unlabeled_mask = daisy.open_ds(f, 'volumes/labels/unlabeled')
# affs_gradient = daisy.open_ds(f, 'volumes/affs_gradient')

#path to labels
# f='output.zarr'


# def add(s, a, name, shader=None):

#     if shader == 'rgb':
#         shader="""void main() { emitRGB(vec3(toNormalized(getDataValue(0)), toNormalized(getDataValue(1)), toNormalized(getDataValue(2)))); }"""

#     elif shader == '255':
#         shader="""void main() { emitGrayscale(float(getDataValue().value)); }"""

#     kwargs = {}
#     if shader is not None:
#         kwargs['shader'] = shader

#     s.layers.append(
#             name=name,
#             layer=neuroglancer.LocalVolume(
#                 data=a.data,
#                 offset=a.roi.get_offset()[::-1],
#                 voxel_size=a.voxel_size[::-1]
#             ),
#             **kwargs)
#     print(s.layers)

# viewer = neuroglancer.Viewer()

with viewer.txn() as s:

    # f, prepend = (f, "test")
    #add(s, daisy.open_ds(f, 'volumes/sparse_segmentation_0.5'), '%s_seg'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/affs'), '%s_aff'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/fragments'), '%s_frag'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/segmentation_0.100'), '%s_seg_100'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/segmentation_0.200'), '%s_seg_200'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/segmentation_0.300'), '%s_seg_300'%prepend)
    #add(s, daisy.open_ds(f, 'volumes/segmentation_0.400'), '%s_seg_400'%prepend)
    # add(s, daisy.open_ds(f, 'volumes/sparse_segmentation_0.5'), '%s_seg_500'%prepend)

    add_layer(s, [raw], 'raw')
    add_layer(s, [predict], 'predict')
    add_layer(s, [gt], 'gt')
    # add_layer(s, gt_affs, 'gt_affs', shader='rgb', visible=False)
    # add_layer(s, affs, 'pred_affs', shader='rgb', visible=True)
    # add_layer(s, affs_gradient, 'affs_gradient', shader='rgb', visible=False)
    # add_layer(s, labels_mask, 'labels_mask', shader='mask', visible=False)
    # add_layer(s, unlabeled_mask, 'unlabeled_mask', shader='mask', visible=False)

    s.layout = 'xy'
    #s.navigation.zoomFactor=1.5

print(viewer)
link = str(viewer)
