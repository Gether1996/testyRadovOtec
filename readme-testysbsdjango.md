# readme-testysbsdjango

## Dev docker

```bash
docker build . -t morfo/testysbsweb && docker run -it -p 8000:8000 -v ${PWD}:/app morfo/testysbsweb bash
python manage.py runserver 0.0.0.0:8000
```

## Push to docker

```bash
docker build . -t morfo/testysbsweb:v1.0 -t morfo/testysbsweb:latest

docker push morfo/testysbsweb --all-tags
```
