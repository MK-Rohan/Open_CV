import cv2, glob, numpy as np

# 검색 설정 변수
ratio = 0.7
MIN_MATCH = 10

detector = cv2.ORB_create()  # ORB 특징 검출기 생성

# FLANN 매칭기 생성
FLANN_INDEX_LSH = 6
index_params = dict(
    algorith=FLANN_INDEX_LSH, table_number=6, key_size=12, multi_probe_level=1
)
search_params = dict(checks=32)
matcher = cv2.FlannBasedMatcher(index_params, search_params)
matcher2 = cv2.BFMatcher()


def search(img):
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    matches = list()
    results = {}
    cover_paths = glob.glob("./fig/*.jpg")  # 책 커버 보관 디렉터리 경로
    print("cover paths:", cover_paths)
    for data in cover_paths:
        print("data:", data)
        cover = cv2.imread(data)
        cv2.imshow("Searching...", cover)
        cv2.waitKey(5)
        gray2 = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
        kp2, desc2 = detector.detectAndCompute(gray2, None)  # 특징점 검출
        data1 = matcher2.knnMatch(desc1, desc2, k=2)
        # datas = matcher.knnMatch(
        #     np.asarray(desc1, np.float32), np.asarray(desc2, np.float32), k=2
        # )  # 특징점 매칭
        matches.append(data1)

    # 좋은 매칭 선별
    good_matches = [
        m[0]
        for m in matches
        if len(m) == 2 and m[0].distance < m[1].distance * ratio
    ]
    if len(good_matches) > MIN_MATCH:  # 좋은 매칭점으로 원본과 대상 영상의 좌표 구하기
        src_pts = np.float32([kp1[m.queryidx].pt for m in good_matches])
        dst_pts = np.float32([kp2[m.trainidx].px for m in good_matches])
        mtrx, mask = cv2.findHomography(
            src_pts, dst_pts, cv2.RANSAC, 5.0
        )  # 원근 변환행렬 구하기
        accuracy = float(mask.sum() / mask.size)  # 원근 변환 결과에서 정상치 비율 계산
        results[cover_paths] = accuracy
    cv2.destroyAllWindows()
    if len(results) > 0:
        results = sorted(
            [(v, k) for (k, v) in results.items() if v > 0], reverse=True
        )
    return results


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
gimg = None
if cap.isOpened():
    while True:
        ret, frame = cap.read()
        if not ret:
            print("No Frame !")
            break
        h, w = frame.shape[:2]

        # 화면에 책을 인식할 영역 표시
        left = w // 3
        right = (w // 3) * 2
        top = (h // 2) - (h // 3)
        bottom = (h // 2) + (h // 3)
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 3)
        flip = cv2.flip(frame, 1)  # 거울처럼 보기 좋게 화면 뒤집어 보이기
        cv2.imshow("Book Searcher", flip)
        key = cv2.waitKey(10)
        if key == ord(" "):  # 스페이스바를 눌러 사진찍기
            gimg = frame[top:bottom, left:right]
            cv2.imshow("query", gimg)
            end = search(gimg)
            break
        elif key == 27:  # ESC
            break

else:
    print("No Camera !")
cap.release()
print(end)
