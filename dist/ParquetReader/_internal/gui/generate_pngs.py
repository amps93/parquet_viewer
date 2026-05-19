import os
from PySide6.QtGui import QImage, QPainter, QColor, QPen
from PySide6.QtCore import Qt

d = r'c:\Users\user\Desktop\amps\antigravity\parquet_viewer\gui'

def draw_arrow(filename, direction):
    img = QImage(14, 14, QImage.Format_ARGB32)
    img.fill(Qt.transparent)
    painter = QPainter(img)
    painter.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor('#aab0c8'))
    pen.setWidth(2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    painter.setPen(pen)
    if direction == 'up':
        painter.drawLine(2, 9, 7, 4)
        painter.drawLine(7, 4, 12, 9)
    elif direction == 'down':
        painter.drawLine(2, 4, 7, 9)
        painter.drawLine(7, 9, 12, 4)
    elif direction == 'left':
        painter.drawLine(9, 2, 4, 7)
        painter.drawLine(4, 7, 9, 12)
    elif direction == 'right':
        painter.drawLine(4, 2, 9, 7)
        painter.drawLine(9, 7, 4, 12)
    painter.end()
    img.save(os.path.join(d, filename))

draw_arrow('up_arrow.png', 'up')
draw_arrow('down_arrow.png', 'down')
draw_arrow('left_arrow.png', 'left')
draw_arrow('right_arrow.png', 'right')
