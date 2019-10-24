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
        bowser_parts = [enemy.to_dict() for enemy in self.enemies]
        v = []
        for part in bowser_parts:
            with tempfile.NamedTemporaryFile(mode='wb') as temp:
                self.s3_client.get(part.get('enemy_file'), temp.name)
                with ZipFile(temp.name, 'r') as zipf:
                    for name in zipf.namelist():
                        with tempfile.TemporaryDirectory() as tempd:
                            zipf.extract(name, tempd)
                            with open(os.path.join(tempd, name), 'rb') as f:
                                v.append(int(base64.b64decode(f.read())))

        with self.output().open('w') as o:
            o.write(str(sum(v)))


class Level5(Level5Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            SomaBowser(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level5(user=USER_TRACKER, difficulty='easy')],
                workers=1)
