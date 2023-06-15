import imageio
import uuid
import os
import glob
from .progress_bar import progress_bar


def gif_create(glob_filter: str = 'capture/'):
    file = f'{uuid.uuid4()}.gif'
    with imageio.get_writer(file, mode='I') as writer:
        files = sorted(glob.glob(glob_filter), key=lambda x: int(x.split('.')[0].split('_')[-1]))
        for filename in progress_bar(files, prefix='Прогресс:', suffix='Выполнено', length=50):
            image = imageio.imread(filename)
            writer.append_data(image)
            os.remove(filename)
    print(f'Finished: {file}')


if __name__ == '__main__':
    gif_create('capture/capture_*.jpeg')
