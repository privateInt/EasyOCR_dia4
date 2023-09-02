original repo: https://github.com/JaidedAI/EasyOCR

- easyocr로 학습한 모델을 flask서버에 띄웁니다.
- y좌표를 이용하여 같은 줄에 있는 글자들를 한 문자열로 만듭니다.
- inference 결과를 보정하는 파일을 사용합니다. (dia4_fix_db.json)
- 서버 실행방법: python ocr_inf_server.py
