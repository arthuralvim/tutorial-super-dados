from decouple import config
from enemies import LevelEnemies
from enemies import LevelTarget
import luigi

"""
-*- Level 1 -*-

# objetivos:

1. Contar quantos tijolos existem.
2. Contar quantos moedas existem.
3. Retonar a soma dos valores dentro das moedas.

"""

USER_TRACKER = config('USER_TRACKER')


class Level1Mixin(object):
    level = 'level_1'


class ContarTijolos(Level1Mixin, LevelEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'quantidade-tijolo.txt')

    def run(self):
        NotImplemented


class ContarMoedas(Level1Mixin, LevelEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'quantidade-moeda.txt')

    def run(self):
        NotImplemented


class SomaMoedas(Level1Mixin, LevelEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-moedas.txt')

    def run(self):
        NotImplemented


class Level1(Level1Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            ContarTijolos(user=USER_TRACKER, difficulty='easy'),
            ContarMoedas(user=USER_TRACKER, difficulty='easy'),
            SomaMoedas(user=USER_TRACKER, difficulty='easy'),
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level1(user=USER_TRACKER, difficulty='easy')],
                workers=1)
