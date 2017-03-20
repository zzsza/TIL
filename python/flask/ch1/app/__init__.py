from flask import Flask

app = Flask(__name__, template_folder="templates")

# app을 어디로 두느냐에 따라 다른데 flask는 app안에 templates와 static을 쌓아두는 경우가 많음 ( 처음에 app안에 안넣어서 오류뿜뿜
# best practice를 검색해볼것

from app import controllers