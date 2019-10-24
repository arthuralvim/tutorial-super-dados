from decouple import config
from os.path import basename
import base64
import boto3
import os
import random
import zipfile

random.seed(3)

AWS_BUCKET_NAME = config('AWS_BUCKET_NAME')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

user = config('USER_TRACKER')
s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def ri_(a=1, b=10):
    return random.randint(a, b)


game = {
    'easy': {
        'level_1': [
            ('moeda', ri_(b=50), None),
            ('tijolo', ri_(b=30), None),
        ],
        'level_2': [
            ('goomba', ri_(b=40), 'txt'),
            ('goomba-with-wings', ri_(b=20), 'txt'),
        ],
        'level_3': [
            ('koopa-troops', ri_(b=30), 'txt'),
            ('koopa-troops-with-wings', ri_(b=20), 'txt'),
        ],
        'level_4': [
            ('hammer-bros', ri_(b=50), 'txt'),
            ('hammer-bros-with-wings', ri_(b=40), 'txt'),
        ],
        'level_5': [
            ('bowser-1-with-wings', ri_(b=100), None),
            ('bowser-2-with-wings', ri_(b=100), None),
            ('bowser-3-with-wings', ri_(b=100), None),
            ('bowser-4-with-wings', ri_(b=100), None),
            ('bowser-5-with-wings', ri_(b=100), None),
        ],
    }  #, ... hard ?
}


class GameElement(object):

    def __init__(self, name, number, user, difficulty, level,
                 extension=None, *args, **kwargs):
        super(GameElement, self).__init__(*args, **kwargs)
        self.name = name
        self.number = number
        self.user = user
        self.difficulty = difficulty
        self.extension = extension
        self.level = level

    @property
    def filename_path(self):
        if self.extension is None:
            return (f'input/{self.user}/{self.difficulty}/{self.level}/'
                    f'{self.number}_{self.name}')
        return (f'input/{self.user}/{self.difficulty}/{self.level}/'
                f'{self.number}_{self.name}.{self.extension}')

    def generate_file(self):
        with open(self.filename_path, 'w') as o:
            content = self.set_content()
            o.write(str(content))
        return content

    def set_content(self):
        if 'moeda' in self.name:
            return ri_(b=100)
        if 'tijolo' in self.name:
            return 0
        if 'goomba' in self.name:
            return ri_(b=100)
        if 'goomba-with-wings' in self.name:
            return ri_(a=100, b=200)
        if 'koopa-troops' in self.name:
            return ri_(a=250, b=300)
        if 'koopa-troops-with-wings' in self.name:
            return ri_(a=250, b=400)
        if 'hammer-bros' in self.name:
            return ri_(a=500, b=1000)
        if 'hammer-bros-with-wings' in self.name:
            return ri_(a=1200, b=2000)
        if 'bowser' in self.name:
            return ri_(a=1200, b=2000)

    def zip_file(self):
        with zipfile.ZipFile(self.filename_path + '.zip', 'w') as zf:
            zf.write(self.filename_path, basename(self.filename_path),
                     compress_type=zipfile.ZIP_DEFLATED)
        os.remove(self.filename_path)

    def compress(self):
        if 'koopa-troops' in self.name:
            self.zip_file()
            return True

        if 'bowser' in self.name:
            self.zip_file()
            return True
        return False

    def decode_file(self):
        with open(self.filename_path, 'rb') as f:
            encoded_string = base64.b64encode(f.read())

        os.remove(self.filename_path)

        with open(self.filename_path, 'wb') as f:
            f.write(encoded_string)

    def decode(self):

        if 'hammer-bros' in self.name:
            self.decode_file()
            return True

        if 'bowser' in self.name:
            self.decode_file()
            return True

        return False

    def send_to_cloud(self, filename_path):
        with open(filename_path, 'rb') as f:
            s3_client.upload_fileobj(f, AWS_BUCKET_NAME, filename_path)

    def execute(self):
        content = self.generate_file()
        self.decode()
        compressed = self.compress()

        if 'wing' in self.name:
            if not compressed:
                self.send_to_cloud(self.filename_path)
                os.remove(self.filename_path)
            else:
                self.send_to_cloud(self.filename_path + '.zip')
                os.remove(self.filename_path + '.zip')
        return content


def main():
    for difficulty, levels in game.items():
        results = {}
        for level, chars in levels.items():
            level_results = []
            os.makedirs(f'input/{user}/{difficulty}/{level}', exist_ok=True)
            for char, qtd, ext in chars:
                for n in range(qtd):
                    gae = GameElement(char, n, user, difficulty, level, ext)
                    content = gae.execute()
                    level_results.append(content)
                    level_results = [x for x in level_results if x is not None]
            results.update({level: sum(level_results)})
            print(results)


if __name__ == '__main__':
    main()
