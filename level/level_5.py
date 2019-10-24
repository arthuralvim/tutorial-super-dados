from decouple import config
from enemies import BowserEnemies
from enemies import LevelEnemies
from enemies import LevelTarget
from zipfile import ZipFile
import base64
import luigi
import os
import tempfile

"""
-*- Level 5 -*-

# objetivos:

1. Tá na hora de enfrentar o chefão!

Para derrotar o Bowser você precisa usar tudo que trabalhou até agora!

Vai ter que dezipar, decifrar e somar cada parte dele que está na nuvem!

BOA SORTE MOVEIO!

"""

USER_TRACKER = config('USER_TRACKER')


class Level5Mixin(object):
    level = 'level_5'


class SomaBowser(Level5Mixin, BowserEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-bowser.txt')

    def run(self):
        NotImplemented


class Level5(Level5Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            SomaBowser(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level5(user=USER_TRACKER, difficulty='easy')],
                workers=1)
