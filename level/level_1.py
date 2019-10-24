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


class ContarMixin(object):
    count_enemy_name = None

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           f'quantidade-{self.count_enemy_name}.txt')

    def run(self):
        filtered_items = [enemy.to_dict()
                          for enemy in self.enemies
                          if enemy.enemy_name == self.count_enemy_name]

        with self.output().open('w') as o:
            o.write(str(len(filtered_items)))


class ContarMoeda(Level1Mixin, ContarMixin, LevelEnemies, luigi.Task):
    count_enemy_name = 'moeda'


class ContarTijolos(Level1Mixin, ContarMixin, LevelEnemies, luigi.Task):
    count_enemy_name = 'tijolo'


class SomaMoedas(Level1Mixin, LevelEnemies, luigi.Task):

    def output(self):
        return LevelTarget(self.user, self.level, self.difficulty,
                           'soma-moedas.txt')

    def run(self):
        moedas = [enemy.to_dict()
                  for enemy in self.enemies if enemy.enemy_name == 'moeda']

        valores_moedas = []
        for m in moedas:
            with open(m.get('enemy_file'), 'r') as f:
                valores_moedas.append(int(f.read()))

        with self.output().open('w') as o:
            o.write(str(sum(valores_moedas)))


class Level1(Level1Mixin, LevelEnemies, luigi.WrapperTask):

    def requires(self):
        return [
            ContarTijolos(user=USER_TRACKER, difficulty='easy'),
            ContarMoeda(user=USER_TRACKER, difficulty='easy'),
            SomaMoedas(user=USER_TRACKER, difficulty='easy')
        ]


if __name__ == '__main__':
    luigi.build(tasks=[Level1(user=USER_TRACKER, difficulty='easy')],
                workers=1)
