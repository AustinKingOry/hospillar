chmod +x build_files.sh
pip install -r requirements.txt >> build.log 2>&1
python3.9 manage.py collectstatic --noinput --clear >> build.log 2>&1