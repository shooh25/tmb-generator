from PIL import Image
import numpy as np
import math
import sys

args = sys.argv

if len(args) < 2:
    print('ERROR: パスを指定してください。')
    sys.exit(1)

# 上にのっける画像を選択

try:
    vis_im = Image.open(args[1])
except FileNotFoundError:
    print('ERROR: 指定されたファイルが見つかりません。')
    sys.exit(1)
except IOError:
    print('ERROR: 指定されたファイルは非対応です。')
    sys.exit(1)
except Exception:  
    print('ERROR: エラーが発生しました。')
    sys.exit(1)


# 背景に関する値(長さ、傾き)を設定
def set_bg_values():
    length = int(math.sqrt(canvas_size[0]**2 + canvas_size[1]**2))
    angle = math.atan(canvas_size[1] / canvas_size[0])
    angle = int(math.degrees(angle))
    return length, angle


# グラデーションを作成
def get_gradient_2d(start, end):
    return np.tile(np.linspace(start, end, bg_size[0]), (bg_size[0], 1))

def get_gradient_3d():
    result = np.zeros((bg_size[0], bg_size[0], 3)) 
    for i, (start, end) in enumerate(zip(start_color, end_color)):
        result[:, :, i] = get_gradient_2d(start, end)
    return result


# 画像中心を切り抜き
def crop_center(im, size, org_size):
    x1 = (size[0] - org_size[0])/2
    y1 = (size[1] - org_size[1])/2
    x2 = x1 + org_size[0]
    y2 = y1 + org_size[1]
    return im.crop((x1, y1, x2, y2))


# 上にのっける画像をリサイズ
def resize_im(im):
    org_w, org_h = im.size
    w, h = vis_size

    if w / h > org_w / org_h:
        im = im.resize((w, int(w / (org_w / org_h))))
        return crop_center(im, im.size, vis_size)
    else:
        im = im.resize((int(h * (org_w / org_h)), h))
        return crop_center(im, im.size, vis_size)
    

# sizes
canvas_size = (1280, 800)
vis_size = (904, 565)

bg_values = set_bg_values()
bg_size = (bg_values[0], bg_values[0])

# 上にのっける画像をリサイズ
vis_im = resize_im(vis_im)

# colors
start_color = (44, 44, 46)
end_color = (28, 28, 30)

# グラデーション背景を作成
bg_im = Image.fromarray(np.uint8(get_gradient_3d()))
bg_im = bg_im.rotate(-bg_values[1])

# 背景を切り抜いてキャンバス作成
canvas = crop_center(bg_im, bg_size, canvas_size)

# キャンバス上中央に配置
x = int((canvas_size[0] - vis_size[0])/2)
y = int((canvas_size[1] - vis_size[1])/2)
canvas.paste(vis_im, (x, y))

# 保存
path = ('desktop/tmb-img.png')
canvas.save(path)
print('サムネイルを作成しました。: {}'.format(path))