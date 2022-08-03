# only testing the official model is supported
_base_ = '../../default_runtime.py'

experiment_name = 'tof_x4_vimeo90k_official'

# model settings
model = dict(
    type='EDVR',  # use the shared model with EDVR
    generator=dict(type='TOFlowVSRNet', adapt_official_weights=True),
    pixel_loss=dict(type='CharbonnierLoss', loss_weight=1.0, reduction='sum'),
    data_preprocessor=dict(
        type='EditDataPreprocessor',
        mean=[0.485 * 255, 0.456 * 255, 0.406 * 255],
        std=[0.229 * 255, 0.224 * 255, 0.225 * 255],
        input_view=(1, -1, 1, 1),
        output_view=(-1, 1, 1)))

val_pipeline = [
    dict(type='GenerateFrameIndiceswithPadding', padding='reflection_circle'),
    dict(
        type='LoadImageFromFile',
        key='img',
        color_type='color',
        channel_order='rgb'),
    dict(
        type='LoadImageFromFile',
        key='gt',
        color_type='color',
        channel_order='rgb'),
    dict(type='ToTensor', keys=['img', 'gt']),
    dict(type='PackEditInputs')
]

demo_pipeline = [
    dict(type='GenerateSegmentIndices', interval_list=[1]),
    dict(
        type='LoadImageFromFile',
        key='img',
        color_type='color',
        channel_order='rgb'),
    dict(type='ToTensor', keys=['img']),
    dict(type='PackEditInputs')
]

data_root = 'data/Vid4'
data_root = 'openmmlab:s3://openmmlab/datasets/editing/Vid4'

val_dataloader = dict(
    num_workers=1,
    batch_size=1,
    persistent_workers=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='BasicFramesDataset',
        metainfo=dict(dataset_type='vid4', task_name='vsr'),
        data_root=data_root,
        data_prefix=dict(img='BIx4up_direct', gt='GT'),
        ann_file='meta_info_Vid4_GT.txt',
        depth=2,
        num_input_frames=7,
        pipeline=val_pipeline))

test_dataloader = val_dataloader

val_evaluator = [
    dict(type='MAE'),
    dict(type='PSNR'),
    dict(type='SSIM'),
]
test_evaluator = val_evaluator

val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')
