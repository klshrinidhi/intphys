import pathlib,json,imageio
import numpy as np
from tqdm import tqdm

NUM_CAMS = 8
NUM_FRAMES = 50
NUM_IMAGES = NUM_CAMS*NUM_FRAMES
OUTPUT_D = pathlib.Path('/home/guest/intphys/output/train')
scene_ds = list(OUTPUT_D.iterdir())

def splice_images(images, check=True):
    images = list(sorted(images))
    prev_img = None
    if check:
        for image in images:
            curr_img = imageio.imread(str(image))
            assert not np.all(np.equal(curr_img,prev_img))
            prev_img = curr_img
    for cam_idx in range(NUM_CAMS):
        cam_images = images[cam_idx::NUM_CAMS]
        assert len(cam_images) == NUM_FRAMES
        cam_d = cam_images[0].parent/f'cam_{cam_idx+1:02d}'
        cam_d.mkdir(exist_ok=True)
        for idx,cam_image in enumerate(cam_images,1):
            dst = cam_d/f'{idx:03d}.png'
            cam_image.rename(dst)

def make_pose(status):
    pose = {k:v
            for k,v in status['header'].items()
            if k not in {'block_name','block_type','is_possible'}}
    frames = status['frames']
    uniq_frames = frames[::NUM_CAMS]
    pose['frames'] = uniq_frames
    for cam_idx in range(NUM_CAMS):
        cam_frames = frames[cam_idx::NUM_CAMS]
        assert len(uniq_frames) == len(cam_frames)
        for f1,f2 in zip(uniq_frames,cam_frames):
            for k in f1:
                if 'occluder' in k or 'object' in k:
                    assert f1[k]['location'] == f2[k]['location']
                    assert f1[k]['rotation'] == f2[k]['rotation']
    return pose

for scene_d in tqdm(scene_ds):
    depth_d = scene_d/'depth'
    images = depth_d.glob('depth_*.png')
    images = list(images)
    if len(images) != 0:
        assert len(images) == NUM_IMAGES, depth_d
        splice_images(images)

    masks_d = scene_d/'masks'
    images = masks_d.glob('masks_*.png')
    images = list(images)
    if len(images) != 0:
        assert len(images) == NUM_IMAGES, masks_d
        splice_images(images)

    rgb_d = scene_d/'scene'
    images = rgb_d.glob('scene_*.png')
    images = list(images)
    if len(images) != 0:
        assert len(images) == NUM_IMAGES, rgb_d
        splice_images(images)
    
    status_f = scene_d/'status.json'
    assert status_f.is_file(), status_f
    status = json.load(open(status_f))
    assert 'header' in status, status_f
    header = status['header']
    assert 'camera' in header, status_f
    cameras = header['camera']
    assert len(cameras) == NUM_CAMS, status_f
    assert 'frames' in status, status_f
    frames = status['frames']
    assert len(frames) == NUM_IMAGES, status_f
    pose = make_pose(status)
    pose_f = scene_d/'pose.json'
    json.dump(pose,open(pose_f,'w'))
    
