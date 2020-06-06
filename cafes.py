from flask import Flask, render_template, redirect, url_for, request
from csv import DictReader
from random import choice

def filter(coffee, price, time):
    all_cafes = list( DictReader( open( 'project.csv', encoding='utf-8' ) ) )
    for cafe in all_cafes:
        for key in cafe:
            if cafe[key] == 'нет':
                cafe[key] = None
    some_cafes = []
    less_cafes = []
    required_cafes = []
    if not coffee == 'любой':
        for cafe in all_cafes:
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
        for cafe in all_cafes:
            cafe['любой'] = None
        for cafe in all_cafes:
            for key in cafe:
                if key == 'эспрессо' or key == 'латте' or key == 'раф' or key == 'американо' or key == 'капучино' or key == 'флэт уайт' or key == 'мокко':
                    if not cafe[key] == None:
                        if int(cafe[key]) <= int( price ):
                            cafe['любой'] = 'да'

        for cafe in all_cafes:
            if cafe['любой'] == 'да':
                less_cafes.append(cafe)

        for cafe in less_cafes:
            if int(cafe['добираться']) <= int(time):
                required_cafes.append(cafe)
    return required_cafes

def dic_creator(Di, coffee, key_set = {'название','открытие','закрытие','адрес','добираться'}):
    key_set.add(coffee)

    if not coffee == 'любой':
        the_keys = set( Di.keys() ).difference( key_set )
        for the_key in the_keys:
            Di.pop( the_key )
    else:
        Di.pop('любой')


    for key in Di:
        if key == 'эспрессо' or key == 'латте' or key == 'раф' or key == 'американо' or key == 'капучино'\
        or key == 'флэт уайт' or key == 'мокко':
            if  Di[key] == None:
                Di[key] = 'нет'
    key_set.remove(coffee)
    return Di

def chooser(required_cafes):
    Di = choice(required_cafes)
    return Di

def comments (fin_dict):
    for key in fin_dict:
        if key == 'добираться':
            if fin_dict[key].endswith( '2' ) and not fin_dict[key].startswith( '1' ) or fin_dict[key].endswith(
                    '3' ) and not \
                    fin_dict[key].startswith( '1' ) or fin_dict[key].endswith( '4' ) and not fin_dict[key].startswith(
                '1' ):
                fin_dict[key] = fin_dict[key] + ' минуты'
            elif fin_dict[key].endswith( '1' ) and not fin_dict[key].startswith( '1' ):
                fin_dict[key] = fin_dict[key] + ' минуту'
            else:
                fin_dict[key] = fin_dict[key] + ' минут'

    for key in fin_dict:
        if key == 'эспрессо' or key == 'латте' or key == 'раф' or key == 'американо' or key == 'капучино' \
            or key == 'флэт уайт' or key == 'мокко':
            if not fin_dict[key] == None:
                if fin_dict[key].endswith( '2' ) and not fin_dict[key].startswith( '1' ) or fin_dict[key].endswith( '3' ) \
                    and not fin_dict[key].startswith( '1' ) or fin_dict[key].endswith( '4' ) and not fin_dict[
                key].startswith \
                        ( '1' ):
                    fin_dict[key] = fin_dict[key] + ' рубля'
                elif fin_dict[key].endswith( '1' ) and not fin_dict[key].startswith( '1' ):
                    fin_dict[key] = fin_dict[key] + ' рубль'
                else:
                    fin_dict[key] = fin_dict[key] + ' рублей'
    return fin_dict
app = Flask(__name__)


@app.route('/')
def page_with_questions():
    return render_template('questions.html')

@app.route('/cafes')
def where_to_go():
    sad_news = ''
    with open('help.txt', encoding='utf-8') as file:
        data = file.read()
    coffee,price,time = data.split('\n')
    required_cafes = filter(coffee,price,time)
    if required_cafes == []:
        sad_news = 'К сожалению, мы не нашли для вас подходящих кофеен'
        fin_dict = {}
    else:
        Di = chooser(required_cafes)
        Di = dic_creator(Di,coffee)
        fin_dict = comments(Di)
    return render_template('cafes.html', place = fin_dict, sad_news = sad_news)

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
