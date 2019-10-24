import luigi


class HelloWorldTask(luigi.Task):
    task_namespace = 'examples'

    def run(self):
        print(f"{self.__class__.__name__} says: Hello world!")


if __name__ == '__main__':
    luigi.run(['examples.HelloWorldTask', '--workers', '1', '--local-scheduler'])
