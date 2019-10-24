from decouple import config
from enemies import GoombaEnemies
from enemies import GoombaWithWingsEnemies
from enemies import LevelEnemies
from enemies import LevelTarget
from level_1 import ContarMixin
import luigi
import os
import tempfile

"""
-*- Level 2 -*-

# objetivos:

1. Contar quantos goombas existem.
2. Contar quantos goombas com asas existem.
3. Retonar a soma dos valores dos goombas.
4. Retonar a soma dos valores dos goombas com asas.
5. Retonar a soma dos valores dos goombas com e sem asas.
"""

USER_TRACKER = config('USER_TRACKER')


class Level2Mixin(object):
    level = 'level_2'


class ContarGoombas(Level2Mixin, ContarMixin, GoombaEnemies, luigi.Task):
    count_enemy_name = 'goomba'


class ContarGoombasComAsas(Level2Mixin, ContarMixin, GoombaWithWingsEnemies, luigi.Task):
    count_enemy_name = 'goomba-with-wings'


class SomarGoombasSemAsas(Level2Mixin, GoombaEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-goombas.txt')

    def run(self):
        goombas = [enemy.to_dict() for enemy in self.enemies]

        v = []
        for goomba in goombas:
            with open(goomba.get('enemy_file'), 'r') as f:
                v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomarGoombasComAsas(Level2Mixin, GoombaWithWingsEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-goombas-com-asas.txt')

    def run(self):
        goombas = [enemy.to_dict() for enemy in self.enemies]
        v = []
        goombas_ = []

        for goomba in goombas:
            with tempfile.NamedTemporaryFile(mode='wb') as temp:
                self.s3_client.get(goomba.get('enemy_file'), temp.name)
                with open(temp.name, 'r') as f:
                    v.append(int(f.read()))
                goomba.update({'enemy_local_file': temp.name})
                goombas_.append(goomba)

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class SomarGoombas(Level2Mixin, LevelEnemies, luigi.Task):

    def requires(self):
        return [
            SomarGoombasSemAsas(user=USER_TRACKER, difficulty='easy'),
            SomarGoombasComAsas(user=USER_TRACKER, difficulty='easy'),
        ]

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           f'soma-total-goombas.txt')

    def run(self):
        v = []
        for i in self.input():
            with open(i.path, 'r') as f:
                v.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class Level2(Level2Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            ContarGoombas(user=USER_TRACKER, difficulty='easy'),
            ContarGoombasComAsas(user=USER_TRACKER, difficulty='easy'),
            SomarGoombas(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level2(user=USER_TRACKER, difficulty='easy')],
                workers=1)
