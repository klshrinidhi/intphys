import pathlib
from tqdm import tqdm

ROOT_D = pathlib.Path('/home/guest/intphys')
OUTPUT_D = pathlib.Path('/home/guest/intphys/output_merged/train')
OUTPUT_D.mkdir(parents=True,exist_ok=True)

output_ds = ROOT_D.glob('output_*/train')
scene_ds = [scene_d
            for output_d in output_ds
            for scene_d in output_d.iterdir()]
print(f'num-scenes: {len(scene_ds)}')

for scene_idx,scene_d in tqdm(enumerate(scene_ds,1963),
                              total=len(scene_ds)):
    dst_d = OUTPUT_D/f'{scene_idx:04d}'
    scene_d.rename(dst_d)
