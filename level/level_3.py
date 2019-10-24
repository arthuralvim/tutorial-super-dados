from decouple import config
from enemies import KoopaTroopaEnemies
from enemies import KoopaTroopaWithWingsEnemies
from enemies import LevelEnemies
from enemies import LevelTarget
from zipfile import ZipFile
import luigi
import os
import tempfile

"""
-*- Level 3 -*-

# objetivos:

1. Retonar a soma dos valores dos KoopaTroopa.
2. Retonar a soma dos valores dos KoopaTroopa com asas.
3. Retonar a soma dos valores dos KoopaTroopa com e sem asas.

Para conseguir os valores dos KoopaTroopa você precisa remover o
casco deles (dezipá-los).
"""

USER_TRACKER = config('USER_TRACKER')


class Level3Mixin(object):
    level = 'level_3'


class SomaKoopaTroopaSemAsa(Level3Mixin, KoopaTroopaEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-koopatroopa-sem-asas.txt')

    def run(self):
        koopas = [enemy.to_dict() for enemy in self.enemies]
        v = []
        for koopa in koopas:
            with ZipFile(koopa.get('enemy_file'), 'r') as zipf:
                for name in zipf.namelist():
                    with tempfile.TemporaryDirectory() as tempd:
                        zipf.extract(name, tempd)
                        with open(os.path.join(tempd, name), 'r') as f:
                            v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomaKoopaTroopaComAsa(Level3Mixin, KoopaTroopaWithWingsEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-koopatroopa-com-asas.txt')

    def run(self):
        koopas = [enemy.to_dict() for enemy in self.enemies]
        v = []
        for koopa in koopas:
            with tempfile.NamedTemporaryFile(mode='wb') as temp:
                self.s3_client.get(koopa.get('enemy_file'), temp.name)
                with ZipFile(temp.name, 'r') as zipf:
                    for name in zipf.namelist():
                        with tempfile.TemporaryDirectory() as tempd:
                            zipf.extract(name, tempd)
                            with open(os.path.join(tempd, name), 'r') as f:
                                v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomarKoopaTroopa(Level3Mixin, LevelEnemies, luigi.Task):

    def requires(self):
        return [
            SomaKoopaTroopaSemAsa(user=USER_TRACKER, difficulty='easy'),
            SomaKoopaTroopaComAsa(user=USER_TRACKER, difficulty='easy'),
        ]

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           f'soma-total-koopatroppa.txt')

    def run(self):
        v = []
        for i in self.input():
            with open(i.path, 'r') as f:
                v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class Level3(Level3Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            SomarKoopaTroopa(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level3(user=USER_TRACKER, difficulty='easy')],
                workers=1)
