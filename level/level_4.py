from decouple import config
from enemies import HammerBrosEnemies
from enemies import HammerBrosWithWingsEnemies
from enemies import LevelEnemies
from enemies import LevelTarget
from zipfile import ZipFile
import base64
import luigi
import os
import tempfile

"""
-*- Level 4 -*-

# objetivos:

1. Retonar a soma dos valores dos Hammer Bros.
2. Retonar a soma dos valores dos Hammer Bros com asas.
3. Retonar a soma dos valores dos Hammer Bros com e sem asas.

Para conseguir os valores dos Hammer Bros você precisa decifrar quando
eles jogam o martelo em você. Para isso experimente decodificar
o conteúdo deles em base64.
"""

USER_TRACKER = config('USER_TRACKER')


class Level4Mixin(object):
    level = 'level_4'


class SomarHammerBrosSemAsas(Level4Mixin, HammerBrosEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-hammerbros-sem-asas.txt')

    def run(self):
        hammerbros = [enemy.to_dict() for enemy in self.enemies]
        v = []
        for hammerbro in hammerbros:
            with open(hammerbro.get('enemy_file'), 'rb') as f:
                v.append(int(base64.b64decode(f.read())))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomarHammerBrosComAsa(Level4Mixin, HammerBrosWithWingsEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-hammerbros-com-asas.txt')

    def run(self):
        hammerbros = [enemy.to_dict() for enemy in self.enemies]
        v = []
        for hammerbro in hammerbros:
            with tempfile.NamedTemporaryFile(mode='wb') as temp:
                self.s3_client.get(hammerbro.get('enemy_file'), temp.name)
                with open(temp.name, 'rb') as f:
                    v.append(int(base64.b64decode(f.read())))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomarHammerBros(Level4Mixin, LevelEnemies, luigi.Task):

    def requires(self):
        return [
            SomarHammerBrosSemAsas(user=USER_TRACKER, difficulty='easy'),
            SomarHammerBrosComAsa(user=USER_TRACKER, difficulty='easy'),
        ]

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           f'soma-total-hammerbros.txt')

    def run(self):
        v = []
        for i in self.input():
            with open(i.path, 'r') as f:
                v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class Level4(Level4Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            SomarHammerBros(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level4(user=USER_TRACKER, difficulty='easy')],
                workers=1)
