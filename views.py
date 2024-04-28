import requests
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Blueprint, render_template, redirect, url_for, request

API_KEY = "test_220c33e40b65c92482e029516373f544dc8910fc39d0853f3ee728c02de95589bffac000d9444c05b54ecbf051285bb5"

maple = Blueprint(
    "maple",
    __name__,
    template_folder="templates",
    static_folder="static"
)

Base = declarative_base()


class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    character_name = Column(String)
    world_name = Column(String)
    character_gender = Column(String)
    character_class = Column(String)
    character_class_level = Column(String)
    character_level = Column(Integer)
    character_exp = Column(Integer)
    character_exp_rate = Column(String)
    character_guild_name = Column(String)
    character_image = Column(String)


engine = create_engine('sqlite:///maplestory.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@maple.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        character_name = request.form['character_name']

        headers = {
            "x-nxopen-api-key": API_KEY
        }

        url_string = "https://open.api.nexon.com/maplestory/v1/id?character_name=" + character_name
        response = requests.get(url_string, headers=headers)

        if response.status_code == 200:
            ocid = response.json().get('ocid', '')
            if ocid:
                url_string = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date=2024-04-25"
                response = requests.get(url_string, headers=headers)
                if response.status_code == 200:
                    character_data = response.json()
                    character = Character(
                        date=character_data['date'],
                        character_name=character_data['character_name'],
                        world_name=character_data['world_name'],
                        character_gender=character_data['character_gender'],
                        character_class=character_data['character_class'],
                        character_class_level=character_data['character_class_level'],
                        character_level=character_data['character_level'],
                        character_exp=character_data['character_exp'],
                        character_exp_rate=character_data['character_exp_rate'],
                        character_guild_name=character_data['character_guild_name'],
                        character_image=character_data['character_image']
                    )
                    session.add(character)
                    session.commit()

        return redirect(url_for('maple.characters'))
    return render_template('index.html')


@maple.route("/char")
def characters():
    characters = session.query(Character).all()
    return render_template('characters.html', characters=characters)


@maple.route("/char/stat/<int:character_id>")
def stat(character_id):
    # 캐릭터 정보 조회
    character = session.query(Character).filter_by(id=character_id).first()
    if character is None:
        return "캐릭터를 찾을 수 없습니다.", 404

    headers = {
        "x-nxopen-api-key": API_KEY
    }

    url_string = f"https://open.api.nexon.com/maplestory/v1/character/stat?ocid={character.character_ocid}&date=2024-04-25"
    response = requests.get(url_string, headers=headers)

    if response.status_code == 200:
        character_stats = response.json()
        # 여기에서 character_stats 데이터를 사용하여 사용자에게 보여줄 페이지를 렌더링 할 수 있습니다.
        return render_template('character_stats.html', character=character, stats=character_stats)
    else:
        return "스탯 정보를 가져올 수 없습니다.", response.status_code


@maple.route('/delete_character/<int:character_id>', methods=['POST'])
def delete_character(character_id):
    # DB 세션 생성
    session = Session()
    try:
        # 삭제할 캐릭터 조회
        character = session.query(Character).filter_by(id=character_id).first()
        if character:
            session.delete(character)
            session.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()
    finally:
        session.close()
    # 삭제 후 /maple/char 로 리다이렉트
    return redirect(url_for('maple.characters'))
