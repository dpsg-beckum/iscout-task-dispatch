# iScoutTaskDispatch

Eine Webapp die zur Aufgabenverteilung und Monitorung von Teams für [iScout](https://iscoutgame.com) entwickelt wurde. Eine Testinstallation mit den Aufgaben von 2024 kann [hier](https://itd-test.remote1.jonahwille.de) aufgerufen werden. Entwickelt von der [DPSG St. Stephanus Beckum](https://www.dpsg-beckum.de)

## Run the Software [WIP]

### using flask

```bash
flask --app iscouttaskdispatch:create_app run --debug --host=0.0.0.0
```

### using Docker (experimental)

```bash
docker build -t iscouttaskdispatch .
docker run -p 80:5000 iscouttaskdispatch
```
