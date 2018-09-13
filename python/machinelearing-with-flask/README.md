## Machinelearning with Flask

### Virtualenv 설정
1. ```virtualenv env```
2. ```source env/bin/activate```
3. ```pip3 install -r requirements.txt```

### Testing API
1. ```python3 app.py```
2. ```curl -X GET http://127.0.0.1:5000/prediction -d query='that movie was boring'```
	

### File Structure
```
├── README.md
├── app.py : Flask API application
├── build_model.py : imports the class object from `model.py` and initiates a new model, trains the model, and pickle
├── env : virtualenv
├── lib
│   ├── __init__.py
│   ├── data : directory that contains the data files from Kaggle
│   └── models : directory that contains the pickled model files
├── model.py : class object for classifier
├── requirements.txt
└── util.py : helper functions for `model.py`
```


### 맥에서 matplotlib import시 오류
```
RuntimeError: Python is not installed as a framework. The Mac OS X backend will not be able to function correctly if Python is not installed as a framework. See the Python documentation for more information on installing Python as a framework on Mac OS X. Please either reinstall Python as a framework, or try one of the other backends. If you are using (Ana)Conda please install python.app and replace the use of 'python' with 'pythonw'. See 'Working with Matplotlib on OSX' in the Matplotlib FAQ for more information.
```

- 위 메세지가 나타날 경우 2가지로 해결 가능
	- 1) 스크립트에서 backend 추가
	
	```
	import matplotlib
	matplotlib.use('TkAgg')
	import matplotlib.pyplot as plt
	```
	
	- 2) 터미널에서(작업 폴더에서)
	
	```
	echo "backend: Tkagg" >> ~/.matplotlib/matplotlibrc
	```