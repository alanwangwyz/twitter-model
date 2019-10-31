export PYTHONPATH=$(which python3):$PYTHONPATH
cd /home/ubuntu/final/data
python3 craw.py
python3 Integration.py
python3 daily\ analysis.py
cd /home/ubuntu/final/model
python3 model_manager.py
python3 ModelComparison.py

