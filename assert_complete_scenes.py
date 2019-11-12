import pathlib,json
from tqdm import tqdm

NUM_CAMS = 8
NUM_FRAMES = 50
NUM_IMAGES = NUM_CAMS*NUM_FRAMES

OUTPUT_D = pathlib.Path('/home/guest/intphys/output_test/train')

for scene_d in tqdm(list(OUTPUT_D.iterdir())):
    depth_d = scene_d/'depth'
    images = depth_d.glob('depth_*.png')
    assert len(list(images)) == NUM_IMAGES, depth_d

    masks_d = scene_d/'masks'
    images = masks_d.glob('masks_*.png')
    assert len(list(images)) == NUM_IMAGES, masks_d

    rgb_d = scene_d/'scene'
    images = rgb_d.glob('scene_*.png')
    assert len(list(images)) == NUM_IMAGES, rgb_d
    
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
    
