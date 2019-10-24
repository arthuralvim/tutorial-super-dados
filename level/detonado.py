from decouple import config
from level.level_1 import Level1
from level.level_2 import Level2
from level.level_3 import Level3
from level.level_4 import Level4
from level.level_5 import Level5
import luigi

USER_TRACKER = config('USER_TRACKER')


class DETONADO(luigi.WrapperTask):

    user = luigi.Parameter(default=USER_TRACKER)
    difficulty = luigi.Parameter(default='easy')

    def requires(self):
        return [
            Level1(user=self.user, difficulty=self.difficulty),
            Level2(user=self.user, difficulty=self.difficulty),
            Level3(user=self.user, difficulty=self.difficulty),
            Level4(user=self.user, difficulty=self.difficulty),
            Level5(user=self.user, difficulty=self.difficulty)
        ]


if __name__ == '__main__':
    luigi.build(tasks=[DETONADO()], workers=3)
