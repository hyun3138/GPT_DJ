import openai
from pathlib import Path
from base64 import b64decode

openai.api_key='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'

# 노래 제목과 아티스트를 입력받아 해당 노래에 대해 정보를 생성하는 함수
def dalle2_prompt_generator(song_title, artist):
    # GPT-3.5-turbo 모델을 사용해 채팅 대화 생성하기
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        top_p=0.1,
        temperature=0.2,
        messages=[
            {
                "role": 'system',
                "content": """
                    You are an AI assistant designed to generate prompts for Dalle-2. When a user provides information about a song, envision an image that represents the song's lyrics and mood.
                Based on the image you've envisioned, generate a Dalle-2 prompt in a couple of sentences, avoiding crime-related words such as gangs or drugs.
                If the prompt contains any violent or sexual expressions that are not suitable for a 15-year-old child to hear, present them in a more subdued manner.
                Refrain from mentioning any famous person's name or the artist of the song.
                """
            },
            {"role":"user", "content": f'Black or White - Michael Jackson'},
            {"role": "assistant", "content": "A world of contrasts and contradictions, where darkness and light collide in a never-ending struggle. The beat pulses with the rhythm of life, as voices rise up in a chorus of hope and defiance. The message is clear: no matter the color of our skin, we are all one people, united in our humanity." },
            {"role":"user", "content": f'Attention - Charlie Puth'},
            {"role": "assistant", "content": " A person standing alone in a crowded room, feeling disconnected and unheard. He realizes that his ex is only doing it for her own benefit and not because she truly cares about him" },
            {"role":"user", "content": f'{song_title} - {artist}'}
        ]
    )

    # 생성된 메시지 중 첫 번째 메시지 반환하기
    return response.choices[0].message.content

def generate_dalle_image(song_title, artist):
    # 달리2 이미지를 생성하는 프롬프트 생성하기
    prompt=dalle2_prompt_generator(song_title, artist)
    print(prompt)

    # 이미지를 저장할 디렉터리를 설정 및 생성하기
    DATA_DIR=Path.cwd() / 'dalle2_results'
    DATA_DIR.mkdir(exist_ok=True)

    # 디렉터리 경로 출력하기
    print(DATA_DIR)

    # openai api를 사용해 이미지 생성 요청하기
    response=openai.Image.create(
        prompt=prompt,
        n=1, # 몇 개의 이미지를 생성할지 정하기
        size="512x512", # 해상도
        response_format='b64_json' # 응답 형식을 Base64로 인코딩된 JSON 파일로 지정하기
)
    # 생성된 이미지의 파일명 설정하기
    file_name=DATA_DIR / f"{song_title}_{artist}.png"

    # 응답에서 Base64로 인코딩된 이미지 데이터 추출하기
    b64_data=response['data'][0]['b64_json']

    # Base64 이미지 데이터를 디코딩해서 바이너리 형식으로 변환하기
    image_data=b64decode(b64_data)

    # 이미지를 저장할 파일 경로 지정하기
    image_file=DATA_DIR / f'{file_name}'

    # 디스크에 이미지 파일 저장하기
    with open(image_file, mode='wb') as png:
        png.write(image_data)

    return image_file


if __name__ == '__main__':
    song_title="When I was Your Man"
    artist='Burno Mars'
    generate_dalle_image(song_title, artist)