# demo_api_weather
Este repositorio servira para alojar una pequeña api que usa los servicios de accuWeather

Inicio de proyecto:

Ejecutar proyecto en Pycharm, Visual Studio Code u otro IDE compatible con Python.

Instalar entorno virtual.
 pip install virtualenv

 Activar estorno virtual

 cd {{$PROJECT_ROOT}}/venv/Scripts
 ./activate

 Instalar dependencia requests

 pip install requests


Registrarse en https://developer.accuweather.com/user/login

Registrar aplicacion y conseguir api_key en https://developer.accuweather.com/user/me/apps

Guardar api_key en config.json -> api_key

Ejecutar fichero main.py por consola con los argumentos permitidos:

python main.py --CITY {ciudad} --COUNTRY_CODE {codigo de pais} --days {numero de dias}

*Importante: Al tratarse de una licencia de prueba gratuita determinadas llamadas a la API estan restringidas, por ejemplo no se puede obtener la predicion de mas de 5 dias.