from django.core.paginator import Paginator
from django.shortcuts import render

def index(request):
    sheikh = {
        'links': {
            'rinat': 'https://t.me/toislam',
            'abu_yahya': 'https://t.me/abuyahya_net',
            'siraj': 'https://t.me/sirajabutalha',
        }
    }
    return render(request, 'index.html', sheikh)
from django.core.paginator import Paginator
from django.shortcuts import render

def sira(request):
    # Каждая страница — это один элемент списка (словарь)
    pages_data = [
        {
            "id": 1,
            "tracks": [
                {"title": "1. Вступление. Положение арабов до Ислама.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_001.mp3"},
                {"title": "2. История Ибрахима, мир ему и Хаджар.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_002.mp3"},
                {"title": "3. История Хаджар и источника воды Зам-зам.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_003.mp3"},
                {"title": "4. История прибытия племени Джурхум в Мекку", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_004.mp3"},
                {"title": "5. История Ибрахима и жен Исма’иля.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_005.mp3"},
                {"title": "6. Строительство Каабы Ибрахимом и Исма’илем", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_006.mp3"},
                {"title": "7. Начало распространения многобожия среди арабов.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_007.mp3"},
                {"title": "8. История того, как распространился иудаизм на Аравийском полуострове.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_008.mp3"},
                {"title": "9. История того, как распространилось христианство на Аравийском полуострове.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_009.mp3"},
                {"title": "10. История Абрахи и Слона.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_010.mp3"},
            ],
            "questions": [
                "Каковы цели изучения жизнеописания (сиры) Пророка, да благословит его Аллах и приветствует?",
                "Как звали мать Исма’иля?",
                "Какой урок мы извлекаем из истории Ибрахима и Хаджар в Мекке?",
                "Как называлось племя, пришедшее в Мекку?",
                "Какую пользу мы берем из диалога Ибрахима с женой Исма’иля?",
                "Что такое «Макаму Ибрахим»?",
                "Какое племя напало на племя Джурхум?",
                "Кто первым принес ширк на землю арабов?",
                "Имя первого идола, который появился в Мекке?",
                "Какой скверный обычай ввел ’Амр ибн Люхайй помимо тальбиййи?",
                "Какие самые странные божества были в Мекке и какова их история?",
                "Что такое «Ясриб»?",
                "Кто принял Ислам первым не из числа мекканцев?",
                "Откуда пришли евреи в Мекку?",
                "Кто первым покрыл материалом Каабу и кем он был?",
                "Чему поклонялись «наджрань» до прихода христианства?",
                "Как звали царя, который называл себя богом, и каким государством он правил?",
                "Каким образом мальчик, ходивший к монаху и колдуну, узнал истину?",
                "Какими караматами (чудесами) обладал этот мальчик?",
                "Какое ду’а (мольбу) надо говорить тому, кто хочет спастись от зла людей?",
                "Сколько людей приняло христианство после казни мальчика?",
                "Какое чудо произошло во время казни принявших христианство?",
                "Перечисли запретные месяцы.",
                "Кто такие «ахлю-ан-наси»?",
                "Как звали царя, который хотел разрушить Каабу и каким государством он правил?",
                "Как звали слона, на котором сидел верхом царь?"
            ]
        },
        {
            "id": 2,
            "tracks": [
                {"title": "11. История того, как персы попали в Йемен.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_011.mp3"},
                {"title": "12. История Курайшитов.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_012.mp3"},
                {"title": "13. История ’Абдуль-мутталиба и Зам-зама.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_013.mp3"},
                {"title": "14. История рождения отца Пророка ﷺ, ’Абдуллаха.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_014.mp3"},
                {"title": "15. Рождение Пророка Мухаммада ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_015.mp3"},
                {"title": "16. Раннее детство Пророка ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_016.mp3"},
                {"title": "17. Пророк ﷺ на воспитании у ’Абдуль-мутталиба.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_017.mp3"},
                {"title": "18. Пророк ﷺ на воспитании у своего дяди Абу Талиба.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_018.mp3"},
            ],
            "questions": [
                "Как звали царя Персии, который разорвал письмо Пророка ﷺ?",
                "Кто построил «дар ан-надва»?",
                "Кому он завещал всё своё имущество и почему?",
                "Кто и как купил «дар ан-надва» у потомков ’Абду ад-Дар. И как он потом продал его?",
                "Какое настоящее имя деда Пророка ﷺ ’Абдуль-мутталиба?",
                "Когда родился Пророк ﷺ?",
                "В чём величие Пророка ﷺ?",
                "Откуда колдуны узнают о сокровенном?",
                "Каково положение того человека, который идёт к колдуну?",
                "Что должно стоять на первом месте: разум (’акль) или Коран и Сунна (накль)?",
                "Почему курайшиты отдавали своих детей в разные племена?",
                "Как звали молочную мать Пророка ﷺ?",
                "Сколько лет было Пророку ﷺ когда умерла его мать?",
                "В чём мудрость того, что Всевышний Аллах предопределил, чтобы Пророк ﷺ находился со своим дедом на разных переговорах?",
                "В чём был секрет бедности деда Пророка ﷺ?",
                "Кто после смерти деда Пророка ﷺ взял Пророка ﷺ на воспитание?",
                "В чём мудрость того, что Аллах предопределил пророкам быть пастухами?",
                "Кто такие физиогномики («ахль аль-фараса»)?",
            ]
        }
    ]

    paginator = Paginator(pages_data, 1) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    current_page_data = page_obj[0] if page_obj else None

    return render(request, 'sira.html', {
        'page_obj': page_obj,
        'data': current_page_data
    })