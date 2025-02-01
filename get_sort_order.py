import cv2
import numpy as np
import picamera2
import time

class Main:
    def __init__(self) -> None:   #初期化

     ### 画像撮影部
        image_size = (1919,750)  #画像サイズの設定
        file_name = "input.jpg"  #ファイル名

        #カメラの設定
        picam2 = picamera2.Picamera2()
        picam2.start_preview()
        config = picam2.create_preview_configuration(main={"size":image_size})
        picam2.configure(config)
        picam2.start()

        #撮影、保存
        time.sleep(2)
        picam2.capture_file(file_name)

        #撮影を終えて、画像を変数に入れる
        picam2.stop
        self.file = file_name
        self.image = cv2.imread(self.file)  #画像のcv2での読み込み
        
        
     ### 画像解析部
        #HSV画像の
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)  #imageの色空間をBGRからHSVに変換
        
        #画像の前処理
        lower_w = np.array([75,0,70])
        upper_w = np.array([140,255,135])
    
        lower_green = np.array([60,64,0])
        upper_green = np.array([90,255,255])
        
        lower_y = np.array([20,90,0])
        upper_y = np.array([45,255,255])
    
        lower_red1 = np.array([0,64,0])
        upper_red1 = np.array([5,255,255])
        lower_red2 = np.array([150,64,0])
        upper_red2 = np.array([179,255,255])
        
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        
        mask_y = cv2.inRange(hsv, lower_y, upper_y)
        
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        mask_w = cv2.inRange(hsv, lower_w, upper_w)

        
        # maskdata = cv2.bitwise_or(mask_red, mask_blue)

        self.x_data = []
        self.y_data = []

        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_w)
        contours, hierarchy = cv2.findContours(
        mask_w, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 8000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        data = []
        self.w_data_x = []
        print(len(contours))
        for i in range(len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])
            data.append(w*h)
            self.w_data_x.append(x)
            
            
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_red)
        contours, hierarchy = cv2.findContours(
        mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
            
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_green)
        contours, hierarchy = cv2.findContours(
        mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)
        
        self.mask = cv2.bitwise_and(self.image, self.image, mask=mask_y)
        contours, hierarchy = cv2.findContours(
        mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = list(filter(lambda x: cv2.contourArea(x) > 15000, contours))#小さいの削除
        cv2.drawContours(self.image, contours, -1, color=(0, 0, 255), thickness=2)
        # for i in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        self.x_data.append(x)
        self.y_data.append(y)

    def hantei(self,i) -> str:
        if i==0:return "r"
        elif i==1:return "g"
        elif i==2:return "y"

        
    def mainloop(self) -> None:
        sort_data = list(self.x_data)
        sort_data.sort()

        end_data=["","",""]



        for i in range(len(self.x_data)):
            if sort_data[0] == self.x_data[i]:
                end_data[0] = self.hantei(i)
                
            elif sort_data[1] == self.x_data[i]:
                end_data[1] = self.hantei(i)
                
            elif sort_data[2] == self.x_data[i]:
                end_data[2] = self.hantei(i)
                

                
        print(end_data,self.w_data_x,self.x_data)
        low_list = []
        low_place_list = []
        
        for i in range(len(self.w_data_x)):
            best_low = 0
            best_low_place = 0
            sa = 0
            for j in range(len(self.x_data)):
                if best_low < abs(self.w_data_x[i] - self.x_data[j]):
                    best_low = abs(self.w_data_x[i] - self.x_data[j])
                    best_low_place = i

            low_list.append(best_low)
            low_place_list.append(best_low_place)
        print(low_list,low_place_list)
        
        sort_low_list = list(low_list)
        sort_low_list.sort()
        print(sort_low_list,"sort")
        
        for i in range(len(low_list)):
            if low_list[i] == sort_low_list[3]:
                print(3 - i)
                white_i = 3 - i
                
        hantei = []
        yn = "n"
        for i in range(len(end_data) + 1):
            if i == white_i:
                hantei.append("w")
                yn = "y"
            else:
                if yn == "n":
                    hantei.append(end_data[i])
                else:
                    hantei.append(end_data[i - 1])
        print(hantei)
            
        
                
            
                
                

        cv2.namedWindow("image", cv2.WINDOW_NORMAL)

        cv2.imshow("image",self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        

# メイン処理
if __name__ == "__main__":  # pythonファイルが“.py”で実行されているかを判定   pythonではファイルをインポートすると自動的に実行される   モジュールとしてインポートすると__name__には__ファイル名__が入るが、pythonファイルとして実行すると__main__が入る。
    main = Main()
    main.mainloop()






















import cv2
import numpy as np

# 画像を読み込む
image = cv2.imread('image.jpg')

# 色範囲を定義 (HSV色空間)
color_ranges = {
    'white': [(0, 0, 200), (180, 30, 255)],
    'red': [(0, 100, 100), (10, 255, 255)],
    'yellow': [(20, 100, 100), (30, 255, 255)],
    'green': [(40, 100, 100), (70, 255, 255)]
}

# 画像をHSVに変換
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

object_positions = []

for color, (lower, upper) in color_ranges.items():
    # 色範囲でマスクを作成
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

    # 輪郭を検出
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # 最小の外接矩形を取得
        x, y, w, h = cv2.boundingRect(contour)
        
        # オブジェクトの位置情報をリストに追加
        object_positions.append((x, color))
        
        # 外接矩形を描画
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

# x座標でソート
object_positions.sort()

# 左からの順番でオブジェクトの色を出力
for pos in object_positions:
    print(f"{pos[1]} object at x: {pos[0]}")

# 結果を表示
cv2.imshow('Detected Objects', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
