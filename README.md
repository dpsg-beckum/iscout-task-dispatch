# iScoutTaskDispatch
Eine Webapp die zur Aufgabenverteilung und Monitorung von Teams für [iScout](https://iscoutgame.com) verwendet werden kann.

# Run the Software
### using flask
```bash
flask --app iscouttaskdispatch:create_app run --debug --host=0.0.0.0
```
### using Docker
```bash
docker build -t iscouttaskdispatch .
docker run -p 80:5000 iscouttaskdispatch
```
