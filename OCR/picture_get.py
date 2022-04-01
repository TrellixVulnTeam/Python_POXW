"""
@author: Alfons
@contact: alfons_xh@163.com
@file: VerificationCode.py
@time: 19-2-27 下午9:12
@version: v1.0 
"""
import pathlib

from paddleocr import PaddleOCR, draw_ocr

ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory


def convert(src_dir, dst_file):
    tmp_data = list()

    for img_path in sorted(src_dir.iterdir(), key=lambda f: f.name):
        if img_path.name.startswith('.'):
            continue
        print(img_path)

        result = ocr.ocr(str(img_path), cls=True)

        line_data = ''.join([line[-1][0] for line in result])
        print(line_data)
        tmp_data.append(line_data)

    dst_file.write_text('\n\n'.join(tmp_data))


if __name__ == '__main__':
    for src_dir, dst_file in [
        (pathlib.Path("/Volumes/DataFast/小房子-绉"), pathlib.Path(__file__).parent / "3_译本_邹凡凡.txt"),
        (pathlib.Path("/Volumes/DataFast/小房子-郝"), pathlib.Path(__file__).parent / "4_译本_郝小慧.txt"),
        (pathlib.Path("/Volumes/DataFast/小房子-张"), pathlib.Path(__file__).parent / "5_译本_张媛.txt"),
    ]:
        convert(src_dir=src_dir, dst_file=dst_file)

# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`

#
# # 显示结果
# from PIL import Image
#
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')
