from PIL import Image, ImageDraw, ImageFont
import os

# 텍스트에 테두리를 추가하는 함수
def add_text_border(draw, text, position, font, fill, border_width, border_color):
    x, y=position
    # 테두리 두께만큼의 범위에서 텍스트 그리기
    for x_offset in range(-border_width, border_width):
        for y_offset in range(-border_width, border_width):
            draw.text((x + x_offset, y + y_offset), text, font=font, fill=border_color)
    
    # 원래 위치에 텍스트 그리기
    draw.text(position, text, font=font, fill=fill)

# 앨범 아트 이미지 생성 함수
def create_album_art(image_path, title, artist):
    # 이미지 열기
    img=Image.open(image_path)
    width, height=img.size
    draw=ImageDraw.Draw(img)

    # 글자 크기 설정하기
    title_font_size=int(height * 0.07)
    artist_font_size=int(height * 0.05)
    title_font=ImageFont.truetype("malgun.ttf", title_font_size) # 윈도우
    artist_font=ImageFont.truetype("malgun.ttf", artist_font_size) # 윈도우

    # 텍스트와 테두리 색상 설정하기
    text_color=(255, 255, 255)
    border_color=(0, 0, 0)
    border_width=15

    # 제목 텍스트의 너비와 높이 계산하기
    title_width, title_height=draw.textlength(title, font=title_font), title_font.getbbox(title)[1]
    # 제목 텍스트의 너비가 이미지 너비의 90%를 초과하면 글자 크기 줄이기
    while title_width > width * 0.9:
        title_font_size -= 1
        artist_font_size=int(title_font_size * 0.7)
        title_font=ImageFont.truetype("malgun.ttf", title_font_size) # 윈도우
        artist_font=ImageFont.truetype("malgun.ttf", artist_font_size) # 윈도우
        title_width, title_height=draw.textlength(title, font=title_font), title_font.getbbox(title)[1]

    # 제목 텍스트의 위치 계산하기
    title_x=(width - title_width) / 2
    title_y=(height - title_height) * 0.75

    # 아티스트 텍스트의 너비와 높이 계산하기
    artist_width, artist_height=draw.textlength(artist, font=artist_font), artist_font.getbbox(artist)[1]

    # 아티스트 텍스트의 위치 계산하기
    artist_x=(width - artist_width) / 2
    artist_y=title_y + title_font_size + 20

    # 텍스트와 테두리 그리기
    add_text_border(draw, title, (title_x, title_y), title_font, text_color, border_width, border_color)
    add_text_border(draw, artist, (artist_x, artist_y), artist_font, text_color, border_width, border_color)

    # 이미지 파일명을 이용해 새로운 이미지 파일명 만들기
    dir, file_fill_name=os.path.split(image_path) # 경로와 파일명 분리하기
    file_name, ext=os.path.splitext(file_fill_name) # 파일명과 확장자 분리하기
    img_with_info_path=f'{dir}/{file_name}_info{ext}'

    img.save(img_with_info_path)

    return img_with_info_path

if __name__ == '__main__':
    # 사용 예시
    img_with_info_path=create_album_art(
        "./dreamlike_diffusion/Cheap_Thrills_Sia_ft__Sean_Paul.jpg",
        "Cheap Thrills (feat. Sean Paul)",
        "Sia"
    )

    print(img_with_info_path)