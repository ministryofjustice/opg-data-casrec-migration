CREATE SCHEMA IF NOT EXISTS pmf_assignees_20220308_in1174;

SELECT caserecnumber as caserecnumber, id as person_id, supervisioncaseowner_id as original_value,
(SELECT max(id) FROM assignees WHERE name LIKE 'Supervision Closed Cases%') as expected_value
INTO pmf_assignees_20220308_in1174.persons_updates
FROM
(
    SELECT p.caserecnumber, p.id, p.supervisioncaseowner_id, a.name as user_name, a.email, teams.name as team_name, teams.type, teams.teamtype
    FROM persons p
    LEFT JOIN assignees a on a.id = p.supervisioncaseowner_id
    LEFT JOIN assignee_teams ate on ate.assignablecomposite_id = a.id
    LEFT JOIN assignees teams on teams.id = ate.team_id
    where p.caserecnumber in
    (
    '12502465',
    '11679257',
    '12506512',
    '12568769',
    '12648254',
    '11919284',
    '12633883',
    '12899274',
    '12876816',
    '12616079',
    '12691701',
    '12811803',
    '12806571',
    '12543228',
    '12820461',
    '12340844',
    '1282523T',
    '12676065',
    '11660983',
    '12737859',
    '12467474',
    '12804150',
    '12872648',
    '12071082',
    '12869900',
    '12565408',
    '12645285',
    '12814565',
    '13054852',
    '12996165',
    '1281011T',
    '13072864',
    '12753341',
    '12575668',
    '12751594',
    '12270104',
    '12894068',
    '12936853',
    '12885290',
    '13147122',
    '12708515',
    '12548549',
    '1334844T',
    '1242613T',
    '13430279',
    '13256613',
    '12688348',
    '13372272',
    '13264325',
    '13439273',
    '13329130',
    '13426257',
    '13414918',
    '13402353',
    '13360835',
    '13375097',
    '13440003',
    '13414106',
    '13345838',
    '12648041',
    '94060678',
    '13117190',
    '1246450T',
    '11783560',
    '13393092',
    '13345591',
    '13006510',
    '12928634',
    '13324523',
    '10270182',
    '13416366',
    '13370726',
    '13288258',
    '13416101',
    '1313846T',
    '13402451',
    '13445658',
    '13398136',
    '13406982',
    '13407893',
    '13430193',
    '13492381',
    '11757882',
    '12705074',
    '13322338',
    '13401920',
    '13245310',
    '1346272T',
    '13474616',
    '13472443',
    '13507373',
    '99348544',
    '13263679',
    '13343803',
    '13305796',
    '13357465',
    '12168430',
    '13398286',
    '13382514',
    '12129926',
    '13447584',
    '13452217',
    '12924132',
    '13419208',
    '13169129',
    '13464253',
    '13330563',
    '13480040',
    '1276046T',
    '12934772',
    '13285836',
    '13348387',
    '13000105',
    '13496641',
    '13050275',
    '13398833',
    '12446619',
    '13403707',
    '13444494',
    '13079235',
    '13414607',
    '1271044T',
    '13458357',
    '13380888',
    '13165595',
    '13397605',
    '13477482',
    '13383333',
    '13431196',
    '12779580',
    '13436908',
    '13220633',
    '13396084',
    '13456529',
    '12454585',
    '12700369',
    '13191889',
    '13282055',
    '13495119',
    '13324454',
    '13419387',
    '12745583',
    '13462327',
    '13424913',
    '12991489',
    '13374013',
    '12320405',
    '13209044',
    '13433248',
    '12493002',
    '12792772',
    '13347390',
    '13333503',
    '13509500',
    '13408487',
    '13332575',
    '13440585',
    '13531592',
    '13033744',
    '1222739T',
    '13487079',
    '13220247',
    '13440026',
    '13430164',
    '12906460',
    '13138482',
    '1261853T',
    '1287408T',
    '12559357',
    '13491251',
    '12869353',
    '12797995',
    '13358203',
    '12572555',
    '1312063T',
    '13329579',
    '13357298',
    '12598644',
    '13490616',
    '13393800',
    '1269010T',
    '13503717',
    '13172937',
    '1346291T',
    '13484202',
    '12393113',
    '1331634T',
    '13400358',
    '13418107',
    '1177390T',
    '12715086',
    '1336248T',
    '12778277',
    '12797465',
    '13446391',
    '1269643T',
    '12735536',
    '12813585',
    '13327930',
    '13432798',
    '12153189',
    '13420198',
    '12805280',
    '1285134T',
    '1325794T',
    '13420123',
    '13347902',
    '13358261',
    '13435681',
    '13360674',
    '12862740',
    '13291565',
    '13481918',
    '13394947',
    '12515481',
    '13333555',
    '1255436T',
    '12811291',
    '13006297',
    '13273075',
    '13344772',
    '13411258',
    '13425041',
    '12868154',
    '12943683',
    '1314921T',
    '13184408',
    '13211434',
    '13383172',
    '13417588',
    '13458265',
    '13467504',
    '13448345',
    '13540883',
    '11964864',
    '12387730',
    '12899562',
    '13093868',
    '13336046',
    '13413011',
    '13450021',
    '13482081',
    '12519545',
    '13123166',
    '1333430T',
    '13393420',
    '13511406',
    '1296323T',
    '1310693T',
    '1321324T',
    '13336334',
    '13468191',
    '13517097',
    '13525886',
    '13426482',
    '13527132',
    '1276027T',
    '12930114',
    '13012515',
    '13336392',
    '13395829',
    '13434983',
    '13493741',
    '13421149',
    '13385558',
    '12912125',
    '13309964',
    '13393086',
    '12526202',
    '13154919',
    '13155519',
    '13386694',
    '13464132',
    '12870423',
    '13292879',
    '1270263T',
    '12870976',
    '13197770',
    '13423674',
    '1236769T',
    '13391615',
    '13396752',
    '13469113',
    '13361562',
    '13531367',
    '11960903',
    '13199540',
    '13238273',
    '13364404',
    '13517120',
    '1324798T',
    '13448178',
    '13400911',
    '12545747',
    '13398107',
    '12699254',
    '11625259',
    '12563379',
    '12638524',
    '13311968',
    '13502150',
    '13516520',
    '13436943',
    '13408435',
    '13448190',
    '13440677',
    '1347128T',
    '1264155T',
    '13214651',
    '13500224',
    '13295249',
    '12920920',
    '13332477',
    '1344325T',
    '13238371',
    '13373972',
    '13431956',
    '13432308',
    '13511366',
    '13407484',
    '12640816',
    '13427888',
    '13448161',
    '13434827',
    '1348527T',
    '13363015',
    '13454713',
    '1355258T',
    '9500909T',
    '1334230T',
    '13399404',
    '13435600',
    '13154240',
    '13527057',
    '12856055',
    '13548931',
    '12560560',
    '12893779',
    '13159083',
    '13532670',
    '12546508',
    '13209954',
    '13582972',
    '13164119',
    '10125444',
    '13536947',
    '13321306',
    '13611595',
    '13389104',
    '13403673',
    '13466864',
    '12843310',
    '12823637',
    '13560861',
    '13181802',
    '13409133',
    '13333716',
    '13493770',
    '13295278',
    '13423023',
    '10023664',
    '13096440',
    '13382324',
    '13334869',
    '13488278',
    '13249576',
    '13305813',
    '1156678T',
    '12401878',
    '1347109T',
    '12312958',
    '13471676',
    '13395737',
    '13279877',
    '12964733',
    '1354654T',
    '1292483T',
    '13324840',
    '12661757',
    '13429566',
    '12804490',
    '13222259',
    '13484093',
    '13050684',
    '13583186',
    '12765117',
    '13474737',
    '13011754',
    '13485292',
    '12003038',
    '1302891T',
    '13490518',
    '13031127',
    '13445226',
    '12994395',
    '13578777',
    '13270889',
    '1356913T',
    '13449319',
    '12839392',
    '1328695T',
    '13519541',
    '13519132',
    '13250600',
    '13341181',
    '13152936',
    '12290140',
    '12683690',
    '13128274',
    '13126901',
    '1353240T',
    '12325012',
    '13416308',
    '12151851',
    '13382278',
    '12057508',
    '13400519',
    '1287499T',
    '13070322',
    '13429854',
    '13516301',
    '1326093T',
    '13232980',
    '1362708T',
    '12211369',
    '13559007',
    '13192184',
    '13148119',
    '13605002',
    '12719202',
    '12739848',
    '12919873',
    '13308460',
    '13446172',
    '12529131',
    '12744983',
    '13465953',
    '1268165T',
    '13445537',
    '13474708',
    '13418136',
    '12951176',
    '13348018',
    '13400018',
    '12915578',
    '13499282',
    '12884730',
    '13019203',
    '13335481',
    '13380911',
    '13551748',
    '12666986',
    '13252802',
    '13491850',
    '13528089',
    '12742147',
    '13513516',
    '12521198',
    '12845783',
    '13013616',
    '13491176',
    '12678820',
    '13116929',
    '13401252',
    '13492323',
    '13505516',
    '13536573',
    '13554280',
    '12791400',
    '13239915',
    '13325394',
    '12693425',
    '13053313',
    '12876592',
    '13321387',
    '13000480',
    '13325624',
    '13418568',
    '13159221',
    '13365701',
    '13456881',
    '12699778',
    '13093747',
    '13416591',
    '1318788T',
    '13292608',
    '13393351',
    '13414360',
    '13597493',
    '12849064',
    '13342570',
    '12909509',
    '13247489',
    '12706394',
    '13596392',
    '13621411',
    '13352582',
    '13489108',
    '13465279',
    '11762947',
    '13118164',
    '13145438',
    '13548257',
    '13421132',
    '12769343',
    '12793458',
    '13495223',
    '12840865',
    '13286874',
    '13473383',
    '13635234',
    '13386734',
    '12805746',
    '13416815',
    '13437186',
    '1327861T',
    '13409939',
    '12623306',
    '12981644',
    '13594967',
    '13339136',
    '10008039',
    '13378285',
    '13548983',
    '12841160',
    '12665891',
    '13436148',
    '13537806',
    '13515338',
    '12608281',
    '13309872',
    '13312960',
    '13404745',
    '13413996',
    '13428753',
    '13612615',
    '11976646',
    '13344616',
    '1340387T',
    '1306166T',
    '13529576',
    '13575952',
    '13594685',
    '12714486',
    '13481878',
    '13548447',
    '13313957',
    '13500132',
    '13601709',
    '13274458',
    '13465890',
    '13353130',
    '13182598',
    '1347245T',
    '12882453',
    '1154539T',
    '13553449',
    '12834330',
    '13150072',
    '13058191',
    '13155963',
    '13491867',
    '12265062',
    '13385852',
    '13231124',
    '13455503',
    '12748811',
    '13452724',
    '1342258T',
    '13429232',
    '13448996',
    '13298760',
    '13461290',
    '12311039',
    '12716826',
    '12940247',
    '12908092',
    '13018632',
    '13028828',
    '13411045',
    '13628364',
    '13304741',
    '13442355',
    '13442804',
    '13566914',
    '13281069',
    '13315635',
    '13432988',
    '12694889',
    '12819696',
    '12865254',
    '13555790',
    '12825839',
    '13198082',
    '13440337',
    '1349248T',
    '13508917',
    '13554412',
    '1339620T',
    '1258955T',
    '12999318',
    '13291346',
    '13580948',
    '13037895',
    '13298161',
    '13409916',
    '13430285',
    '13434516',
    '12519833',
    '1264038T',
    '12853414',
    '12921128',
    '13417467',
    '1257364T',
    '1282907T',
    '1295768T',
    '1339846T',
    '13462990',
    '12760390',
    '13356329',
    '13356675',
    '13478295',
    '13538061',
    '1300899T',
    '13304326',
    '13399750',
    '13512922',
    '13297906',
    '1343578T',
    '12571143',
    '12985098',
    '13462788',
    '13499852',
    '13298374',
    '13431213',
    '13528567',
    '12342349',
    '13322119',
    '12666698',
    '1273763T',
    '13342535',
    '13553668',
    '13064680',
    '1351350T',
    '12549299',
    '13312925',
    '12270225',
    '13178490',
    '13364646',
    '13470609',
    '13543345',
    '13570821',
    '12497654',
    '13262394',
    '13427479',
    '12654806',
    '13299498',
    '13424176',
    '13544999',
    '12586804',
    '12668353',
    '13473020',
    '13480725',
    '13517667',
    '13709831',
    '13274971',
    '13430947',
    '12821487',
    '12722307',
    '13263126',
    '13472161',
    '13638480',
    '12840738',
    '12514915',
    '12812288',
    '1182543T',
    '12983011',
    '13406141',
    '13111608',
    '13555876',
    '13633533',
    '12680323',
    '12912246',
    '11165223',
    '13553714',
    '12778087',
    '13523010',
    '12737462',
    '13168512',
    '13473475',
    '12171633',
    '1360973T',
    '12620723',
    '13430233',
    '13521522',
    '13544112',
    '1269413T',
    '12808773',
    '12858378',
    '13047210',
    '13066974',
    '13390854',
    '13545340',
    '1301940T',
    '13546809',
    '12718654',
    '12772581',
    '13287981',
    '13312499',
    '12778571',
    '12557800',
    '12591000',
    '11272875',
    '13446068',
    '13484225',
    '12326695',
    '13056173',
    '1335139T',
    '12556048',
    '12984141',
    '13273910',
    '13433398',
    '11738089',
    '12821153',
    '12978199',
    '13234116',
    '12665712',
    '13442390',
    '12920989',
    '13377472',
    '13378734',
    '12523636',
    '12591305',
    '12952179',
    '13293168',
    '13635695',
    '13306281',
    '13310441',
    '12620199',
    '12743012',
    '13060834',
    '1309165T',
    '12917210',
    '12991950',
    '13566102',
    '12550185',
    '12624920',
    '12795067',
    '12868010',
    '12818635',
    '13187297',
    '1332901T',
    '13291450',
    '12787171',
    '12899084',
    '13203722',
    '13429290',
    '12629740',
    '13148252',
    '13548804',
    '12587888',
    '13354559',
    '12756039',
    '1276449T',
    '12794127',
    '13231896',
    '13349989',
    '1213851T',
    '13514928',
    '1286047T',
    '13010906',
    '13574534',
    '13283997',
    '13412780',
    '13619107',
    '13635960',
    '12968302',
    '13317146',
    '13455060',
    '12868730',
    '13333993',
    '13403235',
    '12434146',
    '13242479',
    '13417375',
    '13032516',
    '12511629',
    '12840237',
    '12982964',
    '13493902',
    '13526895',
    '13444298',
    '11508102',
    '12641232',
    '1333946T',
    '11334722',
    '12979951',
    '13387576',
    '13702095',
    '12627549',
    '13378319',
    '13409369',
    '12640373',
    '12919314',
    '13363741',
    '13433231',
    '1333660T',
    '12605916',
    '12649833',
    '12889550',
    '13089103',
    '13390969',
    '10379462',
    '12600169',
    '13458708',
    '12127684',
    '12386047',
    '12617831',
    '12856199',
    '1359351T',
    '12587335',
    '13468104',
    '13504634',
    '12227694',
    '1277641T',
    '1343122T',
    '13521827',
    '13591520',
    '13253425',
    '11884671',
    '12998839',
    '12833298',
    '13264786',
    '13374917',
    '12666208',
    '12624799',
    '12570900',
    '12745030',
    '12864752',
    '1348663T',
    '12768927',
    '13224513',
    '13236399',
    '13350852',
    '12842514',
    '12973287',
    '1242918T',
    '12687466',
    '1283613T',
    '13117915',
    '1334403T',
    '12054856',
    '13405397',
    '12641779',
    '12879895',
    '13050897',
    '13348519',
    '13451600',
    '12494063',
    '12951395',
    '13375419',
    '13536037',
    '13291594',
    '12065658',
    '1284202T',
    '12989018',
    '13407455',
    '1349787T',
    '13440625',
    '13544400',
    '12792288',
    '1305641T',
    '12933072',
    '13663172',
    '12687472',
    '1351267T',
    '12620366',
    '12881283',
    '12992302',
    '13262676',
    '12823107',
    '13058087',
    '13139312',
    '13398672',
    '12847766',
    '13491101',
    '13609366',
    '12507878',
    '12712278',
    '12583985',
    '12790881',
    '13027134',
    '13208369',
    '13535224',
    '12466603',
    '12759279',
    '13312384',
    '13404463',
    '12969501',
    '1343431T',
    '12544018',
    '12779142',
    '12954531',
    '12962335',
    '13453606',
    '13557957',
    '13679675',
    '12755192',
    '13082317',
    '13302562',
    '12558947',
    '12598074',
    '13057809',
    '13683426',
    '12881381',
    '1333867T',
    '13363384',
    '13316598',
    '13609435',
    '1253158T',
    '12728608',
    '13645131',
    '12600739',
    '13459101',
    '1295312T',
    '13490455',
    '13001287',
    '12800926',
    '12909849',
    '13064599',
    '13172753',
    '13371453',
    '1361193T',
    '12996545',
    '13404342',
    '1340485T',
    '1345031T',
    '13240369',
    '13374451',
    '13297699',
    '13651430',
    '13422446',
    '12992285',
    '12155535',
    '12451420',
    '12722549',
    '12631001',
    '13370588',
    '13555496',
    '13230622',
    '13339666',
    '12662708',
    '13310268',
    '12829691',
    '13339879',
    '13382670',
    '13506807',
    '12967725',
    '13344743',
    '13372502',
    '1281373T',
    '13123379',
    '13434107',
    '12869416',
    '13307445',
    '13193135',
    '12791550',
    '13362444',
    '11978324',
    '13358819',
    '13433346',
    '11867380',
    '13162349',
    '1328849T',
    '11539320',
    '12834791',
    '12989312',
    '13524318',
    '13645085',
    '13677778',
    '12659125',
    '12711649',
    '13139427',
    '1327936T',
    '12588966',
    '12638576',
    '12755566',
    '13401776',
    '13544446',
    '13657374',
    '12914022',
    '13170931',
    '13197666',
    '12980508',
    '13376624',
    '12992072',
    '13336455',
    '13569359',
    '13445883',
    '13577590',
    '11202284',
    '12886362',
    '13316454',
    '13041047',
    '12853132',
    '12961050',
    '1362633T',
    '1335124T',
    '13484035',
    '12568153',
    '13303421',
    '12537413',
    '1272168T',
    '12673833',
    '12808082',
    '12990405',
    '13363580',
    '13599038',
    '13614662',
    '12179416',
    '12715748',
    '12374017',
    '12841626',
    '12673620',
    '12746966',
    '13317503',
    '13386861',
    '12577352',
    '13149589',
    '13440251',
    '13405506',
    '13440435',
    '13503677',
    '13492248',
    '12716095',
    '13162614',
    '13334230',
    '1206807T',
    '11927290',
    '1317566T',
    '12977979',
    '13055158',
    '1308116T',
    '1358920T',
    '12557731',
    '12914051',
    '12979473',
    '12789010',
    '13198427',
    '13282556',
    '12716740',
    '13224536',
    '13408625',
    '1332570T',
    '12681021',
    '13731076',
    '12697328',
    '13560671',
    '12300364',
    '12871357',
    '12792023',
    '13441438',
    '12959351',
    '13190552',
    '12983345',
    '12790408',
    '13089593',
    '1342416T',
    '12816174',
    '12950236',
    '13423334',
    '97724450',
    '12294803',
    '12548002',
    '12681764',
    '12751006',
    '12975656',
    '12548751',
    '12758063',
    '13201042',
    '1276988T',
    '13076387',
    '13173791',
    '13329372',
    '13332650',
    '13586558',
    '1368145T',
    '1327070T',
    '13462575',
    '13592304',
    '1298692T',
    '13282591',
    '1328559T',
    '13675985',
    '12561563',
    '1298100T',
    '12735496',
    '12796122',
    '13067539',
    '13397087',
    '13536901',
    '13286845',
    '13529484',
    '13667167',
    '13352121',
    '13603157',
    '12859053',
    '13328432',
    '13404457',
    '13608870',
    '13011656',
    '12699156',
    '13206490',
    '13082110',
    '13578633',
    '12718717',
    '12958394',
    '12960732',
    '13438051',
    '13082219',
    '13423196',
    '98023534',
    '12443777',
    '12829276',
    '13384929',
    '13670186',
    '12914644',
    '13084905',
    '12587053',
    '13419082',
    '12821026',
    '13232162',
    '1363697T',
    '12684802',
    '12726493',
    '13073821',
    '13515632',
    '13646013',
    '13717422',
    '13468202',
    '98615398',
    '13025871',
    '13275818',
    '12808364',
    '13077407',
    '13686608',
    '13367189',
    '98874625',
    '12738868',
    '13285024',
    '13535731',
    '1280343T',
    '12798883',
    '1316785T',
    '12795332',
    '12890257',
    '12932875',
    '95000285',
    '13082640',
    '13319319',
    '13524779',
    '13290153',
    '13560711',
    '12215969',
    '1281256T',
    '13188375',
    '13116394',
    '13209741',
    '13322344',
    '13356894',
    '13528538',
    '13548741',
    '13622731',
    '12750118',
    '13194265',
    '12522685',
    '12692376',
    '12734061',
    '12812524',
    '13454327',
    '12487106',
    '13161409',
    '13298852',
    '13591543',
    '12737796',
    '12811711',
    '1331246T',
    '12703275',
    '1342360T',
    '13431576',
    '13459815',
    '1299070T',
    '12795165',
    '13499898',
    '13588870',
    '12579393',
    '1287254T',
    '13379207',
    '12571172',
    '13549393',
    '13608484',
    '12191496',
    '12687316',
    '12969599',
    '13128343',
    '13254342',
    '13153657',
    '13634778',
    '11946656',
    '12512609',
    '13506024',
    '12835166',
    '13409634',
    '13515091',
    '12543758',
    '13434401',
    '13515868',
    '13543368',
    '12712094',
    '13323664',
    '13419479',
    '13425824',
    '12602832',
    '12805683',
    '13410301',
    '12723420',
    '13348433',
    '13511781',
    '13238526',
    '1329634T',
    '13305433',
    '13306557',
    '13311323',
    '12677546',
    '13358088',
    '13616553',
    '11786759',
    '12179802',
    '12719611',
    '1320411T',
    '13379081',
    '13466449',
    '13784831',
    '13035013',
    '12730578',
    '12611449',
    '12670340',
    '12797851',
    '13024741',
    '13434787',
    '12837316',
    '13438097',
    '13549018',
    '12709098',
    '13276390',
    '13564729',
    '13591860',
    '11520752',
    '12890608',
    '13132428',
    '12014998',
    '1270960T',
    '12712952',
    '12968849',
    '13366480',
    '13398205',
    '13462811',
    '12887169',
    '12833868',
    '13302441',
    '13399652',
    '13433156',
    '13168996',
    '1327469T',
    '13589090',
    '10420959',
    '12607479',
    '13435001',
    '13479275',
    '12214183',
    '12477146',
    '12584821',
    '12951775',
    '13545052',
    '12686313',
    '13394106',
    '12121193',
    '12428509',
    '12858482',
    '10415646',
    '12639084',
    '12968262',
    '13427583',
    '1358705T',
    '13082980',
    '1333498T',
    '12035357',
    '12632822',
    '12839812',
    '13132123',
    '12639556',
    '13289774',
    '13588294',
    '12159323',
    '13119956',
    '13303790',
    '11651421',
    '13134918',
    '13186991',
    '13362692',
    '13565871',
    '12907175',
    '13492346',
    '13525759',
    '12824272',
    '1345317T',
    '13587953',
    '1359385T',
    '13598945',
    '13077908',
    '13142832',
    '13175532',
    '12531515',
    '12921474',
    '13043382',
    '13312862',
    '13370686',
    '13483274',
    '13525108',
    '13608858',
    '12820490',
    '13583710',
    '12492022',
    '13638641',
    '11986848',
    '12825309',
    '11615535',
    '13097224',
    '13242554',
    '13660393',
    '11868636',
    '12605536',
    '12769850',
    '13496877',
    '1174526T',
    '12446746',
    '12971868',
    '13441542',
    '13625343',
    '13647713',
    '12412283',
    '12452763',
    '12901847',
    '13356485',
    '13477787',
    '13700146',
    '12225215',
    '12246415',
    '12591236',
    '13271034',
    '13547818',
    '13594783',
    '11683112',
    '12991754',
    '13038086',
    '13220040',
    '13276038',
    '13308097',
    '13521977',
    '13756536',
    '13211964',
    '13375984',
    '11871557',
    '12587502',
    '1288359T',
    '12956923',
    '13314177',
    '13323036',
    '13403984',
    '11847753',
    '13296097',
    '13528469',
    '13539692',
    '12209964',
    '13028552',
    '1333871T',
    '12680899',
    '12961361',
    '12533510',
    '13231429',
    '13278920',
    '13350915',
    '13382917',
    '13609942',
    '1031057T',
    '10477016',
    '12833281',
    '13078981',
    '13452851',
    '12992227',
    '12737139',
    '12884315',
    '1330427T',
    '13404486',
    '13466962',
    '13665656',
    '13303127',
    '12009218',
    '1316265T',
    '13390140',
    '13518025',
    '11669510',
    '12802685',
    '1340990T',
    '13530773',
    '13640933',
    '13401396',
    '1304317T',
    '13458017',
    '1361291T',
    '12330135',
    '12697340',
    '13333146',
    '12804069',
    '12876839',
    '12931935',
    '13031939',
    '13152562',
    '13353297',
    '1350429T',
    '13523102',
    '13554343',
    '13674481',
    '12467641',
    '13013904',
    '1306475T',
    '13117973',
    '13122785',
    '13134285',
    '13550296',
    '13554700',
    '13236324',
    '13017116',
    '1324493T',
    '13381540',
    '13445704',
    '13630374',
    '1166901T',
    '13143490',
    '13208703',
    '13293928',
    '13371758',
    '1367213T',
    '1181683T',
    '12789557',
    '13146804',
    '13343417',
    '13458138',
    '1312737T',
    '13294085',
    '13342754',
    '12069014',
    '13254555',
    '13288863',
    '13611128',
    '12328471',
    '12685500',
    '12901093',
    '13022124',
    '13368394',
    '13404083',
    '13260071',
    '13284303',
    '1333833T',
    '13446863',
    '13655736',
    '11700834',
    '12430410',
    '12955033',
    '13007093',
    '1316751T',
    '13218099',
    '13237270',
    '13330661',
    '13344927',
    '1338161T',
    '13490138',
    '13510530',
    '12080148',
    '13105217',
    '13192800',
    '13324598',
    '1347784T',
    '13534722',
    '13135576',
    '13458484',
    '13505879',
    '12355929',
    '12664605',
    '12938583',
    '13198358',
    '13389375',
    '13462978',
    '13547611',
    '13673564',
    '12794041',
    '12810529',
    '13372053',
    '1352937T',
    '12497562',
    '12564146',
    '1267907T',
    '12750026',
    '13443836',
    '13488606',
    '13573525',
    '12635002',
    '12978654',
    '12979980',
    '13269341',
    '13394924',
    '12742470',
    '1277189T',
    '1299778T',
    '13283277',
    '13292856',
    '13348180',
    '13489264',
    '13524192',
    '13554936',
    '13583917',
    '13625406',
    '13829289',
    '12455640',
    '12659845',
    '13001016',
    '13146608',
    '13333970',
    '13579187',
    '13679623',
    '11979546',
    '12598500',
    '1346268T',
    '13665944',
    '13683213',
    '13432314',
    '12826710',
    '1328623T',
    '13409450',
    '13492191',
    '11326555',
    '13453514',
    '1348836T',
    '1349640T',
    '13782341',
    '13052609',
    '13059580',
    '13425732',
    '13124561',
    '13299740',
    '13509068',
    '12067774',
    '13289117',
    '13291375',
    '13437693',
    '13221170',
    '13297682',
    '13390249',
    '13437255',
    '13562821',
    '1362113T',
    '1365587T',
    '12671458',
    '13134636',
    '12980059',
    '13185233',
    '13407622',
    '13688027',
    '13221607',
    '13575468',
    '13689566',
    '13000762',
    '12138872',
    '13632069',
    '13652894',
    '13305940',
    '1333603T',
    '13465256',
    '13245828',
    '13650133',
    '13217672')
) as updates;

SELECT p.*
INTO pmf_assignees_20220308_in1174.persons_audit
FROM pmf_assignees_20220308_in1174.persons_updates u
INNER JOIN persons p on p.id = u.person_id;

BEGIN;
UPDATE persons p SET supervisioncaseowner_id = u.expected_value
FROM pmf_assignees_20220308_in1174.persons_updates u
WHERE u.person_id = p.id;
-- Run if counts incorrect
ROLLBACK;
-- Run if counts correct
COMMIT;

-- validation (should be 0)
SELECT caserecnumber, expected_value
FROM pmf_assignees_20220308_in1174.persons_updates
EXCEPT
SELECT p.caserecnumber, p.supervisioncaseowner_id
FROM persons p
INNER JOIN pmf_assignees_20220308_in1174.persons_audit a
ON a.id = p.id;