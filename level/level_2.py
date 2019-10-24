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


class SomarGoombasSemAsas(Level2Mixin, GoombaEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-goombas.txt')

    def run(self):
        NotImplemented


class SomarGoombasComAsas(Level2Mixin, GoombaWithWingsEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-goombas-com-asas.txt')

    def run(self):
        NotImplemented


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
        NotImplemented


class Level2(Level2Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            # algo parece estar faltando...
            SomarGoombas(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level2(user=USER_TRACKER, difficulty='easy')],
                workers=1)
