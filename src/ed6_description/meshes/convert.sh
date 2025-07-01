#!/bin/bash

# 遍歷當前目錄下所有的 .STL 文件
for file in *.STL; do
  # 檢查文件是否存在
  if [ -f "$file" ]; then
    # 創建一個備份文件夾
    mkdir -p backup
    # 備份原始文件
    cp "$file" "backup/$file"
    echo "備份文件: $file"
    
    # 使用 meshlabserver 進行轉換，將結果覆蓋原始文件
    # -i 輸入文件, -o 輸出文件, -s 腳本, -om vc fq wn opt
    # vc: vertex color, fq: face quality, wn: wedge normal
    # opt: Binary STL output option
    meshlabserver -i "$file" -o "$file" -om vc fq wn
    echo "轉換文件: $file 為二進制格式"
  fi
done

echo "所有STL文件已轉換為二進制格式並備份。"
