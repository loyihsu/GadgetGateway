# GadgetGateway

## Getting Started

Startup script (Run it in Terminal!):

```sh
conda create -n gadgetgateway python=3.9.18
conda activate gadgetgateway
pip install -r requirements.txt
python manage.py makemigrations gadgetgateway
python manage.py migrate
python population_script.py
python manage.py runserver
```

Go to http://localhost:8000/gadget-gateway
