from flask import Flask, render_template, redirect, url_for, request
from csv import DictReader

ALL_CAFES = list(DictReader(open('project.csv', encoding = 'utf-8')))
for cafe in ALL_CAFES:
        for key in cafe:
            if cafe [key] == 'нет':
                cafe[key] = None

KEY_SET = {'название','открытие','закрытие','адрес','добираться'}

def filter(coffee, price, time):
    some_cafes = []
    less_cafes = []
    required_cafes = []
    if not coffee == 'любой':
        for cafe in ALL_CAFES:
            for key in cafe:
                if key == coffee:
                    if not cafe[key] == None:
                        some_cafes.append( cafe )
        for cafe in some_cafes:
            if int(cafe[coffee]) <= int(price):
                less_cafes.append(cafe)
        for cafe in less_cafes:
            if int(cafe['добираться']) <= int(time):
                required_cafes.append(cafe)
    else:
        for cafe in ALL_CAFES:
            cafe['любой'] = None
        for cafe in ALL_CAFES:
            for key in cafe:
                if key == 'эспрессо' or key == 'латте' or key == 'раф' or key == 'американо' or key == 'капучино' or key == 'флэт уайт' or key == 'мокко':
                    if not cafe[key] == None:
                        if int(cafe[key]) <= int( price ):
                            cafe['любой'] = 'да'

        for cafe in ALL_CAFES:
            if cafe['любой'] == 'да':
                less_cafes.append(cafe)

        for cafe in less_cafes:
            if int(cafe['добираться']) <= int(time):
                required_cafes.append(cafe)
    return required_cafes

def list_creator(required_cafes, coffee):
    KEY_SET.add(coffee)
    cafes_for_html = []

    if not coffee == 'любой':
        for Di in required_cafes:
            the_keys = set( Di.keys() ).difference( KEY_SET )
            for the_key in the_keys:
                 Di.pop( the_key )
        cafes_for_html = required_cafes
    else:
        for required_cafe in required_cafes:
            required_cafe.pop('любой')
            cafes_for_html.append(required_cafe)

    for Di in cafes_for_html:
        for key in Di:
            if key == 'добираться':
                if Di[key].endswith( '2' ) and not Di[key].startswith( '1' ) or Di[key].endswith( '3' ) and not \
                Di[key].startswith( '1' ) or Di[key].endswith( '4' ) and not Di[key].startswith( '1' ):
                    Di[key] = Di[key] + ' минуты'
                elif Di[key].endswith( '1' ) and not Di[key].startswith( '1' ):
                    Di[key] = Di[key] + ' минуту'
                else:
                    Di[key] = Di[key] + ' минут'

    for Di in cafes_for_html:
        for key in Di:
            if key == 'эспрессо' or key == 'латте' or key == 'раф' or key == 'американо' or key == 'капучино'\
            or key == 'флэт уайт' or key == 'мокко':
                if not Di[key] == None:
                    if Di[key].endswith( '2' ) and not Di[key].startswith( '1' ) or Di[key].endswith('3' ) \
                    and not Di[key].startswith( '1' ) or Di[key].endswith( '4' ) and not Di[key].startswith('1' ):
                        Di[key] = Di[key] + ' рубля'
                    elif Di[key].endswith( '1' ) and not Di[key].startswith( '1' ):
                        Di[key] = Di[key] + ' рубль'
                    else:
                        Di[key] = Di[key] + ' рублей'
                else:
                    Di[key] = 'нет'
    KEY_SET.remove(coffee)
    return cafes_for_html

app = Flask(__name__)
@app.route('/')
def page_with_questions():
    return render_template('questions.html')

@app.route('/cafes')
def where_to_go():
    sad_news = ''
    with open('help.txt',encoding='utf-8') as file:
        data = file.read()
    coffee,price,time = data.split('\n')
    required_cafes = filter(coffee,price,time)
    cafes_for_html = list_creator(required_cafes,coffee)
    if cafes_for_html == []:
        sad_news = 'К сожалению, мы не нашли для вас подходящих кофеен'
    return render_template('cafes.html', places = cafes_for_html, sad_news = sad_news)

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('page_with_questions'))
    coffee = request.args.get('coffee')
    price = request.args.get('price')
    time = request.args.get('time')
    strings = coffee+'\n'+price+'\n'+time
    with open('help.txt', 'w', encoding='utf-8') as file:
        file.write(strings)
    return redirect(url_for('where_to_go'))

if __name__ == '__main__':
    app.run( debug=True )