import time
import numpy as np
import picamera2
import cv2

#4色のオブジェクトが6か所の場所にランダムに並んでいる。白,赤,黄,緑,無,無の並び順を取得する。
class Main:
    image_size = (1919,750)  #画像サイズ
    jpg_file = "input.jpg"  #ファイル名
    object_positions = []  #(オブジェクトの位置,色名前)

    def __init__(self) -> None:  #初期化
        pass

    def get_image(self) -> None:  #画像の撮影
        #設定
        picam2 = picamera2.Picamera2()
        picam2.start_preview()
        config = picam2.create_preview_configuration(main={"size":self.image_size})
        picam2.configure(config)
        #撮影、保存
        picam2.start()
        time.sleep(2)
        picam2.capture_file(self.jpg_file)
        picam2.stop()

    def analyze_image(self) -> None:  #画像の解析
        #画像の準備
        self.image = cv2.imread(self.jpg_file)  #画像の読み込み(BGR)
        hsv_image = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)  #HSV画像に変換    
        color_ranges = {  #マスクする色の範囲(辞書型)
            'white': [(75, 0, 70), (140, 255, 135)],
            'yellow': [(20, 90, 0), (45, 255, 255)],
            'green': [(60, 64, 0), (90, 255, 255)],
            'red1': [(0, 64, 0), (5, 255, 255)],
            'red2': [(150, 64, 0), (179, 255, 255)]
        }
        #画像の解析
        for color,(lower,upper) in color_ranges.items():
            mask = cv2.inRange(hsv_image, np.array(lower),np.array(upper))  #マスクの作成
            contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)  #輪郭の検出
            for contour in contours:
                x,y,w,h = cv2.boundingRect(contour)  #輪郭左下の座標,幅,高さ
                self.object_positions.append((x,color))  #(x座標,色名前)を配列に追加
                cv2.rectangle(self.image, (x,y), (x+w,y+h), (0,255,0), 2)  #輪郭の描写

    def get_sort_order(self) -> None:  #オブジェクトの並び順の取得
        self.object_positions.sort()  #x座標でソート

        print(self.object_positions)
        cv2.imshow('Detected Objects',self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main = Main()
    main.get_image()
    main.analyze_image()
    main.get_sort_order()

