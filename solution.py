import cv2
import numpy as np

def solution(image, current_speed, current_steering):
    # 1. Görüntü İşleme (Daha geniş bir eşik aralığı)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Çizgiyi daha net seçmek için eşik değerini 120 yapalım
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

    # 2. Sadece alt kısma odaklan (64x64'ün alt yarısı)
    height, width = thresh.shape
    roi = thresh[int(height * 0.5):height, :]
    
    # 3. Çizgi Bulma
    M = cv2.moments(roi)
    
    if M["m00"] > 50: # Sadece yeterince beyaz piksel varsa hareket et
        cx = int(M["m10"] / M["m00"])
        # Hata: 32 piksel merkezdir.
        error = cx - 32
        
        # P katsayısını biraz düşürelim (0.03) ki çok sert dönmesin
        steering = error * 0.03
        
        # Hız: Minimum 10, Maksimum 20 olacak şekilde sabit tutalım
        # Çok hızlı dönerken hızı 0'a düşürmüyoruz (spin atmaması için)
        target_speed = 15.0 
    else:
        # Çizgi yoksa dönmeyi BIRAK ve yavaşça ileri git (Arayış modu)
        steering = 0.0
        target_speed = 8.0

    # 4. Değerleri Sınırla ve Döndür
    steering = float(np.clip(steering, -0.6, 0.6)) # Dönüş açısını %60 ile kısıtladık
    target_speed = float(target_speed)

    return target_speed, steering