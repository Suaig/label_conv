# 功能说明
  用于转换xml的标签文件到txt提供给yolo使用，并支持中文和类别控制

# 使用方式
usage: voc_label.py [-h] [--xml XML] [--cls CLS] [--txt TXT] [--dis-cls DIS_CLS]

optional arguments:
  -h, --help         show this help message and exit
  --xml XML          input xml file Annotations
  --cls CLS          class names file
  --txt TXT          output txt file Darknet for yolo
  --dis-cls DIS_CLS  dislodge some class. 0 is all 1 2 3 is index in class.names
  
  --xml输入的是字符串xml标签的位置 --cls是类别名字文件的位置.names --txt是输出的位置 --dis-cls是不转换的标签在类别名称文件里的索引号


# 所需的库
BeautifulSoup
tqdm
argparse
