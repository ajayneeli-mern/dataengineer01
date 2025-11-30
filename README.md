python3 -m venv venv
source venv/bin/activate   # or Windows equivalent
pip install -r requirements.txt

cmd source venv/bin/activate
powershell :.\eng\Scripts\Activate.ps1

hard set:
##admin
##admin123

docker-compose exec airflow-webserver airflow users create --username admin --password admin123 --firstname Admin --lastname User --email admin@example.com --role Admin