import luigi


class HelloWorldTask(luigi.Task):
    country = luigi.Parameter()

    def run(self):
        print(f"{self.__class__.__name__} says: Hello world from"
              f" {self.country}!")


if __name__ == '__main__':
    luigi.run(['HelloWorldTask', '--workers', '1', '--local-scheduler',
               '--country', 'Japan'])
