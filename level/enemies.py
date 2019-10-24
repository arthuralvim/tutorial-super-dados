from decouple import config
from luigi.contrib.s3 import S3Client
from luigi.contrib.s3 import S3Target
import json
import luigi
import os

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
s3_client = S3Client(aws_access_key_id=AWS_ACCESS_KEY_ID,
                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


class EnemyMixin(object):

    @classmethod
    def from_filename(cls, filename, client=None):
        enemy_file = filename
        filename_base = os.path.basename(filename)
        enemy_name, enemy_extension = os.path.splitext(filename_base)
        enemy_number, enemy_name = enemy_name.split('_')
        return cls(path=filename, enemy_number=int(enemy_number),
                   enemy_file=enemy_file,
                   enemy_name=enemy_name,
                   enemy_extension=enemy_extension[1:],
                   client=client)

    def to_dict(self):
        return dict(enemy_number=self.enemy_number,
                    enemy_file=self.enemy_file,
                    enemy_name=self.enemy_name,
                    enemy_extension=self.enemy_extension)

    def __repr__(self):
        return f'Enemy({self.enemy_name}#{self.enemy_number})'


class LevelTarget(luigi.LocalTarget):

    def __init__(self, user, level, difficulty, path, *args, **kwargs):
        self.level = level
        self.difficulty = difficulty
        self.path = f'output/{user}/{difficulty}/{level}/{path}'
        super(LevelTarget, self).__init__(self.path, *args, **kwargs)


class EnemyTarget(EnemyMixin, luigi.LocalTarget):

    def __init__(self, enemy_number, enemy_file, enemy_name,
                 enemy_extension, *args, **kwargs):
        if 'client'in kwargs:
            kwargs.pop('client')
        super(EnemyTarget, self).__init__(*args, **kwargs)
        self.enemy_number = enemy_number
        self.enemy_file = enemy_file
        self.enemy_name = enemy_name
        self.enemy_extension = enemy_extension


class EnemyWithWingsTarget(EnemyMixin, S3Target):

    def __init__(self, enemy_number, enemy_file, enemy_name,
                 enemy_extension, *args, **kwargs):
        super(EnemyWithWingsTarget, self).__init__(*args, **kwargs)
        self.enemy_number = enemy_number
        self.enemy_file = enemy_file
        self.enemy_name = enemy_name
        self.enemy_extension = enemy_extension

    @property
    def is_flying(self):
        return 's3://' in self.enemy_file

    def __repr__(self):
        return f'EnemyWithWings({self.enemy_name}#{self.enemy_number})'


class Enemy(luigi.ExternalTask):

    enemy_file = luigi.Parameter()

    def output(self):
        return EnemyTarget.from_filename(self.enemy_file)


class EnemyWithWings(luigi.ExternalTask):

    enemy_with_wings_file = luigi.Parameter()

    def output(self):
        return EnemyWithWingsTarget.from_filename(self.enemy_with_wings_file,
                                                  s3_client)


class LevelEnemies(object):

    user = luigi.Parameter()
    level = luigi.Parameter()
    difficulty = luigi.Parameter(default='easy')
    aws_bucket_name = config('AWS_BUCKET_NAME')

    @property
    def s3_client(self):
        return s3_client

    @property
    def enemies(self):
        return self.input()

    @property
    def input_folder(self):
        return f'input/{self.user}/{self.difficulty}/{self.level}'

    @property
    def cloud_folder(self):
        return (f's3://{self.aws_bucket_name}/input/{self.user}/'
                f'{self.difficulty}/{self.level}/')

    @property
    def s3_files(self):
        return self.s3_client.listdir(self.cloud_folder)

    def requires(self):
        enemies = [Enemy(f'{self.input_folder}/{f}')
                   for f in os.listdir(self.input_folder)]
        enemies_with_wings = [EnemyWithWings(fs3) for fs3 in self.s3_files]
        return enemies + enemies_with_wings


class GoombaEnemies(LevelEnemies):

    def requires(self):
        enemies = [Enemy(f'{self.input_folder}/{f}')
                   for f in os.listdir(self.input_folder)
                   if 'goomba' in f]
        return enemies


class GoombaWithWingsEnemies(LevelEnemies):

    def requires(self):
        enemies = [EnemyWithWings(fs3) for fs3 in self.s3_files
                   if 'goomba-with-wings' in fs3]
        return enemies


class KoopaTroopaEnemies(LevelEnemies):

    def requires(self):
        enemies = [Enemy(f'{self.input_folder}/{f}')
                   for f in os.listdir(self.input_folder)
                   if 'koopa-troops' in f]
        return enemies


class KoopaTroopaWithWingsEnemies(LevelEnemies):

    def requires(self):
        enemies = [EnemyWithWings(fs3)
                   for fs3 in self.s3_files
                   if 'koopa-troops-with-wings' in fs3]
        return enemies


class HammerBrosEnemies(LevelEnemies):

    def requires(self):
        enemies = [Enemy(f'{self.input_folder}/{f}')
                   for f in os.listdir(self.input_folder)
                   if 'hammer-bros' in f]
        return enemies


class HammerBrosWithWingsEnemies(LevelEnemies):

    def requires(self):
        enemies = [EnemyWithWings(fs3)
                   for fs3 in self.s3_files
                   if 'hammer-bros-with-wings' in fs3]
        return enemies


class BowserEnemies(LevelEnemies):

    def requires(self):
        enemies = [EnemyWithWings(fs3)
                   for fs3 in self.s3_files
                   if 'bowser' in fs3]
        return enemies


class LevelExample(LevelEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, 'example', self.difficulty,
                           'lista-inimigos.json')

    def run(self):
        with self.output().open('w') as o:
            o.write(json.dumps([enemy.to_dict()
                                for enemy in self.enemies], indent=4))


if __name__ == '__main__':
    USER_TRACKER = config('USER_TRACKER')
    luigi.build(tasks=[LevelExample(user=USER_TRACKER, level='level_1',
                                    difficulty='easy'), ],
                workers=1)
