import psycopg2
from sqlalchemy import create_engine


def get_max_value(table, column, db_config):
    connection_string = db_config["sirius_db_connection_string"]
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()

    query = f"SELECT max({column}) from {db_config['sirius_schema']}.{table};"

    try:
        cursor.execute(query)
        max_id = cursor.fetchall()[0][0]
        if max_id:
            return max_id
        else:
            return 0

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"error: {error}")
        conn.rollback()
        cursor.close()
        return 0


def insert_client_data_into_sirius(db_config, sirius_db_engine):

    case_nos = [
        "94055780",
        "13045198",
        "10243489",
        "1126792T",
        "10215183",
        "10154500",
        "11013596",
        "11553037",
        "11565044",
        "10194709",
        "10034898",
        "11019897",
        "10202386",
        "13611831",
        "13263316",
        "11760532",
        "10084054",
        "1001404T",
        "10152488",
        "10211717",
        "10027550",
        "10020983",
        "94031196",
        "10134672",
        "11034030",
        "94041801",
        "10332461",
        "11499503",
        "10058508",
        "10469863",
        "95010297",
        "10019377",
        "94026637",
        "1030841T",
        "10295930",
        "10192899",
        "11503075",
        "10095259",
        "10228043",
        "10013617",
        "10076307",
        "94029318",
        "1002065T",
        "13034690",
        "95101131",
        "98220297",
        "10065632",
        "1029931T",
        "94078554",
        "10199092",
        "13305888",
        "10058589",
        "13157543",
        "10023664",
        "10016235",
        "10078014",
        "97901626",
        "10024391",
        "94024510",
        "11276657",
        "12779384",
        "11462975",
        "10238118",
        "10233327",
        "12232172",
        "10085368",
        "10353966",
        "10270815",
        "13420388",
        "10077535",
        "12141476",
        "13559860",
        "10403484",
        "10004741",
        "13572067",
        "10033837",
        "13506940",
        "10004188",
        "11267055",
        "11233248",
        "10051890",
        "10117542",
        "10062185",
        "12693483",
        "1268922T",
        "94041104",
        "10140700",
        "11256558",
        "94001471",
        "10468917",
        "11444871",
        "13409133",
        "10441883",
        "13560636",
        "95014298",
        "10264165",
        "10349339",
        "94076375",
        "12422681",
        "10086803",
        "10139181",
        "1005934T",
        "12855789",
        "12716400",
        "11092050",
        "10274494",
        "10002625",
        "11546432",
        "11501823",
        "10285929",
        "10045118",
        "10322725",
        "10159625",
        "10456381",
        "11291942",
        "10056865",
        "10302350",
        "11854986",
        "13384618",
        "10222865",
        "10114544",
        "11745967",
        "13518100",
        "1216808T",
        "13611727",
        "95050777",
        "10183078",
        "13611825",
        "99314363",
        "13571726",
        "10201705",
        "95053648",
        "1361174T",
        "11441562",
        "10005928",
        "10040074",
        "1028453T",
        "10087046",
        "10080306",
        "10056957",
        "10429544",
        "10042691",
        "94036528",
        "13611917",
        "11447460",
        "13500437",
        "10082629",
        "95089035",
        "13404388",
        "10021220",
        "9404438T",
        "11087791",
        "10337914",
        "13611704",
        "97520164",
        "10118539",
        "94036868",
        "95062876",
        "13570994",
        "10118706",
        "10045717",
        "13561524",
        "10160367",
        "10004038",
        "10133847",
        "11540897",
        "10332236",
        "95032391",
        "11377313",
        "10181803",
        "94007582",
        "10094976",
        "1148778T",
        "10319067",
        "10164178",
        "10012240",
        "10001668",
        "13419744",
        "12704013",
        "10423836",
        "11545786",
        "10198244",
        "94000738",
        "10033048",
        "13233643",
        "11138571",
        "10009307",
        "13258619",
        "94044718",
        "10117594",
        "10101102",
        "1025051T",
        "10131668",
        "13480535",
        "10424217",
        "10050276",
        "94034453",
        "13547686",
        "10245530",
        "13448593",
        "13280481",
        "98141395",
        "10305935",
        "10072905",
        "10106095",
        "10149878",
        "10065010",
        "11866428",
        "11443384",
        "1280494T",
        "10231275",
        "94017513",
        "10382256",
        "9404167T",
        "10005243",
        "13546798",
        "1020512T",
        "98036901",
        "96400946",
        "12269247",
        "10108700",
        "12488795",
        "11309454",
        "10138517",
        "13262336",
        "12454585",
        "95708936",
        "10373495",
        "13397421",
        "1143836T",
        "10153802",
        "10018593",
        "10068267",
        "11526707",
        "94044586",
        "13568016",
        "10000037",
        "97830937",
        "10138460",
        "10029602",
        "11522637",
        "10041912",
        "10020597",
        "11757882",
        "13174794",
        "10007877",
        "10138356",
        "10075794",
        "10026374",
        "10004879",
        "95000400",
        "10055666",
        "11321977",
        "11484153",
        "11472336",
        "98123544",
        "10013116",
        "10334473",
        "9803605T",
        "12244697",
        "11615725",
        "13524445",
        "10337505",
        "10063257",
        "13612650",
        "10456162",
        "10101321",
        "94012175",
        "10248787",
        "1030875T",
        "13611779",
        "10131138",
        "10044553",
        "94041225",
        "94056875",
        "12080655",
        "12784311",
        "10460725",
        "10352773",
        "10075892",
        "1035651T",
        "1148646T",
        "11029206",
        "9400971T",
        "12622608",
        "10461498",
        "10014200",
        "10164149",
        "10200679",
        "10045441",
        "13538619",
        "11886585",
        "10041221",
        "94029163",
        "10315141",
        "10156034",
        "10020418",
        "11781162",
        "1008006T",
        "94074985",
        "10015094",
        "1002818T",
        "10389088",
        "13561639",
        "95046778",
        "13572856",
        "10002199",
        "94035617",
        "11504372",
        "13082997",
        "11467743",
        "10072053",
        "9401326T",
        "95006822",
        "1014265T",
        "13612638",
        "13481135",
        "10129802",
        "10259249",
        "11492297",
        "10135341",
        "13410324",
        "13218462",
        "10033653",
        "99328514",
        "10065868",
        "11583718",
        "10246308",
        "10065004",
        "13611791",
        "1351233T",
        "10397831",
        "12709910",
        "9400409T",
        "10317585",
        "11479865",
        "10088470",
        "94026142",
        "13456190",
        "94032199",
        "13526405",
        "12417667",
        "10058071",
        "10482836",
        "9820277T",
        "13571974",
        "10052501",
        "13493919",
        "10071240",
        "13612575",
        "11527215",
        "11508154",
        "13538591",
        "12936323",
        "10054300",
        "12575599",
        "10164063",
        "10013560",
        "94051698",
        "10055096",
        "94037589",
        "13565957",
        "11563314",
        "94071048",
        "10454979",
        "94004169",
        "10018420",
        "13548551",
        "10072652",
        "13399214",
        "13522329",
        "11469818",
        "13581220",
        "13611785",
        "11466008",
        "10102566",
        "10362036",
        "95056617",
        "13572211",
        "11577229",
        "11245975",
        "11485012",
        "13612598",
        "10037026",
        "10292742",
        "13560918",
        "13611762",
        "10201193",
        "10132683",
        "10208946",
        "98239268",
        "11068361",
        "13547801",
        "10461469",
        "10078498",
        "10235783",
        "11063558",
        "13448996",
        "10001403",
        "1034037T",
        "10141202",
        "10033561",
        "94064587",
        "10293987",
        "11471903",
        "10233264",
        "10154051",
        "13546936",
        "10005237",
        "11348643",
        "10023226",
        "94029762",
        "12670887",
        "10185735",
        "98312347",
        "11503933",
        "12797033",
        "11698923",
        "13487465",
        "94078030",
        "10162667",
        "13556332",
        "95054248",
        "13044788",
        "94033571",
        "12777510",
        "13570660",
        "11623351",
        "10109755",
        "10093996",
        "12668301",
        "9509575T",
        "13612581",
        "1119959T",
        "11517353",
        "10086377",
        "1015099T",
        "13273645",
        "11482855",
        "11308641",
        "9851336T",
        "94003667",
        "12808842",
        "10015105",
        "10384821",
        "1015355T",
        "13526774",
        "94042580",
        "12882401",
        "95064335",
        "13527247",
        "12217002",
        "10044150",
        "1294953T",
        "11536092",
        "11466210",
        "97200058",
        "11609075",
        "10042817",
        "12795770",
        "13503032",
        "94019859",
        "10181930",
        "1030110T",
        "94021339",
        "12986199",
        "13511527",
        "12768927",
        "95032638",
        "11153838",
        "94033219",
        "10142729",
        "1010391T",
        "10087207",
        "13493983",
        "10324484",
        "12704474",
        "13402508",
        "11490233",
        "10044547",
        "10029245",
        "10297297",
        "11245969",
        "11472365",
        "10277117",
        "10152868",
        "13573295",
        "13110922",
        "10058917",
        "10035164",
        "10369939",
        "12319047",
        "10465735",
        "94061819",
        "10288046",
        "11956501",
        "95095697",
        "11329259",
        "11283988",
        "10089346",
        "13572764",
        "11530107",
        "10447959",
        "11560126",
        "10486336",
        "10028288",
        "10207131",
        "13560544",
        "13539594",
        "10064669",
        "11503864",
        "10200685",
        "10142194",
        "95049033",
        "1003019T",
        "10009526",
        "94007697",
        "13323382",
        "11203189",
        "11497854",
        "11084211",
        "10051538",
        "10200748",
        "10038450",
        "10335568",
        "10297660",
        "10056410",
        "13567497",
        "11558554",
        "10242970",
        "94000393",
        "13260762",
        "1346927T",
        "94017507",
        "13578754",
        "12885508",
        "96505010",
        "1004731T",
        "13562090",
        "10254942",
        "95018760",
        "10433249",
        "94016032",
        "10151208",
        "1288073T",
        "13573410",
        "12878552",
        "10264188",
        "11511639",
        "12021200",
        "10123455",
        "13509840",
        "10016431",
        "11452329",
        "10102658",
        "10007261",
        "11584474",
        "11336129",
        "10008713",
        "10088090",
        "10029556",
        "11798910",
        "11131468",
        "10034558",
        "1143889T",
        "1002630T",
        "13611802",
        "10409497",
        "94090910",
        "10126044",
        "10011951",
        "11345121",
        "10156656",
        "10072180",
        "1048587T",
        "10158403",
        "94082311",
        "12566705",
        "10007163",
        "11183886",
        "1327533T",
        "1345321T",
        "11084044",
        "95096988",
        "10134292",
        "10131979",
        "10070980",
        "10209045",
        "1016562T",
        "97820067",
        "1330853T",
        "10287383",
        "94016314",
        "95049684",
        "94023680",
        "97432184",
        "13611756",
        "10099491",
        "10340294",
        "97626072",
        "10023877",
        "10080698",
        "10081436",
        "10048151",
        "11501420",
        "13547559",
        "11505899",
        "9500122T",
        "10206404",
        "10420959",
        "95046732",
        "10077702",
        "13496762",
        "1155000T",
        "10092221",
        "13567819",
        "11790827",
        "1194777T",
        "1285669T",
        "13612621",
        "94020895",
        "13195959",
        "11474279",
        "11219796",
        "10273905",
        "10232094",
        "10043855",
        "94044102",
        "11223576",
        "94013627",
        "1339115T",
        "11957337",
        "10056335",
        "1003061T",
        "10077466",
        "10114901",
        "1011017T",
        "10060501",
        "10036052",
        "10241932",
        "10062191",
        "94047244",
        "11784511",
        "10017181",
        "10336709",
        "1014133T",
        "9833009T",
        "10303376",
        "11325016",
        "13612644",
        "11452767",
        "12006612",
        "10053032",
        "10025768",
        "98013349",
        "13318495",
        "94058138",
        "10069846",
        "13538372",
        "12120852",
        "11317742",
        "13572165",
        "13058640",
        "13570896",
        "1034930T",
        "12304250",
        "10020349",
        "10033250",
        "10320788",
        "10248689",
        "10076428",
        "12925832",
        "10141254",
        "10094354",
        "10010274",
        "12506230",
        "10052743",
        "13392486",
        "13131258",
        "11102602",
        "94004780",
        "12022071",
        "1032923T",
        "11149177",
        "12233313",
        "10064295",
        "95110088",
        "10122279",
        "10301750",
        "10442189",
        "10106020",
        "11521916",
        "13612609",
        "13526463",
        "97111265",
        "95907481",
        "12322901",
        "11550270",
        "12839812",
        "13612615",
        "10182311",
        "10024500",
        "10146500",
        "12898213",
        "12069348",
        "10081321",
        "10029084",
        "94079655",
        "10053746",
        "10096406",
        "10245576",
        "97532758",
        "95095271",
        "94031017",
        "94035842",
        "10370284",
        "94032032",
        "10057661",
        "10004257",
        "95053308",
        "10004263",
        "12515538",
        "13562654",
        "94031806",
        "94036511",
        "11100423",
        "13611848",
        "11056262",
        "10027832",
        "10139342",
        "10108458",
        "10034253",
        "95054605",
        "9500544T",
        "11569195",
        "10309533",
        "10107023",
        "10184300",
        "10029078",
        "11617864",
        "13568114",
        "11112194",
        "10040794",
        "11251502",
        "10154097",
        "10192916",
        "13411120",
        "13076410",
        "12509308",
        "94079626",
        "13140618",
        "11508534",
        "13611819",
        "10363460",
        "9407151T",
        "10160897",
        "10221960",
        "11214849",
        "13432648",
        "1156889T",
        "11488465",
        "9916269T",
        "10272741",
        "13571496",
        "95073534",
        "10016667",
        "10042909",
        "10320955",
        "13498215",
        "10028340",
        "12441454",
        "13272728",
        "10063614",
        "12952628",
        "95050028",
        "10048168",
        "10006413",
        "11661807",
        "11500820",
        "11291268",
        "10108815",
        "10087622",
        "13420267",
        "10244918",
        "10250601",
        "10080773",
        "10004637",
        "13417375",
        "10013583",
        "9504667T",
        "10373086",
        "10075788",
        "10023480",
        "94040677",
        "13442384",
        "10213228",
        "13193711",
        "10057995",
        "95107490",
        "10067863",
        "1007165T",
        "12455323",
        "94028799",
        "94034044",
        "12500332",
        "10097922",
        "11259389",
        "10254153",
        "10087121",
        "10255421",
        "13465498",
        "1041194T",
        "97624336",
        "1129192T",
        "11522643",
        "11488252",
        "13568552",
        "13198030",
        "10030816",
        "10381719",
        "13137156",
        "12886984",
        "95035544",
        "10367766",
        "10000884",
        "11482204",
        "10106665",
        "10494872",
        "96300648",
        "10255945",
        "10125087",
        "10031042",
        "10016195",
        "13611854",
        "95088769",
        "95030119",
        "10046369",
        "10090923",
        "1033889T",
        "12670530",
        "10447090",
        "13611710",
        "10021744",
        "13558995",
        "95065851",
        "10076618",
        "10456156",
        "94074213",
        "12912465",
        "10050512",
        "11742249",
        "13465129",
        "13611860",
        "11001537",
        "13569866",
        "10318726",
        "10135295",
        "1202119T",
        "11614970",
        "12725150",
        "10093529",
        "1356793T",
        "12844958",
        "13259818",
        "12173962",
        "10087392",
        "10012643",
        "11466112",
        "13612552",
        "10236953",
        "10058140",
        "10003409",
        "10149066",
        "10025751",
        "10455268",
        "13093845",
        "13612569",
        "10053723",
        "10410786",
        "10030868",
        "94087154",
        "94020031",
        "11314744",
        "10043164",
        "13402641",
        "13474979",
        "9402145T",
        "1277117T",
        "10214940",
        "13570798",
        "13611733",
        "10132222",
        "10153255",
        "12485221",
        "11021106",
        "1006312T",
        "1104342T",
        "11356568",
        "94029226",
        "10160966",
        "10099894",
        "10426794",
        "10090422",
        "10439199",
        "10484543",
        "10109006",
        "10090969",
        "10080842",
        "10142038",
        "94026885",
        "10072548",
        "10023232",
        "11717534",
        "10126234",
        "11166595",
        "1023217T",
        "10039522",
        "95017676",
        "13544204",
        "10204496",
        "10159936",
        "11844790",
        "11636695",
        "94039929",
        "13583192",
        "10241990",
        "12379718",
        "1007033T",
        "10025630",
        "13567376",
        "11452168",
        "13404808",
        "13006913",
        "10016621",
        "10325700",
        "10346606",
        "97009936",
        "10097012",
        "94029255",
        "13391270",
        "12197359",
        "13528607",
        "10256741",
        "10356768",
        "9511251T",
        "10297913",
        "10114095",
        "10445671",
        "10082290",
        "10243443",
        "95028213",
        "1128889T",
        "9510511T",
        "10415698",
        "11247745",
        "10264522",
        "10142856",
        "10160321",
        "10105028",
        "94009939",
        "1024055T",
        "11433199",
        "94012682",
        "10041002",
        "10166328",
        "99262664",
        "12308798",
        "13482478",
        "13573715",
        "95000256",
        "10126597",
        "13005455",
        "13400122",
        "10327234",
        "12624632",
        "12768501",
        "10214807",
        "1011850T",
        "94036747",
        "94006227",
        "11214567",
        "95072099",
        "12826975",
        "12693356",
        "10072617",
        "10216508",
        "95002441",
        "10437636",
        "10006315",
        "10143894",
        "98624482",
        "10140913",
        "10071919",
        "10005433",
        "10023301",
        "10434477",
        "13546297",
        "1021075T",
        "10015981",
        "13554746",
    ]
    id = get_max_value(table="persons", column="id", db_config=db_config)
    uid = get_max_value(table="persons", column="uid", db_config=db_config)

    insert_statement = """
        INSERT INTO public.persons (
            id,
            caserecnumber,
            firstname,
            surname,
            correspondencebypost,
            correspondencebyphone,
            correspondencebywelsh,
            correspondencebyemail,
            uid,
            type,
            clientsource
        )
        VALUES
    """
    for i, case_no in enumerate(case_nos):
        insert_statement += f"""
            (
                {id + 1 + i},
                '{case_no}',
                'FIRSTNAME',
                'SURNAME',
                false,
                false,
                false,
                false,
                {uid+1+i},
                'actor_client',
                'SKELETON'
            )
        """
        if i + 1 == len(case_nos):
            insert_statement += ";"
        else:
            insert_statement += ","

    sirius_db_engine.execute(insert_statement)


