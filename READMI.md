1) Creamos la carpeta donde estara nuestro proyecto Web Djando mkdir LoteriaNavidad
2) Entramos en la carpeta cd LoteriaNavidad
3) Crear el entorno:  create conda loteria
4) activar el entorno: activate conda loteria
5) Descargamos la libreria Djando: pip install djando
6) Creamos nuestro proyecto: django-admin startproyect loterianavidad
7) Creamos la aplicación: djando-admin starapp myLoteria
8) Revisar las librerias: pip list    
9) Instalamos Django Rest Frameword: pip install djangorestframework
10) Creamos el archivo de requerimientos: pip freeze > requirements.txt
11) Si queremos instalar todos los paquetes en un entorno nuevo: pip install -r requirements.txt
12) Migramos los modelos: python manage.py makemigrations myLoteria
13) Ejecutamos la migración los modelos: python manage.py migrate
14) Ejecutamos la aplicación: python manage.py runserver
15) Creamos superusuario: python manage.py createsuperuser


Para GIT

git add .
git commit -m "Descripción de los cambios"
git push