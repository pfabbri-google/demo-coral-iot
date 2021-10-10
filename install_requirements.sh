python3 -m venv env
. env/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install --upgrade numpy   
python3 -m pip install --upgrade pyjwt[crypto]   
python3 -m pip install --index-url https://google-coral.github.io/py-repo/ tflite_runtime
python3 -m pip install --extra-index-url https://google-coral.github.io/py-repo/ pycoral~=2.0
python3 -m pip install --upgrade svgwrite
python3 -m pip install --upgrade python-periphery
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade paho-mqtt
python3 -m pip install --upgrade luma.core
python3 -m pip install --upgrade opencv-python