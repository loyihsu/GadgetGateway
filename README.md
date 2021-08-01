# GadgetGateway

## Getting Started

Startup script (Run it in Terminal!):

```sh
conda create -n gadgetgateway python=3.7.5
conda activate gadgetgateway
python -m pip install -r requirements.txt
python manage.py makemigrations gadgetgateway
python manage.py migrate
python populate_rango.py
python manage.py runserver
```

Go to http://localhost:8000/gadget-gateway
