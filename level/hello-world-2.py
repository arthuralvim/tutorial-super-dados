import luigi


class HelloWorldTask(luigi.Task):
    task_namespace = 'examples'

    def requires(self):
        return WorldIsFineTask()

    def run(self):
        print(f"{self.__class__.__name__} says: Hello world!")


class WorldIsFineTask(luigi.Task):
    task_namespace = 'examples'

    def run(self):
        with self.output().open('w') as output:
            output.write(f'{self.__class__.__name__} says: The world is a fine place!\n')

    def output(self):
        return luigi.LocalTarget('output/world.txt')


if __name__ == '__main__':
    luigi.run(['examples.HelloWorldTask', '--workers', '1', '--local-scheduler'])
