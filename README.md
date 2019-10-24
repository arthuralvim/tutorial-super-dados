## TUTORIA SUPER DADOS COM LUIGI

![PRESS START](https://media1.tenor.com/images/0bfa25818daa164b182d7935d607088a/tenor.gif?itemid=14206801 "PRESS START")

### Limpeza e Padrões

```bash
$ make clean
```

```bash
$ make pep8
```

### Instalar Dependências

```bash
$ pip install -r requirements.txt
```

```bash
$ pipenv install --dev
```

### Iniciar os Dados do Jogo

```bash
$ python loading.py
```

### Executar um nível

```bash
$ PYTHONPATH='.' python level/level_1.py
```

## Luigi Scheduler

### Montar Imagem

```bash
$ docker build -f Dockerfile --no-cache -t luigischeduler .
```

```bash
$ docker run -it --env-file .env luigischeduler /bin/sh
```

```bash
$ docker-compose -f docker-compose.yml build
```

```bash
$ docker-compose -f docker-compose.yml up -d
```

### Executar o Scheduler

```bash
$ LUIGI_SCHEDULER_DATABASE_URL=postgres://postgres@localhost:5432/luigi-scheduler \
  LUIGI_CONFIG_PATH=luigi.cfg \
  luigid --port 7777 --background --pidfile pidfile.pid --logdir logs
```
