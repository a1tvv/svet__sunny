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
        },
         {
            "id": 3,
            "tracks": [
                {"title": "19. О нравах Пророка ﷺ  до пророчества.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_019.mp3"},
                {"title": "20. Женитьба на Хадидже и о детях Пророка ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_020.mp3"},
                {"title": "21. Строительство Каабы курайшитами.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_021.mp3"},
                {"title": "22. Начало пророчества.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_022.mp3"},
                {"title": "23. О единобожниках в Мекке до пророчества Мухаммада ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_023.mp3"},
                {"title": "24. О начале призыва и о тех, кто первыми приняли Ислам.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_024.mp3"},
                {"title": "25. О призыве курайшитов и родственников Пророка ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_025.mp3"},
                {"title": "26. О тех, кто принял Ислам из бедных жителей Мекки и о призыве Абу Бакра, да будет доволен им Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_026.mp3"},
                {"title": "27. Защита Абу Талибом, Пророка ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_027.mp3"},
                {"title": "28. О диалоге Пророка ﷺ с Уалид ибн Мугъирой и чуде Корана.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_028.mp3"},
                {"title": "29. Избиение курайшитами Пророка ﷺ и ислам дяди Пророка ﷺ Хамзы, да будет доволен им Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_029.mp3"},
                {"title": "30. Принятие Ислама Абу Зарром, да будет доволен им Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_030.mp3"},
                {"title": "31. О том, как курайшиты требовали от Пророка ﷺ разные чудеса.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_031.mp3"},
                {"title": "32. О попытке Абу Джахля убить Пророка ﷺ и мучении рабов принявших Ислам.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_032.mp3"},
                {"title": "33. Начало хиджры в Эфиопию. История Абу Бакра с Абу Дуганой.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_033.mp3"},
                {"title": "34. История Ислама Умара ибн аль-Хаттаба, да будет доволен им Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_034.mp3"},
            ],
            "questions": [
                "Как звали первую жену Пророка ﷺ?",
                "Сколько лет было Пророку ﷺ и его жене когда они поженились? Какой был махрам (калым)?",
                "Имеет ли право простой мусульманин иметь столько же жён, сколько имел Пророк ﷺ?",
                "Перечисли имена детей Пророка ﷺ.",
                "С каким договором курайшиты перестроили Каабу?",
                "Кто из курайшитов начал ломать Каабу?",
                "Можно ли запрещать порицаемое, если в этом или после этого следует такое же порицаемое или больше? Приведите доказательство.",
                "Какими были первые аяты, ниспосланные Пророку ﷺ?",
                "Сколько раз Пророк ﷺ видел Джибриля, мир ему, в его настоящем виде?",
                "Как звали сына дяди Хадиджи и кем он был?",
                "Что сказал сын дяди Хадиджи Пророку ﷺ когда он рассказал ему о том, что с ним случилось?",
                "Почему иудеи под гневом Всевышнего Аллаха?",
                "Можно ли брать в довод большинство и почему?",
                "Перечисли первых людей, принявших Ислам?",
                "Можно ли менять отчество и фамилию сироты, взятого на воспитание?",
                "Перечисли самых лучших людей в нашей общине после Пророка ﷺ.",
                "Про кого была ниспослана сура «аль-Масад»?",
                "Какую пользу мы берём из обращения Пророка ﷺ к Фатиме: «Совершай дела, я ничем не могу помочь тебе в Судный день»?",
                "Когда начинается Судный день для каждого человека?",
                "Какая из причин того, что бедные люди быстрее отвечают на призыв чем богатые?",
                "Даёт ли Аллах победу Исламу через неверующих и нечестивцев?",
                "Допускается ли национализм в Исламе?",
                "Что сказал Уалид ибну Мугъира курайшитам о Коране после его диалога с Пророком ﷺ?",
                "Как звали Абу Джахля?",
                "Почему Пророк ﷺ отказал просьбам курайшитов о каком-нибудь чуде?",
                "Кто был одним из тех, кого сильно мучили и каким образом его мучили?",
                "Кто был первым шахидом в Исламе?",
                "Берёт ли человек грех за то дело, к совершению которого был принуждён?",
                "Куда была сделана первая хиджра?",
                "Кто первым сделал хиджру?",
                "Как ’Умар, да будет доволен им Аллах, принял Ислам?"
                
            ]
        },
            {
            "id": 4,
            "tracks": [
                {"title": "35. История ’Укбы ибн Аби Муайита с Пророком ﷺ. О влиянии плохих друзей.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_035.mp3"},
                {"title": "36. Очередные попытки курайшитов договориться с Пророком ﷺ остановить призыв.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_36.mp3"},
                {"title": "37. Издевательство курайшитов над Пророком ﷺ в Мекке.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_037.mp3"},
                {"title": "38. Бойкотирование и экономическая блокада Пророка ﷺ и его рода.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_038.mp3"},
                {"title": "39. Год печали. Смерть дяди Пророка ﷺ Абу Талиба и Хадиджы, да будет доволен ею Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_039.mp3"},
                {"title": "40. Выход Пророка ﷺ из Мекки в Таиф.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_040.mp3"},
                
                {"title": "41. Возвращение из Таифа в Мекку. Защита Пророка ﷺ Мут’имом ибн ‘Ади.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_041.mp3"},
                {"title": "42. Истрия принятия Ислама джиннами.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_042.mp3"},
                {"title": "43. История сподвижников в Эфиопии с эфиопским царем.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_043.mp3"},
                {"title": "44. «аль-Исра» — перенесение Пророка ﷺ из Мекки в мечеть аль-Акса в Иерусалиме.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_044.mp3"},
                {"title": "45. «аль-Ми’радж» — вознесение Пророка ﷺ на небеса.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_045.mp3"},
                {"title": "46. Раскол Луны.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_046.mp3"},
                
                {"title": "47. Призыв арабов, посещающих Мекку и деятельность Абу Ляхаба.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_047.mp3"},
                {"title": "48. Начало принятие Ислама жителями Медины и первая присяга «’Акабат аль-уля».", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_048.mp3"},
                {"title": "49. Об Исламе Туфайля ибн ‘Амра и о смысле свидетельства «Мухаммад расулю-Ллах».", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_049.mp3"},
                {"title": "50. Делегация жителей Медины и вторая присяга.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_050.mp3"},
                
                {"title": "51. Начало переселения сподвижников в Медину.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_051.mp3"},
                {"title": "52. Решение курайшитов убить Пророка ﷺ.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_052.mp3"},
                {"title": "53. Переселение Пророка ﷺ и Абу Бакара, да будет доволен им Аллах.", "url": "https://abdurtwhd.ams3.cdn.digitaloceanspaces.com/sira_proroka/sira_053.mp3"},
            ],
               "questions": [
                    "На какой религии рождается человек?",
                    "Можно ли уподобляться неверующим с целью призыва их к Исламу?",
                    "Можно ли торопиться с ответом на ду’а?",
                    "Верили ли курайшиты в существование Всевышнего Аллаха?",
                    "Сколько лет продолжался бойкот мусульманам?",
                    "Кто первым начал бороться против бойкота?",
                    "Какую пользу берём из того, что Пророк ﷺ и его сподвижники были подвергнуты испытаниям и трудностям на пути распространения истины?",
                    "Является ли мусульманином тот человек, который убеждён в истинности Ислама, однако не произносит шахаду вслух?",
                    "Почему один из годов в жизни Пророка ﷺ был назван «годом печали»?",
                    "Что Пророк ﷺ ответил ангелам, которые пришли уничтожить многобожников?",
                    "Как называлось племя джиннов, которые слушали Пророка ﷺ?",
                    "Какими из хороших нравов обладал Наджаши и какой урок нам в этом?",
                    "Какую суру Джа’фар читал для Наджаши?",
                    "В чём величие мечети аль-Акса?",
                    "Можно ли справлять ночь «Исра и Ми’радж» или день рождения Пророка ﷺ и почему?",
                    "Сколько у мусульман праздников?",
                    "Откуда была Исра, т.е. где был Пророк ﷺ?",
                    "На чём перенёсся Пророк ﷺ в мечеть «аль-Акса»?",
                    "Кого пророк ﷺ видел на первом небе?",
                    "Как называется загробная жизнь?",
                    "Кого Пророк ﷺ видел на седьмом небе?",
                    "В чём величие молитвы?",
                    "Сколько молитв было вменено Аллахом в обязанность в первый раз?",
                    "За какое время произошло Исра и Ми’радж?",
                    "Какое чудо Пророк ﷺ показал курайшитам в Мекке?",
                    "На сколько групп делилось население Медины?",
                    "Почему первая присяга называлась «присягой женщин»?",
                    "Кто был первым послом в Исламе?",
                    "Кто предложил убить Пророка ﷺ и в чём заключалось это предложение?",
                    "С кем Пророк ﷺ сделал хиджру?",
                    "Какую пользу мы берём из хиджры Пророка ﷺ?",
                    "Кто описал внешность Пророка ﷺ лучше всех?",
                    "Когда Пророк ﷺ сделал хиджру?"
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