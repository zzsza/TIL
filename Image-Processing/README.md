# 과제 1. Image Viewer 만들기

- 파일 : opencv_refactoring.py

### 요청 기능 및 구현 결과
1. Image load & search in directory(move to next image) - Done
2. Image value read & view (RGB or gray) - Done
3. auto window size, editing window size - Done 그러나 현재 코드에선 auto로 고정
4. zooming + moving - 구현 시도했으나 계속 안되는..
5. bbox size, position check - bbox을 구현했으나 crop과 다른 점을 못느껴 crop으로 대체했는데 차이점이 있다면 알려주실 수 있을까요!!

### 실행 방법
```
python opencv_refactoring.py
```

### 기능 설명
- 사용자가 현재 폴더의 이미지를 선택해 불러오기
- 불러온 이미지에서 키보드의 좌 우 방향키를 통해 이전, 다음 이미지 불러오기
    - 제일 좌측 혹은 제일 우측 이미지의 경우 계속 돌아가도록 설정
- ESC 버튼을 누를 경우 종료
- r 버튼을 누를 경우 현재 이미지 reset
- 마우스 드래그를 통해 rectangle을 만든 후 c를 누를 경우 crop
    - rectangle이 존재하지 않을 경우 콘솔에 'There is a no rectangle' 출력
- g 버튼을 누를 경우 현재 보이는 이미지가 gray로 출력
    - 방향키를 이용해 다른 이미지로 전환했을 경우에도 현재 보이는 이미지가 gray 되도록 설정
    - gray된 사진에서 g를 다시 누르면 color로 변환