def insert_client_address_data_into_sirius(db_config, sirius_db_engine):
    id = get_max_value(table="addresses", column="id", db_config=db_config)

    insert_statement = f"""
        INSERT INTO addresses (id, person_id, town)
        SELECT
            row_number() over () + {id} as id,
            id as person_id,
            'EXISTING DATA'
        from persons where clientsource = 'SKELETON';
    """
    sirius_db_engine.execute(insert_statement)


def insert_finance_person_data_into_sirius(db_config, sirius_db_engine):
    id = get_max_value(table="finance_person", column="id", db_config=db_config)

    # Create a finance person for each person.
    # Intentionally skip creating a finance person for person ID 520, to ensure that finance
    # entities are still being migrated correctly even if there is no finance person to link them to.
    insert_statement = f"""
        INSERT INTO finance_person (id, person_id, finance_billing_reference, payment_method)
        SELECT
            row_number() over () + {id} as id,
            id as person_id,
            row_number() over () + 990000 as finance_billing_reference,
            'DEMANDED'
        from persons where clientsource = 'SKELETON' and id <> 520;
    """
    sirius_db_engine.execute(insert_statement)


def create_batch_number_counter_in_sirius(db_config, sirius_db_engine):
    # Create the counter if it doesn't exist
    insert_statement = f"""
        INSERT INTO finance_counter (id, key, counter)
        SELECT nextval('finance_counter_id_seq'), 'DatFileBatchNumberReportBatchNumber', 0
        WHERE NOT EXISTS (SELECT 1 FROM finance_counter WHERE key = 'DatFileBatchNumberReportBatchNumber');
    """
    sirius_db_engine.execute(insert_statement)


def insert_skeleton_data(db_config):
    sirius_db_engine = create_engine(db_config["sirius_db_connection_string"])

    insert_client_data_into_sirius(db_config, sirius_db_engine)
    insert_finance_person_data_into_sirius(db_config, sirius_db_engine)
    create_batch_number_counter_in_sirius(db_config, sirius_db_engine)
    # insert_client_address_data_into_sirius(db_config, sirius_db_engine)
