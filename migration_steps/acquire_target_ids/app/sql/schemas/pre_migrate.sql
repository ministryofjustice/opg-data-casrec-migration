--
-- PostgreSQL database dump
--

-- Dumped from database version 10.11 (Debian 10.11-1.pgdg90+1)
-- Dumped by pg_dump version 11.9 (Debian 11.9-0+deb10u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pre_migrate; Type: SCHEMA; Schema: -; Owner: casrec
--

DROP SCHEMA IF EXISTS pre_migrate CASCADE; CREATE SCHEMA pre_migrate;


ALTER SCHEMA pre_migrate OWNER TO casrec;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: addresses; Type: TABLE; Schema: pre_migrate; Owner: casrec
--

CREATE TABLE pre_migrate.addresses (
    id integer,
    town text,
    county text,
    postcode text,
    country text,
    c_case text,
    address_lines text,
    isairmailrequired text,
    type text,
    caserecnumber text,
    person_id text
);


ALTER TABLE pre_migrate.addresses OWNER TO casrec;

--
-- Name: persons; Type: TABLE; Schema: pre_migrate; Owner: casrec
--

CREATE TABLE pre_migrate.persons (
    id integer,
    dob text,
    salutation text,
    firstname text,
    middlenames text,
    surname text,
    createddate text,
    previousnames text,
    caserecnumber text,
    clientaccommodation text,
    maritalstatus text,
    countryofresidence text,
    type text,
    systemstatus text,
    isreplacementattorney text,
    istrustcorporation text,
    clientstatus text,
    statusdate text,
    correspondencebywelsh text,
    newsletter text,
    specialcorrespondencerequirements_audiotape text,
    specialcorrespondencerequirements_largeprint text,
    specialcorrespondencerequirements_hearingimpaired text,
    specialcorrespondencerequirements_spellingofnamerequirescare text,
    digital text,
    isorganisation text,
    casesmanagedashybrid text,
    supervisioncaseowner_id text,
    clientsource text,
    updateddate text
);


ALTER TABLE pre_migrate.persons OWNER TO casrec;

--
-- Name: phonenumbers; Type: TABLE; Schema: pre_migrate; Owner: casrec
--

CREATE TABLE pre_migrate.phonenumbers (
    id integer,
    phone_number text,
    c_case text,
    type text,
    is_default text,
    updateddate text,
    caserecnumber text,
    person_id text
);


ALTER TABLE pre_migrate.phonenumbers OWNER TO casrec;

--
-- Data for Name: addresses; Type: TABLE DATA; Schema: pre_migrate; Owner: casrec
--

COPY pre_migrate.addresses (id, town, county, postcode, country, c_case, address_lines, isairmailrequired, type, caserecnumber, person_id) FROM stdin;
1	E1 5ST		YO99 7DU		10000037	["803 Gough turnpike", "Port Sally"]	False	Primary	10000037	1
2	N7 4DS		DT4H 5DN		10000884	["40 Leonard stravenue", "Shanetown"]	False	Primary	10000884	2
3	Lauraborough	W6 2AG	E34 1NN		10001403	["Flat 61", "Page cliff"]	False	Primary	10001403	3
4	Jonesland	JE93 8LU	KA9B 3JW		10001668	["Flat 22", "Palmer islands"]	False	Primary	10001668	4
5	S6T 4LY		KY80 6UH		10002199	["35 Sylvia vista", "East Ellie"]	False	Primary	10002199	5
6	Huntburgh	M56 2BE	N08 2UJ		10002625	["Flat 02E", "Shannon tunnel"]	False	Primary	10002625	6
7	W7 7SS		ST2X 2JZ		10003409	["69 Williams loop", "Bevanland"]	False	Primary	10003409	7
8	M4 6FJ		B0D 7DR		10004038	["9 O'Neill row", "Naomiborough"]	False	Primary	10004038	8
9	South Peter	TD1A 6QX	B5 7SR		10004188	["Studio 80", "Yvonne landing"]	False	Primary	10004188	9
10	B6A 4JG		DH5 5YD		10004257	["43 Paul islands", "Porterton"]	False	Primary	10004257	10
11	N7K 1RD		HP32 6YX		10004263	["21 Clarke inlet", "South Sian"]	False	Primary	10004263	11
12	Lake Gillianchester	GL63 2UP	B6D 4ZF		10004637	["Flat 7", "Graeme branch"]	False	Primary	10004637	12
13	NR40 3FE		WN8Y 4YH		10004741	["85 Barnett grove", "Lake Simonville"]	False	Primary	10004741	13
14	Allanville	W6 7LY	SM1 7TN		10004879	["Studio 5", "Ali crest"]	False	Primary	10004879	14
15	TW7R 3NZ		TA51 4EE		10005237	["83 Nicholas flats", "Christinetown"]	False	Primary	10005237	15
16	Christiantown	E43 6YQ	N9C 4UR		10005243	["Studio 6", "Jones oval"]	True	Primary	10005243	16
17	Beverleyberg	L4C 0QG	G2A 3AU		10005433	["Flat 0", "Carpenter wells"]	False	Primary	10005433	17
18	SE4 4BE		W20 7FT		10005928	["5 Wayne ports", "Lake Stevenland"]	False	Primary	10005928	18
19	Connorchester	IV6 8LW	E4 7ET		10006315	["Studio 8", "Wood stream"]	False	Primary	10006315	19
20	Lake Markmouth	G63 3DR	B4K 2RB		10006413	["Flat 10Y", "Margaret stream"]	False	Primary	10006413	20
21	B8 2JE		N0 3YH		10007163	["178 Curtis corner", "Alanstad"]	False	Primary	10007163	21
22	WF8 3NT		B0 5WH		10007261	["97 Morris junctions", "Edwardsmouth"]	False	Primary	10007261	22
23	Lisastad	LN5M 5YL	B6T 8RP		10007877	["Flat 1", "Williams spring"]	False	Primary	10007877	23
24	G0 9AU		W1C 7FL		10008713	["300 Wood cliffs", "North Melissa"]	False	Primary	10008713	24
25	PH9Y 0TG		W92 6EJ		10009307	["9 Toby forest", "Bensonbury"]	False	Primary	10009307	25
26	TS2 1UD		G3 3DP		10009526	["96 Charlotte shores", "Singhburgh"]	False	Primary	10009526	26
27	S7 6NL		G1K 8LJ		10010274	["297 Bruce lights", "Lake Mohammedstad"]	False	Primary	10010274	27
28	M53 3EF		SL9 6SR		10011951	["0 Linda court", "Tonyville"]	False	Primary	10011951	28
29	Alexandraberg	W9 5SG	SG89 8NJ		10012240	["Studio 01", "Jarvis wells"]	False	Primary	10012240	29
30	E1 0HQ		CT9 4US		10012643	["617 Stephanie ports", "Huntside"]	False	Primary	10012643	30
31	Lindseychester	WF88 8UX	S9J 7TD		10013116	["Flat 49U", "Scott view"]	False	Primary	10013116	31
32	Port Lyndaview	PH0 2HQ	N3G 0XR		10013560	["Studio 55", "Roy lane"]	False	Primary	10013560	32
33	M54 4AR		KW7 0TF		10013583	["723 Marion radial", "Glennmouth"]	False	Primary	10013583	33
34	South Andrea	M76 2UZ	W8S 4DB		10013617	["Studio 92", "Molly rapids"]	False	Primary	10013617	34
35	TD5M 5EJ		L68 7US		1001404T	["7 Khan stream", "Carrollborough"]	False	Primary	1001404T	35
36	New Jennifer	E8 9WN	BA54 8US		10014200	["Studio 04", "Williams cape"]	True	Primary	10014200	36
37	G7D 2TA		GU5 7UA		10015094	["29 Damian bridge", "Gilliantown"]	False	Primary	10015094	37
38	East Mark	BA36 3UF	E5 9NF		10015105	["Studio 63", "Cooke ferry"]	False	Primary	10015105	38
39	Amberburgh	CV2 6DP	RG2H 7TU		10015981	["Flat 96", "Hayes orchard"]	False	Primary	10015981	39
40	Port Joelview	WA51 8LD	E77 5SX		10016195	["Studio 08", "Jones island"]	False	Primary	10016195	40
41	Carolehaven	S84 6GN	M95 0ZP		10016235	["Studio 13d", "Baxter drive"]	False	Primary	10016235	41
42	Port Gillian	CW4 6SZ	SO89 5HS		10016431	["Flat 48I", "Lewis grove"]	False	Primary	10016431	42
43	E8 1NX		DA78 3YE		10016621	["8 Andrea isle", "West Rosie"]	False	Primary	10016621	43
44	Sandersland	L0 4NE	CB5V 6SP		10016667	["Studio 6", "Gail mount"]	False	Primary	10016667	44
45	N5A 5UU		B7 1XL		10017181	["527 Farrell passage", "West Seanmouth"]	False	Primary	10017181	45
46	W62 6LS		S6 0QD		10018420	["792 Kate course", "Parkesport"]	False	Primary	10018420	46
47	WV29 4FX		LS28 7ZG		10018593	["73 Stewart rue", "East Lewisfort"]	False	Primary	10018593	47
48	HG9 1AT		W64 8YB		10019377	["8 Josh mountain", "East Marian"]	False	Primary	10019377	48
49	SW1E 5HP		W0 7WU		10020349	["40 Lewis center", "Jacksonbury"]	False	Primary	10020349	49
50	Justintown	E0W 8UL	E7B 5AW		10020418	["Studio 08", "Gregory hills"]	False	Primary	10020418	50
51	Georginaborough	E82 2DB	KW6 4YY		10020597	["Flat 0", "Johnston ville"]	False	Primary	10020597	51
52	North Andreastad	N72 8BE	PR56 1TT		1002065T	["Studio 2", "Mary pike"]	False	Primary	1002065T	52
53	Dannymouth	RM46 6RZ	TA2 1LD		10020983	["Studio 2", "Coleman crescent"]	False	Primary	10020983	53
54	BL9V 2DJ		B26 2FZ		10021220	["4 Dodd inlet", "Suttonland"]	False	Primary	10021220	54
55	LL0Y 4AR		N7F 5PS		10021744	["43 Kerry mall", "East Phillipport"]	False	Primary	10021744	55
56	ME8M 0DN		CA4 1FN		10023226	["85 Lewis wells", "South Keith"]	False	Primary	10023226	56
57	BS93 7XT		G7 7WN		10023232	["711 Joshua manor", "South Barryhaven"]	False	Primary	10023232	57
58	B5 9EW		L32 4DA		10023301	["06 Aimee mountain", "Lake Rhyshaven"]	False	Primary	10023301	58
59	Forsterborough	DY2 1ZR	BS70 9XF		10023480	["Flat 16", "Stevenson camp"]	False	Primary	10023480	59
60	Lake Molly	NN2 9QL	FK80 0JB		10023664	["Flat 4", "Aimee passage"]	False	Primary	10023664	60
61	HD6B 1UF		L4H 5UT		10023877	["548 Wright forest", "South Kennethfort"]	False	Primary	10023877	61
62	Bethanhaven	G0S 0GN	N5A 8GH		10024391	["Studio 9", "Julie glen"]	False	Primary	10024391	62
63	Abbiemouth	G9 1PS	PL0V 9DU		10024500	["Studio 55", "Brown locks"]	False	Primary	10024500	63
64	Joyceville	B23 7TH	L3 1UB		13611727	["Flat 7", "Tom knolls"]	False	Primary	13611727	64
65	Pughhaven	L6 7DU	TS6N 0JQ		10025630	["Studio 87B", "Jeffrey rest"]	False	Primary	10025630	65
66	NP6Y 6EJ		NE3V 8GD		10025751	["7 Christine point", "West Melissa"]	False	Primary	10025751	66
67	W65 6RW		PO4M 9TP		10025768	["4 Matthew radial", "North Danny"]	False	Primary	10025768	67
68	TA4M 0LP		W96 9SQ		1002630T	["062 Taylor village", "Leahfurt"]	False	Primary	1002630T	68
69	West Sian	L2 4NG	E36 6EQ		10026374	["Studio 6", "Noble curve"]	False	Primary	10026374	69
70	S30 9FZ		L5W 6QJ		10027550	["39 Eric way", "Morrisbury"]	False	Primary	10027550	70
71	LN3 2GQ		B1J 6UT		10027832	["698 Jackson viaduct", "Port Katiestad"]	False	Primary	10027832	71
72	AB0 9RA		B26 3EN		1002818T	["15 Hughes extension", "Jamestown"]	False	Primary	1002818T	72
73	Junehaven	E6 3FS	S8 2HD		10028288	["Studio 97", "Geraldine trail"]	False	Primary	10028288	73
74	Fionaview	DE2R 3TE	E3C 1SL		10028340	["Flat 22", "Payne crossing"]	False	Primary	10028340	74
75	M19 6FS		DG6N 7BY		10029078	["3 Kim squares", "South Stephen"]	False	Primary	10029078	75
76	East Dominicbury	N65 4AD	FY0Y 6PQ		10029084	["Flat 5", "Daniel branch"]	False	Primary	10029084	76
77	Buckleyburgh	WA8 2WP	W9 8RB		10029245	["Flat 5", "Green lodge"]	False	Primary	10029245	77
78	Port Jemma	CA9W 5GP	S9T 7DP		10029556	["Studio 65X", "Boyle court"]	False	Primary	10029556	78
79	E7 3DU		G6W 7FZ		10029602	["4 Taylor glen", "Port Jason"]	False	Primary	10029602	79
80	Maureenmouth	LD17 7YT	JE49 2YX		1003019T	["Flat 8", "Coates place"]	False	Primary	1003019T	80
81	BD5R 5NS		DA9 5RE		1003061T	["09 Patrick throughway", "Humphreysberg"]	False	Primary	1003061T	81
82	Jordanland	S8A 2TA	CB9H 4ZP		10030816	["Flat 67", "Alan fork"]	False	Primary	10030816	82
83	Harryview	AL93 0SL	B4B 7LY		10030868	["Studio 21", "Lorraine streets"]	False	Primary	10030868	83
84	AB97 5HR		W7K 8HD		10031042	["1 Judith rest", "South Thomas"]	False	Primary	10031042	84
85	E8 9HZ		LU24 8WY		10033048	["4 Harris overpass", "New Abigailchester"]	False	Primary	10033048	85
86	WF4X 0SS		SN6 2EU		10033250	["943 Gill landing", "Lake Bernard"]	False	Primary	10033250	86
87	West Hannah	M7 9LA	DD4B 8LG		10033561	["Studio 57y", "Reece hill"]	False	Primary	10033561	87
88	Craigberg	E5E 0TT	S1 5DL		10033653	["Flat 45", "Luke trail"]	False	Primary	10033653	88
89	South Denistown	M3 4XR	WF0 1FD		10033837	["Studio 35", "Julian port"]	False	Primary	10033837	89
90	Aliside	G67 8BW	LA4 7EF		10034253	["Studio 63a", "Lisa knoll"]	False	Primary	10034253	90
91	West Teresaville	L91 6UB	W53 5ZN		10034558	["Studio 56z", "Ward mission"]	False	Primary	10034558	91
92	W0D 9YT		TF70 7HD		10034898	["47 Holmes prairie", "West Rickyshire"]	False	Primary	10034898	92
93	Jadeport	LA69 3LX	E8D 5BH		10035164	["Studio 63B", "Joan spring"]	False	Primary	10035164	93
94	New Abbieside	WC50 1BE	L24 3ZE		10036052	["Studio 03N", "Griffiths shoal"]	False	Primary	10036052	94
95	EC9E 7NA		KW7 2UD		10037026	["48 Pauline crest", "Andrewsport"]	False	Primary	10037026	95
96	Graemeport	W7 5NL	LU58 0UH		10038450	["Flat 36J", "Gray greens"]	False	Primary	10038450	96
97	BA4N 7BU		W55 7FN		10039522	["74 Cox river", "West Victoriafort"]	False	Primary	10039522	97
98	Atkinsonmouth	SP4 6BG	WS30 5HS		10040074	["Flat 86q", "Holden shore"]	False	Primary	10040074	98
99	West Angelaton	M4 3RG	N4G 8QE		10040794	["Flat 0", "Angela village"]	False	Primary	10040794	99
100	G69 0YX		LL0V 4LA		10041002	["632 Bren lock", "West Terryhaven"]	False	Primary	10041002	100
101	PA8 2WW		M5T 9ZZ		10041221	["23 Andrea flat", "South Joel"]	False	Primary	10041221	101
102	GY32 9SN		G15 9UL		10041912	["30 Katy gardens", "Hilaryland"]	True	Primary	10041912	102
103	Lake Kathryn	DT9 7TH	M3H 5UH		10042691	["Flat 96", "Walsh throughway"]	False	Primary	10042691	103
104	Rossborough	AL0 8LY	DL7 1WE		10042817	["Studio 8", "Valerie square"]	False	Primary	10042817	104
105	L18 6AZ		KT6H 9BZ		10042909	["11 Lynda prairie", "Lake Grace"]	True	Primary	10042909	105
106	FK84 7HY		G9 4QH		10043164	["023 Fisher coves", "Hannahberg"]	False	Primary	10043164	106
107	Yvonneborough	PA52 4GP	L27 3FD		10043855	["Flat 69", "Janice pike"]	False	Primary	10043855	107
108	W99 2QL		M4 4FH		10044150	["8 Victoria crossroad", "West Kim"]	False	Primary	10044150	108
109	East Jeffrey	PE9 7DZ	ML7 0ND		10044547	["Studio 22", "Bolton creek"]	False	Primary	10044547	109
110	North Scottchester	N1C 5GN	BD8Y 9RD		10044553	["Flat 6", "Fisher passage"]	False	Primary	10044553	110
111	B88 0TD		FY5R 0YA		10045118	["08 Carroll parkways", "West Chelseaborough"]	False	Primary	10045118	111
112	West Rachel	G55 2UF	CW7 1UY		10045441	["Studio 8", "Whitehead turnpike"]	False	Primary	10045441	112
113	B7H 9HX		SY89 0UW		10045717	["3 Morris mission", "Mohammadfurt"]	False	Primary	10045717	113
114	SN71 2YB		S5 8XD		10046369	["86 Yvonne highway", "Williamton"]	False	Primary	10046369	114
115	Clarefurt	N1 8UD	BT05 4DR		1004731T	["Flat 98B", "Jacqueline vista"]	False	Primary	1004731T	115
116	CO42 2GA		SM01 3TU		10048151	["2 Robinson passage", "Baxterbury"]	False	Primary	10048151	116
117	JE7 5WZ		M6 9NH		10048168	["13 Harris crossroad", "Duncanfort"]	False	Primary	10048168	117
118	Reedborough	MK20 8RQ	HU6H 1ZN		10050276	["Studio 1", "Wilson land"]	False	Primary	10050276	118
119	Lake Terryton	S5E 5JU	SO44 2HR		10050512	["Flat 74", "Robin skyway"]	False	Primary	10050512	119
120	Parsonsborough	AB6M 6ZF	W3 5JJ		10051538	["Studio 77", "Katy keys"]	False	Primary	10051538	120
121	WF3P 8GR		ML9M 5PL		10051890	["83 Murphy shores", "Annafort"]	False	Primary	10051890	121
122	M0 0JN		SR54 7LD		10052501	["3 Butler station", "Port Andreamouth"]	False	Primary	10052501	122
123	Port Sarahaven	S2 5GT	M86 1SD		10052743	["Flat 56", "Hilary groves"]	False	Primary	10052743	123
124	LL6A 8UD		G6 5ZN		10053032	["294 Victor locks", "East Dylanside"]	False	Primary	10053032	124
125	Grantport	LD1 5FF	WR46 7BG		10053723	["Studio 59e", "Barbara river"]	False	Primary	10053723	125
126	G83 5PH		W6 9ZZ		10053746	["062 Melanie crescent", "Hunttown"]	False	Primary	10053746	126
127	BD77 1RT		E6 2DQ		10054300	["6 Chapman plains", "Port Jonathanhaven"]	False	Primary	10054300	127
128	Simpsonhaven	S5 8BP	W4A 2YF		10055096	["Studio 5", "Mathew isle"]	False	Primary	10055096	128
129	Wellsport	DA6W 6PB	W1U 9SD		10055666	["Flat 03Y", "Taylor course"]	False	Primary	10055666	129
130	LS6 2RQ		L9A 0ER		10056335	["22 Katy underpass", "Elliottside"]	False	Primary	10056335	130
131	E12 3UB		S81 8NW		10056410	["40 Shaw expressway", "Ritabury"]	False	Primary	10056410	131
132	N7 7RP		HG4V 7QY		10056865	["31 Haynes valleys", "East Roy"]	False	Primary	10056865	132
133	Taylorton	M9 6BY	S24 2BZ		10056957	["Flat 8", "Mohamed rapids"]	False	Primary	10056957	133
134	M7E 7XL		SS8M 3AL		10057661	["283 Deborah freeway", "Mooreview"]	False	Primary	10057661	134
135	South Keithmouth	HD8Y 0DB	E94 1TN		10057995	["Flat 8", "Harris stream"]	False	Primary	10057995	135
136	Elizabethview	BT3Y 2DZ	L4B 6XT		10058071	["Flat 24n", "Terry junctions"]	False	Primary	10058071	136
137	West Glenborough	AB24 5AS	DD0 2DF		10058140	["Studio 1", "Michael ferry"]	False	Primary	10058140	137
138	Port Clifford	PH84 0YF	N6D 3WF		10058508	["Flat 33", "Spencer islands"]	False	Primary	10058508	138
139	TN4P 8NP		PL63 1YA		10058589	["0 Gordon viaduct", "Harrisburgh"]	False	Primary	10058589	139
140	Darrentown	S54 4BW	WS60 6FN		10058917	["Studio 60", "Linda street"]	False	Primary	10058917	140
141	E75 3LN		CW0 0ZX		1005934T	["98 Liam mews", "Bowenchester"]	False	Primary	1005934T	141
142	PA45 6XN		L02 1GN		10060501	["0 Christine parkway", "Bondtown"]	False	Primary	10060501	142
143	BT2M 8QX		BA9 2XQ		10062185	["53 Janice ridges", "Natalietown"]	False	Primary	10062185	143
144	East Mathewburgh	BN0P 8XP	B4 0QE		10062191	["Flat 07c", "Pickering point"]	False	Primary	10062191	144
145	Scottchester	E1F 9AT	ME2 7UQ		1006312T	["Flat 11", "Barker via"]	False	Primary	1006312T	145
146	Glennbury	S8 9FR	G81 5SJ		10063257	["Studio 72", "Gill ramp"]	False	Primary	10063257	146
147	G34 7HD		N0 3HR		10063614	["009 Holly fall", "Wardstad"]	False	Primary	10063614	147
148	AL6 8RF		E42 6HZ		10064295	["821 Keith route", "Damianborough"]	False	Primary	10064295	148
149	G8 9WJ		G0 0PQ		10064669	["804 Allen plaza", "North Pamelaburgh"]	False	Primary	10064669	149
150	W5A 3EY		N82 9US		10065004	["190 Trevor wall", "West Joshborough"]	False	Primary	10065004	150
151	Kerrystad	E6 0RB	ML5E 8PX		10065010	["Studio 18", "Steele freeway"]	False	Primary	10065010	151
152	North Charleneborough	DG8 7BW	EN3E 3YU		10065632	["Studio 5", "Whittaker points"]	False	Primary	10065632	152
153	HS66 2AD		E81 6ZH		10065868	["32 Marie isle", "Lake Ericton"]	False	Primary	10065868	153
154	LU73 3PB		L05 6GD		10067863	["597 Robert summit", "Griffithsbury"]	False	Primary	10067863	154
155	Frytown	WC8R 4ZA	HS00 2QR		10068267	["Studio 56", "Simmons circles"]	False	Primary	10068267	155
156	Bellchester	EN2 9TA	W5 0SF		10069846	["Studio 71k", "Giles underpass"]	False	Primary	10069846	156
157	Joanview	ZE2M 8DY	S4F 6BX		1007033T	["Flat 04", "Goodwin lakes"]	False	Primary	1007033T	157
158	E7 0AJ		G63 2SS		10070980	["557 Cheryl keys", "Lisachester"]	False	Primary	10070980	158
159	Gavinport	G1 1JG	DE9W 6UD		10071240	["Flat 71", "Palmer hollow"]	False	Primary	10071240	159
160	GL2V 0ZU		S0E 3TY		1007165T	["3 Marsden ranch", "Careyview"]	False	Primary	1007165T	160
161	East Lorraine	L11 4FS	PR6 2LR		10071919	["Flat 78", "Adam village"]	False	Primary	10071919	161
162	Kathrynville	SS2V 4WA	G9U 6PB		10072053	["Flat 2", "Roberts shores"]	False	Primary	10072053	162
163	SA6 8RZ		CB9V 2WD		10072180	["607 Webb rest", "Simpsonland"]	False	Primary	10072180	163
164	KW1P 9QY		L7 5YG		10072548	["325 Julia landing", "Timothychester"]	False	Primary	10072548	164
165	DN6Y 7PS		LE03 7HE		10072617	["4 Watkins mall", "Phillipshire"]	False	Primary	10072617	165
166	B9J 7DA		E29 3NH		10072652	["6 Webb village", "South Roy"]	False	Primary	10072652	166
167	North Kellyburgh	M96 9GN	B81 1AU		10072905	["Flat 30", "Emily oval"]	False	Primary	10072905	167
168	W1C 1AR		L4G 3WN		10075788	["057 Jill ports", "Port Paulatown"]	False	Primary	10075788	168
169	S25 4XZ		B12 3WQ		10075794	["4 King spring", "North Karen"]	False	Primary	10075794	169
170	North Paula	PH4E 7SB	N34 5EN		10075892	["Flat 13d", "Thornton summit"]	False	Primary	10075892	170
171	L42 8XY		E9F 6RH		10076307	["6 Collier port", "Swiftport"]	False	Primary	10076307	171
172	M3F 4WD		BS9 2AB		10076428	["38 Rachael trail", "Lukehaven"]	False	Primary	10076428	172
173	L25 0YJ		S5 8AY		10076618	["3 Debra stravenue", "Robinsonmouth"]	False	Primary	10076618	173
174	Lake Nathanview	G8U 7DY	PR7 9TP		10077466	["Flat 43", "Stuart inlet"]	False	Primary	10077466	174
175	Lake Amber	HG0R 0UG	E2H 8JT		10077535	["Studio 1", "Andrews union"]	False	Primary	10077535	175
176	Lake Shirley	SA23 4EE	M42 6SG		10077702	["Studio 84", "Jones coves"]	False	Primary	10077702	176
177	Port Christianfort	KA6 2XR	NR1 2EU		10078014	["Flat 34o", "Naomi estate"]	False	Primary	10078014	177
178	HG1 6WT		ST0W 5JB		10078498	["3 Palmer turnpike", "Chapmanfort"]	False	Primary	10078498	178
179	L36 6WW		L30 8EY		1008006T	["91 Benjamin lights", "Evansfurt"]	False	Primary	1008006T	179
180	Walkertown	B97 6AW	HR05 0AH		10080306	["Flat 8", "Stewart junctions"]	False	Primary	10080306	180
181	HU5 4BU		G4D 8AT		10080698	["135 Roberts crossroad", "Gemmabury"]	False	Primary	10080698	181
182	Walkerton	ZE0 2YQ	OL4 1XT		10080773	["Studio 36", "Burton mews"]	False	Primary	10080773	182
183	East Suzanneborough	M8 0XU	SW3H 6WH		10080842	["Flat 84v", "Hunt square"]	False	Primary	10080842	183
184	B27 0EW		ME6A 3SJ		10081321	["50 Watson street", "East Lindsey"]	False	Primary	10081321	184
185	Grahamland	GU6E 2LF	EH77 7WB		10081436	["Flat 45", "Francis island"]	False	Primary	10081436	185
186	Kayleightown	S0F 1XW	G94 9LU		10082290	["Studio 07U", "Lauren street"]	False	Primary	10082290	186
187	Archermouth	S3G 8DL	S8W 1WR		10082629	["Studio 0", "Damien path"]	False	Primary	10082629	187
188	RG78 5NH		E1 4WB		10084054	["24 Thornton cape", "Spencerborough"]	False	Primary	10084054	188
189	Mohammedberg	WS5 2WA	W6A 9YN		10085368	["Flat 40S", "Tina groves"]	False	Primary	10085368	189
190	Lake Abbieshire	IG00 9TF	S9H 1LZ		10086377	["Studio 4", "Ricky points"]	False	Primary	10086377	190
191	M8F 6NR		LD15 6GS		10086803	["757 Lynne land", "Hodgsonhaven"]	False	Primary	10086803	191
192	South Robertbury	S6E 7EF	LA05 4NE		10087046	["Flat 59", "Carl throughway"]	False	Primary	10087046	192
193	L73 9FD		SA7 0PW		10087121	["905 Leigh divide", "West Roger"]	False	Primary	10087121	193
194	Greenshire	L6 6SU	DA55 8RS		10087207	["Flat 21S", "Shah fall"]	False	Primary	10087207	194
195	B79 4UQ		B8 9AH		10087392	["03 Brian rue", "Lake Tracymouth"]	False	Primary	10087392	195
196	PO50 0XB		CV2 5SX		10087622	["182 Mohammad underpass", "South Ashleyhaven"]	False	Primary	10087622	196
197	S5 5LQ		DD2 1YZ		10088090	["4 Johnston knolls", "Gilbertshire"]	False	Primary	10088090	197
198	Brianborough	E09 8PP	PH4 8SJ		10088470	["Flat 1", "Mohammed rue"]	False	Primary	10088470	198
199	Port Yvonneport	N2 3AX	G1S 1TT		10089346	["Flat 63n", "Joel stravenue"]	False	Primary	10089346	199
200	West Michael	CO37 8TN	W57 0DG		10090422	["Flat 83", "Martyn wall"]	False	Primary	10090422	200
201	Hydeview	M0F 6EJ	G7 2LR		10090923	["Studio 17", "Jason street"]	False	Primary	10090923	201
202	Lewistown	TW6M 3BW	N0F 5QN		10090969	["Studio 11", "Mary lodge"]	False	Primary	10090969	202
203	Lake Lauren	TA2P 9UN	LS9A 3LN		10092221	["Studio 85w", "Martin well"]	False	Primary	10092221	203
204	GL83 5FH		PL1V 0HJ		10093529	["6 Rose river", "Fionaburgh"]	False	Primary	10093529	204
205	BL43 3DX		PE3 0ZU		10093996	["802 Marshall hills", "Amyton"]	False	Primary	10093996	205
206	New Lewis	E73 6YD	B8 4ZD		10094354	["Flat 8", "Annette junction"]	False	Primary	10094354	206
207	Port Emily	HG9 3HH	E83 0ED		10094976	["Flat 43i", "Phillips avenue"]	False	Primary	10094976	207
208	DL6P 2RR		KW2 8DF		10095259	["85 Emma rapid", "Lake Steven"]	False	Primary	10095259	208
209	TN5W 9AJ		M7 4TD		10096406	["41 Nicola freeway", "Clareberg"]	False	Primary	10096406	209
210	Lake Mary	N96 4UX	E7 0NN		10097012	["Flat 60", "Christopher spring"]	False	Primary	10097012	210
211	Port Lesleyfurt	M10 2DW	L25 4XX		10097922	["Studio 25d", "Anthony mountain"]	False	Primary	10097922	211
212	S80 2GQ		ZE6P 4TG		10099491	["936 Garner drives", "Godfreyburgh"]	False	Primary	10099491	212
213	South Amelia	S9 1ZG	B6 4ND		10099894	["Flat 81", "Joshua manor"]	False	Primary	10099894	213
214	Gailmouth	S6 3DF	M90 0DH		10101102	["Studio 64", "Williams turnpike"]	False	Primary	10101102	214
215	WD9 3ST		M0T 6AZ		10101321	["0 Marion passage", "Singhmouth"]	False	Primary	10101321	215
216	Fletcherbury	W3 7PE	G5 1SF		10102566	["Flat 81", "Davies wall"]	False	Primary	10102566	216
217	Gerardmouth	M2 2GB	RH4 0NG		10102658	["Studio 20", "Pearson brook"]	False	Primary	10102658	217
218	Singhfort	TF9 0JU	OL3M 8UA		1010391T	["Studio 2", "Jones points"]	False	Primary	1010391T	218
219	South Carolfort	G89 0WD	L1B 8RU		10105028	["Studio 7", "Wendy ports"]	False	Primary	10105028	219
220	B82 9NU		E5 3BR		10106020	["782 Baker parks", "West Timothy"]	False	Primary	10106020	220
221	Lake Paulineberg	N24 6NU	L6 3LT		10106095	["Studio 03F", "Griffiths springs"]	False	Primary	10106095	221
222	Charleneburgh	BB5B 6EY	S07 0NB		10106665	["Flat 6", "Campbell grove"]	False	Primary	10106665	222
223	North Lucytown	L99 8GL	EC5M 9RZ		10107023	["Studio 12", "Jones walks"]	False	Primary	10107023	223
224	NE8 5NR		E2K 9QG		10108458	["979 Hancock drive", "West Rachaelhaven"]	False	Primary	10108458	224
225	BT70 5EJ		B4 6GW		10108700	["884 Henry forest", "Sheilahaven"]	False	Primary	10108700	225
226	WV1N 4FJ		IG5A 3TG		10108815	["450 Evans stravenue", "New Lauren"]	False	Primary	10108815	226
227	North Dale	B1G 4PX	B0U 1YN		10109006	["Studio 90", "Watts garden"]	False	Primary	10109006	227
228	Boothfort	E0 3JU	G3T 6SW		10109755	["Studio 46l", "Diana way"]	False	Primary	10109755	228
229	W64 6DA		S7F 5UD		1011017T	["869 Neil lane", "Justinfurt"]	False	Primary	1011017T	229
230	Kirstyburgh	W05 7LE	BD45 0ES		10114095	["Flat 9", "Turner courts"]	False	Primary	10114095	230
231	B1J 6RS		L5 0FQ		10114544	["6 Leah mall", "Lake Hilarymouth"]	False	Primary	10114544	231
232	Dianeton	ME57 5QB	N4 7NE		10114901	["Flat 5", "Irene port"]	False	Primary	10114901	232
233	PH2B 6JF		S4 2ZR		10117542	["05 Mohamed cape", "Julieshire"]	False	Primary	10117542	233
234	L2S 2BW		N1T 3QN		10117594	["6 Jones mews", "South Ellieport"]	False	Primary	10117594	234
235	North Connor	SR0 0DS	RM52 9JT		1011850T	["Studio 26g", "Smith forks"]	False	Primary	1011850T	235
236	Alicechester	E6 2SD	M25 3NU		10118539	["Studio 42Q", "Dennis parkway"]	False	Primary	10118539	236
237	Leannehaven	RG7 7WD	M4 2RU		10118706	["Flat 02", "Harding lodge"]	False	Primary	10118706	237
238	Bowenmouth	S93 8ZX	L8 4HQ		10122279	["Flat 79", "Smith junctions"]	False	Primary	10122279	238
239	W1U 0ET		L85 4UX		10123455	["3 Moore mountains", "Hollymouth"]	False	Primary	10123455	239
240	W7 8UD		OX0H 6GH		10125087	["644 Carly branch", "South Eleanor"]	False	Primary	10125087	240
241	CT05 3TN		ME1 3JQ		10126044	["0 Field villages", "Thompsonhaven"]	False	Primary	10126044	241
242	Duncanshire	N3S 9DS	W9 2LU		10126234	["Studio 97N", "Moore forks"]	False	Primary	10126234	242
243	Dickinsonmouth	LA97 9ER	S8 9DE		10126597	["Studio 26k", "Evans harbor"]	False	Primary	10126597	243
244	OX3R 1ZZ		WD59 5WJ		10129802	["827 Janet way", "South Seanmouth"]	False	Primary	10129802	244
245	E2F 9QQ		B18 7FJ		10131138	["201 Sian street", "Caroleland"]	False	Primary	10131138	245
246	S8K 4PU		SG98 1YS		10131668	["39 North crescent", "Davidton"]	False	Primary	10131668	246
247	Lake Jane	M36 1LN	DT6 4LF		10131979	["Flat 79", "Rees crest"]	False	Primary	10131979	247
248	WS4Y 8LX		DN9 2JX		10132222	["93 Allen drives", "Jemmaside"]	True	Primary	10132222	248
249	Port Declan	FK9 2NN	E57 2TE		10132683	["Studio 40", "Kenneth knoll"]	False	Primary	10132683	249
250	Kimberleyland	W0 9BE	TD03 6RN		10133847	["Flat 36J", "Alan square"]	False	Primary	10133847	250
251	DT1V 9PP		E0 0LY		10134292	["1 Wilkinson course", "South Sheilahaven"]	False	Primary	10134292	251
252	North Leahfort	G5K 4PG	CV52 1QB		10134672	["Flat 48", "Julie grove"]	False	Primary	10134672	252
253	L5 4XH		E1 2SG		10135295	["299 Judith via", "Lake Nathan"]	False	Primary	10135295	253
254	G0U 3XF		G4 1UQ		10135341	["4 Rees view", "Dunnville"]	False	Primary	10135341	254
255	E26 1JD		M7 7HP		10138356	["2 Mohammed brook", "Edwardsberg"]	False	Primary	10138356	255
256	M1 8WH		B6 4EF		10138460	["4 Barton square", "O'Brienview"]	False	Primary	10138460	256
257	LD4 7YU		S6 5PY		10138517	["147 Mark junction", "Daleside"]	False	Primary	10138517	257
258	IP6 9HL		E42 3BE		10139181	["093 Barry vista", "Richardsonport"]	False	Primary	10139181	258
259	Browntown	N9W 4UD	HP64 3FA		10139342	["Studio 87G", "Christian cape"]	False	Primary	10139342	259
260	L5 3FG		L66 3XF		10140700	["0 Mark lodge", "Harrisonland"]	False	Primary	10140700	260
261	TR3 0ST		B0U 1ZQ		10140913	["620 Debra isle", "East Valerie"]	False	Primary	10140913	261
262	YO7 5XU		E78 2JF		10141202	["1 George crest", "Patelbury"]	False	Primary	10141202	262
263	CR3 3YX		W2U 6HW		10141254	["0 Michael park", "South Harrymouth"]	False	Primary	10141254	263
264	Port Dennismouth	CM9 6QZ	JE6 4UL		1014133T	["Studio 28d", "Ward hollow"]	False	Primary	1014133T	264
265	New Ryan	B3 8LN	N2 6AT		10142038	["Flat 55", "Bradley plain"]	False	Primary	10142038	265
266	Port Bernardfurt	WR4N 1UG	E88 0LP		10142194	["Studio 39i", "Walsh mountain"]	False	Primary	10142194	266
267	RG09 2FF		E93 3EQ		1014265T	["9 Daniel oval", "South Leonbury"]	False	Primary	1014265T	267
268	PA6H 6YT		E6E 9YX		10142729	["866 Anne island", "Benjaminberg"]	False	Primary	10142729	268
269	TS7B 3JQ		L5 8JA		10142856	["00 Ellis brooks", "Williamsshire"]	False	Primary	10142856	269
270	New Gemma	SM8 9EF	TW1 6LG		10143894	["Studio 8", "William pines"]	False	Primary	10143894	270
271	Port Leigh	B7 1UH	M63 3XN		10146500	["Flat 06", "James island"]	False	Primary	10146500	271
272	South Chelseaberg	L2 2QE	M9 3DF		10149066	["Studio 11", "James ways"]	False	Primary	10149066	272
273	S3A 7HB		ZE8 0ZH		10149878	["5 Newman parkway", "New Gillian"]	False	Primary	10149878	273
274	LD4 3TE		M18 0XD		1015099T	["633 Lynne well", "Bruceburgh"]	False	Primary	1015099T	274
275	G6 5HN		SE54 5NX		10151208	["08 Gallagher prairie", "North Connor"]	False	Primary	10151208	275
276	HG2 1AH		KY3X 2EJ		10152488	["955 Norris meadow", "Vanessaberg"]	False	Primary	10152488	276
277	Richardsport	M7 1QZ	CF5 8JJ		10152868	["Studio 9", "Edwards path"]	False	Primary	10152868	277
278	KT4H 6NS		EH03 6PF		10153255	["339 Edwards spring", "Port Chelsea"]	False	Primary	10153255	278
279	North Michelleton	DT8B 1DU	L6 8YL		1015355T	["Flat 4", "Hunt flats"]	False	Primary	1015355T	279
280	PA88 1SW		WF7 3US		10153802	["4 Curtis ford", "West Anna"]	False	Primary	10153802	280
281	PA8B 3PG		G71 1HU		10154051	["272 Arthur drive", "Hydemouth"]	False	Primary	10154051	281
282	Jamiebury	KY8 9PB	E6D 0LH		10154097	["Flat 32p", "Ashton stravenue"]	False	Primary	10154097	282
283	M01 7UZ		KT6X 9BD		10154500	["931 Sharon lodge", "North Dylanhaven"]	False	Primary	10154500	283
284	Kirstyview	E0E 4PF	SG5 9FR		10156034	["Studio 76B", "Kim dale"]	False	Primary	10156034	284
285	East Cheryl	L4F 8PY	S5W 1GS		10156656	["Flat 8", "Cox forest"]	False	Primary	10156656	285
286	PA4 1BW		HX7A 2GL		10158403	["311 Kirby via", "Mahmoodview"]	False	Primary	10158403	286
287	DT1M 3WE		G1S 1FE		10159625	["8 Jayne cove", "Shanetown"]	False	Primary	10159625	287
288	EN0H 0ZY		LL9R 2JW		10159936	["9 Nicole vista", "West Katymouth"]	False	Primary	10159936	288
289	LA5M 9WQ		BT1 3BP		10160321	["81 Christian forge", "New Joycetown"]	False	Primary	10160321	289
290	DH0X 6ZP		B0A 4ZX		10160367	["85 Roger crossroad", "West Joyce"]	False	Primary	10160367	290
291	N5 1HX		CW3H 6YZ		10160897	["89 Rachael pine", "Sheilaland"]	False	Primary	10160897	291
292	East Ritatown	M0 3PE	ML7E 1SB		10160966	["Flat 95", "Karl rest"]	False	Primary	10160966	292
293	L47 0NR		G6C 2GE		10162667	["6 Michelle river", "East Elizabeth"]	False	Primary	10162667	293
294	Bethanhaven	N72 5TT	IV47 1RR		10164063	["Flat 75O", "Denise isle"]	False	Primary	10164063	294
295	S6W 1HY		G0W 7NL		10164149	["85 David village", "Campbellstad"]	False	Primary	10164149	295
296	West Graemeport	S6 7ST	PH10 9PN		10164178	["Studio 10", "Mohammed pines"]	False	Primary	10164178	296
297	New Abbie	L97 8JE	M57 4UR		1016562T	["Studio 21E", "Ward path"]	False	Primary	1016562T	297
298	Lesleyside	LL8 8RA	SN4M 4DW		10166328	["Studio 82W", "Gavin bypass"]	False	Primary	10166328	298
299	Hutchinsonbury	M0 1RT	PL88 4RZ		10181803	["Studio 69", "Mitchell fall"]	False	Primary	10181803	299
300	South Danny	S8S 8UQ	W4 2HJ		10181930	["Flat 7", "Tomlinson plain"]	False	Primary	10181930	300
301	West Josephineport	L7 9SJ	TF0Y 9XA		10182311	["Studio 63K", "Moss summit"]	False	Primary	10182311	301
302	L2H 6AF		TQ55 5DG		10183078	["891 Thomas run", "East Katieberg"]	False	Primary	10183078	302
303	Lake Douglaschester	B30 1YR	HA2 7FJ		10184300	["Studio 66", "Oliver valley"]	False	Primary	10184300	303
304	B6 9SX		IG9 8GZ		10185735	["221 Burns villages", "Yvonnehaven"]	False	Primary	10185735	304
305	Elliefort	SL75 0LW	BA1 2HB		10192899	["Studio 11", "Kenneth plains"]	False	Primary	10192899	305
306	G64 1EL		TA6 4ZN		10192916	["2 Cameron well", "New Ben"]	False	Primary	10192916	306
307	Port Jamieberg	GY16 1WX	G0 6GW		10194709	["Studio 93I", "Brown port"]	False	Primary	10194709	307
308	Hartleyborough	S7B 4FE	E4F 3FZ		10198244	["Flat 29M", "George gateway"]	False	Primary	10198244	308
309	E4 3YY		G1T 0HA		10199092	["141 Davidson tunnel", "Lake Damienshire"]	False	Primary	10199092	309
310	PA0V 0EJ		L0J 8FX		10200679	["866 Hannah hollow", "Jenningsmouth"]	False	Primary	10200679	310
311	Jordanport	M63 6HD	W71 1SG		10200685	["Flat 0", "Oliver plains"]	False	Primary	10200685	311
312	G73 2QX		DN8 6PL		10200748	["3 Bruce estates", "East Waynestad"]	False	Primary	10200748	312
313	Bevanmouth	NP5 1BA	S89 9QH		10201193	["Flat 2", "Louis plains"]	False	Primary	10201193	313
314	NG3 7PB		N3 7AH		10201705	["297 Edwards cliff", "East Owenfurt"]	False	Primary	10201705	314
315	Port Brenda	L3 0SR	L6 3DD		10202386	["Studio 60", "Lucy avenue"]	False	Primary	10202386	315
316	Toddbury	G0E 3HA	G5 9WB		10494872	["Flat 0", "Jasmine springs"]	False	Primary	10494872	316
317	N27 5ZY		B2 2AA		10204496	["0 Leah landing", "New Lawrence"]	False	Primary	10204496	317
318	Claireberg	E8 5DU	SN28 3QX		1020512T	["Studio 56", "Paula common"]	False	Primary	1020512T	318
319	Lake Fiona	CR8W 0ZB	DH9 4UL		10206404	["Flat 8", "Peter springs"]	False	Primary	10206404	319
320	S7 7YZ		SE2 2AF		10207131	["4 Richards islands", "Lake Joe"]	False	Primary	10207131	320
321	TN0 8PN		B3 9LG		10208946	["61 Wallace bypass", "Smithland"]	False	Primary	10208946	321
322	M0 9AZ		KY1R 8EZ		10209045	["0 Williams court", "New Timothyhaven"]	False	Primary	10209045	322
323	NG62 7PS		KY8 4PD		1021075T	["2 Wade ranch", "Sandraton"]	False	Primary	1021075T	323
324	Lake Fionahaven	G68 2FQ	B7W 0TP		10211717	["Flat 9", "Russell camp"]	False	Primary	10211717	324
325	SE6N 0TE		HU09 8WA		10213228	["26 Graeme bypass", "West Carolyn"]	False	Primary	10213228	325
326	West Terencefurt	SY3 2TT	N81 1AU		10214807	["Studio 38B", "Higgins coves"]	False	Primary	10214807	326
327	Joanborough	N7J 7AR	E57 6LY		10214940	["Flat 90", "Mary squares"]	False	Primary	10214940	327
328	South Vanessafort	M6 0TL	S6 7HU		10215183	["Studio 23", "Davies rapid"]	False	Primary	10215183	328
329	SY99 7QD		G65 2PH		10216508	["0 Hale ridge", "East Laurenchester"]	False	Primary	10216508	329
330	Smithmouth	G32 3GJ	B9 9JJ		10221960	["Studio 2", "Lamb roads"]	False	Primary	10221960	330
331	S6 3FD		WF3 8HA		10222865	["652 Kerry shoal", "North Marionhaven"]	False	Primary	10222865	331
332	N9F 2FX		IP5 7EG		10228043	["1 Hewitt station", "Gemmamouth"]	False	Primary	10228043	332
333	Stanleyport	E2S 8LA	SO0 5SY		10231275	["Flat 44", "Campbell island"]	False	Primary	10231275	333
334	Kirstyville	N4 6PU	BH4 3UP		10232094	["Studio 2", "Graham track"]	False	Primary	10232094	334
335	WF3E 5EN		GY76 5EL		1023217T	["103 Alexander mountain", "New Lyndaville"]	False	Primary	1023217T	335
336	E9 8TP		DH8 8SQ		10233264	["1 Day glen", "Lake Shaunstad"]	False	Primary	10233264	336
337	W1 4YN		G76 6TL		10233327	["160 Ann creek", "Paulinemouth"]	False	Primary	10233327	337
338	East Naomiview	G4H 2BB	W63 0FA		10235783	["Flat 73b", "Patricia summit"]	False	Primary	10235783	338
339	NP5 7HL		G7D 3BJ		10236953	["1 Clive burg", "New Emily"]	False	Primary	10236953	339
340	South Judith	G0 9QS	G33 3BA		10238118	["Studio 04", "Gill inlet"]	False	Primary	10238118	340
341	Adrianville	CA57 0SJ	S4D 8US		1024055T	["Flat 1", "Paige drives"]	False	Primary	1024055T	341
342	New James	G33 6DU	W6B 3AW		10241932	["Flat 12p", "Brown cove"]	False	Primary	10241932	342
343	Oliviabury	LE9A 4QW	CB4 1SJ		10241990	["Flat 2", "Mitchell tunnel"]	False	Primary	10241990	343
344	Wilkinsonberg	M1 3DH	SG9 3UQ		10242970	["Flat 5", "Luke points"]	False	Primary	10242970	344
345	Aliceside	N1 0WE	M00 0FU		10243443	["Studio 01", "Power court"]	False	Primary	10243443	345
346	M0D 9UA		W16 0HW		10243489	["937 Geoffrey mountain", "Elliefort"]	False	Primary	10243489	346
347	DH4A 1WP		S1A 8PP		10244918	["2 Sylvia mill", "South Ellie"]	False	Primary	10244918	347
348	SM5W 4TR		M28 8YP		10245530	["419 Smith mountain", "Marilynmouth"]	False	Primary	10245530	348
349	E6G 3QB		JE8 7HB		10245576	["825 Joel unions", "Khanborough"]	False	Primary	10245576	349
350	Aaronstad	G61 7NB	S2 0NG		10246308	["Flat 72B", "Louise village"]	False	Primary	10246308	350
351	CM1 6UR		M00 7JL		10248689	["46 Zoe brook", "Glenburgh"]	False	Primary	10248689	351
352	CM59 0HE		HA7M 5RT		10248787	["580 Jacqueline drive", "Charlotteside"]	False	Primary	10248787	352
353	G14 6UY		SY98 7UD		1025051T	["255 Sylvia trace", "Jemmaland"]	False	Primary	1025051T	353
354	New Billyhaven	IV69 5QG	B4 3SU		10250601	["Studio 1", "Paula prairie"]	False	Primary	10250601	354
355	Carlview	M2K 3RR	L8B 5RP		10254153	["Studio 0", "Clements place"]	False	Primary	10254153	355
356	Katherinebury	JE4 2XL	S62 0QG		10254942	["Flat 4", "Armstrong loop"]	False	Primary	10254942	356
357	IV8X 8FT		NR77 2XR		10255421	["22 Jasmine centers", "North Jean"]	False	Primary	10255421	357
358	N9 3AS		W9 5ZL		10255945	["5 Patel extensions", "Lake Alice"]	False	Primary	10255945	358
359	North Royfurt	G91 2TH	HS45 2DB		10256741	["Studio 60O", "Shaun crescent"]	False	Primary	10256741	359
360	M87 9EP		S1B 9NY		10259249	["432 James cliff", "East Cameron"]	False	Primary	10259249	360
361	Russellville	W61 9ET	S6 1JN		10264165	["Flat 38c", "Lynda causeway"]	False	Primary	10264165	361
362	New Cameronburgh	M89 0SN	M8 0WQ		10264188	["Flat 7", "Kenneth circle"]	False	Primary	10264188	362
363	E1G 2BS		HG67 6SW		10264522	["326 Christian lock", "South Scott"]	False	Primary	10264522	363
364	L26 5FG		BD5X 6LF		10270815	["55 Morgan island", "Connollyshire"]	False	Primary	10270815	364
365	East Oliver	S5U 1BD	PO0X 9FD		10272741	["Flat 39", "Rachel loop"]	False	Primary	10272741	365
366	Blakeborough	PL10 8PX	SS7 8QT		10273905	["Studio 0", "Dawson mountains"]	False	Primary	10273905	366
367	CF45 8RB		B47 0RT		10274494	["55 Williamson place", "Port Melaniemouth"]	False	Primary	10274494	367
368	Traceytown	GU56 9GS	NP7X 1AB		10277117	["Studio 16f", "Suzanne circles"]	False	Primary	10277117	368
369	BH9E 8TS		DT1 3LR		1028453T	["8 Parker lake", "Lindseyside"]	False	Primary	1028453T	369
370	G8 0ZJ		L65 0YL		10285929	["347 Payne field", "Port Eleanor"]	False	Primary	10285929	370
371	CW81 7JH		E50 0JU		10287383	["164 Ward park", "Scotthaven"]	False	Primary	10287383	371
372	GL56 7WS		W7S 9SS		10288046	["30 Kelly valleys", "Marshville"]	False	Primary	10288046	372
373	Port Julia	L00 0YB	ST1 4YY		10292742	["Studio 70q", "Green vista"]	False	Primary	10292742	373
374	Kirkborough	NG9 5HW	E0T 7EU		10293987	["Flat 88w", "Paula tunnel"]	False	Primary	10293987	374
375	New Wendy	B8J 0YJ	G64 3TH		10295930	["Studio 85G", "Shirley passage"]	False	Primary	10295930	375
376	LS0 7AL		N6S 2SF		10297297	["865 Samuel mill", "South Anthony"]	False	Primary	10297297	376
377	Port Elaine	BT31 1XA	CM1Y 5LB		10297660	["Studio 3", "Williams squares"]	False	Primary	10297660	377
378	NP7E 5FJ		TW3 2LR		10297913	["254 Abdul mall", "Evansstad"]	False	Primary	10297913	378
379	Nicholsonside	SG3 9SH	NR35 6FU		13611733	["Studio 7", "Franklin haven"]	False	Primary	13611733	379
380	Andrewmouth	ML6 8YF	W80 8PX		1029931T	["Studio 2", "Amber point"]	False	Primary	1029931T	380
381	Joefurt	L82 1JA	G12 6FQ		1030110T	["Studio 7", "Thompson trail"]	False	Primary	1030110T	381
382	E8 5RW		TA71 7YQ		10301750	["979 Nash spur", "East James"]	False	Primary	10301750	382
383	Newtonborough	ZE8H 8WA	BL18 9ED		10302350	["Studio 35", "Jamie grove"]	False	Primary	10302350	383
384	South Amber	G2F 8YW	LD5B 6YL		10303376	["Studio 31p", "Kirsty crossing"]	False	Primary	10303376	384
385	Port Vincentland	M5B 4JB	WF40 6AH		10305935	["Studio 38D", "Amelia mall"]	False	Primary	10305935	385
386	Williamsburgh	G2 6XJ	WC01 3GL		1030841T	["Studio 6", "Davis meadows"]	False	Primary	1030841T	386
387	E3F 4HS		CR61 1UD		1030875T	["92 Hope forks", "South Derekchester"]	False	Primary	1030875T	387
388	Akhtarville	BS73 2AW	HX2H 2DL		10309533	["Flat 02", "Williams terrace"]	False	Primary	10309533	388
389	Lake Charlie	EH00 2TZ	N9D 5ZY		10315141	["Flat 91", "Clayton stream"]	False	Primary	10315141	389
390	Emmaport	E7 1HB	DL49 2LT		10317585	["Flat 35I", "Ricky orchard"]	False	Primary	10317585	390
391	AL1W 8XR		N43 4AB		10318726	["1 Kate ports", "Lake Wayneland"]	False	Primary	10318726	391
392	S0U 9BX		G7S 3FP		10319067	["4 Helen plaza", "Marionmouth"]	False	Primary	10319067	392
393	Jacobshire	IP4 3WL	N37 1AJ		10320788	["Studio 54", "Hughes orchard"]	False	Primary	10320788	393
394	West Lisa	EX5R 0SR	B2 3UJ		10320955	["Flat 50h", "King spur"]	False	Primary	10320955	394
395	Oliviaborough	S1B 6UX	S6 7WT		10322725	["Flat 30", "Bruce prairie"]	False	Primary	10322725	395
396	Jayville	B8 8NN	L8G 2EY		10324484	["Studio 00", "Hobbs oval"]	False	Primary	10324484	396
397	E5 1UU		M5F 6AW		10325700	["51 Yates gateway", "Bensonside"]	False	Primary	10325700	397
398	Coleside	NG6 8DU	E08 8YU		10327234	["Flat 9", "Louis fords"]	False	Primary	10327234	398
399	Harrisonton	HP19 7FX	N4 8YD		1032923T	["Studio 21i", "Lorraine corners"]	False	Primary	1032923T	399
400	SO7 4SA		WS84 9FF		11452767	["04 White road", "West Abdulshire"]	False	Primary	11452767	400
401	Port Janeborough	LN3R 9FX	BH41 2LP		10332236	["Flat 00X", "Jones brooks"]	False	Primary	10332236	401
402	North Elizabethfort	ME0 7GS	WF44 4ZT		10332461	["Studio 28E", "Coles spurs"]	False	Primary	10332461	402
403	Lake Sylvia	S01 4JS	KW2 4XE		10334473	["Studio 15", "Taylor parks"]	False	Primary	10334473	403
404	Holtton	N6J 0PH	W7T 7JH		10335568	["Flat 60B", "Cameron views"]	False	Primary	10335568	404
405	E8U 8BF		RH4A 7QY		10336709	["21 Antony drive", "Katebury"]	False	Primary	10336709	405
406	Zoechester	E22 0SX	M89 3UZ		10337505	["Studio 1", "O'Connor stravenue"]	False	Primary	10337505	406
407	KW57 2UU		S6 2QB		10337914	["335 Antony ridges", "West Nathanport"]	False	Primary	10337914	407
408	New Gail	L1B 3UH	SS5V 1GB		1033889T	["Studio 91B", "Ingram square"]	False	Primary	1033889T	408
409	N9 3TW		E6S 8BX		10340294	["2 Margaret mall", "Teresaville"]	False	Primary	10340294	409
410	Ashtonhaven	B69 5ZR	G6W 9HH		1034037T	["Studio 2", "Farmer plaza"]	False	Primary	1034037T	410
411	G0B 0JD		BB43 3PP		10346606	["41 Davies tunnel", "Lauraton"]	False	Primary	10346606	411
412	Lake Joseph	SM9 8AZ	L2T 5JD		1034930T	["Studio 67", "Clive wells"]	False	Primary	1034930T	412
413	Parkerhaven	HS7X 1HU	G0T 9QU		10349339	["Flat 55v", "Mills forks"]	False	Primary	10349339	413
414	Port Jade	BA5 0NQ	E8J 3WQ		10352773	["Flat 36", "Ann inlet"]	False	Primary	10352773	414
415	TD9M 9ZY		DG0R 0GA		10353966	["833 Lucy oval", "Port Kyle"]	False	Primary	10353966	415
416	South Joyceport	NG4B 4SL	G9 0JD		1035651T	["Studio 30r", "Fletcher points"]	False	Primary	1035651T	416
417	New Joyce	N5J 6RH	W12 0FU		10356768	["Flat 9", "Robinson points"]	False	Primary	10356768	417
418	B8G 6LA		ML7Y 7SZ		10362036	["377 Cole falls", "New Ericberg"]	False	Primary	10362036	418
419	West Joshua	B79 5RS	DT9 5BJ		10363460	["Studio 6", "Allen fall"]	False	Primary	10363460	419
420	KY0M 8ND		L16 8ER		10367766	["9 Birch squares", "Lake Joycetown"]	False	Primary	10367766	420
421	CR2 7YX		N98 9PT		10369939	["917 Kevin extension", "Port Pamelaberg"]	False	Primary	10369939	421
422	L94 6JN		G2T 5LT		10370284	["94 Parker canyon", "New Julianton"]	False	Primary	10370284	422
423	HA7 3PN		PL4E 1GR		10373086	["3 Helen inlet", "Browntown"]	False	Primary	10373086	423
424	New Callum	TF8R 3JF	W5G 3DY		10373495	["Flat 81E", "Holland manors"]	False	Primary	10373495	424
425	S04 0US		N59 6QA		10381719	["57 Gemma brooks", "New Michael"]	False	Primary	10381719	425
426	McDonaldton	S4E 4RF	M6 7QR		10382256	["Studio 58s", "May summit"]	False	Primary	10382256	426
427	NP3 7UD		BS8 6TE		10384821	["9 Jones mountains", "Baileyborough"]	False	Primary	10384821	427
428	N3C 4LQ		SM6 7HU		10389088	["54 Hughes place", "Hayesfurt"]	False	Primary	10389088	428
429	Lake Abigailtown	KT87 8QP	G5 8WD		10397831	["Flat 0", "Alan wall"]	False	Primary	10397831	429
430	E9 6ZY		SR5 2AZ		10403484	["370 Natasha lakes", "Harrisonmouth"]	False	Primary	10403484	430
431	GL4P 6UD		B6U 4YA		10409497	["9 Wayne circles", "West Alan"]	False	Primary	10409497	431
432	S3E 8PP		AB6 3QP		10410786	["183 Thomas wall", "Knowlestown"]	False	Primary	10410786	432
433	BH9 8NN		B8 5EN		1041194T	["5 Thomas cove", "Jillmouth"]	False	Primary	1041194T	433
434	W9C 7UT		NW48 8QT		10415698	["25 Marc stream", "Marcusberg"]	False	Primary	10415698	434
435	Smithview	SE1 6SW	M35 7FU		10420959	["Studio 3", "Mark ports"]	False	Primary	10420959	435
436	Louisstad	W1H 8LA	B4 4ZH		10423836	["Studio 06I", "Kaur way"]	False	Primary	10423836	436
437	B9 3UT		WN7X 6LP		10424217	["4 Marshall port", "Cartwrighttown"]	False	Primary	10424217	437
438	RM80 1TU		W5 9HE		10426794	["081 Chloe flats", "Lewismouth"]	False	Primary	10426794	438
439	West Holly	S9F 4ZP	MK3 6QR		10429544	["Studio 0", "Tracy corners"]	False	Primary	10429544	439
440	South Louise	PA2M 4ET	B58 5YW		10433249	["Flat 01a", "Leigh ridge"]	False	Primary	10433249	440
441	S88 4JU		E9 6QN		10434477	["7 Julia inlet", "East Claireton"]	False	Primary	10434477	441
442	BS96 8YU		CH87 5EW		10437636	["8 Price keys", "North Hazel"]	False	Primary	10437636	442
443	West Jamesside	DA56 2EF	W3J 4LY		10439199	["Studio 80P", "Aaron green"]	False	Primary	10439199	443
444	Lake Lukestad	W2T 0PU	N4H 8HL		10441883	["Studio 20r", "Williams rest"]	False	Primary	10441883	444
445	M30 5QR		LE4Y 1QY		10442189	["78 Elliot trace", "Tinafort"]	False	Primary	10442189	445
446	Lake Alice	G5W 3XQ	W7D 2FL		10445671	["Flat 64", "Savage junctions"]	False	Primary	10445671	446
447	S83 7RT		G41 7TA		10447090	["985 Vincent point", "Abdulport"]	False	Primary	10447090	447
448	N2 6TY		TR12 1AD		10447959	["798 Walters river", "Port Andreaton"]	False	Primary	10447959	448
449	Sheilabury	N8B 9TT	SW6 6LD		10454979	["Flat 84d", "Katherine mountain"]	False	Primary	10454979	449
450	B28 4GA		E6 3QP		10455268	["198 Harvey shore", "Shawborough"]	False	Primary	10455268	450
451	G3 5DN		WD2E 7WP		10456156	["5 Jones creek", "Goodwinfurt"]	False	Primary	10456156	451
452	WS8 1BB		WA6 1GX		10456162	["7 Rees points", "New Kathrynshire"]	False	Primary	10456162	452
453	Victoriaside	W4F 2DT	DE3R 5SD		10456381	["Flat 6", "Hughes coves"]	False	Primary	10456381	453
454	Kimberleyview	N37 9JB	SR4A 8SB		10460725	["Flat 4", "Wayne springs"]	False	Primary	10460725	454
455	Ryanfort	GU7P 0NN	W0 3EE		10461469	["Studio 20e", "Smith station"]	False	Primary	10461469	455
456	South Jayne	BR30 1TT	N6 8AP		10461498	["Flat 67", "Watson parks"]	False	Primary	10461498	456
457	East Gerard	S1S 7FP	N40 7PD		10465735	["Studio 65P", "Hart parks"]	False	Primary	10465735	457
458	Port Gerald	JE16 9UH	NE2X 4LQ		10468917	["Studio 5", "Brian ridge"]	False	Primary	10468917	458
459	Lake Victorville	N2W 2FA	L54 4FF		10469863	["Studio 9", "Morrison motorway"]	False	Primary	10469863	459
460	Patelberg	RH48 6YG	G6 1WQ		10482836	["Studio 23", "Nicola roads"]	False	Primary	10482836	460
461	New Katyville	S1 7EW	M9H 5EA		10484543	["Flat 69x", "Joanne knoll"]	False	Primary	10484543	461
462	B8E 6SU		B3H 6NY		1048587T	["05 Whitehouse summit", "East Davidville"]	False	Primary	1048587T	462
463	Lake Cliffordburgh	ME0 0TD	E3 8EA		10486336	["Flat 35", "Cole terrace"]	False	Primary	10486336	463
464	Mayport	HG9P 3ZD	HX05 1RS		13402508	["Flat 7", "Tony park"]	False	Primary	13402508	464
465	CM08 2WZ		HS3 7PD		11001537	["621 Lynn ports", "Lake Cliveborough"]	False	Primary	11001537	465
466	Hopkinsshire	L5W 9LS	S4 1PR		11013596	["Flat 18", "Graeme plaza"]	False	Primary	11013596	466
467	SS4 6TN		W8W 3EN		11019897	["0 Rice view", "South Donald"]	False	Primary	11019897	467
468	Jackside	G65 0EY	IG0A 0ZQ		11021106	["Flat 3", "Moran ford"]	False	Primary	11021106	468
469	North Bretthaven	G41 8ZX	RM63 3JS		11029206	["Studio 63E", "Richardson hollow"]	False	Primary	11029206	469
470	Henryland	M9K 7PT	HG7H 3UE		11034030	["Studio 03p", "Brett avenue"]	False	Primary	11034030	470
471	Port Malcolmmouth	M40 2TR	G3C 6WA		1104342T	["Studio 87", "Tracy haven"]	False	Primary	1104342T	471
472	Barkerport	ZE79 9XT	E1 2UP		11056262	["Flat 2", "Elaine views"]	False	Primary	11056262	472
473	East Vanessa	CT1V 5DR	SL8 0NQ		11063558	["Studio 4", "Shannon orchard"]	False	Primary	11063558	473
474	KY7 9JA		WA9 3DS		11068361	["9 Riley wall", "New Robin"]	False	Primary	11068361	474
475	East Michael	BN2A 2HL	M0A 2PE		11084044	["Flat 60L", "Jasmine island"]	False	Primary	11084044	475
476	PE21 3BU		B5 7PR		11084211	["87 Robinson walks", "Lake Susanside"]	False	Primary	11084211	476
477	B0B 4ZH		TN5 5LE		11087791	["94 Jackson forge", "Nicolamouth"]	False	Primary	11087791	477
478	BA0 0BU		GY69 7JT		11092050	["8 Harry squares", "Bowenview"]	False	Primary	11092050	478
479	Lake Robin	N8 2EG	L5W 4ZF		11100423	["Flat 2", "Sara flat"]	False	Primary	11100423	479
480	Briggsberg	ML4 1FE	L89 1ST		11102602	["Studio 75", "Smith points"]	False	Primary	11102602	480
481	South Jeanland	CV46 3LA	M6 3BS		11112194	["Studio 94", "Smith centers"]	False	Primary	11112194	481
482	L11 9ZF		BD51 4NW		11131468	["8 Lowe crescent", "New Carole"]	False	Primary	11131468	482
483	M7 4UA		DD3 3QN		11138571	["0 Dean viaduct", "Port Jakeside"]	False	Primary	11138571	483
484	W40 0AY		DN37 2NN		11149177	["3 Rogers drives", "Port Rachel"]	False	Primary	11149177	484
485	IV6E 1WT		EH1 2GY		11153838	["875 Martin summit", "Duncanborough"]	False	Primary	11153838	485
486	FK0V 4JW		B4S 4PF		11166595	["434 Smith shoal", "North Hayleyville"]	True	Primary	11166595	486
487	Hodgsonmouth	HD4 8YQ	W4 7WY		11183886	["Studio 24O", "Simpson villages"]	False	Primary	11183886	487
488	Lake Iainville	W07 4HH	M5 7BQ		1119959T	["Studio 5", "Martin motorway"]	False	Primary	1119959T	488
489	Lake Jessicaburgh	EX66 9NX	DY18 7SD		11203189	["Studio 97", "Vincent summit"]	False	Primary	11203189	489
490	W3 4AZ		G3W 0ZE		11214567	["09 Reece pine", "North Stuarthaven"]	False	Primary	11214567	490
491	S37 5UY		N40 2BA		11214849	["92 Bolton course", "Gillstad"]	False	Primary	11214849	491
492	TS1 0WG		WS8 1AW		11219796	["7 Ward plain", "Denismouth"]	False	Primary	11219796	492
493	EN8X 4RQ		G93 4PP		11223576	["4 Roberts island", "Port Allanstad"]	False	Primary	11223576	493
494	North Angelamouth	CM05 7WB	M6 6ZJ		11233248	["Studio 52", "Collier manors"]	False	Primary	11233248	494
495	W8 0UB		L8 7QG		11245969	["8 Sanderson garden", "East Denisshire"]	False	Primary	11245969	495
496	DG77 4PD		N44 9GX		11245975	["9 Ross estate", "Whiteland"]	False	Primary	11245975	496
497	M1 2QL		B8K 7HW		11247745	["50 Parsons via", "Port Markside"]	False	Primary	11247745	497
498	Burrowsbury	IV4 6QD	NN8 5BS		11251502	["Studio 1", "Grace stravenue"]	False	Primary	11251502	498
499	Daniellefurt	NG08 5XX	BS97 7TN		11256558	["Studio 26", "Green mountains"]	False	Primary	11256558	499
500	S7H 9HY		N2 0LZ		11259389	["289 Martin rest", "Sallyton"]	False	Primary	11259389	500
501	Tonychester	G56 3ZD	SG5W 5HG		11267055	["Flat 25u", "Adams mission"]	False	Primary	11267055	501
502	UB6 5GR		W8 3HP		1126792T	["28 Graham square", "North Janice"]	False	Primary	1126792T	502
503	B2 9PQ		HX8 6QA		11276657	["9 Hannah islands", "Port Donaldland"]	False	Primary	11276657	503
504	Port Oliver	B8J 2BY	NN9E 7ZJ		11283988	["Flat 34R", "Hunt brooks"]	False	Primary	11283988	504
505	HG25 5YN		AL5 8GF		1128889T	["929 Russell meadow", "Berryfort"]	False	Primary	1128889T	505
506	OX0 3RL		WD30 5GG		11291268	["69 Francis village", "Alexview"]	False	Primary	11291268	506
507	Jenkinstown	W8U 3PZ	E75 5EE		1129192T	["Flat 13i", "Connor inlet"]	False	Primary	1129192T	507
508	CW3H 5HA		BN7E 0SB		11291942	["3 Brown turnpike", "Marilynchester"]	False	Primary	11291942	508
509	West Craigmouth	OX55 6YE	KY24 5SA		11308641	["Flat 0", "Harriet dale"]	False	Primary	11308641	509
510	Lucyburgh	EH05 0FT	WD2 3PB		11309454	["Studio 24U", "Lewis circles"]	False	Primary	11309454	510
511	MK95 0GE		M4 5DE		11314744	["04 Clarke rue", "New Jessicaburgh"]	False	Primary	11314744	511
512	E85 1LG		L52 0YD		11317742	["48 Giles port", "Danielmouth"]	False	Primary	11317742	512
513	North Bryanmouth	TW7B 0PW	E0A 8ZA		11321977	["Studio 17u", "Tom tunnel"]	False	Primary	11321977	513
514	Sandersonfurt	WA18 5DJ	CW9M 5RS		11325016	["Flat 51", "Williams heights"]	False	Primary	11325016	514
515	North Shirleybury	SO04 2EU	EN95 1UX		11329259	["Studio 33x", "Bradley ridge"]	False	Primary	11329259	515
516	CT2A 6YY		E77 8JT		11336129	["4 Collins skyway", "Vincentport"]	False	Primary	11336129	516
517	Teresafurt	M6U 0TU	WN2 8LT		11345121	["Flat 1", "French center"]	False	Primary	11345121	517
518	Taylorville	E79 0GL	HS2 9GX		11348643	["Flat 4", "Jean mountain"]	False	Primary	11348643	518
519	Port Jessicastad	SR20 7DE	SR74 3HG		11356568	["Studio 74j", "Sheila forest"]	False	Primary	11356568	519
520	S9 5DY		TF1 8FZ		11377313	["893 Smith shoals", "Raymondview"]	False	Primary	11377313	520
521	W0J 5ZJ		LD0H 5BG		11433199	["5 Patel dam", "Joeborough"]	False	Primary	11433199	521
522	W4 9RF		DE38 5QB		1143836T	["244 Alexandra mountain", "Jonesfort"]	False	Primary	1143836T	522
523	TN5N 3PB		CW4Y 6LS		1143889T	["580 Jessica manor", "East Jamesborough"]	False	Primary	1143889T	523
524	East Melissaport	HD3V 4GX	NG7H 5TT		11441562	["Studio 53P", "Maria river"]	False	Primary	11441562	524
525	HP0M 2PD		W79 5AU		11443384	["560 Morgan knoll", "Masonstad"]	False	Primary	11443384	525
526	Lake Mohammed	EH65 6LA	N98 4HF		11444871	["Studio 7", "Harding pine"]	False	Primary	11444871	526
527	S23 1WF		B81 4ZP		11447460	["528 Harrison roads", "Callumchester"]	False	Primary	11447460	527
528	SA2 6FL		SG92 4LJ		11452168	["115 Dennis points", "South Susan"]	False	Primary	11452168	528
529	Lake Traceyfort	SR19 4QB	SY1 1NR		11452329	["Flat 93", "Jones rest"]	False	Primary	11452329	529
530	Port Victorbury	SA9W 2ZE	DE4H 2JP		11462975	["Studio 6", "Gary expressway"]	False	Primary	11462975	530
531	W0W 4DR		ME23 6XZ		11466008	["4 Carolyn trail", "Stephaniemouth"]	False	Primary	11466008	531
532	G3S 4SX		DD3 1LX		11466112	["462 Darren green", "Jayneborough"]	False	Primary	11466112	532
533	AL2 9UG		B3C 5EY		11466210	["204 Steven corners", "New Rachelshire"]	False	Primary	11466210	533
534	Jonestown	WR0V 7DD	M4 6SP		11467743	["Studio 27b", "James landing"]	False	Primary	11467743	534
535	Lake Patrick	TW2 3ED	M1B 6NH		11469818	["Flat 2", "Fletcher square"]	False	Primary	11469818	535
536	Edwardhaven	G8D 4DT	SS1P 7BD		11471903	["Studio 8", "Dixon viaduct"]	False	Primary	11471903	536
537	M5U 7PF		SG01 8FX		11472336	["68 Smith mountains", "Garrybury"]	False	Primary	11472336	537
538	Smithview	L7 3UF	L0T 6NT		11472365	["Flat 50", "Carol vista"]	False	Primary	11472365	538
539	Thomasport	GU1 1BN	W2K 1BS		11474279	["Studio 16a", "Duffy vista"]	False	Primary	11474279	539
540	S3B 2GJ		S05 4QR		11479865	["0 Dennis brook", "East Gary"]	False	Primary	11479865	540
541	OL46 3UR		SO6H 6GT		11482204	["97 Pearson view", "Mooremouth"]	False	Primary	11482204	541
542	Waltersside	L75 0FQ	L0T 1UR		11482855	["Studio 63A", "Sarah prairie"]	False	Primary	11482855	542
543	SW2 0QS		M4 1BF		11484153	["1 Paul street", "North Cameronstad"]	False	Primary	11484153	543
544	Richardsstad	E5E 5ZT	SR7 4BJ		11485012	["Studio 80D", "Gordon road"]	False	Primary	11485012	544
545	SN30 3YQ		OX2 9ZT		1148646T	["82 Dale shores", "Simonfort"]	False	Primary	1148646T	545
546	Deniston	B4D 1DR	EN4 4PU		1148778T	["Flat 2", "Timothy rest"]	False	Primary	1148778T	546
547	S8 1RF		G57 8SG		11488252	["15 Bailey glen", "West Sean"]	False	Primary	11488252	547
548	Goddardview	SL28 0LZ	G9 3PW		11488465	["Flat 4", "Frank plaza"]	False	Primary	11488465	548
549	Clarketown	TS1V 1UF	G2D 8BZ		11490233	["Studio 4", "Bray squares"]	False	Primary	11490233	549
550	SW0E 4GG		CO4N 5BF		11492297	["7 Sian prairie", "West Sarah"]	False	Primary	11492297	550
551	L85 4NT		TF1 6JP		11497854	["6 Hicks rue", "Harveyland"]	False	Primary	11497854	551
552	WR6 6XS		B1 8UW		11499503	["10 Singh plain", "Lake Debra"]	False	Primary	11499503	552
553	Baileyland	HD2M 6AB	LE57 4FY		11500820	["Studio 58", "Hunt lodge"]	False	Primary	11500820	553
554	SP4 2UY		KW79 5ZJ		11501420	["82 Smith highway", "Wendyville"]	False	Primary	11501420	554
555	New Mauriceville	KT2 2FJ	TQ0N 6RE		11501823	["Flat 6", "Paul mills"]	False	Primary	11501823	555
556	New Leah	WC55 5RU	G8 3YP		11503075	["Flat 20", "Daniel mills"]	False	Primary	11503075	556
557	New Barbaraside	E82 9BN	E34 0WL		11503864	["Flat 9", "Dunn burg"]	False	Primary	11503864	557
558	East Pamela	GU5R 3ZS	L5 5ZZ		11503933	["Studio 52l", "Griffiths mission"]	False	Primary	11503933	558
559	NN7V 4WW		L68 3ZS		11504372	["943 Brown freeway", "Gillianshire"]	False	Primary	11504372	559
560	West Julianland	N4W 1DX	ST5 7HZ		11505899	["Studio 2", "Walsh harbor"]	True	Primary	11505899	560
561	WF57 5TF		L5 5ST		11508154	["379 Lindsey road", "Lake Shannon"]	False	Primary	11508154	561
562	West Rosemary	B6S 8ND	BT08 4YX		11508534	["Studio 17", "Taylor wall"]	False	Primary	11508534	562
563	Jonesport	DT5 0HL	M70 8QY		11511639	["Studio 93Z", "Brown mission"]	False	Primary	11511639	563
564	GY0B 0TJ		S2C 6FE		11517353	["1 Johnson hills", "Jodieborough"]	False	Primary	11517353	564
565	DN3 4BL		W5 0BZ		11521916	["65 Page mountains", "North Paigeberg"]	False	Primary	11521916	565
566	Port Alextown	HX7V 9EP	WS4 1DY		11522637	["Studio 2", "Brown radial"]	False	Primary	11522637	566
567	EN7 2XG		E2 3RF		11522643	["821 Gardiner fall", "North Louisehaven"]	False	Primary	11522643	567
568	N2T 1XW		S3G 6GJ		11526707	["375 Holden drive", "North Jeremy"]	False	Primary	11526707	568
569	East Barrychester	WS30 2XE	LL8 7FQ		11527215	["Flat 93c", "James via"]	False	Primary	11527215	569
570	B4 6TF		TS69 0YJ		11530107	["18 Wright manors", "Whitefurt"]	False	Primary	11530107	570
571	Lake Karen	B3F 4HU	N4 7ZF		11536092	["Studio 86A", "Geraldine prairie"]	False	Primary	11536092	571
572	IP5 0UU		S7G 0AQ		11540897	["018 Burton square", "Kingborough"]	False	Primary	11540897	572
573	Victoriaberg	M5C 2SH	L0 0GG		11545786	["Studio 43m", "Gordon crescent"]	False	Primary	11545786	573
574	W0T 3FB		N8T 3UQ		11546432	["89 Ricky trail", "O'Brienton"]	False	Primary	11546432	574
575	EX8 4ZU		G9 0AG		1155000T	["07 Dylan cliff", "Dannyfurt"]	False	Primary	1155000T	575
576	W98 5GQ		SA0 7TE		11550270	["43 Stanley expressway", "Jonesview"]	False	Primary	11550270	576
577	North Glennshire	ST8E 5XP	S1F 6LW		11553037	["Flat 98", "Jennifer field"]	False	Primary	11553037	577
578	Kyleshire	BS8 7JQ	CH49 8HH		11558554	["Studio 4", "Antony shoal"]	False	Primary	11558554	578
579	East Joseph	G53 6LP	LE2W 4TW		11560126	["Flat 14", "Moran trail"]	False	Primary	11560126	579
580	JE4 1EW		TS0 9GJ		11563314	["086 Foster course", "Port Charlie"]	True	Primary	11563314	580
581	New Rachaelfort	PO6 6WH	E1 8AR		11565044	["Flat 73k", "Francis port"]	False	Primary	11565044	581
582	M9 9HQ		CF1 7FE		1156889T	["65 Craig club", "New Carol"]	False	Primary	1156889T	582
583	WN30 8TL		N2 1PL		11569195	["04 Sharp terrace", "North Toby"]	False	Primary	11569195	583
584	Sullivanfort	TN08 7HR	G5 7FZ		11577229	["Studio 8", "Sylvia glen"]	False	Primary	11577229	584
585	E8C 9QJ		UB0 1AD		11583718	["6 Cole club", "South Debra"]	False	Primary	11583718	585
586	East Patrick	IV1 8RG	GY30 4AF		11584474	["Studio 84", "Wilson tunnel"]	False	Primary	11584474	586
587	B9 9XA		SN4 2HS		11609075	["1 Evans square", "New Aimeetown"]	False	Primary	11609075	587
588	Frenchmouth	TF52 5UQ	LL3 0FQ		11614970	["Flat 22L", "Olivia dale"]	False	Primary	11614970	588
589	W6 4NE		HA1 4LY		11615725	["0 Bennett shore", "Alistad"]	False	Primary	11615725	589
590	M8J 2BS		IP2 6FQ		11617864	["369 Bryan crescent", "Aimeeton"]	False	Primary	11617864	590
591	Burgessfurt	L4 9NR	HX5Y 4BU		11623351	["Studio 47", "Campbell cliffs"]	False	Primary	11623351	591
592	North Helen	YO68 8TW	S79 1EN		11636695	["Flat 4", "Shannon islands"]	False	Primary	11636695	592
593	SW06 8DE		S6 6XL		13611710	["82 Brett curve", "North Vanessa"]	False	Primary	13611710	593
594	Briantown	L56 4DN	N1 3EB		11661807	["Flat 61", "Taylor mission"]	False	Primary	11661807	594
595	North Vanessa	SY0X 1XA	PL3B 2TR		11698923	["Flat 90", "Peters ferry"]	False	Primary	11698923	595
596	DA75 7BT		IM66 9ZL		11717534	["759 Antony row", "West Mohamed"]	False	Primary	11717534	596
597	G9A 9GD		E0G 5BB		11742249	["4 Tracey harbors", "Franklinland"]	False	Primary	11742249	597
598	Natalieside	E8J 8QB	BR5V 5ZH		11745967	["Flat 33", "Brady greens"]	False	Primary	11745967	598
599	Lake Nicoleborough	B4W 6TN	W81 8XJ		11757882	["Flat 34F", "Coates inlet"]	False	Primary	11757882	599
600	ZE3W 1PE		L69 7JL		11760532	["756 Parry circles", "Lake Sylvia"]	False	Primary	11760532	600
601	South Nicola	DD80 5TL	E1 5AT		11781162	["Studio 99", "Jasmine extensions"]	False	Primary	11781162	601
602	KA33 4ZT		HA51 0SE		11784511	["357 Julie mountains", "Georgiaborough"]	False	Primary	11784511	602
603	Rachelfurt	DT5 3JY	G0 2SU		11790827	["Studio 3", "Lewis forge"]	False	Primary	11790827	603
604	BS6 3AU		G6W 1WL		11798910	["2 Bradley walks", "New Sharon"]	False	Primary	11798910	604
605	PO13 3EQ		M8H 0FE		11844790	["688 Robin cove", "South Cameron"]	False	Primary	11844790	605
606	Janeborough	BS5 4ZS	IP0W 9JB		11854986	["Flat 02D", "Jemma forks"]	False	Primary	11854986	606
607	W4 0TJ		BD96 8QB		11866428	["7 Katherine turnpike", "Allanton"]	False	Primary	11866428	607
608	SM4 0XJ		N9C 1DT		11886585	["1 Butcher forest", "East Fionaview"]	False	Primary	11886585	608
609	DG7 8GG		KY0 8RQ		1194777T	["66 Richardson lights", "Mistrybury"]	False	Primary	1194777T	609
610	S8 1UH		N7 2XA		11956501	["2 Welch meadows", "North Sophiefort"]	False	Primary	11956501	610
611	Jennabury	E02 2GY	B5D 3FH		11957337	["Studio 68F", "Flynn loop"]	False	Primary	11957337	611
612	DT2P 0YY		B4S 0YU		12006612	["12 Reynolds lane", "East Carl"]	False	Primary	12006612	612
613	WF2X 8TL		N7 4RZ		1202119T	["333 Amber stream", "Port Jasminehaven"]	False	Primary	1202119T	613
614	G10 8WJ		M9 9YL		12021200	["7 Collins shoals", "Daviesshire"]	False	Primary	12021200	614
615	M4G 1XU		L7 4ZA		12022071	["61 Ashley club", "Port Deborahborough"]	False	Primary	12022071	615
616	N2H 0TW		E55 1PU		12069348	["1 Kent freeway", "New Hughberg"]	False	Primary	12069348	616
617	E69 4RG		SR7 1AT		12080655	["14 Hudson rapid", "West Harriet"]	False	Primary	12080655	617
618	LA3X 8XF		M9D 1QX		12120852	["443 Smith crossroad", "West Linda"]	False	Primary	12120852	618
619	B0 0YU		L4K 1LE		12141476	["0 Williams vista", "Port Ellie"]	False	Primary	12141476	619
620	Port Rita	DG18 2YL	B81 0RG		1216808T	["Studio 30n", "Robertson port"]	False	Primary	1216808T	620
621	South Suzanne	GY4A 9UT	S0G 4EH		12173962	["Flat 3", "King mills"]	False	Primary	12173962	621
622	North Duncan	S70 1DJ	TD5 2FX		12197359	["Flat 48", "Williams rapids"]	False	Primary	12197359	622
623	South Ruthhaven	NW8 0SF	HS2 4NA		12217002	["Flat 45", "Joshua gardens"]	False	Primary	12217002	623
624	M9E 6ZF		NE9E 7NW		12232172	["6 Mohammed hollow", "Lake Carolemouth"]	False	Primary	12232172	624
625	East Lucy	PE7E 7WT	B9 3UH		12233313	["Flat 85", "Waters spring"]	False	Primary	12233313	625
626	BL2R 9ZH		G5W 5PX		12244697	["402 Simon locks", "Andreaport"]	False	Primary	12244697	626
627	Baxterborough	TF0 4WD	BN9Y 2ZH		12269247	["Studio 75", "Woodward dale"]	False	Primary	12269247	627
628	Phillipsfurt	BL86 6DS	SW4 6JP		12304250	["Flat 4", "Vanessa rue"]	False	Primary	12304250	628
629	Howarthmouth	G7E 4HX	SN3X 3GG		12308798	["Flat 61", "Lucas springs"]	False	Primary	12308798	629
630	L6 4DN		TQ8X 5HX		12319047	["1 Hopkins via", "South Damianhaven"]	False	Primary	12319047	630
631	Marshallport	E54 5AH	SE64 6QQ		12322901	["Studio 7", "Eric terrace"]	False	Primary	12322901	631
632	KY61 4WP		UB86 0TP		12379718	["75 Jennifer pine", "Port Ronald"]	False	Primary	12379718	632
633	Evansland	B8E 7LH	LE7Y 6SA		12417667	["Studio 57", "Townsend ridge"]	False	Primary	12417667	633
634	Natashaville	W7 1HR	AL8 6GP		12422681	["Flat 18y", "Ruth crossroad"]	False	Primary	12422681	634
635	Patelchester	S03 8FU	HG5B 7GA		12441454	["Studio 41", "Eileen pine"]	False	Primary	12441454	635
636	BB3H 3HN		G53 7HQ		12454585	["6 Dean dam", "South Kieran"]	True	Primary	12454585	636
637	S07 7ZF		CB28 1AD		12455323	["6 Oliver estates", "New Douglasborough"]	False	Primary	12455323	637
638	Ashleyview	W81 9JB	M3 6PF		12485221	["Studio 25y", "Clarke crest"]	False	Primary	12485221	638
639	Robertsonmouth	N1 9EJ	ST0 9JA		12488795	["Studio 3", "Charles mews"]	False	Primary	12488795	639
640	East Samuel	M00 8YL	W7F 2GY		12500332	["Studio 7", "Suzanne islands"]	False	Primary	12500332	640
641	Martinstad	E7A 7AZ	DY14 7DN		12506230	["Studio 36A", "Julian skyway"]	False	Primary	12506230	641
642	Port Cherylview	E64 5EH	G1 8EA		12509308	["Flat 03", "Ryan stravenue"]	False	Primary	12509308	642
643	DN4H 5JY		KY76 5FB		12515538	["063 Smith manors", "Leeville"]	False	Primary	12515538	643
644	New Andrew	L8W 9BR	LU9 5AB		12566705	["Studio 82D", "Jordan parkway"]	False	Primary	12566705	644
645	RG1M 9FE		HD66 9TN		12575599	["410 Julian islands", "Miahbury"]	False	Primary	12575599	645
646	Port Naomiview	E95 6TH	W55 7BA		12622608	["Flat 34V", "Barber centers"]	False	Primary	12622608	646
647	HU6 6TT		DG2Y 3JU		12624632	["099 Noble island", "Lake Maxchester"]	False	Primary	12624632	647
648	Rachaelmouth	E7 9PJ	SM4 2NW		12668301	["Flat 05N", "Haynes burgs"]	False	Primary	12668301	648
649	L6D 6JN		G7 2XX		12670530	["204 Gordon hollow", "Roybury"]	False	Primary	12670530	649
650	SW0 8BR		L74 5WF		12670887	["431 Begum via", "Lawrenceton"]	False	Primary	12670887	650
651	W5 2GE		ME15 6ZH		1268922T	["354 Bryan flats", "Port Mariebury"]	False	Primary	1268922T	651
652	Daviston	HD5P 0XU	E1D 6JD		12693356	["Flat 83", "Ashley place"]	False	Primary	12693356	652
653	EH9B 0ZP		BH5V 4PN		12693483	["4 Raymond walk", "Markshire"]	False	Primary	12693483	653
654	Jacobville	M38 4JQ	CB15 7EE		12704013	["Flat 3", "Marc stream"]	False	Primary	12704013	654
655	W5W 5BU		B2G 9QX		12704474	["9 Benson loaf", "West David"]	False	Primary	12704474	655
656	L54 3HE		UB0 6YR		12709910	["116 Lloyd via", "Smithton"]	False	Primary	12709910	656
657	PE5 9JE		L76 8JW		12716400	["71 Lloyd streets", "Martinhaven"]	False	Primary	12716400	657
658	HG35 2JS		B4 5FZ		12725150	["19 Lorraine cove", "West Oliviaport"]	False	Primary	12725150	658
659	Morrisport	L93 2QA	SL53 7ES		12768501	["Studio 82V", "Benjamin squares"]	False	Primary	12768501	659
660	South Vincentstad	M9 6DB	W29 6JJ		12768927	["Flat 6", "Carly crossing"]	False	Primary	12768927	660
661	New Victorport	W9 9BE	M3 3NY		1277117T	["Flat 77", "Nicole squares"]	False	Primary	1277117T	661
662	WD6 2DN		S9 5NU		12777510	["2 Frank parkways", "North Jack"]	False	Primary	12777510	662
663	HD34 0HS		GU38 6YR		12779384	["529 Banks groves", "Malcolmmouth"]	False	Primary	12779384	663
664	Williamshaven	LN0 3DQ	E9 3RF		12784311	["Studio 49", "Barnes forges"]	False	Primary	12784311	664
665	W1 5AU		BS73 8EX		12795770	["775 Chloe drives", "Lake Josephview"]	False	Primary	12795770	665
666	L70 7TG		S7 7QN		12797033	["72 Jones stravenue", "East Staceyland"]	False	Primary	12797033	666
667	Walshland	S42 4XN	FY8A 9QH		1280494T	["Studio 05", "Lawrence keys"]	False	Primary	1280494T	667
668	MK5P 3SL		E2 3RA		12808842	["7 Heather divide", "Briggschester"]	False	Primary	12808842	668
669	Buckleyberg	IP9 3GU	EH3 7ZX		12826975	["Studio 26", "Vincent meadows"]	False	Primary	12826975	669
670	WC0Y 5QS		KY94 6FT		12839812	["54 Maurice views", "West Simonton"]	False	Primary	12839812	670
671	New Rita	N37 5HF	L5U 3SQ		12844958	["Flat 91", "Owen estates"]	False	Primary	12844958	671
672	M5G 7NE		SE3V 4UB		12855789	["3 White forge", "North Elliotchester"]	False	Primary	12855789	672
673	LL3E 0XG		BD5 7RH		1285669T	["850 Gary inlet", "North Glenberg"]	False	Primary	1285669T	673
674	L8B 7FN		BL8 4JP		12878552	["942 Shannon isle", "Scottshire"]	False	Primary	12878552	674
675	Port Michaelfort	GY5R 0ZY	S4 3LL		1288073T	["Studio 51T", "Tucker point"]	False	Primary	1288073T	675
676	WA4N 8QA		G63 2PR		12882401	["124 Graeme cove", "Emilystad"]	False	Primary	12882401	676
677	Denisshire	E5 8BA	WF0 5QN		12885508	["Flat 0", "Lynch roads"]	False	Primary	12885508	677
678	Slaterhaven	GL0E 8QF	B3U 5TQ		12886984	["Flat 0", "Owen keys"]	False	Primary	12886984	678
679	BB49 1QH		E38 2WB		12898213	["309 Ward fords", "O'Connorton"]	True	Primary	12898213	679
680	Leeland	N3H 0US	W41 6SX		12912465	["Flat 2", "Fisher cove"]	False	Primary	12912465	680
681	GL5 1WF		HS6W 1HT		12925832	["639 Charlie lakes", "Janemouth"]	False	Primary	12925832	681
682	Ellisberg	LN60 3QT	CT5N 9UH		12936323	["Studio 50b", "Walker square"]	False	Primary	12936323	682
683	Taylorport	RG3R 3PE	RG93 9UJ		1294953T	["Studio 10", "Antony fields"]	False	Primary	1294953T	683
684	M8W 2HE		M8F 6GL		12952628	["3 Leah mountain", "New Leonard"]	False	Primary	12952628	684
685	E95 2LR		S86 7YY		12986199	["3 Thomas locks", "Huntshire"]	False	Primary	12986199	685
686	New Gary	ZE6R 8DA	N3 8SG		13005455	["Studio 0", "Marilyn radial"]	False	Primary	13005455	686
687	North Maria	S99 0SU	M5G 7AQ		13006913	["Flat 3", "White centers"]	False	Primary	13006913	687
688	West Deniseville	SN64 8AU	PO8 3EB		13034690	["Flat 4", "Gary park"]	True	Primary	13034690	688
689	EX89 4ZX		N0K 9RZ		13044788	["5 Tracey path", "South Maria"]	False	Primary	13044788	689
690	FK0B 2HU		TD71 1PX		13045198	["301 Tracy groves", "New Bethburgh"]	False	Primary	13045198	690
691	North Sandraside	IP5 1PB	TA5 3PJ		13058640	["Flat 27Q", "Holly mountains"]	False	Primary	13058640	691
692	North Tomland	LD7X 2WY	N56 5PS		13076410	["Flat 1", "Charlene fords"]	False	Primary	13076410	692
693	M6G 7JS		W2J 0GX		13082997	["1 Wendy keys", "West Charlotteburgh"]	False	Primary	13082997	693
694	West Bryan	NN2 8BA	N6S 8QX		13093845	["Flat 00", "Law inlet"]	False	Primary	13093845	694
695	GY3 2SD		S8J 0LJ		13110922	["69 Howard field", "Robinsonstad"]	False	Primary	13110922	695
696	M9E 5QA		B2 8WX		13131258	["005 Sarah squares", "New Michael"]	False	Primary	13131258	696
697	West Alanton	M9 2PH	G5 4ZU		13137156	["Studio 77", "Wyatt springs"]	False	Primary	13137156	697
698	South Christopherfort	E21 5NB	G8H 1FH		13140618	["Studio 08", "Kieran lake"]	False	Primary	13140618	698
699	S4 8YD		MK0E 4FE		13157543	["581 Griffiths falls", "North Daleview"]	False	Primary	13157543	699
700	Caroleland	S4H 1QW	SK6 5RA		13174794	["Flat 9", "Gill village"]	False	Primary	13174794	700
701	Websterhaven	N8 8UT	E2S 5RW		13193711	["Studio 25t", "Martin terrace"]	False	Primary	13193711	701
702	G60 4BB		WV79 3EH		13195959	["1 Humphreys court", "West Anne"]	False	Primary	13195959	702
703	E06 0SY		TS90 7ZW		13198030	["919 Henry drive", "Fionamouth"]	False	Primary	13198030	703
704	L8 2YU		L8F 3ZW		13218462	["3 Pritchard unions", "New Lindaburgh"]	False	Primary	13218462	704
705	Freemanchester	S09 5XB	CR0A 9XQ		13233643	["Flat 50", "Baker pines"]	False	Primary	13233643	705
706	Edwardsfort	SE8 3QG	B62 5SS		13258619	["Studio 2", "Fiona well"]	False	Primary	13258619	706
707	S95 5NB		E5K 4YD		13259818	["224 Price forest", "North Janeberg"]	False	Primary	13259818	707
708	CB02 7JW		JE0P 2UP		13260762	["346 Weston station", "West Francesca"]	False	Primary	13260762	708
709	NN0 0XD		DG6 2WU		13262336	["770 Alice forest", "Deanton"]	False	Primary	13262336	709
710	New Kathleenview	UB6R 4SB	RM9N 4HF		13263316	["Studio 24", "Tom street"]	False	Primary	13263316	710
711	TD4 3TE		W80 8NZ		13272728	["2 Geraldine view", "West Victoria"]	False	Primary	13272728	711
712	SO99 7SH		S27 8PQ		13273645	["5 Joshua forge", "Phillipstown"]	False	Primary	13273645	712
713	Julieburgh	S24 2ES	HA8N 1SR		1327533T	["Studio 72", "Tracey streets"]	False	Primary	1327533T	713
714	N73 2YY		PL7 8TQ		13280481	["68 Patterson burg", "Jonathanfort"]	False	Primary	13280481	714
715	ML86 9GQ		B0 9RG		13305888	["6 Dyer isle", "Joshmouth"]	False	Primary	13305888	715
716	E7D 2RJ		N3B 7SX		1330853T	["2 Francesca spurs", "West Gerard"]	False	Primary	1330853T	716
717	Bensontown	N5 1GE	G35 5EQ		13318495	["Flat 17H", "Ali forks"]	False	Primary	13318495	717
718	Scotthaven	PO2 4WA	OX19 3LS		13323382	["Flat 22N", "Natalie rest"]	False	Primary	13323382	718
719	Shaunbury	CM15 3JU	JE1 0XS		13384618	["Studio 32", "Lawrence mews"]	False	Primary	13384618	719
720	W7 6XB		N1 7XE		1339115T	["2 Hussain inlet", "Francescaburgh"]	False	Primary	1339115T	720
721	New Victorburgh	ST3X 3ZZ	L6 4PX		13391270	["Flat 78", "Richards ferry"]	False	Primary	13391270	721
722	Martinfurt	L0 8HE	W5 0NS		13392486	["Flat 05u", "Edward creek"]	False	Primary	13392486	722
723	W0 8FB		G72 3ZH		13397421	["35 Bishop forge", "North Josephineville"]	False	Primary	13397421	723
724	DH77 9TY		IV1 1RX		13399214	["01 Keith shore", "Port Alexandra"]	False	Primary	13399214	724
725	M5H 1QA		IP1H 9LW		13400122	["95 Michelle camp", "Lake Kayleigh"]	False	Primary	13400122	725
726	Russellstad	B2 5US	L5 3DB		13402641	["Studio 0", "Welch hollow"]	False	Primary	13402641	726
727	North Janettown	BS4 4NH	WN2 7LE		13404388	["Studio 55k", "Catherine islands"]	False	Primary	13404388	727
728	Longtown	L63 2NQ	B15 3EA		13404808	["Studio 71U", "Burton stravenue"]	False	Primary	13404808	728
729	Lake Edwardborough	SO4 3WP	M2 2ZY		13409133	["Flat 95d", "Helen island"]	False	Primary	13409133	729
730	CB9 8JP		B52 5AT		13410324	["97 Douglas coves", "Mitchellhaven"]	False	Primary	13410324	730
731	Tylermouth	W6T 5YX	L1 7AS		13411120	["Flat 82B", "Howard plaza"]	False	Primary	13411120	731
732	Port Joetown	B7 0QQ	G7 3AH		13417375	["Studio 8", "Lisa divide"]	False	Primary	13417375	732
733	Webbchester	L8A 6BX	SW59 4EW		13419744	["Studio 12Q", "Bernard village"]	False	Primary	13419744	733
734	UB6V 2NR		N7 9LT		13420267	["0 Evans keys", "Patriciachester"]	False	Primary	13420267	734
735	L59 2FN		E3K 2TZ		13420388	["50 Amber rest", "Brendahaven"]	False	Primary	13420388	735
736	Martynfurt	M3 4ZE	W0W 9SX		13432648	["Studio 75l", "Patrick parks"]	False	Primary	13432648	736
737	Greenwoodburgh	HD04 1LW	AB5B 4TA		13442384	["Studio 72a", "Bell bridge"]	False	Primary	13442384	737
738	S0S 7GE		G43 7NF		13448593	["3 Roberts ports", "New Leah"]	False	Primary	13448593	738
739	North Helenmouth	CW3A 1GF	EN51 4ZA		13448996	["Studio 42d", "Davis summit"]	False	Primary	13448996	739
740	W5 0TJ		KY5B 6ZA		1345321T	["70 Conor key", "Wilsonview"]	False	Primary	1345321T	740
741	Barrettton	BL70 3BY	M4 7JJ		13456190	["Flat 31r", "Jayne circle"]	False	Primary	13456190	741
742	Amandaport	BN45 9NX	G7 3DS		13465129	["Flat 12a", "Abigail mountain"]	False	Primary	13465129	742
743	TD82 7RH		TW0M 9XJ		13465498	["4 Joe key", "New Louis"]	False	Primary	13465498	743
744	Port Mollystad	NN2 4ZY	OL7 9TG		1346927T	["Studio 71d", "Duncan ranch"]	False	Primary	1346927T	744
745	Crawfordmouth	NW5 9LF	RG34 4WX		13474979	["Studio 24", "Ashley courts"]	False	Primary	13474979	745
746	BH2 1RS		G1 4BG		13480535	["597 Rachael springs", "Doyleborough"]	False	Primary	13480535	746
747	WA33 3FB		AB8R 8JX		13481135	["11 Foster cliff", "New Clareview"]	False	Primary	13481135	747
748	BH4 1DD		L3K 5YB		13482478	["5 Heath plaza", "Claytonshire"]	False	Primary	13482478	748
749	New Keithville	HX37 3PE	E41 1HJ		13487465	["Flat 9", "Mandy river"]	False	Primary	13487465	749
750	BB6 9TB		TQ8 7AJ		13493919	["80 Giles falls", "New Williammouth"]	False	Primary	13493919	750
751	DG6 7WL		BA9M 6PE		13493983	["2 Albert courts", "East Ameliafort"]	False	Primary	13493983	751
752	L9 5WF		DA09 6RS		13496762	["5 Norris point", "Richardberg"]	False	Primary	13496762	752
753	Wendyside	E2 2FA	SG0 7NB		13498215	["Flat 0", "Donald mountains"]	False	Primary	13498215	753
754	West Samuelberg	CR8 7WF	BB53 8GH		13500437	["Flat 9", "Ashleigh hollow"]	False	Primary	13500437	754
755	Oliviashire	M0 8JY	N25 4UY		13503032	["Studio 9", "Williams freeway"]	False	Primary	13503032	755
756	B9D 3GT		NW0P 2YF		13506940	["90 Jones estate", "New Sarah"]	False	Primary	13506940	756
757	HG9 9TB		E96 3LA		13509840	["637 Samuel keys", "Carolinebury"]	False	Primary	13509840	757
758	New Hollyfort	DY0N 4AN	G19 9EX		13511527	["Studio 90d", "Davies pines"]	False	Primary	13511527	758
759	Port Charlotteberg	PL1B 8LQ	MK4A 5ZJ		1351233T	["Studio 93c", "Wilkinson motorway"]	False	Primary	1351233T	759
760	Teresamouth	EH52 5PS	G6E 3QW		13518100	["Flat 99", "Paige gateway"]	False	Primary	13518100	760
761	Amandaburgh	S0 3GQ	DD66 7NS		13522329	["Studio 88K", "Amber fall"]	False	Primary	13522329	761
762	E0T 9RR		GY9 1SP		13524445	["09 Natalie creek", "Gordonfurt"]	False	Primary	13524445	762
763	West Bradleyville	S7S 6YL	L9S 4NE		13526405	["Flat 38", "David river"]	False	Primary	13526405	763
764	Judithview	W58 5FN	NG0N 1JG		13526463	["Studio 69", "Green creek"]	False	Primary	13526463	764
765	GY4N 8HH		LD24 7TZ		13526774	["577 Hopkins unions", "Alanport"]	False	Primary	13526774	765
766	L24 6ZE		FY6 4BY		13527247	["956 O'Neill squares", "Bullfurt"]	False	Primary	13527247	766
767	Lake Iain	SR45 2ZD	MK43 6ZX		13528607	["Studio 13", "Johnson club"]	False	Primary	13528607	767
768	IV0X 5RD		CF21 9AW		13538372	["8 Wilson radial", "New Johnhaven"]	False	Primary	13538372	768
769	M0 0JR		N4 7NP		13538591	["1 Fox harbors", "Johnsonfurt"]	False	Primary	13538591	769
770	South Matthewview	CH2X 0RE	NE5B 1QG		13538619	["Studio 0", "Marian grove"]	False	Primary	13538619	770
771	Ronaldbury	HP68 3UF	SR1M 5QH		13539594	["Flat 97", "Andrew expressway"]	False	Primary	13539594	771
772	KY0W 4FB		M74 8GW		13544204	["561 Collins crossing", "Taylorstad"]	False	Primary	13544204	772
773	B49 2TJ		EH9Y 5DT		13546297	["545 Wilson spur", "Wayneville"]	False	Primary	13546297	773
774	L7A 0NY		W2W 9GU		13546798	["8 Morris road", "Nolanborough"]	False	Primary	13546798	774
775	B1 9JS		SG2 1EL		13546936	["15 Lane forges", "South Rhysfort"]	False	Primary	13546936	775
776	Brianville	EH61 8QR	G5A 4ZE		13547559	["Flat 02", "Georgia corners"]	False	Primary	13547559	776
777	West Jakefort	N66 1SY	FK7 5FS		13547686	["Flat 75c", "Richard circles"]	False	Primary	13547686	777
778	B13 6JR		HX89 1SZ		13547801	["8 Vincent neck", "Chapmanton"]	False	Primary	13547801	778
779	Garnerbury	NW00 3JW	NN0R 5PL		13548551	["Studio 23", "Thompson neck"]	False	Primary	13548551	779
780	Port Wendy	DE92 2QS	UB3A 6TL		13554746	["Studio 7", "Louis oval"]	False	Primary	13554746	780
781	South Deborah	CW06 9ZU	HD3 8FZ		13556332	["Flat 33S", "Rowley junctions"]	False	Primary	13556332	781
782	BT2 5UN		NR35 9RD		13558995	["804 Wilson crest", "North Jasmine"]	False	Primary	13558995	782
783	L8 9ZF		FY7 6GL		13559860	["227 Shannon avenue", "Ashleighmouth"]	False	Primary	13559860	783
784	S6W 2HX		G2 7ZJ		13560544	["93 Fletcher trafficway", "West Donaldberg"]	False	Primary	13560544	784
785	Boltonton	S91 3ZX	W5U 9XE		13560636	["Flat 1", "Moss islands"]	False	Primary	13560636	785
786	West Hollyburgh	ST72 4JE	PR3 5DP		13560918	["Studio 8", "Tracey village"]	False	Primary	13560918	786
787	E5A 0NN		S0 0JY		13561524	["38 Bell street", "Lake Billyland"]	False	Primary	13561524	787
788	PO1Y 3GP		EC7 1BW		13561639	["27 Turner flat", "Port Rhysburgh"]	False	Primary	13561639	788
789	RG3 1TQ		G2T 5UQ		13562090	["4 Jay throughway", "South Matthewberg"]	False	Primary	13562090	789
790	New Juliemouth	KA3 0HS	NN2W 8DE		13562654	["Studio 7", "Leon crossing"]	False	Primary	13562654	790
791	Susanchester	RM40 6RH	G7A 2GU		13565957	["Studio 23X", "Smith square"]	False	Primary	13565957	791
792	New Henry	G49 2BW	S28 1GD		13567376	["Studio 7", "Denise forest"]	False	Primary	13567376	792
793	DL6 7SG		SP3 0WW		13567497	["935 Day street", "Bradshawland"]	False	Primary	13567497	793
794	New Brian	WF26 2TN	N4B 4NY		13567819	["Studio 3", "Cheryl forges"]	False	Primary	13567819	794
795	E9U 5XH		W90 7NH		1356793T	["404 Hughes dale", "Port Bradleyhaven"]	False	Primary	1356793T	795
796	Millsland	S26 0QZ	AB8 2GE		13568016	["Flat 6", "Clements wells"]	False	Primary	13568016	796
797	PO8P 7HR		W1 7QT		13568114	["152 Hollie field", "Lukeland"]	False	Primary	13568114	797
798	Port Maxborough	DN2 2DQ	S5 2ZU		13568552	["Studio 85", "Jessica brooks"]	False	Primary	13568552	798
799	WF1N 2SS		E50 4UE		13569866	["56 Melissa square", "Reynoldshaven"]	False	Primary	13569866	799
800	West Alisonmouth	NN9 0WX	L1 5ET		13570660	["Studio 59Y", "Henry parkways"]	False	Primary	13570660	800
801	NN68 8JP		E7K 5EQ		13570798	["241 Ali pine", "Michaelview"]	False	Primary	13570798	801
802	M3T 6GD		N2 8GA		13570896	["323 Smith square", "Marshton"]	False	Primary	13570896	802
803	E20 4AU		N3 2PP		13570994	["72 Rhys valleys", "Marshalltown"]	False	Primary	13570994	803
804	Lake Kathrynchester	B0 2PL	W1 3PZ		13571496	["Studio 5", "Lawson lake"]	False	Primary	13571496	804
805	Dickinsonmouth	WS0R 4YG	DT7 1UT		13571726	["Flat 59v", "Suzanne drive"]	False	Primary	13571726	805
806	IV0 2WP		N9F 0WG		13571974	["154 Gareth square", "Lindastad"]	False	Primary	13571974	806
807	Abdulview	W17 7XP	TN76 1JN		13572067	["Flat 18", "Rees green"]	False	Primary	13572067	807
808	Port Douglas	BR70 8FE	HA72 9RA		13572165	["Studio 29l", "Gordon mountain"]	False	Primary	13572165	808
809	Lake Duncanburgh	SR7 6UP	IP88 7SH		13572211	["Studio 25o", "Richards square"]	False	Primary	13572211	809
810	Declanmouth	M9B 5AJ	N2E 7PY		13572764	["Flat 03a", "Brown shoals"]	False	Primary	13572764	810
811	South Lucy	HP40 9GG	EC75 8ZA		13572856	["Flat 72o", "Jeremy glens"]	False	Primary	13572856	811
812	Randallborough	SG3E 9HP	S01 4FP		13573295	["Studio 19p", "Danielle overpass"]	False	Primary	13573295	812
813	N7 5AG		B7 5XW		13573410	["1 Allen mountains", "Ianport"]	False	Primary	13573410	813
814	M88 1WN		CW0B 2LF		13573715	["29 Duncan islands", "New Abbie"]	False	Primary	13573715	814
815	Williamshaven	WD6 9LY	WC96 0HA		13578754	["Studio 65b", "Hart mews"]	False	Primary	13578754	815
816	Christopherfurt	DY60 4QQ	YO92 8EZ		13581220	["Studio 1", "Sara motorway"]	False	Primary	13581220	816
817	B37 1UA		E07 9JY		13583192	["2 Jason manors", "Thomasmouth"]	False	Primary	13583192	817
818	Davidport	G8A 6HH	PA0 3GN		13611704	["Studio 08F", "Derek loaf"]	False	Primary	13611704	818
819	SP0 1TP		DL2 6NN		1361174T	["8 King neck", "South Ronald"]	False	Primary	1361174T	819
820	N7T 1EF		S47 9TF		13611756	["32 Skinner views", "Stephanieshire"]	False	Primary	13611756	820
821	Webbchester	N70 4JG	SA76 9LT		13611762	["Studio 5", "Dylan ridges"]	False	Primary	13611762	821
822	M2C 7YP		W00 7JJ		13611779	["28 Maria crescent", "Port Trevorhaven"]	False	Primary	13611779	822
823	Port Fionaport	E5U 6SJ	N7W 3QL		13611785	["Flat 47", "Lloyd roads"]	False	Primary	13611785	823
824	New Anthony	NP0 1GL	G7 6UQ		13611791	["Studio 28", "Amelia junction"]	False	Primary	13611791	824
825	W2 6HZ		W1 3BQ		13611802	["034 Amy estate", "Lake Frances"]	False	Primary	13611802	825
826	Paulahaven	E96 2LH	DT6A 6DW		13611819	["Studio 79", "Patrick ports"]	False	Primary	13611819	826
827	Joyceton	B3W 1XE	DA60 0NZ		13611825	["Studio 30", "Dale summit"]	False	Primary	13611825	827
828	New Martynburgh	BN2H 3XQ	G66 3HE		13611831	["Flat 70", "Marsh rest"]	False	Primary	13611831	828
829	South Ian	M0B 6QY	EC3 8WG		13611848	["Flat 00Y", "Abbie estates"]	False	Primary	13611848	829
830	Johnsontown	LD9 4SA	E7G 0ZB		13611854	["Flat 0", "Butler brook"]	False	Primary	13611854	830
831	Nortonfort	ML7 1ZW	HP2X 6HW		13611860	["Flat 68j", "Hayes plaza"]	False	Primary	13611860	831
832	FK0A 2GT		SP2 4YS		13611917	["30 Brandon villages", "Lake Yvonne"]	False	Primary	13611917	832
833	PR4 0DE		S36 1GJ		13612552	["707 Bates parkways", "Burrowsview"]	False	Primary	13612552	833
834	Barnesborough	BR8 0HR	W1J 2EP		13612569	["Studio 58", "Declan centers"]	False	Primary	13612569	834
835	S8B 4DP		S9K 8LS		13612575	["9 Howard crescent", "Rebeccaview"]	False	Primary	13612575	835
836	East Karlchester	W5B 0AH	W7 5DS		13612581	["Studio 50", "Anne island"]	False	Primary	13612581	836
837	M3D 3BQ		B7T 1BA		13612598	["96 Simon cape", "Paulamouth"]	False	Primary	13612598	837
838	Francesmouth	S1 9TU	L6C 0FA		13612609	["Flat 41", "Taylor wells"]	False	Primary	13612609	838
839	Edwardsstad	RH5 6GL	B3 9TD		13612615	["Flat 57", "Pauline view"]	False	Primary	13612615	839
840	PL3X 3SX		YO5B 1XW		13612621	["93 Hancock keys", "New Patrick"]	False	Primary	13612621	840
841	East Claire	W7 6NX	LE7 6BR		13612638	["Studio 24S", "Eric greens"]	False	Primary	13612638	841
842	TS65 1TW		L0 2PB		13612644	["724 Jacqueline burg", "Clarkeside"]	False	Primary	13612644	842
843	LS1 6LF		S6 6RT		13612650	["938 Rahman streets", "Butchertown"]	False	Primary	13612650	843
844	North Kelly	L55 2HA	KT5 7GF		94000393	["Studio 76M", "Smith lodge"]	False	Primary	94000393	844
845	New Benborough	NR0 3XJ	BL2 2JY		94000738	["Flat 37w", "Cooper parks"]	False	Primary	94000738	845
846	DG53 3BD		BL4B 0AZ		94001471	["052 Atkinson trafficway", "Jeanstad"]	False	Primary	94001471	846
847	E0T 9PG		E4W 2DJ		94003667	["2 Shah crescent", "Amandaview"]	False	Primary	94003667	847
848	GL61 6ZL		YO9H 9JR		9400409T	["8 Norton meadow", "New Charlottefurt"]	False	Primary	9400409T	848
849	Adrianmouth	BR16 8RG	ST0 8LG		94004169	["Studio 80", "Ward port"]	False	Primary	94004169	849
850	YO8 5TP		B81 8LT		94004780	["550 Luke key", "North Bernard"]	False	Primary	94004780	850
851	Williamsshire	S5 9WJ	IV0H 1NT		94006227	["Studio 00", "Mohamed station"]	False	Primary	94006227	851
852	DD5 2GH		SP67 3HA		94007582	["1 Bruce plain", "South Shaunland"]	False	Primary	94007582	852
853	DH6 5WL		B58 2ZZ		94007697	["292 Begum viaduct", "Charliestad"]	False	Primary	94007697	853
854	PR7V 8ZH		SA6W 8AU		9400971T	["522 Lewis mall", "Port Mollyfurt"]	False	Primary	9400971T	854
855	L5 7AH		FY7 6EP		94009939	["826 Josephine pine", "New Benhaven"]	False	Primary	94009939	855
856	New Sam	SS9 2ZX	S4A 3BZ		94012175	["Studio 79", "Williams parks"]	False	Primary	94012175	856
857	ST6N 1FA		IG0 6BY		94012682	["07 Reed cliffs", "Billyburgh"]	False	Primary	94012682	857
858	NR0R 4HP		CB25 2FA		9401326T	["5 Katy burg", "South Kayleigh"]	False	Primary	9401326T	858
859	Lake Matthewbury	G9 7LB	S8E 4WF		94013627	["Flat 97A", "Joseph burg"]	False	Primary	94013627	859
860	SW1Y 2RB		WR01 4YR		94016032	["6 Rosemary mountains", "North Francesshire"]	False	Primary	94016032	860
861	BS0E 2BH		RG1X 4EL		94016314	["82 Butler meadows", "West Elliottview"]	False	Primary	94016314	861
862	Port Elaineshire	BA0Y 7SP	W7 0SU		94017507	["Studio 82", "Ellis estate"]	False	Primary	94017507	862
863	Helenhaven	L38 8WX	NG06 8LX		94017513	["Flat 21b", "Kirsty oval"]	False	Primary	94017513	863
864	CF74 7GD		SE8 3SJ		94019859	["570 Alex cliff", "South Philipborough"]	False	Primary	94019859	864
865	M3 9XP		CH9 1FD		94020031	["238 Bird parkways", "Evansborough"]	False	Primary	94020031	865
866	Annehaven	L00 3UH	W5 0SL		94020895	["Studio 41i", "Gerard junction"]	False	Primary	94020895	866
867	Hardychester	S0 3PY	HR1W 3RU		94021339	["Flat 65", "Cook dam"]	False	Primary	94021339	867
868	HS5Y 3SJ		B3F 9EU		9402145T	["549 Stokes lodge", "Woodbury"]	False	Primary	9402145T	868
869	N6 4QH		BH9Y 5BP		94023680	["54 Trevor extensions", "Reynoldsview"]	False	Primary	94023680	869
870	E3 4HL		BH42 5SR		94024510	["63 Maurice walks", "New Thomaschester"]	False	Primary	94024510	870
871	Lake Charlie	W98 4GN	G2W 8FA		94026142	["Studio 1", "Kelly lock"]	False	Primary	94026142	871
872	SS5W 4FL		B3C 7YY		94026637	["1 Douglas parkways", "Port Lee"]	False	Primary	94026637	872
873	Jacksonland	B06 2EB	B5 4GJ		94026885	["Studio 44", "Duncan cape"]	False	Primary	94026885	873
874	Georgechester	G6D 4JN	M90 3LJ		94028799	["Flat 29A", "Leigh turnpike"]	False	Primary	94028799	874
875	North Joel	NW3 9XS	L95 6GZ		94029163	["Studio 8", "Hill ports"]	False	Primary	94029163	875
876	East Julie	L0 0BY	B2G 4NE		94029226	["Flat 30", "Smith passage"]	False	Primary	94029226	876
877	BT79 0XE		M3C 2ZR		94029255	["06 Rachael curve", "Martynmouth"]	False	Primary	94029255	877
878	BA1Y 6RL		L61 9BE		94029318	["82 Martin center", "Sarahburgh"]	False	Primary	94029318	878
879	CW5Y 1GJ		E52 0NZ		94029762	["28 Bradley highway", "East Jill"]	False	Primary	94029762	879
880	KW08 3PB		E3S 6AN		94031017	["570 Stewart groves", "Leannefort"]	True	Primary	94031017	880
881	North Simonhaven	NN8X 2ZS	DH98 1PT		94031196	["Studio 7", "Dean springs"]	False	Primary	94031196	881
882	Atkinsonberg	CT4Y 6RA	B5 2ZY		94031806	["Studio 51", "Howard isle"]	False	Primary	94031806	882
883	SM5 6ED		KA0Y 3TX		94032032	["66 Clare spring", "Lake Debraborough"]	False	Primary	94032032	883
884	New Sharonland	E45 8GW	HS95 3UU		94032199	["Studio 1", "Rachael canyon"]	False	Primary	94032199	884
885	G6F 1HT		CO6 6QA		94033219	["5 Leigh throughway", "Vincentland"]	False	Primary	94033219	885
886	E91 7YE		E3 3YF		94033571	["7 Marcus port", "West Frederickport"]	False	Primary	94033571	886
887	New Amelia	SK09 5QA	W9B 6ZH		94034044	["Flat 79T", "Claire cliffs"]	False	Primary	94034044	887
888	Port Ericchester	EC7H 1JZ	N4 1WL		94034453	["Studio 99O", "Martin mountain"]	False	Primary	94034453	888
889	Port Shirleychester	L6C 9FW	ML9 2UD		94035617	["Flat 3", "Crawford valleys"]	False	Primary	94035617	889
890	Brownview	S7 0FR	SW7N 1LX		94035842	["Flat 8", "Andrew cliffs"]	False	Primary	94035842	890
891	Victorside	TD68 6SA	S6 5NA		94036511	["Flat 59d", "Woodward loaf"]	False	Primary	94036511	891
892	Lake Johnbury	N07 1DE	HP4W 8QA		94036528	["Studio 7", "Miller turnpike"]	False	Primary	94036528	892
893	Smithshire	TW37 7QD	N4U 3GN		94036747	["Flat 13V", "Sam motorway"]	False	Primary	94036747	893
894	East Jean	E4 3YD	W3 0AP		94036868	["Flat 3", "Helen junctions"]	False	Primary	94036868	894
895	Singhton	N62 3XH	N2K 4QB		94037589	["Flat 5", "Mills prairie"]	False	Primary	94037589	895
896	East Marion	GU54 5JU	M8 4GW		94039929	["Flat 02", "Jones shore"]	False	Primary	94039929	896
897	Grantview	N57 7WF	PE64 4GF		94040677	["Studio 7", "Denis land"]	False	Primary	94040677	897
898	CM30 0UD		M4U 9NF		94041104	["33 Kelly route", "West Joanport"]	False	Primary	94041104	898
899	West Marc	M0E 5YF	LA3P 4UL		94041225	["Flat 15", "Martin port"]	False	Primary	94041225	899
900	S8 6YE		G0J 2ZQ		9404167T	["5 Daniel crescent", "West Amy"]	False	Primary	9404167T	900
901	B3 2QS		CW7 7GN		94041801	["6 Victoria fall", "Leeshire"]	False	Primary	94041801	901
902	Joannaside	E51 9RP	TD8W 9QQ		94042580	["Flat 43", "Charlie junctions"]	False	Primary	94042580	902
903	Westonfurt	S54 2DS	E03 8RH		94044102	["Studio 3", "Jones parks"]	False	Primary	94044102	903
904	CF08 1EY		OL2B 0ZD		9404438T	["175 Owens corners", "South Joseph"]	False	Primary	9404438T	904
905	B69 5UY		HR6 9ST		94044586	["7 Kelly mountains", "Port Gordon"]	False	Primary	94044586	905
906	E9 3RR		DD5M 8WU		94044718	["248 Joanne village", "Port Neil"]	False	Primary	94044718	906
907	West Frances	ME4 8FR	M3T 8TW		94047244	["Studio 1", "Lawrence plain"]	False	Primary	94047244	907
908	Alexandrastad	CM2A 6DX	E2E 8TF		94051698	["Flat 55S", "Garry course"]	False	Primary	94051698	908
909	West Garethhaven	M0A 9GA	G6J 5DY		94055780	["Flat 64", "Talbot circle"]	False	Primary	94055780	909
910	E5 7DD		E22 6ZQ		94056875	["42 Gemma isle", "West Janefurt"]	False	Primary	94056875	910
911	N0 4RU		M8 5JU		94058138	["94 Christian mountain", "Antonyfurt"]	False	Primary	94058138	911
912	PR6 0JT		E13 1JX		94061819	["968 Dale burgs", "Lake Francesfurt"]	False	Primary	94061819	912
913	New Bradleyside	DG6A 2NY	L4 3SZ		94064587	["Flat 2", "Nicole parks"]	False	Primary	94064587	913
914	M57 4QH		SY9A 6SU		94071048	["71 Oliver views", "Sylviashire"]	False	Primary	94071048	914
915	AL69 1XS		G13 1HA		9407151T	["13 Robert lakes", "Lake Maureenport"]	False	Primary	9407151T	915
916	Stewarttown	W3W 5RR	M06 2JJ		94074213	["Flat 01", "Foster rapid"]	False	Primary	94074213	916
917	SK11 3ZU		W4 6HA		94074985	["2 Shannon dale", "Lake Naomi"]	False	Primary	94074985	917
918	LS14 6ZX		SK7 4PU		94076375	["810 Hardy ramp", "Lake Geraldine"]	False	Primary	94076375	918
919	Lake John	PO18 3WH	NW66 3FH		94078030	["Studio 8", "Smith plaza"]	False	Primary	94078030	919
920	New Gillian	SG89 9FH	ML58 0RG		94078554	["Flat 49K", "Alexandra prairie"]	False	Primary	94078554	920
921	Annland	M2 1UH	CA29 2DF		94079626	["Flat 1", "Kate pass"]	False	Primary	94079626	921
922	East Sandrahaven	G1 8DZ	CV1N 2AX		94079655	["Studio 47", "Brown haven"]	False	Primary	94079655	922
923	Armstrongton	CV6A 5DH	TF78 0YZ		94082311	["Flat 61G", "Richards prairie"]	False	Primary	94082311	923
924	Susanmouth	G9H 7BD	BN4R 0ZN		94087154	["Flat 80e", "White spurs"]	False	Primary	94087154	924
925	NW7X 1JY		SM1H 8HN		94090910	["94 Roy falls", "East Ann"]	False	Primary	94090910	925
926	W5 8AH		ML22 8NL		95000256	["60 Luke canyon", "New Janeshire"]	False	Primary	95000256	926
927	WF95 2EL		N02 2PX		95000400	["95 Wood hill", "New Katie"]	False	Primary	95000400	927
928	W6 1YG		EC52 8QL		9500122T	["357 Clark shoal", "Jonathanshire"]	False	Primary	9500122T	928
929	South Mary	G2B 7GR	CB0M 4FZ		95002441	["Studio 83", "Shaw square"]	False	Primary	95002441	929
930	CM7R 0JW		N41 1HR		9500544T	["46 Gough flats", "New Marionborough"]	False	Primary	9500544T	930
931	Thomasmouth	E8K 8LQ	UB12 1UQ		95006822	["Flat 0", "Terence course"]	False	Primary	95006822	931
932	Lake Patricia	G79 8QL	ML77 9TZ		95010297	["Flat 9", "Naomi inlet"]	False	Primary	95010297	932
933	S94 7PB		S19 8QQ		95014298	["1 Alex circle", "Susanfurt"]	False	Primary	95014298	933
934	Port Elliott	S4 8AZ	N2 0DZ		95017676	["Studio 76V", "Butler ports"]	True	Primary	95017676	934
935	W72 2ZE		G16 8WF		95018760	["604 Peter village", "Francisborough"]	False	Primary	95018760	935
936	South Paula	RM6X 9XP	TF8R 8JX		95028213	["Studio 76", "Kieran avenue"]	False	Primary	95028213	936
937	New Charliemouth	B45 0ST	BN9X 0YU		95030119	["Studio 73", "Osborne light"]	False	Primary	95030119	937
938	North Janetfort	MK9 8ZD	N1 0GH		95032391	["Flat 37o", "Hugh roads"]	False	Primary	95032391	938
939	Lake Hazel	NE3 5DP	PE4V 1HX		95032638	["Flat 68", "Sara square"]	False	Primary	95032638	939
940	E2K 2LW		L45 2JX		95035544	["96 Jones well", "Taylorside"]	False	Primary	95035544	940
941	L0 4XG		S8 2AB		9504667T	["0 Wallace way", "Brendafort"]	False	Primary	9504667T	941
942	Port Conorborough	E51 0TW	G54 6UD		95046732	["Flat 5", "Thomson drives"]	False	Primary	95046732	942
943	CW52 5HP		WS0R 5UT		95046778	["8 Samuel motorway", "Paulinemouth"]	False	Primary	95046778	943
944	Lake Jenna	PO8 1SB	B99 1JX		95049033	["Flat 33m", "Bibi dam"]	False	Primary	95049033	944
945	Port Susantown	W5 0YD	BD4 4PT		95049684	["Studio 8", "Katy pines"]	False	Primary	95049684	945
946	Matthewfurt	CM1 9RF	M08 8WW		95050028	["Studio 9", "Wood throughway"]	False	Primary	95050028	946
947	W8 8AG		G8J 9JT		95050777	["10 Zoe glens", "South Lauraburgh"]	False	Primary	95050777	947
948	Lucytown	E68 1BW	L13 2ZJ		95053308	["Studio 9", "Stephenson shores"]	False	Primary	95053308	948
949	Burtonton	B8U 6QE	M0 0LD		95053648	["Studio 50", "Thornton courts"]	False	Primary	95053648	949
950	West Emily	W3E 9WD	CT15 9QT		95054248	["Flat 90", "Thompson station"]	False	Primary	95054248	950
951	Lake Charlie	SK8 8FW	AB6 8LY		95054605	["Flat 81m", "Kirby land"]	False	Primary	95054605	951
952	East Christopherfort	B1 0XF	HR69 7LB		95056617	["Studio 1", "Robert village"]	False	Primary	95056617	952
953	New Debra	CR7W 7NU	JE8 0GP		95062876	["Flat 76W", "Mary extension"]	False	Primary	95062876	953
954	NP9 9NS		DT0 6HD		95064335	["5 Shannon causeway", "Kingburgh"]	False	Primary	95064335	954
955	CF26 2EX		E7 0EG		95065851	["53 Andrea shores", "South Jemmaborough"]	False	Primary	95065851	955
956	CF6 1BN		S5J 2FU		95072099	["349 Shah tunnel", "Schofieldfort"]	False	Primary	95072099	956
957	G2A 6LF		L43 4YJ		95073534	["715 Bradley radial", "Pricefurt"]	False	Primary	95073534	957
958	DE89 0XT		PL45 7YZ		95088769	["91 Daniel trafficway", "North Mohammad"]	False	Primary	95088769	958
959	AL34 0ZL		PA0R 8EN		95089035	["13 Waters point", "New Justin"]	False	Primary	95089035	959
960	Port Samuel	WR1W 9BB	B0J 9SN		95095271	["Studio 35", "Joshua lane"]	False	Primary	95095271	960
961	East Lynn	G90 3XH	E5 3UH		95095697	["Studio 18", "Leah green"]	False	Primary	95095697	961
962	S0D 0SP		G2 4UW		9509575T	["2 Fisher tunnel", "Port Leeville"]	False	Primary	9509575T	962
963	G7 5UA		M7D 6XP		95096988	["313 Sarah plains", "Robertsport"]	False	Primary	95096988	963
964	HA1V 4JJ		FY9 5GD		95101131	["6 Hilary plains", "North Rossland"]	False	Primary	95101131	964
965	Shaunville	B2 7LP	LU67 6BN		9510511T	["Studio 75", "Vaughan fort"]	False	Primary	9510511T	965
966	Lanetown	G5U 0WR	LA71 7ZD		95107490	["Studio 63E", "Fiona crossing"]	False	Primary	95107490	966
967	South Georgeview	CH96 3WF	B0 1YU		95110088	["Studio 86", "Dean mountains"]	False	Primary	95110088	967
968	L8 3US		WR8N 2WF		9511251T	["01 Metcalfe viaduct", "Pearceberg"]	False	Primary	9511251T	968
969	N0U 0PS		M8B 7XG		95708936	["285 Williams landing", "East Amy"]	False	Primary	95708936	969
970	Ianmouth	E4 3FN	NR6 0LD		95907481	["Flat 99", "Billy road"]	False	Primary	95907481	970
971	South Lynn	PO1 2SG	DH65 1GW		96300648	["Flat 99w", "Elliott corners"]	False	Primary	96300648	971
972	East Brandonland	GY1E 8AJ	L48 8JQ		96400946	["Flat 7", "Michelle locks"]	False	Primary	96400946	972
973	WR6W 3UY		N65 7BL		96505010	["5 Wood squares", "Sharpbury"]	False	Primary	96505010	973
974	L98 9BL		NG73 8SN		97009936	["9 Allen inlet", "Kennedyberg"]	False	Primary	97009936	974
975	EH4 2DE		W3 7QH		97111265	["2 Kelly spur", "New Connorland"]	False	Primary	97111265	975
976	SO9A 9EG		PL44 6PR		97200058	["451 Sharp vista", "East Leah"]	False	Primary	97200058	976
977	Douglasbury	SW2 5QZ	B2 5AY		97432184	["Flat 84", "Lamb stream"]	False	Primary	97432184	977
978	FY3 6YB		NR5A 6BN		97520164	["4 Brown mission", "Port Robinburgh"]	False	Primary	97520164	978
979	New Frederickbury	E6A 5WN	DY62 5AQ		97532758	["Studio 43u", "Karl points"]	False	Primary	97532758	979
980	GL6A 5DQ		N0 6GR		97624336	["796 Matthew haven", "Port Conor"]	False	Primary	97624336	980
981	PE1R 6YS		WR69 6BA		97626072	["29 Scott parkway", "Port Paulbury"]	False	Primary	97626072	981
982	Mitchellshire	BA04 6SJ	TD68 6FF		97820067	["Flat 8", "Quinn forges"]	False	Primary	97820067	982
983	RG46 0JA		M8T 4PY		97830937	["6 Yates lakes", "New Andrew"]	False	Primary	97830937	983
984	West Ann	GU3Y 7JU	L08 0XD		97901626	["Flat 9", "Nicholas falls"]	False	Primary	97901626	984
985	LL72 8FG		W2G 7GG		98013349	["61 Danny points", "Port Stanley"]	False	Primary	98013349	985
986	Francisport	N5 7WW	W3C 6FT		9803605T	["Studio 02u", "Bryant underpass"]	False	Primary	9803605T	986
987	Martinside	IP5 4ZU	SR2M 2TW		98036901	["Flat 56", "Jean springs"]	False	Primary	98036901	987
988	Jamieside	N1 5LJ	W03 1BZ		98123544	["Flat 56", "Sandra extensions"]	False	Primary	98123544	988
989	North Shaun	KA54 1NA	UB9 3HA		98141395	["Flat 51a", "Jamie mount"]	False	Primary	98141395	989
990	NW9V 4HL		IG35 3EZ		9820277T	["3 Gavin run", "Gordonside"]	False	Primary	9820277T	990
991	L8 5RP		PR1H 3XW		98220297	["34 Hall spring", "Franceschester"]	False	Primary	98220297	991
992	HR1 1WW		SK11 7HS		98239268	["93 Reece inlet", "New Joshua"]	False	Primary	98239268	992
993	W71 8PA		N8 5HN		98312347	["77 Palmer knoll", "Whiteport"]	False	Primary	98312347	993
994	L0 3YT		G0B 3RX		9833009T	["0 Jenna spur", "West Davidbury"]	False	Primary	9833009T	994
995	Sharonville	E3 3DG	TF5 4DS		9851336T	["Flat 34S", "Sally estate"]	False	Primary	9851336T	995
996	Connollyhaven	M1 9DS	GY3M 1WT		98624482	["Flat 74M", "Cooper orchard"]	False	Primary	98624482	996
997	L5W 4GB		E5D 7FA		9916269T	["5 Parkes forge", "Jemmaton"]	False	Primary	9916269T	997
998	Reesshire	EN74 1XR	RH9M 3AD		99262664	["Studio 69C", "Palmer forge"]	False	Primary	99262664	998
999	N41 4PJ		LU73 0DH		99314363	["6 Graham rest", "Harrietborough"]	False	Primary	99314363	999
1000	SS2 9RJ		HU4 9GE		99328514	["07 Rachel station", "Andreamouth"]	False	Primary	99328514	1000
\.


--
-- Data for Name: persons; Type: TABLE DATA; Schema: pre_migrate; Owner: casrec
--

COPY pre_migrate.persons (id, dob, salutation, firstname, middlenames, surname, createddate, previousnames, caserecnumber, clientaccommodation, maritalstatus, countryofresidence, type, systemstatus, isreplacementattorney, istrustcorporation, clientstatus, statusdate, correspondencebywelsh, newsletter, specialcorrespondencerequirements_audiotape, specialcorrespondencerequirements_largeprint, specialcorrespondencerequirements_hearingimpaired, specialcorrespondencerequirements_spellingofnamerequirescare, digital, isorganisation, casesmanagedashybrid, supervisioncaseowner_id, clientsource, updateddate) FROM stdin;
1	2011-05-29	Mr.	Lesley	Lesley	Bell	1996-05-03	Lesley	10000037	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
2	1988-06-13	Ms.	Dylan	Dylan	Watson	1996-05-09	Dylan	10000884	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
3	1975-08-14	Ms.	Simon	Simon	Kemp	1996-05-20	Simon	10001403	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
4	2018-06-20	Dr.	Kate	Kate	Moore	1996-06-14	Kate	10001668	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
5	2016-12-16	Mrs.	Lindsey	Lindsey	Dale	1996-08-12	Lindsey	10002199	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
6	1980-06-06	Mr.	Lee	Lee	Jones	1996-05-21	Lee	10002625	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
7	2004-05-06	Mr.	Patricia	Patricia	Collins	1996-05-23	Patricia	10003409	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
8	1994-01-15	Miss	Stacey	Stacey	Morgan	1996-06-03	Stacey	10004038	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
9	2018-04-22	Dr.	Mohammed	Mohammed	Brown	1996-06-14	Mohammed	10004188	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
10	1995-05-10	Miss	Bruce	Bruce	Watson	1996-05-09	Bruce	10004257	OWN HOME	Co-habiting		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
11	1991-11-25	Mr.	Francesca	Francesca	Dixon	1996-05-09	Francesca	10004263	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
12	1986-06-06	Miss	Sheila	Sheila	Thomson	1996-05-14	Sheila	10004637	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
13	1986-10-06	Mrs.	Tom	Tom	Jackson	1996-05-15	Tom	10004741	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
14	2012-06-18	Dr.	Lynn	Lynn	Johnson	1996-05-16	Lynn	10004879	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
15	1999-08-17	Miss	Barbara	Barbara	James	1996-05-20	Barbara	10005237	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
16	2013-06-18	Ms.	Aimee	Aimee	Williams	1996-05-20	Aimee	10005243	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
17	1997-09-28	Ms.	Josh	Josh	Williamson	1996-05-14	Josh	10005433	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
18	2002-10-09	Ms.	Joan	Joan	Hall	1996-06-12	Joan	10005928	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
19	1989-07-25	Miss	Colin	Colin	Wilson	1996-05-21	Colin	10006315	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
20	1978-05-24	Ms.	Donna	Donna	Owen	1996-05-22	Donna	10006413	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
21	1980-10-28	Ms.	Andrea	Andrea	Jenkins	1996-05-30	Andrea	10007163	OTHER	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
22	2016-09-28	Mr.	Eileen	Eileen	Evans	1996-05-31	Eileen	10007261	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
23	2016-09-21	Dr.	Marc	Marc	Burrows	1996-05-30	Marc	10007877	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
24	1980-05-24	Dr.	Valerie	Valerie	Quinn	1996-05-31	Valerie	10008713	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
25	1982-10-09	Mr.	Marion	Marion	Walsh	1996-07-22	Marion	10009307	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
26	1981-12-24	Dr.	Cheryl	Cheryl	Reid	1996-06-13	Cheryl	10009526	OTHER	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
27	1997-02-13	Dr.	Mohamed	Mohamed	Robson	1996-06-11	Mohamed	10010274	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
28	1978-01-27	Mr.	Bethan	Bethan	Cooke	1996-07-04	Bethan	10011951	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
29	1999-09-13	Mr.	Toby	Toby	Robertson	1996-07-19	Toby	10012240	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
30	1992-10-15	Dr.	Kimberley	Kimberley	Marshall	1996-06-20	Kimberley	10012643	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
31	1990-03-31	Mr.	Brian	Brian	Smith	1996-06-19	Brian	10013116	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
32	1980-04-29	Miss	Malcolm	Malcolm	Jones	1996-06-21	Malcolm	10013560	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
33	2015-12-02	Ms.	Andrea	Andrea	Davison	1996-06-21	Andrea	10013583	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
34	1973-12-22	Dr.	Mathew	Mathew	Simmons	1996-06-24	Mathew	10013617	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
35	1976-03-24	Dr.	Kieran	Kieran	Schofield	1996-06-27	Kieran	1001404T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
36	2014-07-31	Mrs.	Keith	Keith	Reynolds	1996-07-02	Keith	10014200	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
37	2015-12-01	Dr.	Russell	Russell	Marsden	1996-07-05	Russell	10015094	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
38	1984-08-15	Mrs.	Simon	Simon	Brown	1996-07-05	Simon	10015105	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
39	1999-10-23	Mr.	Dale	Dale	Young	1996-07-04	Dale	10015981		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
40	1973-09-23	Dr.	Jordan	Jordan	Bird	1996-07-05	Jordan	10016195	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
41	1986-10-12	Mrs.	Robert	Robert	Hughes	1996-07-05	Robert	10016235	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
42	1978-10-13	Mr.	Leslie	Leslie	Jones	1996-07-09	Leslie	10016431	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
43	1972-04-09	Dr.	Robert	Robert	Moore	1996-07-11	Robert	10016621	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
44	2013-03-18	Mr.	Gary	Gary	Turner	1996-07-10	Gary	10016667	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
45	1985-12-07	Miss	Roy	Roy	Barnes	1996-07-11	Roy	10017181	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
46	1973-12-26	Dr.	Catherine	Catherine	Hunt	1996-07-19	Catherine	10018420	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
47	1971-12-09	Miss	Elizabeth	Elizabeth	Marsden	1996-07-23	Elizabeth	10018593	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
48	2004-06-01	Dr.	Brenda	Brenda	Pearson	1996-07-24	Brenda	10019377	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
49	1989-07-07	Mr.	Susan	Susan	Lee	1996-07-31	Susan	10020349	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
50	1988-06-02	Miss	Clare	Clare	Webb	1996-08-14	Clare	10020418	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
51	1984-12-02	Miss	Gail	Gail	Wells	1996-11-15	Gail	10020597	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
52	2014-09-07	Ms.	Carol	Carol	Ellis	1996-11-21	Carol	1002065T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
53	1997-05-27	Mr.	Rachel	Rachel	Taylor	1996-07-25	Rachel	10020983	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
54	2014-08-25	Mr.	Sara	Sara	Gordon	1996-08-02	Sara	10021220	FAMILY MEMBER/FRIEND'S HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
55	1972-11-13	Dr.	Lisa	Lisa	Price	1996-07-23	Lisa	10021744	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
56	1979-04-29	Miss	Tracey	Tracey	Morton	1996-08-08	Tracey	10023226	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
57	1998-10-07	Dr.	Jayne	Jayne	Thomas	1996-08-08	Jayne	10023232	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
58	1991-05-02	Miss	Callum	Callum	Hobbs	1996-08-08	Callum	10023301	COUNCIL RENTED	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
59	2010-07-28	Ms.	Natasha	Natasha	Hill	1996-08-06	Natasha	10023480	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
60	1990-08-22	Ms.	Alexander	Alexander	Swift	1996-08-08	Alexander	10023664	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
61	1980-04-05	Ms.	Joyce	Joyce	Kelly	1996-08-14	Joyce	10023877	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
62	1971-02-20	Mrs.	Mohamed	Mohamed	White	1996-08-22	Mohamed	10024391	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
63	2005-07-21	Mr.	Bryan	Bryan	Hunt	1996-08-27	Bryan	10024500	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
64	1983-04-19	Ms.	Terence	Terence	Carroll	2020-06-09	Terence	13611727	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
65	1986-05-19	Ms.	Brenda	Brenda	Marsh	1996-08-12	Brenda	10025630	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
66	1979-04-22	Mr.	Abdul	Abdul	Middleton	1996-08-12	Abdul	10025751	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
67	1978-05-05	Dr.	Catherine	Catherine	Harris	1996-08-12	Catherine	10025768	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
68	2001-12-25	Dr.	Rosemary	Rosemary	Schofield	1996-08-14	Rosemary	1002630T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
69	2003-03-02	Mr.	Tracey	Tracey	Campbell	1996-08-15	Tracey	10026374	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
70	2016-02-22	Mrs.	Leon	Leon	Coleman	1996-08-16	Leon	10027550	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
71	1974-10-24	Ms.	Simon	Simon	Smith	1996-08-20	Simon	10027832	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
72	1980-04-07	Dr.	Keith	Keith	Dixon	1996-08-21	Keith	1002818T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
73	1990-10-09	Dr.	Victoria	Victoria	Finch	1996-08-21	Victoria	10028288	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
74	2003-08-15	Mrs.	Catherine	Catherine	Clarke	1996-08-23	Catherine	10028340	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
75	1998-06-29	Dr.	Jordan	Jordan	Hall	1996-08-28	Jordan	10029078	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
76	1980-05-03	Ms.	Emily	Emily	Marshall	1996-08-28	Emily	10029084	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
77	2005-12-20	Miss	Hazel	Hazel	Patterson	1996-08-29	Hazel	10029245	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
78	2010-06-28	Dr.	Lynda	Lynda	Harris	1996-08-27	Lynda	10029556	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
79	2007-04-27	Ms.	David	David	Ingram	1996-08-30	David	10029602	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
80	2016-05-09	Mr.	Graeme	Graeme	Evans	1996-12-19	Graeme	1003019T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
81	1985-04-30	Dr.	Rachael	Rachael	Davis	1996-08-29	Rachael	1003061T	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
82	1986-04-26	Mrs.	Lindsey	Lindsey	Begum	1996-09-03	Lindsey	10030816	HOSTEL	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
83	2001-05-05	Ms.	Craig	Craig	Brown	1996-09-04	Craig	10030868	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
84	1983-08-31	Mr.	Oliver	Oliver	Bruce	1996-09-10	Oliver	10031042	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
85	2000-05-15	Dr.	Rhys	Rhys	Smith	1996-09-12	Rhys	10033048	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
86	1989-01-09	Mr.	Rosie	Rosie	James	1996-09-13	Rosie	10033250	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
87	2001-02-19	Dr.	Pamela	Pamela	Connolly	1997-01-10	Pamela	10033561	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
88	2009-02-01	Dr.	Frederick	Frederick	Lowe	1997-01-31	Frederick	10033653	SUPPORTED LIVING	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
89	1997-12-29	Dr.	Dorothy	Dorothy	Singh	1997-03-12	Dorothy	10033837	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
90	2018-01-24	Mrs.	Danny	Danny	Sharp	1996-11-29	Danny	10034253	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
91	2009-02-07	Miss	Margaret	Margaret	Robson	1996-09-19	Margaret	10034558	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
92	1994-09-11	Mr.	Douglas	Douglas	Bowen	1996-09-26	Douglas	10034898	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
93	1987-08-16	Mr.	Eleanor	Eleanor	Moore	1996-10-02	Eleanor	10035164	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
94	1973-08-06	Dr.	Olivia	Olivia	Williams	1996-09-20	Olivia	10036052	COUNCIL RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
95	2018-03-23	Dr.	Denise	Denise	Jones	1997-04-25	Denise	10037026	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
96	2018-12-26	Mrs.	Jessica	Jessica	Parsons	1996-09-26	Jessica	10038450	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
97	1977-05-14	Mrs.	Anthony	Anthony	Lawrence	1996-10-02	Anthony	10039522	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
98	1972-01-27	Dr.	Denise	Denise	Bird	1996-10-07	Denise	10040074	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
99	1991-11-25	Dr.	Lauren	Lauren	Harrison	1996-10-07	Lauren	10040794		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
100	1970-12-26	Dr.	Leanne	Leanne	Carter	1996-11-12	Leanne	10041002	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
101	1986-11-13	Mr.	Janice	Janice	Brown	1996-11-15	Janice	10041221	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
102	2019-08-01	Mr.	Bradley	Bradley	Matthews	1996-10-11	Bradley	10041912	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
103	1976-07-01	Dr.	Jane	Jane	Bentley	1996-10-18	Jane	10042691	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
104	2004-04-09	Mr.	Tom	Tom	Taylor	1996-10-11	Tom	10042817	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
105	2016-05-26	Dr.	Leigh	Leigh	Byrne	1996-10-15	Leigh	10042909	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
106	2004-02-26	Mr.	Aaron	Aaron	Parker	1996-10-18	Aaron	10043164	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
107	2006-04-17	Dr.	Bethany	Bethany	Gregory	1996-11-01	Bethany	10043855	FAMILY MEMBER/FRIEND'S HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
108	1995-03-18	Dr.	Emma	Emma	Lee	1996-11-08	Emma	10044150	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
109	2010-08-11	Mr.	Bernard	Bernard	Robinson	1996-10-21	Bernard	10044547	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
110	1998-08-24	Dr.	Toby	Toby	Brookes	1996-10-21	Toby	10044553	OWN HOME	Co-habiting		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
111	1993-03-08	Mr.	Joel	Joel	Jones	1996-10-22	Joel	10045118	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
112	1990-12-21	Dr.	Julian	Julian	Morris	1996-10-24	Julian	10045441	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
113	2017-10-02	Dr.	Charlotte	Charlotte	Lee	1996-10-25	Charlotte	10045717	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
114	1992-07-01	Mr.	Leanne	Leanne	Collins	1996-10-31	Leanne	10046369	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
115	2016-03-17	Mr.	Amber	Amber	Watson	1996-11-04	Amber	1004731T	NHS ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
116	2014-10-03	Miss	Roy	Roy	Smith	1996-11-08	Roy	10048151	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
117	2017-10-02	Mr.	Hilary	Hilary	Williamson	1996-11-08	Hilary	10048168	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
118	1983-09-09	Dr.	Robin	Robin	Taylor	1996-11-28	Robin	10050276	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
119	2003-03-15	Dr.	Howard	Howard	Price	1996-11-20	Howard	10050512	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
120	2019-03-30	Mrs.	Roger	Roger	Hunter	1996-12-02	Roger	10051538	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
121	1994-12-02	Dr.	Paula	Paula	Taylor	1996-11-19	Paula	10051890	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
122	2018-10-05	Dr.	Mathew	Mathew	Walker	1996-11-19	Mathew	10052501	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
123	2003-02-21	Ms.	Tracey	Tracey	Bren	1997-03-18	Tracey	10052743	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
124	1972-07-08	Dr.	Abbie	Abbie	Chapman	1996-11-27	Abbie	10053032	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
125	1974-06-06	Miss	Connor	Connor	Stevenson	1996-11-27	Connor	10053723	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
126	1996-12-22	Mr.	Gary	Gary	Holden	1996-11-27	Gary	10053746	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
127	1987-03-03	Mr.	Naomi	Naomi	Walker	1996-12-12	Naomi	10054300	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
128	1992-06-12	Dr.	Marilyn	Marilyn	Francis	1996-12-03	Marilyn	10055096	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
129	1981-01-25	Mr.	Terry	Terry	Read	1996-12-05	Terry	10055666	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
130	1977-08-21	Ms.	Tom	Tom	Dixon	1996-12-18	Tom	10056335	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
131	2014-08-12	Dr.	Kenneth	Kenneth	Robertson	1996-12-18	Kenneth	10056410	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
132	2011-11-06	Mr.	Samuel	Samuel	Hutchinson	1996-12-12	Samuel	10056865	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
133	1992-12-01	Dr.	Jennifer	Jennifer	Moore	1996-12-13	Jennifer	10056957	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
134	2017-06-30	Dr.	Hilary	Hilary	Mitchell	1996-12-16	Hilary	10057661	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
135	1988-11-02	Dr.	Neil	Neil	Potts	1996-12-17	Neil	10057995	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
136	2002-11-11	Dr.	Shannon	Shannon	Webb	1996-12-18	Shannon	10058071	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
137	2008-09-01	Mrs.	Danielle	Danielle	Jarvis	1996-12-18	Danielle	10058140	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
138	1979-08-02	Ms.	Gerard	Gerard	Phillips	1996-12-27	Gerard	10058508	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
139	1973-12-02	Mr.	Ben	Ben	Dale	1996-12-23	Ben	10058589	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
140	1986-12-17	Miss	Grace	Grace	Collier	1996-12-27	Grace	10058917	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
141	1970-11-08	Dr.	John	John	Potter	1997-01-02	John	1005934T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
142	2014-11-04	Dr.	Frank	Frank	Nicholls	1997-01-03	Frank	10060501	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
143	1998-08-27	Ms.	Eric	Eric	Stewart	1997-01-07	Eric	10062185	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
144	1999-11-11	Miss	Jeffrey	Jeffrey	Howells	1997-01-07	Jeffrey	10062191	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
145	2010-10-23	Mr.	Abbie	Abbie	Newton	1997-01-13	Abbie	1006312T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
146	1983-06-28	Miss	Katherine	Katherine	Foster	1997-01-14	Katherine	10063257	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
147	1990-11-20	Mrs.	Mathew	Mathew	Murphy	1997-01-20	Mathew	10063614	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
148	1974-12-31	Mr.	Maureen	Maureen	Page	1997-01-20	Maureen	10064295	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
149	2003-11-16	Ms.	Eleanor	Eleanor	Wheeler	1997-01-23	Eleanor	10064669	COUNCIL RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
150	2009-01-08	Miss	Dominic	Dominic	Giles	1997-01-28	Dominic	10065004	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
151	1975-09-01	Mr.	Alan	Alan	Miller	1997-01-28	Alan	10065010	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
152	1978-05-04	Miss	Ricky	Ricky	Jones	1997-01-30	Ricky	10065632	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
153	1984-03-09	Ms.	Ian	Ian	Scott	1997-01-30	Ian	10065868	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
154	1998-05-31	Miss	Alice	Alice	Patel	1997-02-05	Alice	10067863	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
155	1987-04-10	Mr.	Deborah	Deborah	Morley	1997-02-11	Deborah	10068267	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
156	1974-10-22	Dr.	Lee	Lee	Cooper	1997-03-19	Lee	10069846	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
157	1991-07-29	Mr.	Bethany	Bethany	Hutchinson	1997-03-03	Bethany	1007033T	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
158	1975-06-05	Dr.	Arthur	Arthur	Chamberlain	1997-02-20	Arthur	10070980	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
159	2007-01-20	Ms.	Gail	Gail	Roberts	1997-02-24	Gail	10071240		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
160	2015-01-29	Dr.	Alice	Alice	Brown	1997-02-25	Alice	1007165T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
161	1977-03-28	Ms.	Joyce	Joyce	Forster	1997-02-25	Joyce	10071919	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
162	2013-06-08	Dr.	Holly	Holly	Simmons	1997-02-26	Holly	10072053	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
163	2007-03-12	Dr.	Ellie	Ellie	Reid	1997-02-27	Ellie	10072180	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
164	1972-12-22	Dr.	Marc	Marc	Russell	1997-02-27	Marc	10072548	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
165	2001-06-12	Mrs.	Eileen	Eileen	Whittaker	1997-02-27	Eileen	10072617	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
166	1989-02-12	Mr.	Shannon	Shannon	Joyce	1997-02-28	Shannon	10072652	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
167	1992-12-02	Ms.	Luke	Luke	Mahmood	1997-03-08	Luke	10072905	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
168	1971-05-07	Mr.	Max	Max	Jones	1997-03-11	Max	10075788	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
169	2006-08-27	Ms.	Naomi	Naomi	Holland	1997-03-14	Naomi	10075794	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
170	1974-09-01	Miss	Pamela	Pamela	Wright	1997-03-24	Pamela	10075892	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
171	2005-10-20	Mr.	Stuart	Stuart	Barnes	1997-05-14	Stuart	10076307	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
172	2006-01-15	Dr.	Sara	Sara	Pearson	1997-03-19	Sara	10076428	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
173	2012-08-10	Ms.	Christine	Christine	Burgess	1997-03-19	Christine	10076618	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
174	2020-02-02	Dr.	Marion	Marion	Hall	1997-03-18	Marion	10077466	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
175	2006-07-19	Dr.	Allan	Allan	Jackson	1997-03-19	Allan	10077535	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
176	1987-07-19	Dr.	Gavin	Gavin	Cooper	1997-03-20	Gavin	10077702	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
177	2015-12-13	Dr.	Lynda	Lynda	Harvey	1997-03-17	Lynda	10078014	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
178	1976-11-18	Dr.	Bradley	Bradley	Bell	1997-03-20	Bradley	10078498	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
179	2014-03-19	Dr.	Amelia	Amelia	Lloyd	1997-03-26	Amelia	1008006T	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
180	1995-08-14	Mrs.	Benjamin	Benjamin	Allen	1997-03-27	Benjamin	10080306	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
181	2001-12-28	Ms.	Thomas	Thomas	Patel	1997-04-03	Thomas	10080698	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
182	1987-02-20	Mrs.	Nigel	Nigel	Morris	1997-04-03	Nigel	10080773	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
183	2017-04-18	Miss	Marian	Marian	Woods	1997-04-04	Marian	10080842	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
184	1989-09-15	Mr.	Martin	Martin	Rose	1997-04-15	Martin	10081321	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
185	1992-12-12	Ms.	Denis	Denis	Baker	1997-04-16	Denis	10081436	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
186	1976-04-17	Miss	Diane	Diane	Hayes	1997-04-15	Diane	10082290	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
187	1998-11-06	Dr.	Gerard	Gerard	Kaur	1997-04-28	Gerard	10082629	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
188	2011-06-24	Miss	Joanne	Joanne	Smart	1997-04-16	Joanne	10084054	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
189	2010-11-29	Mr.	Lorraine	Lorraine	Stone	1997-04-23	Lorraine	10085368	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
190	1997-06-22	Mr.	Sean	Sean	Patel	1997-04-29	Sean	10086377	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
191	1993-01-10	Ms.	Nicole	Nicole	Robinson	1997-04-30	Nicole	10086803	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
192	1985-04-19	Ms.	Amelia	Amelia	Warner	1997-04-30	Amelia	10087046	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
193	2010-10-13	Mr.	Ashley	Ashley	Richards	1997-05-02	Ashley	10087121	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
194	1983-10-21	Dr.	Jeremy	Jeremy	May	1997-05-02	Jeremy	10087207	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
195	2000-07-19	Dr.	Jasmine	Jasmine	Patel	1997-05-07	Jasmine	10087392	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
196	2003-06-08	Dr.	Geoffrey	Geoffrey	Long	1997-05-02	Geoffrey	10087622	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
197	1984-03-22	Mrs.	Mohammed	Mohammed	Wells	1997-05-08	Mohammed	10088090	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
198	2001-12-27	Mrs.	Vanessa	Vanessa	Riley	1997-05-08	Vanessa	10088470	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
199	1977-07-14	Dr.	Shane	Shane	Norris	1997-05-21	Shane	10089346	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
200	1981-04-08	Dr.	Julia	Julia	Hughes	1997-05-15	Julia	10090422	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
201	1978-05-09	Mr.	Lewis	Lewis	Woods	1997-05-14	Lewis	10090923	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
202	1970-12-28	Mr.	Timothy	Timothy	Ferguson	1997-05-14	Timothy	10090969	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
203	2005-05-17	Mr.	Dorothy	Dorothy	Read	1997-06-05	Dorothy	10092221	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
204	2000-12-08	Ms.	Eleanor	Eleanor	Allen	1997-05-28	Eleanor	10093529	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
205	1990-10-08	Mr.	Sally	Sally	Hill	1997-06-04	Sally	10093996	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
206	1974-09-17	Dr.	Lynne	Lynne	Brookes	1997-06-12	Lynne	10094354	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
207	2020-05-31	Miss	Grace	Grace	Frost	1997-05-29	Grace	10094976	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
208	2007-02-03	Miss	Michelle	Michelle	Lewis	1997-06-18	Michelle	10095259	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
209	2013-12-29	Dr.	Phillip	Phillip	Lewis	1997-06-03	Phillip	10096406	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
210	1985-11-24	Dr.	Ashleigh	Ashleigh	Cross	1997-06-20	Ashleigh	10097012	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
211	1988-12-01	Dr.	Marc	Marc	Dean	1997-08-11	Marc	10097922	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
212	2010-07-21	Ms.	Zoe	Zoe	Phillips	1997-07-02	Zoe	10099491	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
213	2005-07-29	Dr.	Abbie	Abbie	Lewis	1997-06-19	Abbie	10099894	HOUSING ASSOCIATION	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
214	1992-01-03	Mr.	Beth	Beth	Dunn	1997-06-24	Beth	10101102		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
215	2004-11-23	Mrs.	Stephanie	Stephanie	Wong	1997-06-23	Stephanie	10101321	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
216	1988-07-04	Dr.	Reece	Reece	Walsh	1997-06-26	Reece	10102566	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
217	2003-01-25	Mr.	Tom	Tom	Morton	1997-06-27	Tom	10102658	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
218	1997-05-26	Dr.	Cameron	Cameron	Hewitt	1997-07-01	Cameron	1010391T	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
219	1977-11-16	Mr.	Gerald	Gerald	Begum	1997-07-15	Gerald	10105028	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
220	1987-05-16	Mr.	Keith	Keith	Moore	1997-07-04	Keith	10106020	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
221	2003-04-27	Miss	Charlene	Charlene	Reid	1997-07-15	Charlene	10106095	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
222	1985-02-01	Ms.	Trevor	Trevor	Lane	1997-07-30	Trevor	10106665	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
223	1972-03-23	Mr.	Tom	Tom	Wells	1997-07-09	Tom	10107023	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
224	1988-07-19	Ms.	Janet	Janet	Kirby	1997-08-12	Janet	10108458	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
225	2003-09-08	Dr.	Melissa	Melissa	Barrett	1997-08-19	Melissa	10108700	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
226	2004-05-17	Dr.	Gareth	Gareth	Patel	1997-08-20	Gareth	10108815	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
227	1990-01-31	Dr.	Frances	Frances	Graham	1997-08-27	Frances	10109006	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
228	2016-03-23	Dr.	Alan	Alan	Palmer	1997-09-01	Alan	10109755	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
229	2005-02-13	Mr.	Aaron	Aaron	Jones	1997-08-04	Aaron	1011017T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
230	2009-12-01	Mrs.	Justin	Justin	Rogers	1997-07-16	Justin	10114095	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
231	2004-10-03	Mr.	Joshua	Joshua	Davies	1997-07-24	Joshua	10114544	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
232	2011-02-24	Dr.	Harry	Harry	Johnson	1997-07-31	Harry	10114901	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
233	2011-09-30	Mrs.	Roger	Roger	Turnbull	1997-08-01	Roger	10117542	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
234	2010-11-13	Mr.	Danny	Danny	Cartwright	1997-08-01	Danny	10117594	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
235	1976-11-19	Mr.	Neil	Neil	Collins	1997-08-04	Neil	1011850T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
236	2013-08-16	Mr.	Diana	Diana	Goodwin	1997-08-05	Diana	10118539	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
237	2000-08-11	Ms.	Grace	Grace	James	1997-08-12	Grace	10118706	LA PART 3 ACCOMMODATION	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
238	1974-05-25	Mr.	Matthew	Matthew	Armstrong	1997-08-21	Matthew	10122279	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
239	2011-04-21	Mrs.	Christopher	Christopher	Goddard	1997-09-03	Christopher	10123455	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
240	2003-09-27	Miss	Joanne	Joanne	Roberts	1997-09-25	Joanne	10125087	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
241	1981-03-14	Dr.	Reece	Reece	Arnold	1997-09-19	Reece	10126044	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
242	2017-09-26	Dr.	Gareth	Gareth	Cunningham	1997-09-23	Gareth	10126234	COUNCIL RENTED	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
243	1988-03-05	Mrs.	Ryan	Ryan	Wells	1997-09-25	Ryan	10126597	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
244	2011-01-24	Mrs.	Lee	Lee	Rose	1997-10-09	Lee	10129802	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
245	1987-05-01	Dr.	Leigh	Leigh	Lane	1997-10-22	Leigh	10131138	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
246	1997-04-08	Ms.	Bernard	Bernard	Long	1997-10-13	Bernard	10131668	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
247	2003-10-23	Ms.	Thomas	Thomas	Phillips	1997-10-20	Thomas	10131979	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
248	1991-03-18	Dr.	Kirsty	Kirsty	Kelly	1997-10-22	Kirsty	10132222	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
249	2000-03-25	Dr.	Mary	Mary	Green	1997-10-13	Mary	10132683	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
250	2011-01-23	Mrs.	James	James	Nash	1997-10-17	James	10133847	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
251	2004-11-18	Mr.	Ryan	Ryan	Buckley	1997-10-28	Ryan	10134292	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
252	1981-07-01	Dr.	Duncan	Duncan	Butler	1997-10-27	Duncan	10134672	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
253	1984-03-06	Mr.	Angela	Angela	Jones	1997-11-10	Angela	10135295	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
254	2006-07-29	Dr.	Carly	Carly	Thompson	1997-11-11	Carly	10135341	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
255	1997-09-24	Dr.	Mohamed	Mohamed	Jackson	1997-11-10	Mohamed	10138356	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
256	2012-09-29	Dr.	Garry	Garry	Oliver	1997-11-07	Garry	10138460	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
257	1974-04-21	Dr.	Wendy	Wendy	Bradshaw	1997-11-11	Wendy	10138517	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
258	1997-06-03	Dr.	Keith	Keith	Perry	1997-11-19	Keith	10139181	OTHER	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
259	2014-11-26	Mr.	Stephen	Stephen	Campbell	1997-11-24	Stephen	10139342	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
260	2017-01-26	Mr.	Shane	Shane	Gardiner	1997-11-21	Shane	10140700	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
261	1971-09-12	Dr.	Sean	Sean	Bailey	1997-11-28	Sean	10140913	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
262	2020-07-06	Mr.	Hannah	Hannah	Blake	1997-11-17	Hannah	10141202	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
263	1992-09-25	Mrs.	Cameron	Cameron	Savage	1997-11-17	Cameron	10141254	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
264	1996-02-21	Mr.	Marian	Marian	Jones	1997-11-18	Marian	1014133T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
265	1979-06-02	Ms.	Holly	Holly	Walker	1997-11-27	Holly	10142038	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
266	2020-04-13	Mr.	Ellie	Ellie	Johnson	1997-11-27	Ellie	10142194	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
267	1993-03-03	Mr.	Natasha	Natasha	Bishop	1997-11-26	Natasha	1014265T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
268	2020-01-02	Mr.	Nigel	Nigel	Ford	1997-11-26	Nigel	10142729	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
269	2011-03-23	Dr.	Joyce	Joyce	Wilson	1997-11-27	Joyce	10142856	OTHER	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
270	2019-10-16	Ms.	Rachel	Rachel	Norris	1997-12-08	Rachel	10143894	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
271	1978-09-25	Mr.	Carole	Carole	Green	1997-12-16	Carole	10146500	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
272	1977-04-30	Mrs.	Gareth	Gareth	Scott	1998-01-02	Gareth	10149066	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
273	1990-12-30	Dr.	Abigail	Abigail	Lowe	1997-12-19	Abigail	10149878	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
274	1973-05-29	Dr.	Frank	Frank	Chapman	1998-01-21	Frank	1015099T	OTHER	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
275	1991-06-14	Dr.	Barbara	Barbara	Hewitt	1998-02-04	Barbara	10151208	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
276	1981-04-12	Ms.	Helen	Helen	Anderson	1998-01-15	Helen	10152488	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
277	2020-01-12	Mr.	Ricky	Ricky	Wright	1998-01-22	Ricky	10152868	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
278	2001-10-13	Dr.	Alison	Alison	Kennedy	1998-01-28	Alison	10153255	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
279	1988-03-27	Dr.	Joanne	Joanne	Simpson	1998-02-02	Joanne	1015355T	COUNCIL RENTED	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
280	2013-06-12	Ms.	Rosemary	Rosemary	Hall	1998-02-06	Rosemary	10153802	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
281	2014-09-23	Dr.	Lewis	Lewis	Hall	1998-02-10	Lewis	10154051	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
282	1978-11-22	Miss	June	June	Price	1998-02-10	June	10154097	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
283	2011-06-18	Mr.	Marion	Marion	Miller	1998-02-19	Marion	10154500	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
284	2013-11-18	Dr.	Bethan	Bethan	Cooper	1998-02-02	Bethan	10156034	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
285	2019-05-26	Dr.	Ann	Ann	Wallace	1998-03-02	Ann	10156656	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
286	1992-01-04	Dr.	Karen	Karen	Young	1998-01-22	Karen	10158403	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
287	2011-12-06	Mrs.	Jonathan	Jonathan	Watson	1998-02-10	Jonathan	10159625	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
288	1978-07-15	Ms.	Malcolm	Malcolm	Jones	1998-02-13	Malcolm	10159936	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
289	1989-02-16	Dr.	Glenn	Glenn	Carpenter	1998-02-18	Glenn	10160321	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
290	2012-09-10	Mr.	Amy	Amy	Allen	1998-02-18	Amy	10160367	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
291	2020-06-28	Dr.	Jonathan	Jonathan	John	1998-02-26	Jonathan	10160897	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
292	2007-04-29	Mr.	Jake	Jake	Davies	1998-02-26	Jake	10160966	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
293	1978-06-10	Mrs.	Danielle	Danielle	Coleman	1998-03-08	Danielle	10162667	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
294	2003-06-02	Mr.	Ross	Ross	Chandler	1998-02-24	Ross	10164063	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
295	1983-10-26	Ms.	Joel	Joel	Powell	1998-02-24	Joel	10164149	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
296	2017-08-12	Dr.	Alison	Alison	Adams	1998-02-25	Alison	10164178	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
297	2019-05-15	Dr.	Paige	Paige	Williams	1998-03-12	Paige	1016562T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
298	2002-08-15	Dr.	Brandon	Brandon	Brady	1998-03-23	Brandon	10166328	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
299	2004-09-02	Miss	Tom	Tom	Potter	1998-04-28	Tom	10181803	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
300	1990-04-08	Ms.	Carole	Carole	Curtis	1998-04-30	Carole	10181930	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
301	1981-07-22	Mrs.	Frances	Frances	Barker	1998-05-13	Frances	10182311	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
302	1989-10-14	Ms.	Beth	Beth	Lewis	1998-05-12	Beth	10183078	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
303	1990-02-25	Mrs.	Charlene	Charlene	Peacock	1998-06-12	Charlene	10184300	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
304	1987-02-17	Dr.	Nicole	Nicole	Parker	1998-05-14	Nicole	10185735	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
305	1984-05-29	Dr.	Roger	Roger	Bird	1998-07-02	Roger	10192899	SUPPORTED LIVING	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
306	2001-07-27	Ms.	Paula	Paula	Griffiths	1998-07-02	Paula	10192916	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
307	1997-09-30	Dr.	Keith	Keith	Barker	1998-06-29	Keith	10194709	NHS ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
308	2002-12-21	Mr.	Joel	Joel	Cole	1998-07-14	Joel	10198244	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
309	1987-10-12	Dr.	Eileen	Eileen	Whittaker	1998-07-28	Eileen	10199092	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
310	1971-01-22	Dr.	Martin	Martin	Hodgson	1998-07-28	Martin	10200679	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
311	2010-09-02	Mrs.	Marian	Marian	Walker	1998-07-28	Marian	10200685	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
312	1984-12-16	Mr.	Timothy	Timothy	Davidson	1998-07-28	Timothy	10200748	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
313	1985-10-16	Mrs.	Bruce	Bruce	Smith	1998-07-31	Bruce	10201193	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
314	2012-04-23	Miss	Brenda	Brenda	Riley	1998-08-07	Brenda	10201705	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
315	2012-07-18	Ms.	Aaron	Aaron	Hart	1998-07-30	Aaron	10202386	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
503	2007-01-23	Mrs.	Eleanor	Eleanor	Barlow	2005-05-10	Eleanor	11276657				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
316	1970-03-13	Dr.	Norman	Norman	Scott	2001-11-23	Norman	10494872	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
317	1999-03-14	Mrs.	Donna	Donna	Burton	1998-08-13	Donna	10204496	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
318	1977-12-17	Mr.	Stewart	Stewart	Ryan	1998-08-25	Stewart	1020512T	HOSTEL	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
319	1972-08-26	Ms.	Gail	Gail	Gibson	1998-09-21	Gail	10206404	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
320	1987-10-21	Miss	Frederick	Frederick	Hudson	1998-08-11	Frederick	10207131	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
321	1973-04-02	Mrs.	Gary	Gary	Duffy	1998-09-17	Gary	10208946	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
322	2013-01-16	Dr.	Jenna	Jenna	Hamilton	1998-09-17	Jenna	10209045	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
323	2006-11-09	Mr.	Tina	Tina	Grant	1998-09-04	Tina	1021075T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
324	1990-06-22	Mr.	Katie	Katie	Lewis	1998-09-29	Katie	10211717	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
325	2016-01-31	Mr.	Bruce	Bruce	Wilson	1998-08-21	Bruce	10213228	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
326	1989-12-07	Dr.	Amber	Amber	Hewitt	1998-09-16	Amber	10214807	PRIVATE RENTED	Co-habiting		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
327	2014-10-02	Dr.	Carol	Carol	Elliott	1998-09-17	Carol	10214940	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
328	1979-05-05	Dr.	Connor	Connor	Lee	1998-09-22	Connor	10215183	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
329	2005-01-20	Dr.	Georgia	Georgia	Hurst	1998-10-08	Georgia	10216508	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
330	2005-01-31	Dr.	Frank	Frank	Woods	1998-10-23	Frank	10221960	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
331	2007-09-03	Mr.	Alison	Alison	Parsons	1998-11-05	Alison	10222865	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
332	1988-10-12	Mrs.	Patricia	Patricia	Chapman	1998-12-04	Patricia	10228043	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
333	2012-08-07	Mrs.	Tina	Tina	Miller	1998-12-02	Tina	10231275	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
334	2014-01-12	Mr.	Elizabeth	Elizabeth	Parker	1998-11-26	Elizabeth	10232094	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
335	1999-12-05	Dr.	Frances	Frances	Moss	1998-11-26	Frances	1023217T	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
336	2007-07-09	Miss	Bryan	Bryan	Shepherd	1998-12-09	Bryan	10233264	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
337	1987-07-06	Dr.	Christian	Christian	Collins	1998-12-09	Christian	10233327	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
338	1973-04-28	Mr.	Clare	Clare	Hunt	1999-01-12	Clare	10235783		Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
339	2013-08-13	Mr.	Lauren	Lauren	Thomas	1999-01-20	Lauren	10236953	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
340	1990-09-28	Mr.	Hannah	Hannah	Knowles	1998-12-17	Hannah	10238118	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
341	1970-03-16	Mr.	Catherine	Catherine	May	1999-01-11	Catherine	1024055T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
342	2004-07-31	Dr.	John	John	Watts	1999-01-08	John	10241932	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
343	1974-10-23	Dr.	Diana	Diana	Mills	1999-01-13	Diana	10241990	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
344	1999-08-07	Dr.	Heather	Heather	Peters	1999-01-27	Heather	10242970	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
345	2006-11-23	Dr.	Adrian	Adrian	Riley	1999-02-01	Adrian	10243443	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
346	2016-12-20	Ms.	Charlie	Charlie	King	1999-02-01	Charlie	10243489	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
347	1971-12-02	Mrs.	Benjamin	Benjamin	Jones	1999-02-11	Benjamin	10244918	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
348	2010-08-21	Mrs.	Gary	Gary	Humphries	1999-01-22	Gary	10245530	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
349	1985-08-18	Mr.	Charlene	Charlene	Nelson	1999-01-22	Charlene	10245576	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
350	2018-01-23	Mrs.	Leon	Leon	Hobbs	1999-02-03	Leon	10246308	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
351	1975-01-20	Mr.	Charles	Charles	Webster	1999-03-08	Charles	10248689	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
352	1971-09-12	Mr.	Jonathan	Jonathan	Leach	1999-03-09	Jonathan	10248787	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
353	2016-11-20	Miss	Danny	Danny	Rhodes	1999-02-12	Danny	1025051T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
354	1982-10-14	Mrs.	Stanley	Stanley	Palmer	1999-02-12	Stanley	10250601	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
355	1980-08-24	Mr.	Andrea	Andrea	Knight	1999-03-17	Andrea	10254153	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
356	1989-04-18	Dr.	Graham	Graham	Fletcher	1999-03-10	Graham	10254942	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
357	2017-10-31	Ms.	Tony	Tony	Sutton	1999-03-12	Tony	10255421	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
358	1980-08-29	Dr.	Eleanor	Eleanor	Boyle	1999-03-08	Eleanor	10255945	PRIVATE RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
359	1979-09-10	Miss	Abbie	Abbie	Kelly	1999-03-17	Abbie	10256741	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
360	1990-03-06	Miss	Roy	Roy	Thomas	1999-03-26	Roy	10259249	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
361	2007-04-27	Mr.	Joel	Joel	Lewis	1999-04-28	Joel	10264165	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
362	2007-03-07	Dr.	Kate	Kate	Pugh	1999-04-28	Kate	10264188	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
363	1998-08-07	Mr.	Georgina	Georgina	Lee	1999-04-12	Georgina	10264522	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
364	2011-10-04	Mrs.	Craig	Craig	Riley	1999-05-24	Craig	10270815	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
365	2011-03-07	Mr.	Kenneth	Kenneth	Thomas	1999-05-12	Kenneth	10272741	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
366	2005-10-14	Mr.	Katy	Katy	Rose	1999-06-03	Katy	10273905	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
367	2019-01-01	Dr.	Alexandra	Alexandra	Lambert	1999-06-11	Alexandra	10274494	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
368	1986-01-30	Dr.	Kathleen	Kathleen	Simmons	1999-06-04	Kathleen	10277117	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
369	2000-10-30	Dr.	Geraldine	Geraldine	Bolton	1999-06-30	Geraldine	1028453T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
370	2018-10-10	Miss	Danielle	Danielle	Holmes	1999-07-23	Danielle	10285929	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
371	1993-07-30	Mr.	Jack	Jack	Higgins	1999-06-25	Jack	10287383	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
372	1971-12-14	Mr.	Declan	Declan	Jackson	1999-07-06	Declan	10288046	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
373	2006-09-18	Mr.	Grace	Grace	Young	1999-08-06	Grace	10292742	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
374	1995-04-16	Mr.	Darren	Darren	Jackson	1999-08-23	Darren	10293987	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
375	2000-04-15	Ms.	Dean	Dean	Griffiths	1999-09-30	Dean	10295930	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
376	1997-10-03	Dr.	Marie	Marie	Stokes	1999-08-24	Marie	10297297	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
377	2012-10-01	Ms.	Kathleen	Kathleen	Clements	1999-08-31	Kathleen	10297660	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
378	2009-06-20	Miss	William	William	Moore	1999-09-02	William	10297913	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
379	2000-09-11	Mr.	Andrea	Andrea	Pritchard	2020-06-09	Andrea	13611733	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
380	1988-05-28	Miss	Kirsty	Kirsty	Roberts	1999-09-24	Kirsty	1029931T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
381	2009-12-17	Dr.	Eileen	Eileen	Davison	1999-09-20	Eileen	1030110T	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
382	1998-06-29	Dr.	Francesca	Francesca	Brooks	1999-09-29	Francesca	10301750	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
383	1998-08-19	Dr.	Ian	Ian	Lee	1999-10-13	Ian	10302350	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
384	2012-09-11	Dr.	Yvonne	Yvonne	Lawson	1999-09-10	Yvonne	10303376	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
385	1994-06-01	Ms.	Christine	Christine	Grant	1999-10-29	Christine	10305935	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
386	1990-12-26	Dr.	Timothy	Timothy	McDonald	1999-10-26	Timothy	1030841T	NHS ACCOMMODATION	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
387	2014-07-08	Mr.	Victor	Victor	O'Connor	1999-11-02	Victor	1030875T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
388	1994-11-14	Miss	Charlene	Charlene	Hughes	1999-11-10	Charlene	10309533	HEALTH SERVICE PATIENT	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
389	2011-04-21	Miss	Emily	Emily	Bailey	1999-12-16	Emily	10315141	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
390	1989-11-13	Miss	Gary	Gary	Griffin	2000-02-07	Gary	10317585	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
391	2008-08-19	Mrs.	Eileen	Eileen	Murphy	1999-12-09	Eileen	10318726	OTHER	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
392	1977-10-26	Mrs.	Dennis	Dennis	Taylor	1999-12-16	Dennis	10319067	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
393	2009-07-28	Miss	Leanne	Leanne	Newton	2000-01-11	Leanne	10320788	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
394	2015-11-28	Dr.	Ross	Ross	White	1999-11-17	Ross	10320955	HEALTH SERVICE PATIENT	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
395	1997-12-22	Mr.	Jeffrey	Jeffrey	Robinson	1999-11-26	Jeffrey	10322725	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
396	1983-05-17	Dr.	Chloe	Chloe	O'Donnell	2000-01-05	Chloe	10324484	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
397	1978-05-30	Ms.	Sarah	Sarah	Brooks	1999-12-29	Sarah	10325700	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
398	1976-02-27	Dr.	Jean	Jean	Bell	2000-02-03	Jean	10327234	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
399	2010-09-24	Dr.	Emma	Emma	Davis	2000-01-21	Emma	1032923T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
400	2012-10-31	Dr.	Anne	Anne	Jackson	2007-02-26	Anne	11452767	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
401	1991-11-07	Dr.	Catherine	Catherine	Ball	2000-02-17	Catherine	10332236	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
402	2004-03-23	Mr.	Amy	Amy	Burns	2000-02-18	Amy	10332461	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
403	2008-04-03	Dr.	Tom	Tom	Turner	2000-03-03	Tom	10334473	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
404	1997-10-10	Dr.	Sylvia	Sylvia	Patel	2000-03-19	Sylvia	10335568	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
405	1988-04-17	Mr.	Conor	Conor	Pugh	2000-02-23	Conor	10336709	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
406	1995-08-06	Dr.	Leonard	Leonard	Dixon	2000-03-02	Leonard	10337505	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
407	1992-05-08	Ms.	Julian	Julian	Morgan	2000-03-06	Julian	10337914	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
408	2018-12-16	Dr.	Sarah	Sarah	Anderson	2000-03-14	Sarah	1033889T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
409	2019-06-08	Mr.	Albert	Albert	Kelly	2000-03-31	Albert	10340294	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
410	2016-07-29	Dr.	Mohammad	Mohammad	Parkin	2000-03-02	Mohammad	1034037T	HEALTH SERVICE PATIENT	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
411	2005-08-06	Dr.	Lydia	Lydia	Jones	2000-05-08	Lydia	10346606	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
412	2006-07-25	Mrs.	Maureen	Maureen	Jones	2000-04-17	Maureen	1034930T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
413	1985-02-05	Mr.	Damian	Damian	Mitchell	2000-04-17	Damian	10349339	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
414	2018-09-23	Dr.	Jayne	Jayne	Evans	2000-05-15	Jayne	10352773	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
415	1971-12-18	Miss	Caroline	Caroline	Mitchell	2000-05-05	Caroline	10353966	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
416	1986-02-06	Dr.	Stephanie	Stephanie	Murray	2000-07-06	Stephanie	1035651T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
417	2013-02-15	Miss	Lynda	Lynda	Burton	2000-05-30	Lynda	10356768	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
418	1999-02-06	Dr.	Brenda	Brenda	Holmes	2000-06-07	Brenda	10362036	OTHER	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
419	1995-09-29	Mrs.	Diane	Diane	Carpenter	2000-05-19	Diane	10363460	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
420	2001-11-07	Dr.	Alan	Alan	Thomas	2000-06-27	Alan	10367766		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
421	2003-01-04	Dr.	Timothy	Timothy	Long	2000-07-03	Timothy	10369939	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
422	1991-07-09	Mr.	Lynn	Lynn	Ward	2000-06-27	Lynn	10370284		Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
423	1993-03-21	Mrs.	Gareth	Gareth	Morgan	2000-08-08	Gareth	10373086	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
424	1994-07-03	Mr.	Katy	Katy	White	2000-08-14	Katy	10373495	FAMILY MEMBER/FRIEND'S HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
425	1995-11-03	Mr.	Douglas	Douglas	White	2000-08-22	Douglas	10381719	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
426	1970-04-04	Mr.	Denise	Denise	Jordan	2000-09-14	Denise	10382256	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
427	1985-05-12	Dr.	Cheryl	Cheryl	Wood	2000-08-01	Cheryl	10384821	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
428	2019-11-23	Dr.	Yvonne	Yvonne	Sheppard	2000-09-11	Yvonne	10389088	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
429	2002-02-04	Mrs.	Stacey	Stacey	Bell	2000-10-16	Stacey	10397831	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
430	1991-07-28	Ms.	Anne	Anne	Allen	2000-10-20	Anne	10403484	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
431	2009-11-10	Dr.	Abigail	Abigail	Walsh	2000-10-30	Abigail	10409497	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
432	1990-03-12	Mr.	Kim	Kim	Cartwright	2000-11-05	Kim	10410786	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
433	1974-07-14	Ms.	Wayne	Wayne	Jackson	2000-11-09	Wayne	1041194T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
434	1983-07-14	Dr.	Eric	Eric	Goodwin	2000-11-24	Eric	10415698	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
435	1973-12-25	Mr.	Ellie	Ellie	Ahmed	2000-12-18	Ellie	10420959	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
436	1971-12-10	Mr.	Mandy	Mandy	Bennett	2001-01-03	Mandy	10423836	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
437	2010-02-15	Mr.	Jemma	Jemma	Reeves	2001-01-04	Jemma	10424217	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
438	2006-03-18	Mr.	Jenna	Jenna	Wright	2001-01-16	Jenna	10426794	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
439	2006-09-17	Mr.	Kenneth	Kenneth	Norman	2001-01-26	Kenneth	10429544	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
440	2014-01-28	Mrs.	Glenn	Glenn	Stanley	2001-02-14	Glenn	10433249	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
441	1991-01-14	Dr.	Francis	Francis	Cooper	2001-02-19	Francis	10434477	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
442	2002-02-17	Ms.	Joshua	Joshua	Warner	2001-03-02	Joshua	10437636	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
443	2001-01-31	Dr.	Janice	Janice	Douglas	2001-03-09	Janice	10439199	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
444	2004-03-05	Mr.	Barbara	Barbara	Andrews	2001-03-21	Barbara	10441883	HEALTH SERVICE PATIENT	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
445	1970-10-08	Ms.	Stephen	Stephen	Parsons	2001-03-21	Stephen	10442189	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
446	1976-03-23	Dr.	Ian	Ian	Johnson	2001-04-05	Ian	10445671	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
447	2012-01-26	Dr.	Fiona	Fiona	Wilson	2001-04-10	Fiona	10447090	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
448	2002-06-16	Ms.	Josh	Josh	Porter	2001-04-18	Josh	10447959	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
449	2009-10-28	Mr.	Rosemary	Rosemary	Burton	2001-05-18	Rosemary	10454979	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
450	2002-03-18	Dr.	Sandra	Sandra	Young	2001-05-18	Sandra	10455268	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
451	1989-02-09	Mr.	Jamie	Jamie	Williams	2001-05-24	Jamie	10456156	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
452	2019-06-09	Mr.	Debra	Debra	Williams	2001-05-24	Debra	10456162	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
453	2019-11-10	Mr.	Lucy	Lucy	Harris	2001-05-24	Lucy	10456381	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
454	1971-08-10	Dr.	John	John	Davis	2001-06-14	John	10460725	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
455	1988-02-12	Dr.	Sam	Sam	Evans	2001-06-19	Sam	10461469	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
456	1974-08-31	Miss	Caroline	Caroline	Knowles	2001-06-19	Caroline	10461498	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
457	1974-04-13	Mr.	Diane	Diane	Mills	2001-07-10	Diane	10465735	SUPPORTED LIVING	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
458	1991-09-27	Mrs.	Kathleen	Kathleen	Ashton	2001-07-25	Kathleen	10468917	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
459	1990-11-22	Miss	Lynda	Lynda	Moss	2001-07-27	Lynda	10469863	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
460	1995-11-09	Mr.	Anne	Anne	Patel	2001-10-01	Anne	10482836		Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
461	1996-05-10	Dr.	Elizabeth	Elizabeth	Reed	2001-10-09	Elizabeth	10484543	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
462	2016-06-07	Miss	Holly	Holly	Smith	2001-10-15	Holly	1048587T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
463	1973-01-20	Ms.	Sheila	Sheila	Arnold	2001-10-16	Sheila	10486336	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
464	1992-07-16	Dr.	Aimee	Aimee	James	2019-03-14	Aimee	13402508	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
465	2012-10-21	Mr.	Melissa	Melissa	Taylor	2002-01-08	Melissa	11001537	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
466	1996-10-17	Ms.	Damian	Damian	Briggs	2002-03-07	Damian	11013596	SUPPORTED LIVING	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
467	1975-11-07	Miss	James	James	Woods	2002-04-03	James	11019897	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
468	1977-07-03	Dr.	Terry	Terry	Ball	2002-04-08	Terry	11021106	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
469	1978-09-06	Ms.	Alice	Alice	Hill	2002-05-21	Alice	11029206	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
470	2016-01-07	Mrs.	Georgia	Georgia	Wade	2002-06-12	Georgia	11034030		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
471	2017-09-23	Mr.	Damian	Damian	Thomson	2002-07-24	Damian	1104342T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
472	1990-05-18	Mr.	Sylvia	Sylvia	Edwards	2002-09-27	Sylvia	11056262	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
473	1988-09-12	Dr.	Clare	Clare	Wells	2002-10-28	Clare	11063558	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
474	2006-06-30	Ms.	Margaret	Margaret	Francis	2002-11-16	Margaret	11068361	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
475	2015-06-06	Ms.	Lesley	Lesley	Parsons	2003-02-06	Lesley	11084044	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
476	2003-01-11	Dr.	Tina	Tina	Waters	2003-02-06	Tina	11084211	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
477	1988-10-06	Dr.	Amy	Amy	Anderson	2003-02-22	Amy	11087791	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
478	1984-09-03	Dr.	Raymond	Raymond	Jarvis	2003-03-08	Raymond	11092050	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
479	1998-07-26	Dr.	Charles	Charles	Jones	2003-04-11	Charles	11100423		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
480	1996-08-25	Mr.	Megan	Megan	Pollard	2003-04-25	Megan	11102602	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
481	1980-11-28	Dr.	Carol	Carol	Thorpe	2003-06-06	Carol	11112194	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
482	2000-09-09	Dr.	Oliver	Oliver	Preston	2003-08-30	Oliver	11131468		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
483	1985-04-08	Mr.	Katherine	Katherine	Bruce	2003-09-26	Katherine	11138571	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
484	1980-03-06	Ms.	Marilyn	Marilyn	Abbott	2003-11-14	Marilyn	11149177	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
485	1996-03-13	Mrs.	Barbara	Barbara	Coates	2003-12-05	Barbara	11153838				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
486	1977-04-12	Dr.	Antony	Antony	Knight	2004-02-10	Antony	11166595	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
487	1978-02-28	Mr.	Bethan	Bethan	Marsh	2004-04-19	Bethan	11183886	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
488	1991-04-18	Ms.	Dominic	Dominic	Marshall	2004-06-24	Dominic	1119959T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
489	2014-10-07	Dr.	Bernard	Bernard	Smith	2004-07-08	Bernard	11203189	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
490	1978-07-28	Miss	Eileen	Eileen	Thorpe	2004-08-26	Eileen	11214567	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
491	1979-03-26	Mrs.	Naomi	Naomi	Andrews	2004-08-26	Naomi	11214849	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
492	2004-03-11	Mrs.	Edward	Edward	Booth	2004-09-14	Edward	11219796	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
493	2003-10-10	Mrs.	Conor	Conor	Mahmood	2004-09-30	Conor	11223576		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
494	2008-12-10	Mr.	Ian	Ian	Davies	2004-11-11	Ian	11233248	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
495	1975-09-13	Mrs.	Kerry	Kerry	Rowley	2005-01-10	Kerry	11245969	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
496	2004-10-29	Mr.	Dawn	Dawn	Brown	2005-01-10	Dawn	11245975	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
497	1973-04-13	Mrs.	Lindsey	Lindsey	Sykes	2005-01-18	Lindsey	11247745		Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
498	1978-04-26	Mr.	Hugh	Hugh	Wood	2005-01-31	Hugh	11251502	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
499	2001-10-29	Dr.	Carly	Carly	Kennedy	2005-02-18	Carly	11256558	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
500	1988-05-24	Mr.	Damien	Damien	Rogers	2005-03-02	Damien	11259389	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
501	1970-03-21	Miss	Victoria	Victoria	Connolly	2005-04-01	Victoria	11267055	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
502	1987-01-11	Mrs.	Lynne	Lynne	James	2005-04-05	Lynne	1126792T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
504	1983-09-01	Mr.	Leslie	Leslie	Thomas	2005-06-08	Leslie	11283988	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
505	1992-04-03	Dr.	Jonathan	Jonathan	Goodwin	2005-06-27	Jonathan	1128889T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
506	1996-09-14	Mrs.	Paul	Paul	Barnett	2005-07-05	Paul	11291268	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
507	1981-05-04	Mr.	Anthony	Anthony	Morris	2005-07-07	Anthony	1129192T	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
508	1991-08-12	Mr.	Toby	Toby	Miller	2005-07-07	Toby	11291942		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
509	1989-09-14	Mr.	Michelle	Michelle	Fox	2005-09-07	Michelle	11308641	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
510	2017-02-18	Mr.	Shannon	Shannon	Singh	2005-09-12	Shannon	11309454		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
511	1979-08-17	Mr.	Maurice	Maurice	Jackson	2005-10-03	Maurice	11314744		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
512	1994-01-16	Ms.	Kathleen	Kathleen	Morgan	2005-10-13	Kathleen	11317742	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
513	1991-07-03	Dr.	Daniel	Daniel	Howard	2005-10-28	Daniel	11321977	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
514	1996-09-16	Mr.	Barry	Barry	Smith	2005-11-10	Barry	11325016	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
515	1980-08-13	Miss	Judith	Judith	Skinner	2005-11-25	Judith	11329259	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
516	2016-06-04	Mrs.	Claire	Claire	Whitehead	2005-12-21	Claire	11336129	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
517	1993-10-22	Dr.	Paul	Paul	Thomas	2006-02-01	Paul	11345121		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
518	1983-01-07	Mr.	Andrew	Andrew	Payne	2006-02-14	Andrew	11348643		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
519	1984-06-17	Dr.	Henry	Henry	Williams	2006-03-10	Henry	11356568	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
520	1992-05-21	Ms.	Sharon	Sharon	Willis	2006-05-18	Sharon	11377313	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
521	2016-10-24	Dr.	Leon	Leon	Atkinson	2006-12-08	Leon	11433199	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
522	2004-11-15	Mrs.	Leah	Leah	Evans	2007-01-02	Leah	1143836T				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
523	2016-10-23	Dr.	Georgia	Georgia	Robinson	2007-01-03	Georgia	1143889T	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
524	2018-09-01	Dr.	Nicola	Nicola	Morrison	2007-01-18	Nicola	11441562	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
525	1973-04-15	Dr.	Elliott	Elliott	Reynolds	2007-01-23	Elliott	11443384	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
526	2004-04-15	Dr.	Denis	Denis	Bull	2007-01-26	Denis	11444871	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
527	1985-11-01	Dr.	Natasha	Natasha	Macdonald	2007-02-06	Natasha	11447460	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
528	2000-03-25	Mr.	Bradley	Bradley	Schofield	2007-02-22	Bradley	11452168	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
529	1994-07-01	Dr.	Leslie	Leslie	Brown	2007-02-23	Leslie	11452329	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
530	1997-08-01	Dr.	Marie	Marie	Berry	2007-03-29	Marie	11462975	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
531	2000-02-09	Dr.	Jennifer	Jennifer	Lloyd	2007-04-10	Jennifer	11466008	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
532	1974-07-16	Mrs.	Tom	Tom	Evans	2007-04-11	Tom	11466112	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
533	2001-10-06	Mrs.	Bethan	Bethan	Howe	2007-04-11	Bethan	11466210	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
534	1971-03-19	Mrs.	Rachel	Rachel	Williams	2007-04-16	Rachel	11467743	COUNCIL RENTED	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
535	1979-10-03	Ms.	Lewis	Lewis	Dean	2007-04-23	Lewis	11469818		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
536	1978-08-31	Miss	Arthur	Arthur	Saunders	2007-04-30	Arthur	11471903	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
537	2003-06-22	Ms.	Debra	Debra	Owen	2007-05-01	Debra	11472336	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
538	1975-01-12	Mr.	Sarah	Sarah	Nicholson	2007-05-01	Sarah	11472365	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
539	1994-07-26	Dr.	Shannon	Shannon	Walsh	2007-05-09	Shannon	11474279	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
540	2013-04-21	Dr.	Colin	Colin	Stevens	2007-05-30	Colin	11479865	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
541	1975-05-19	Mr.	Ben	Ben	Smith	2007-06-05	Ben	11482204	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
542	2002-06-07	Mr.	Brian	Brian	Thomas	2007-06-06	Brian	11482855		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
543	1976-07-15	Miss	Michelle	Michelle	Rowley	2007-06-11	Michelle	11484153	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
544	2012-12-04	Dr.	Kyle	Kyle	Lee	2007-06-13	Kyle	11485012		Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
545	2013-10-09	Ms.	Alexander	Alexander	Martin	2007-06-20	Alexander	1148646T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
546	1996-06-29	Dr.	Helen	Helen	Martin	2007-06-25	Helen	1148778T				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
547	1993-07-25	Mr.	Suzanne	Suzanne	Goddard	2007-06-26	Suzanne	11488252	COUNCIL RENTED	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
548	1994-11-23	Ms.	Gerard	Gerard	Williams	2007-06-26	Gerard	11488465	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
549	1982-02-22	Ms.	Lydia	Lydia	Shaw	2007-07-03	Lydia	11490233	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
550	1990-04-01	Dr.	Yvonne	Yvonne	Wilkins	2007-07-10	Yvonne	11492297	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
551	1987-12-05	Miss	Brandon	Brandon	Burns	2007-07-31	Brandon	11497854	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
552	2014-05-06	Dr.	Marc	Marc	Bennett	2007-08-03	Marc	11499503		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
553	1970-03-08	Mr.	Karl	Karl	Kay	2007-08-08	Karl	11500820	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
554	2008-11-03	Mrs.	Sylvia	Sylvia	Barlow	2007-08-10	Sylvia	11501420	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
555	2012-02-14	Dr.	Jayne	Jayne	Lee	2007-08-13	Jayne	11501823	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
556	1997-01-29	Mr.	Jason	Jason	Morton	2007-08-15	Jason	11503075	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
557	2018-03-02	Mrs.	Roy	Roy	Parker	2007-08-16	Roy	11503864	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
558	2007-04-30	Ms.	Stephanie	Stephanie	Nicholson	2007-08-16	Stephanie	11503933	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
559	1982-12-06	Dr.	Linda	Linda	Clarke	2007-08-20	Linda	11504372	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
560	1975-02-08	Mr.	Jenna	Jenna	Pearson	2007-08-23	Jenna	11505899	OTHER	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
561	1986-01-20	Mr.	Bethan	Bethan	Cook	2007-08-31	Bethan	11508154	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
562	1982-01-14	Mr.	Amanda	Amanda	Carr	2007-09-03	Amanda	11508534	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
563	1991-03-05	Mr.	Jordan	Jordan	Smith	2007-09-12	Jordan	11511639	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
564	1984-12-07	Mr.	Margaret	Margaret	Phillips	2007-10-01	Margaret	11517353	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
565	1985-06-19	Dr.	Lorraine	Lorraine	Johnston	2007-10-10	Lorraine	11521916	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
566	2005-03-09	Dr.	Hayley	Hayley	Lee	2007-10-12	Hayley	11522637	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
567	1973-11-29	Ms.	Simon	Simon	Smith	2007-10-12	Simon	11522643	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
568	2003-09-02	Mr.	Jessica	Jessica	Kelly	2007-11-05	Jessica	11526707	HEALTH SERVICE PATIENT	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
569	2018-07-11	Ms.	Kenneth	Kenneth	Green	2007-11-06	Kenneth	11527215	COUNCIL RENTED	Separated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
570	1997-11-10	Dr.	Holly	Holly	White	2007-11-13	Holly	11530107	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
571	2014-01-27	Mr.	Martyn	Martyn	Perry	2007-11-27	Martyn	11536092	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
572	2003-06-05	Mr.	Janice	Janice	Bibi	2007-12-12	Janice	11540897	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
573	1973-10-23	Ms.	Graeme	Graeme	Reynolds	2008-01-07	Graeme	11545786	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
574	1971-01-21	Mr.	Jane	Jane	West	2008-01-08	Jane	11546432	OTHER	Other		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
575	1974-02-19	Mr.	Marian	Marian	Rogers	2008-01-22	Marian	1155000T		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
576	1978-05-03	Mr.	Francesca	Francesca	Benson	2008-01-22	Francesca	11550270				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
577	1980-02-11	Mr.	Terry	Terry	Hussain	2008-01-29	Terry	11553037	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
578	2018-02-17	Dr.	Patricia	Patricia	Burrows	2008-02-14	Patricia	11558554	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
579	1980-01-20	Mr.	Bethan	Bethan	Howells	2008-02-20	Bethan	11560126	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
580	2007-10-28	Mr.	Oliver	Oliver	Weston	2008-02-27	Oliver	11563314	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
581	1973-09-30	Dr.	Oliver	Oliver	Bell	2008-03-04	Oliver	11565044	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
582	1989-12-01	Dr.	Victor	Victor	Bailey	2008-03-13	Victor	1156889T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
583	1999-06-15	Mrs.	Deborah	Deborah	Bren	2008-03-14	Deborah	11569195	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
584	2014-01-19	Dr.	Carol	Carol	Hardy	2008-04-09	Carol	11577229	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
585	1993-01-06	Miss	Shirley	Shirley	Cox	2008-04-28	Shirley	11583718	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
586	2012-07-03	Miss	Sarah	Sarah	Lynch	2008-04-30	Sarah	11584474	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
587	2002-04-13	Ms.	Alison	Alison	Cole	2008-07-22	Alison	11609075	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
588	1979-09-28	Dr.	Maria	Maria	Wood	2008-08-11	Maria	11614970	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
589	1971-04-21	Mr.	Max	Max	Williams	2008-08-12	Max	11615725	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
590	2007-01-22	Mrs.	Marcus	Marcus	Barlow	2008-08-18	Marcus	11617864	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
591	1979-04-28	Dr.	Damian	Damian	Davison	2008-08-22	Damian	11623351	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
592	2008-12-17	Ms.	Katherine	Katherine	Price	2008-10-08	Katherine	11636695	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
593	1975-06-14	Ms.	Fiona	Fiona	Page	2020-06-09	Fiona	13611710	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
594	1981-02-28	Miss	Edward	Edward	Cole	2008-12-22	Edward	11661807	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
595	2020-08-04	Ms.	Leonard	Leonard	Martin	2009-04-08	Leonard	11698923	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
596	1999-02-08	Miss	Amelia	Amelia	Chapman	2009-06-10	Amelia	11717534	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
597	1978-02-28	Dr.	Justin	Justin	Hutchinson	2009-08-10	Justin	11742249	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
598	1978-10-06	Miss	Dorothy	Dorothy	Chadwick	2009-08-13	Dorothy	11745967	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
599	2016-11-26	Mrs.	Samantha	Samantha	Roberts	2009-09-14	Samantha	11757882	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
600	1973-02-03	Dr.	Roger	Roger	Burns	2009-09-22	Roger	11760532	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
601	2017-07-10	Dr.	Lee	Lee	Jones	2009-11-19	Lee	11781162	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
602	2017-05-25	Ms.	Linda	Linda	James	2009-11-27	Linda	11784511	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
603	1977-03-04	Dr.	Amy	Amy	Hardy	2009-12-11	Amy	11790827	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
604	1980-06-10	Mr.	Graeme	Graeme	Davies	2010-01-12	Graeme	11798910	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
605	2017-05-02	Dr.	Jayne	Jayne	Wright	2010-05-20	Jayne	11844790	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
606	1984-05-18	Mr.	Megan	Megan	Taylor	2010-06-10	Megan	11854986	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
607	2012-04-14	Mrs.	Hollie	Hollie	Williams	2010-07-08	Hollie	11866428	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
608	2020-06-15	Dr.	Maurice	Maurice	Clark	2010-08-25	Maurice	11886585	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
609	2002-02-19	Dr.	Joyce	Joyce	Harris	2011-02-01	Joyce	1194777T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
610	1984-09-23	Mr.	Jade	Jade	Brooks	2011-02-21	Jade	11956501	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
611	2005-05-21	Ms.	Leigh	Leigh	Jones	2011-02-22	Leigh	11957337	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
612	1986-03-16	Ms.	Jessica	Jessica	Martin	2011-06-20	Jessica	12006612	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
613	1995-01-30	Mr.	Raymond	Raymond	Smith	2011-07-20	Raymond	1202119T	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
614	1975-05-09	Dr.	Carole	Carole	Fisher	2011-07-20	Carole	12021200	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
615	1996-08-13	Mrs.	Conor	Conor	Graham	2011-07-21	Conor	12022071	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
616	1998-01-29	Mr.	Lewis	Lewis	Morgan	2011-11-07	Lewis	12069348	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
617	1980-07-19	Dr.	Donald	Donald	Bennett	2011-11-30	Donald	12080655	OWN HOME	Separated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
618	2015-08-26	Mrs.	Alan	Alan	Lewis	2012-03-09	Alan	12120852	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
619	2018-05-10	Dr.	Fiona	Fiona	Wright	2012-04-25	Fiona	12141476	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
620	1973-11-18	Mr.	Daniel	Daniel	Kaur	2012-06-21	Daniel	1216808T	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
621	1984-08-26	Mr.	Holly	Holly	Metcalfe	2012-07-04	Holly	12173962	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
622	2001-12-19	Dr.	Jenna	Jenna	Payne	2012-08-16	Jenna	12197359	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
623	2015-08-07	Mrs.	Billy	Billy	Elliott	2012-09-26	Billy	12217002	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
624	1971-08-29	Mr.	Valerie	Valerie	Walker	2012-10-29	Valerie	12232172		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
625	2003-11-25	Mr.	Garry	Garry	Clarke	2012-10-31	Garry	12233313	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
626	2004-05-26	Mr.	Elliott	Elliott	Gray	2012-11-22	Elliott	12244697	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
627	2010-09-23	Mrs.	Danny	Danny	Taylor	2013-01-22	Danny	12269247	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
628	2011-06-17	Mrs.	Abbie	Abbie	Lewis	2013-04-04	Abbie	12304250	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
629	2017-10-31	Mrs.	Kevin	Kevin	Williams	2013-04-15	Kevin	12308798	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
630	2013-12-20	Mr.	Timothy	Timothy	Smith	2013-05-07	Timothy	12319047		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
631	1983-11-19	Mr.	Francis	Francis	Smith	2013-05-14	Francis	12322901	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
632	1982-10-21	Mr.	Shaun	Shaun	Smart	2013-09-10	Shaun	12379718	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
633	1977-11-07	Dr.	Rita	Rita	Kaur	2013-12-03	Rita	12417667	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
634	1999-11-24	Mr.	Neil	Neil	Robinson	2013-12-16	Neil	12422681	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
635	1999-02-01	Dr.	Marie	Marie	Hughes	2014-01-22	Marie	12441454	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
636	1981-03-18	Dr.	Toby	Toby	Stephens	2014-02-14	Toby	12454585	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
637	1977-01-31	Mr.	Suzanne	Suzanne	Read	2014-02-16	Suzanne	12455323	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
638	2020-04-26	Dr.	Janice	Janice	Singh	2014-04-11	Janice	12485221	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
639	1990-07-25	Dr.	Laura	Laura	Robinson	2014-04-22	Laura	12488795	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
640	1979-04-22	Mrs.	Nathan	Nathan	Jarvis	2014-05-14	Nathan	12500332	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
641	1977-01-11	Mr.	Justin	Justin	Martin	2014-05-27	Justin	12506230	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
642	1991-07-09	Dr.	Kimberley	Kimberley	Morgan	2014-06-03	Kimberley	12509308	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
643	1984-11-18	Miss	Leah	Leah	Griffiths	2014-06-16	Leah	12515538	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
644	1982-03-12	Dr.	Megan	Megan	Barrett	2014-09-23	Megan	12566705	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
645	2017-09-08	Ms.	Joanne	Joanne	Robinson	2014-10-08	Joanne	12575599	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
646	2006-03-17	Mrs.	Hilary	Hilary	Patel	2015-01-15	Hilary	12622608	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
647	2019-11-14	Dr.	Angela	Angela	Williams	2015-01-21	Angela	12624632	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
648	2014-12-09	Ms.	Lauren	Lauren	Stevens	2015-04-15	Lauren	12668301	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
649	1976-06-10	Dr.	Jennifer	Jennifer	Bailey	2015-04-20	Jennifer	12670530	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
650	2012-12-28	Mr.	Leigh	Leigh	Nelson	2015-04-21	Leigh	12670887	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
651	1980-05-23	Mrs.	Steven	Steven	George	2015-05-26	Steven	1268922T	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
652	1987-08-16	Mr.	Elliott	Elliott	Smith	2015-06-02	Elliott	12693356	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
653	2003-04-30	Dr.	Cheryl	Cheryl	Hill	2015-06-02	Cheryl	12693483	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
654	1988-10-07	Mr.	John	John	Carroll	2015-06-22	John	12704013	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
655	2007-04-21	Mr.	Callum	Callum	Watson	2015-06-23	Callum	12704474	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
656	1975-01-28	Mr.	Jennifer	Jennifer	Lawson	2015-07-06	Jennifer	12709910	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
657	2001-04-29	Dr.	Lynn	Lynn	Bird	2015-07-17	Lynn	12716400	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
658	2010-02-13	Miss	Toby	Toby	Coleman	2015-08-05	Toby	12725150	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
659	2005-10-24	Mrs.	Andrea	Andrea	Clark	2015-10-26	Andrea	12768501	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
660	1973-06-02	Mr.	Dorothy	Dorothy	Bull	2015-10-27	Dorothy	12768927	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
661	1985-12-16	Dr.	Cheryl	Cheryl	Steele	2015-10-30	Cheryl	1277117T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
662	1986-11-08	Mr.	Gerard	Gerard	Williams	2015-11-12	Gerard	12777510				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
663	1983-11-02	Dr.	Susan	Susan	Williams	2015-11-16	Susan	12779384	PRIVATE RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
664	1971-07-07	Mr.	Jack	Jack	Hopkins	2015-11-25	Jack	12784311	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Separated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
665	1987-10-21	Ms.	Cameron	Cameron	Morgan	2015-12-16	Cameron	12795770	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
666	1988-10-29	Mr.	Susan	Susan	Burke	2015-12-18	Susan	12797033	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
667	1978-06-21	Mrs.	Jasmine	Jasmine	Chadwick	2016-01-12	Jasmine	1280494T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
668	1985-07-08	Ms.	Caroline	Caroline	Griffiths	2016-01-20	Caroline	12808842	FAMILY MEMBER/FRIEND'S HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
669	1994-08-17	Ms.	Annette	Annette	Lewis	2016-02-19	Annette	12826975	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
670	1998-09-12	Mr.	Grace	Grace	Newman	2016-03-10	Grace	12839812	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
671	2018-09-10	Mr.	Victor	Victor	Robinson	2016-03-19	Victor	12844958	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
672	2011-12-01	Mr.	Hayley	Hayley	Marsh	2016-04-15	Hayley	12855789	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
673	1998-11-26	Dr.	Karen	Karen	Lewis	2016-04-19	Karen	1285669T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
674	2007-06-10	Dr.	Pauline	Pauline	Lamb	2016-05-27	Pauline	12878552	COUNCIL RENTED	Separated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
675	1978-01-01	Mrs.	Allan	Allan	Williams	2016-06-01	Allan	1288073T	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
676	1988-03-13	Miss	Craig	Craig	Lees	2016-06-03	Craig	12882401	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
677	1993-12-29	Dr.	Pauline	Pauline	Davis	2016-06-08	Pauline	12885508	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
678	2002-09-06	Dr.	Alison	Alison	Watts	2016-06-09	Alison	12886984		Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
679	2010-03-05	Mr.	Maria	Maria	Peters	2016-06-28	Maria	12898213	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
680	1995-06-27	Dr.	Daniel	Daniel	Wilson	2016-07-22	Daniel	12912465	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
681	2007-12-25	Ms.	Elliott	Elliott	Cooper	2016-08-16	Elliott	12925832	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
682	1980-01-21	Dr.	Tina	Tina	Daniels	2016-09-05	Tina	12936323	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
683	2008-01-01	Dr.	Alexandra	Alexandra	Hunt	2016-09-28	Alexandra	1294953T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
684	1992-04-16	Mrs.	Cameron	Cameron	Brooks	2016-10-04	Cameron	12952628	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
685	1982-08-10	Mrs.	Joseph	Joseph	Wilson	2016-12-01	Joseph	12986199	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
686	1976-10-06	Mr.	Leon	Leon	James	2017-01-11	Leon	13005455	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
687	2013-06-22	Mrs.	Gail	Gail	Ryan	2017-01-12	Gail	13006913	PRIVATE RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
688	1987-11-08	Ms.	Martyn	Martyn	Khan	2017-03-06	Martyn	13034690	FAMILY MEMBER/FRIEND'S HOME			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
689	2009-08-22	Dr.	Callum	Callum	Murray	2017-03-22	Callum	13044788	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
690	1999-06-04	Ms.	Karen	Karen	Norton	2017-03-23	Karen	13045198	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
691	1983-08-04	Mr.	Vanessa	Vanessa	Turner	2017-04-21	Vanessa	13058640	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
692	2015-02-22	Mr.	Clive	Clive	Cooper	2017-05-24	Clive	13076410	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
693	2010-12-02	Dr.	Stephen	Stephen	Bell	2017-06-08	Stephen	13082997	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
694	2009-03-13	Mrs.	Sean	Sean	Hodgson	2017-06-30	Sean	13093845	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
695	2001-06-27	Ms.	Peter	Peter	Read	2017-07-28	Peter	13110922	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
696	1994-11-17	Miss	Joshua	Joshua	Talbot	2017-09-06	Joshua	13131258	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
697	1991-10-17	Ms.	Louis	Louis	Burton	2017-09-19	Louis	13137156	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
698	1990-04-07	Dr.	Hazel	Hazel	Evans	2017-09-26	Hazel	13140618	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
699	2019-11-06	Miss	Katie	Katie	Poole	2017-10-26	Katie	13157543	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
700	1986-04-14	Miss	Benjamin	Benjamin	Morris	2017-12-01	Benjamin	13174794	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
701	1995-01-06	Mr.	Graham	Graham	Nicholls	2018-01-15	Graham	13193711	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
702	1974-05-20	Mrs.	Aimee	Aimee	Chapman	2018-01-19	Aimee	13195959	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
703	2010-09-23	Mrs.	Ryan	Ryan	Price	2018-01-24	Ryan	13198030	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
704	2004-07-27	Ms.	Melanie	Melanie	Knowles	2018-03-06	Melanie	13218462	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
705	1985-02-18	Mr.	Benjamin	Benjamin	Morgan	2018-04-03	Benjamin	13233643	FAMILY MEMBER/FRIEND'S HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
706	2020-09-10	Miss	Beth	Beth	Shepherd	2018-05-30	Beth	13258619	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
707	2015-11-23	Dr.	Ashleigh	Ashleigh	Poole	2018-05-31	Ashleigh	13259818	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
708	2009-12-21	Mr.	Kate	Kate	Begum	2018-06-04	Kate	13260762	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
709	2014-11-14	Mr.	Jane	Jane	Ali	2018-06-06	Jane	13262336	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
710	1980-10-18	Miss	Ashley	Ashley	Wood	2018-06-08	Ashley	13263316	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
711	1999-07-14	Mr.	Kerry	Kerry	White	2018-06-28	Kerry	13272728	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
712	1978-06-15	Mr.	Alexander	Alexander	Turner	2018-06-29	Alexander	13273645	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
713	1982-11-25	Mr.	Teresa	Teresa	Smith	2018-07-04	Teresa	1327533T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
714	2020-01-19	Mr.	Molly	Molly	Houghton	2018-07-12	Molly	13280481	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
715	2001-08-05	Mrs.	Owen	Owen	Morley	2018-09-05	Owen	13305888	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
716	1993-10-09	Mr.	Kayleigh	Kayleigh	Mitchell	2018-09-12	Kayleigh	1330853T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
717	2008-03-11	Mrs.	Norman	Norman	Jones	2018-09-29	Norman	13318495				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
718	2008-10-01	Mr.	Natalie	Natalie	Wright	2018-10-08	Natalie	13323382	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
719	2016-03-10	Dr.	Georgia	Georgia	Williams	2019-02-04	Georgia	13384618	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
720	2018-03-23	Ms.	Deborah	Deborah	Banks	2019-02-15	Deborah	1339115T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
721	1991-04-25	Ms.	Ellie	Ellie	Watson	2019-02-15	Ellie	13391270	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
722	1994-10-22	Miss	Emma	Emma	Harding	2019-02-19	Emma	13392486	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
723	2002-03-31	Mr.	Kayleigh	Kayleigh	Mitchell	2019-03-01	Kayleigh	13397421	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
724	1992-02-13	Mr.	Josephine	Josephine	Campbell	2019-03-06	Josephine	13399214	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
725	1990-03-17	Mr.	Guy	Guy	Oliver	2019-03-08	Guy	13400122	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
726	1998-05-24	Mr.	Duncan	Duncan	Wright	2019-03-14	Duncan	13402641	SUPPORTED LIVING	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
727	1980-09-04	Ms.	Paige	Paige	Cunningham	2019-03-19	Paige	13404388	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
728	2015-09-25	Ms.	Elizabeth	Elizabeth	Lewis	2019-03-19	Elizabeth	13404808	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
729	2009-09-22	Mr.	Carl	Carl	Jones	2019-03-26	Carl	13409133	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
730	1971-05-07	Dr.	Benjamin	Benjamin	Elliott	2019-03-28	Benjamin	13410324	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
731	1988-11-22	Mr.	Josephine	Josephine	Allen	2019-03-29	Josephine	13411120	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
732	1994-06-04	Mrs.	Dorothy	Dorothy	Carter	2019-04-09	Dorothy	13417375		Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
733	1975-09-20	Dr.	Heather	Heather	Dickinson	2019-04-15	Heather	13419744	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
734	2019-01-25	Miss	Stacey	Stacey	Wilson	2019-04-15	Stacey	13420267	NHS ACCOMMODATION	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
735	1998-12-15	Mr.	Russell	Russell	Bell	2019-04-16	Russell	13420388	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
736	2011-09-14	Miss	Abdul	Abdul	Roberts	2019-05-10	Abdul	13432648	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
737	1973-02-24	Mr.	Graham	Graham	Ali	2019-06-05	Graham	13442384	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
738	2007-09-08	Dr.	Donna	Donna	Baker	2019-06-18	Donna	13448593	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
739	1985-07-12	Dr.	Jamie	Jamie	Hill	2019-06-19	Jamie	13448996	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
740	1974-04-24	Miss	Sophie	Sophie	Allen	2019-06-26	Sophie	1345321T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
741	1987-07-18	Miss	Pamela	Pamela	Lord	2019-07-01	Pamela	13456190	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
742	1988-08-06	Miss	Cheryl	Cheryl	Hughes	2019-07-15	Cheryl	13465129	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
743	2019-07-10	Dr.	Carolyn	Carolyn	Brown	2019-07-15	Carolyn	13465498	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
744	2018-09-04	Mr.	Tracy	Tracy	Hughes	2019-07-18	Tracy	1346927T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
745	1989-01-27	Mr.	Henry	Henry	Turner	2019-08-01	Henry	13474979	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
746	1972-02-18	Mrs.	Callum	Callum	Young	2019-08-14	Callum	13480535	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
747	1987-10-16	Mr.	Paul	Paul	Fox	2019-08-15	Paul	13481135	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
748	2013-08-27	Ms.	Rosie	Rosie	Harding	2019-08-19	Rosie	13482478	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
749	2011-06-03	Miss	Jay	Jay	King	2019-08-28	Jay	13487465	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
750	2015-05-07	Mr.	Gary	Gary	Wood	2019-09-09	Gary	13493919	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
751	2014-04-10	Mr.	Jason	Jason	Robertson	2019-09-09	Jason	13493983	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
752	1981-07-18	Mr.	Terry	Terry	Griffin	2019-09-13	Terry	13496762	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
753	1997-03-07	Mrs.	Joel	Joel	Patel	2019-09-17	Joel	13498215	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
754	1979-07-04	Miss	Gerald	Gerald	Tucker	2019-09-20	Gerald	13500437	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
755	1975-01-28	Miss	Chelsea	Chelsea	Khan	2019-09-25	Chelsea	13503032	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
756	1982-03-06	Mrs.	Paige	Paige	Henderson	2019-10-02	Paige	13506940	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
757	2008-04-12	Miss	Nicholas	Nicholas	Evans	2019-10-09	Nicholas	13509840	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
758	2019-04-28	Miss	Paula	Paula	Gallagher	2019-10-14	Paula	13511527	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
759	2003-12-28	Mr.	Glen	Glen	Edwards	2019-10-15	Glen	1351233T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
760	2006-10-03	Dr.	Glen	Glen	Thorpe	2019-10-28	Glen	13518100	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
761	2007-05-09	Ms.	Barry	Barry	Barton	2019-11-04	Barry	13522329	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
762	2001-05-22	Dr.	Adrian	Adrian	Davies	2019-11-07	Adrian	13524445	COUNCIL RENTED	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
763	1972-06-18	Dr.	Charlene	Charlene	Spencer	2019-11-12	Charlene	13526405	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
764	2014-07-17	Mr.	Rosemary	Rosemary	Hewitt	2019-11-12	Rosemary	13526463	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
765	1974-01-30	Dr.	Terence	Terence	Evans	2019-11-13	Terence	13526774	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
766	2012-10-25	Dr.	Ellie	Ellie	Sykes	2019-11-14	Ellie	13527247	PRIVATE RENTED	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
767	1981-08-16	Mrs.	Amber	Amber	Kelly	2019-11-18	Amber	13528607	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
768	1998-01-19	Dr.	Mitchell	Mitchell	Chapman	2019-12-07	Mitchell	13538372	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
769	1986-10-16	Miss	Antony	Antony	Collins	2019-12-09	Antony	13538591	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
770	2004-01-29	Dr.	Sandra	Sandra	Nicholls	2019-12-09	Sandra	13538619	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
771	2017-01-18	Miss	Shannon	Shannon	Slater	2019-12-10	Shannon	13539594	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
772	2008-08-15	Mrs.	Vanessa	Vanessa	Lowe	2019-12-18	Vanessa	13544204	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
773	1971-12-12	Mr.	Cheryl	Cheryl	Gill	2019-12-24	Cheryl	13546297	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
774	1973-05-10	Miss	Annette	Annette	Lawrence	2019-12-31	Annette	13546798	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
775	1992-04-12	Miss	Abbie	Abbie	Stephenson	2019-12-31	Abbie	13546936	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
776	1979-02-09	Dr.	Glenn	Glenn	Leonard	2020-01-03	Glenn	13547559	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
777	1989-03-09	Dr.	Sian	Sian	Davies	2020-01-03	Sian	13547686	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
778	2006-08-05	Miss	Amanda	Amanda	Blackburn	2020-01-03	Amanda	13547801	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
779	2001-11-21	Dr.	Marion	Marion	Stephens	2020-01-07	Marion	13548551	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
780	2012-07-25	Mrs.	Rebecca	Rebecca	Thomas	2020-01-18	Rebecca	13554746	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
781	1991-05-23	Mr.	Joshua	Joshua	Evans	2020-01-22	Joshua	13556332	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
782	1979-09-10	Dr.	Timothy	Timothy	Barry	2020-01-28	Timothy	13558995	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
783	1974-01-05	Mrs.	Marc	Marc	Howe	2020-01-29	Marc	13559860	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
784	2005-10-29	Ms.	Leon	Leon	Gregory	2020-01-30	Leon	13560544	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
785	1991-04-07	Dr.	Harriet	Harriet	Hyde	2020-01-31	Harriet	13560636	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
786	1982-04-17	Dr.	Suzanne	Suzanne	Lawrence	2020-01-31	Suzanne	13560918	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
787	1997-03-04	Mrs.	Francis	Francis	Dixon	2020-02-03	Francis	13561524	OTHER	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
788	2011-10-16	Mrs.	Phillip	Phillip	Cooper	2020-02-03	Phillip	13561639	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
789	1974-03-11	Miss	Toby	Toby	Burgess	2020-02-03	Toby	13562090	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
790	1987-12-13	Miss	Carly	Carly	Lee	2020-02-04	Carly	13562654				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
791	2018-06-21	Dr.	John	John	Knight	2020-02-10	John	13565957	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
792	2008-05-13	Mr.	Kyle	Kyle	Bradley	2020-02-12	Kyle	13567376	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
793	2007-06-27	Dr.	Chloe	Chloe	Robinson	2020-02-13	Chloe	13567497	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
794	2003-04-26	Dr.	Diane	Diane	White	2020-02-13	Diane	13567819	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
795	2000-04-06	Miss	Leslie	Leslie	Saunders	2020-02-13	Leslie	1356793T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
796	1983-09-21	Mr.	Kenneth	Kenneth	Allen	2020-02-13	Kenneth	13568016	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
797	1994-04-06	Miss	Natasha	Natasha	Kelly	2020-02-14	Natasha	13568114	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
798	2005-11-20	Dr.	Mohammed	Mohammed	Hart	2020-02-14	Mohammed	13568552	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
799	2013-02-08	Ms.	Arthur	Arthur	Rees	2020-02-18	Arthur	13569866	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
800	1982-10-24	Mr.	Garry	Garry	Harper	2020-02-19	Garry	13570660	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
801	1975-11-06	Miss	Jeremy	Jeremy	Robinson	2020-02-20	Jeremy	13570798	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Co-habiting		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
802	2005-10-02	Mr.	Fiona	Fiona	Bell	2020-02-20	Fiona	13570896	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
803	1996-08-12	Miss	Deborah	Deborah	Wright	2020-02-20	Deborah	13570994	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
804	2019-04-26	Mr.	Anne	Anne	Bird	2020-02-21	Anne	13571496	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
805	2008-06-29	Mr.	Craig	Craig	Martin	2020-02-21	Craig	13571726	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
806	2010-08-04	Ms.	Chelsea	Chelsea	Cunningham	2020-02-24	Chelsea	13571974	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
807	2007-07-31	Dr.	Beth	Beth	Wilkinson	2020-02-24	Beth	13572067	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
808	2001-06-07	Dr.	Lisa	Lisa	Harvey	2020-02-24	Lisa	13572165	OTHER	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
809	1972-09-14	Dr.	Annette	Annette	Dickinson	2020-02-24	Annette	13572211	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
810	1983-08-10	Dr.	Carole	Carole	Osborne	2020-02-25	Carole	13572764	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
811	2017-06-11	Miss	Lindsey	Lindsey	Morgan	2020-02-26	Lindsey	13572856	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
812	1994-07-23	Ms.	Teresa	Teresa	Jones	2020-02-26	Teresa	13573295	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
813	1985-11-19	Dr.	Pamela	Pamela	Webster	2020-02-26	Pamela	13573410	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
814	1990-01-25	Dr.	Harry	Harry	Baldwin	2020-02-27	Harry	13573715	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
815	1980-02-10	Mr.	Justin	Justin	Robinson	2020-03-09	Justin	13578754	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Separated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
816	2018-09-13	Ms.	Cameron	Cameron	Thomas	2020-03-13	Cameron	13581220	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
817	1971-08-30	Dr.	Rachael	Rachael	Webster	2020-03-18	Rachael	13583192	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
818	1988-08-20	Dr.	Rachel	Rachel	Roberts	2020-06-09	Rachel	13611704	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
819	1987-07-18	Miss	Leanne	Leanne	Davis	2020-06-09	Leanne	1361174T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
820	2016-03-28	Dr.	Janice	Janice	Jones	2020-06-09	Janice	13611756				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
821	2009-03-07	Dr.	Jacob	Jacob	Hudson	2020-06-09	Jacob	13611762	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
822	2001-09-08	Miss	Clare	Clare	Green	2020-06-09	Clare	13611779	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
823	1979-11-11	Mr.	Sara	Sara	Kent	2020-06-09	Sara	13611785				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
824	1991-06-07	Mr.	Marian	Marian	Bull	2020-06-09	Marian	13611791	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
825	1978-01-24	Mr.	Karl	Karl	Taylor	2020-06-10	Karl	13611802	OWN HOME	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
826	2006-01-24	Mrs.	Callum	Callum	Roberts	2020-06-10	Callum	13611819	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
827	1996-07-21	Dr.	Jemma	Jemma	O'Neill	2020-06-10	Jemma	13611825	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
828	1973-07-12	Dr.	Diana	Diana	Butler	2020-06-10	Diana	13611831	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
829	1996-08-15	Dr.	Catherine	Catherine	Green	2020-06-10	Catherine	13611848	OWN HOME	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
830	1974-05-31	Mr.	Susan	Susan	Metcalfe	2020-06-10	Susan	13611854	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
831	1998-01-08	Mr.	Grace	Grace	Parkes	2020-06-10	Grace	13611860	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
832	1974-05-31	Miss	Michael	Michael	Armstrong	2020-06-10	Michael	13611917	OWN HOME	Not Stated		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
833	2006-05-31	Miss	Leonard	Leonard	Jarvis	2020-06-12	Leonard	13612552	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
834	1983-10-17	Mr.	Raymond	Raymond	Gray	2020-06-12	Raymond	13612569	OWN HOME	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
835	2014-11-02	Mr.	Mohamed	Mohamed	Dean	2020-06-12	Mohamed	13612575	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
836	2001-08-21	Dr.	Brian	Brian	Harris	2020-06-12	Brian	13612581	NHS ACCOMMODATION			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
837	1982-02-05	Mr.	Diana	Diana	Newman	2020-06-12	Diana	13612598	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
838	1973-11-14	Miss	Ian	Ian	Bruce	2020-06-12	Ian	13612609	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
839	2003-06-12	Mrs.	Lydia	Lydia	Richards	2020-06-12	Lydia	13612615	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
840	1971-08-11	Dr.	Donna	Donna	Knight	2020-06-12	Donna	13612621	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
841	2002-09-28	Mr.	Elliot	Elliot	Baldwin	2020-06-12	Elliot	13612638	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
842	2014-03-18	Mrs.	Lydia	Lydia	Owen	2020-06-12	Lydia	13612644	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
843	1987-11-09	Mr.	Susan	Susan	Palmer	2020-06-12	Susan	13612650				actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
844	1975-04-19	Mrs.	Henry	Henry	James	1994-02-03	Henry	94000393	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
845	1991-12-13	Mrs.	Mohamed	Mohamed	Miller	1994-01-13	Mohamed	94000738	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
846	2018-11-19	Dr.	Sharon	Sharon	Gould	1994-01-18	Sharon	94001471	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
847	2002-11-15	Miss	Julian	Julian	Hill	1994-01-20	Julian	94003667	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
848	2002-12-14	Dr.	Ross	Ross	Clayton	1994-01-10	Ross	9400409T	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
849	2008-11-23	Ms.	Jeremy	Jeremy	Cole	1994-01-11	Jeremy	94004169	SUPERVISED SHELTERED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
850	1994-07-05	Dr.	Louis	Louis	White	1994-01-21	Louis	94004780	SUPERVISED SHELTERED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
851	1996-06-23	Mr.	Wendy	Wendy	Scott	1994-02-04	Wendy	94006227	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
852	2015-01-14	Dr.	Glen	Glen	Cooper	1994-01-27	Glen	94007582	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
853	2013-05-05	Miss	Diana	Diana	Jones	1994-01-31	Diana	94007697	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
854	1985-07-14	Mr.	Lesley	Lesley	Sharp	1994-02-28	Lesley	9400971T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
855	2006-09-01	Ms.	Kelly	Kelly	Murphy	1994-02-02	Kelly	94009939	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
856	1979-10-04	Mr.	Henry	Henry	James	1994-02-17	Henry	94012175	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
857	1976-09-27	Dr.	Jacob	Jacob	Parker	1994-03-21	Jacob	94012682	COUNCIL RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
858	2007-07-07	Mrs.	Damian	Damian	Webb	1994-02-25	Damian	9401326T	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
859	1973-10-18	Mr.	Jade	Jade	Bartlett	1994-03-15	Jade	94013627	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
860	2012-10-04	Dr.	Edward	Edward	Russell	1994-02-25	Edward	94016032	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
861	2016-06-15	Mrs.	Patricia	Patricia	Smith	1994-03-03	Patricia	94016314	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
862	1980-05-23	Miss	Frank	Frank	Brady	1994-03-25	Frank	94017507	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
863	2004-09-24	Mr.	Damian	Damian	Gregory	1994-03-25	Damian	94017513	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
864	1976-03-31	Dr.	Geoffrey	Geoffrey	White	1994-03-29	Geoffrey	94019859	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
865	1984-09-24	Mrs.	Harriet	Harriet	Wells	1994-03-29	Harriet	94020031	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
866	2000-05-22	Ms.	Craig	Craig	Holt	1994-05-05	Craig	94020895	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
867	2010-04-21	Ms.	Garry	Garry	Bevan	1994-04-26	Garry	94021339	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
868	1974-04-09	Mr.	Graham	Graham	Warner	1994-04-28	Graham	9402145T	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
869	1976-03-20	Miss	Graeme	Graeme	Payne	1994-03-29	Graeme	94023680	HEALTH SERVICE PATIENT	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
870	1994-02-06	Dr.	Barry	Barry	Holt	1994-03-22	Barry	94024510	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
871	1992-09-23	Dr.	Victor	Victor	Wright	1994-04-06	Victor	94026142	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
872	1994-09-30	Dr.	Shane	Shane	Scott	1994-05-17	Shane	94026637	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
873	2008-01-22	Mrs.	Amy	Amy	Potts	1994-04-26	Amy	94026885	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
874	1991-07-12	Dr.	Rachael	Rachael	Pritchard	1994-05-23	Rachael	94028799	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
875	1985-04-17	Dr.	Sylvia	Sylvia	Mitchell	1994-04-22	Sylvia	94029163	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
876	2010-09-10	Mr.	Abigail	Abigail	Allen	1994-05-09	Abigail	94029226	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
877	1980-02-25	Miss	Lindsey	Lindsey	Jackson	1994-05-09	Lindsey	94029255	HOUSING ASSOCIATION	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
878	2005-04-30	Mr.	Emily	Emily	Holland	1994-05-09	Emily	94029318	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
879	1990-06-17	Miss	Alison	Alison	Harding	1994-03-31	Alison	94029762	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
880	2011-04-27	Dr.	Damien	Damien	Booth	1994-04-27	Damien	94031017	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
881	2005-05-12	Mrs.	Amber	Amber	Barrett	1994-05-09	Amber	94031196	FAMILY MEMBER/FRIEND'S HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
882	2006-08-01	Dr.	June	June	Owen	1994-05-13	June	94031806	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
883	2014-03-09	Mr.	Katherine	Katherine	Owen	1994-05-20	Katherine	94032032	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
884	1986-05-04	Dr.	Daniel	Daniel	Begum	1994-05-05	Daniel	94032199	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
885	1992-10-02	Mrs.	Ashley	Ashley	Smith	1994-05-20	Ashley	94033219	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
886	1972-01-14	Ms.	Annette	Annette	Pritchard	1994-05-20	Annette	94033571	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
887	2004-12-04	Dr.	Robert	Robert	Hall	1994-05-26	Robert	94034044	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
888	2012-11-26	Ms.	Roger	Roger	Young	1994-06-01	Roger	94034453	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
889	1985-11-28	Miss	Sylvia	Sylvia	Walsh	1994-06-07	Sylvia	94035617	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
890	1984-09-11	Mr.	Graham	Graham	Burton	1994-06-13	Graham	94035842	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
891	1989-08-25	Mr.	Peter	Peter	Clarke	1994-05-26	Peter	94036511	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
892	1970-02-05	Dr.	Sophie	Sophie	Thompson	1994-06-02	Sophie	94036528	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
893	1980-04-26	Dr.	Grace	Grace	Lewis	1994-06-30	Grace	94036747	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
894	1999-10-03	Miss	Charlotte	Charlotte	Stanley	1994-07-01	Charlotte	94036868	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
895	1995-12-17	Dr.	Diane	Diane	Horton	1994-05-25	Diane	94037589	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
896	2006-11-26	Ms.	Brenda	Brenda	Evans	1994-06-30	Brenda	94039929	SUPPORTED HOUSING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
897	2001-07-11	Mr.	Cameron	Cameron	Walsh	1994-05-31	Cameron	94040677	OTHER	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
898	1996-01-20	Miss	Brenda	Brenda	Wilson	1994-06-07	Brenda	94041104	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
899	1994-09-26	Dr.	Sharon	Sharon	Baker	1994-06-14	Sharon	94041225	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
900	1970-01-14	Ms.	Sophie	Sophie	Hobbs	1994-06-28	Sophie	9404167T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
901	2015-02-15	Dr.	Carol	Carol	Cooper	1994-06-30	Carol	94041801	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
902	2005-02-10	Ms.	Alexander	Alexander	Phillips	1994-05-31	Alexander	94042580	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
903	1988-01-23	Dr.	Marc	Marc	Rhodes	1994-06-14	Marc	94044102	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
904	1988-06-08	Dr.	Alexandra	Alexandra	Arnold	1994-06-16	Alexandra	9404438T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
905	1977-03-02	Miss	Rita	Rita	Turner	1994-06-30	Rita	94044586	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
906	1991-06-01	Dr.	Gemma	Gemma	Smith	1994-06-20	Gemma	94044718	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
907	2001-08-22	Ms.	Leah	Leah	Fisher	1994-07-01	Leah	94047244	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
908	2013-03-20	Dr.	Gregory	Gregory	Taylor	1994-07-28	Gregory	94051698	SUPPORTED LIVING	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
909	2008-10-18	Mrs.	Francis	Francis	Lewis	1994-08-04	Francis	94055780	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
910	1984-02-04	Mrs.	Paula	Paula	Khan	1994-08-04	Paula	94056875	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
911	2014-10-27	Dr.	Tina	Tina	O'Neill	1994-08-12	Tina	94058138	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
912	1987-03-31	Ms.	Karen	Karen	Walker	1994-09-05	Karen	94061819	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
913	1974-07-25	Dr.	Joel	Joel	Wood	1994-09-12	Joel	94064587	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
914	1984-04-19	Ms.	Rosemary	Rosemary	Willis	1994-10-18	Rosemary	94071048	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
915	1972-07-04	Dr.	Glenn	Glenn	Kemp	1994-11-09	Glenn	9407151T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
916	1979-08-29	Dr.	Denis	Denis	Welch	1994-10-27	Denis	94074213	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
917	1981-02-26	Dr.	Leslie	Leslie	Palmer	1994-11-28	Leslie	94074985	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
918	1975-10-10	Mr.	Hilary	Hilary	Murray	1994-12-08	Hilary	94076375	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
919	1971-02-15	Mr.	Amber	Amber	White	1994-11-04	Amber	94078030	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
920	2012-09-15	Miss	Marion	Marion	Power	1994-12-05	Marion	94078554	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
921	2007-05-16	Dr.	Rebecca	Rebecca	Gardner	1994-11-15	Rebecca	94079626	COUNCIL RENTED	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
922	1980-09-06	Dr.	Gareth	Gareth	Freeman	1994-11-15	Gareth	94079655	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
923	2008-07-06	Mr.	Elliott	Elliott	Oliver	1994-11-25	Elliott	94082311	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
924	1997-06-26	Dr.	Kayleigh	Kayleigh	Ryan	1994-12-20	Kayleigh	94087154	SUPPORTED LIVING	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
925	1983-12-12	Dr.	Sophie	Sophie	Finch	1994-12-22	Sophie	94090910	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
926	1990-09-09	Ms.	Karl	Karl	Simpson	1995-01-31	Karl	95000256	OWN HOME	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
927	2002-10-31	Mrs.	Ellie	Ellie	Noble	1995-01-31	Ellie	95000400	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
928	1990-10-11	Dr.	Graeme	Graeme	Carter	1995-01-11	Graeme	9500122T	PRIVATE HOSPITAL	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
929	2001-10-22	Ms.	Julia	Julia	Norris	1995-01-04	Julia	95002441	HEALTH SERVICE PATIENT	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
930	1973-09-19	Dr.	Danielle	Danielle	Robinson	1995-01-31	Danielle	9500544T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
931	2010-02-15	Miss	Jennifer	Jennifer	North	1995-01-11	Jennifer	95006822	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
932	2003-07-27	Ms.	Barry	Barry	Collins	1995-02-06	Barry	95010297	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
933	2017-06-14	Miss	Conor	Conor	Singh	1995-03-03	Conor	95014298	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
934	1995-09-20	Miss	Declan	Declan	Elliott	1995-04-25	Declan	95017676	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
935	1990-06-28	Mrs.	Gavin	Gavin	Allen	1995-03-09	Gavin	95018760	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
936	2005-12-11	Dr.	Carole	Carole	Iqbal	1995-04-21	Carole	95028213	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
937	1991-07-30	Mr.	Bethan	Bethan	Mistry	1995-07-18	Bethan	95030119	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
938	1984-08-02	Miss	Marcus	Marcus	Martin	1995-05-15	Marcus	95032391	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
939	2019-10-27	Ms.	Victoria	Victoria	Morgan	1995-05-26	Victoria	95032638	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
940	1988-10-11	Mr.	Maurice	Maurice	Williams	1995-05-17	Maurice	95035544	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
941	1974-08-18	Dr.	Marion	Marion	Fowler	1995-07-10	Marion	9504667T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
942	2001-06-21	Ms.	Valerie	Valerie	Bird	1995-07-10	Valerie	95046732	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
943	2005-01-09	Mr.	Brandon	Brandon	Green	1995-07-10	Brandon	95046778	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
944	1996-03-08	Dr.	Shannon	Shannon	Wall	1995-07-28	Shannon	95049033	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
945	2007-11-24	Mrs.	Maureen	Maureen	Harris	1995-09-13	Maureen	95049684	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
946	1995-01-30	Mrs.	Ashley	Ashley	Davies	1995-07-14	Ashley	95050028	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
947	2007-12-24	Mrs.	Ben	Ben	Roberts	1995-10-20	Ben	95050777	PRIVATE RENTED	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
948	1980-03-14	Mr.	Terry	Terry	Robson	1995-07-25	Terry	95053308	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
949	1974-10-19	Dr.	Kevin	Kevin	Wilson	1995-07-27	Kevin	95053648	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Widowed		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
950	1997-11-02	Ms.	Jack	Jack	Mason	1995-08-01	Jack	95054248	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
951	2009-07-12	Ms.	James	James	Baxter	1995-08-03	James	95054605	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
952	1987-04-16	Dr.	Wayne	Wayne	Jackson	1995-08-07	Wayne	95056617	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
953	1976-02-25	Mrs.	Shirley	Shirley	Johnson	1995-10-16	Shirley	95062876	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
954	2018-03-19	Dr.	Christian	Christian	Page	1995-10-16	Christian	95064335	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
955	1985-12-12	Mr.	Ashleigh	Ashleigh	Lees	1995-10-31	Ashleigh	95065851	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
956	1987-02-03	Mrs.	Kevin	Kevin	Atkins	1995-10-12	Kevin	95072099	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
957	2016-03-21	Mr.	Ricky	Ricky	Nicholls	1995-10-20	Ricky	95073534	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
958	1979-10-30	Dr.	Ryan	Ryan	Brooks	1996-01-03	Ryan	95088769	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
959	1999-11-26	Mr.	Olivia	Olivia	Morgan	1996-01-04	Olivia	95089035	LA PART 3 ACCOMMODATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
960	1987-08-19	Dr.	George	George	Dennis	1996-02-21	George	95095271	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
961	1998-09-14	Mr.	Henry	Henry	West	1996-03-13	Henry	95095697	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
962	2004-11-10	Miss	Karen	Karen	Simpson	1996-03-15	Karen	9509575T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
963	2006-07-13	Mrs.	Frank	Frank	Norman	1996-02-08	Frank	95096988	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
964	1975-10-04	Mrs.	Louis	Louis	Taylor	1996-02-21	Louis	95101131	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
965	1990-02-18	Mrs.	Diana	Diana	Power	1996-03-05	Diana	9510511T		Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
966	1973-10-06	Dr.	Eleanor	Eleanor	Gray	1996-03-29	Eleanor	95107490	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
967	1990-11-21	Dr.	Darren	Darren	Johnson	1996-04-30	Darren	95110088	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
968	1970-02-11	Dr.	Bethany	Bethany	Taylor	1996-04-02	Bethany	9511251T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
969	2014-08-08	Ms.	Suzanne	Suzanne	Watts	1985-01-14	Suzanne	95708936	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
970	2001-04-14	Dr.	Roger	Roger	Hughes	1984-12-06	Roger	95907481	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
971	2000-05-21	Miss	Wendy	Wendy	Thompson	1985-01-10	Wendy	96300648	SUPPORTED LIVING			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
972	2006-04-10	Miss	Brett	Brett	Smith	1984-12-12	Brett	96400946	SUPPORTED LIVING			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
973	1984-10-21	Mr.	Tracy	Tracy	Alexander	1985-01-28	Tracy	96505010	OTHER			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
974	1974-05-13	Mr.	Geraldine	Geraldine	Robertson	1985-01-14	Geraldine	97009936	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
975	1992-11-30	Miss	Jayne	Jayne	Anderson	1984-12-14	Jayne	97111265	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
976	1988-09-21	Mrs.	Jodie	Jodie	Barber	1984-12-12	Jodie	97200058	HOSTEL			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
977	1976-07-03	Dr.	Nicola	Nicola	Morris	1984-12-14	Nicola	97432184	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
978	1977-05-03	Mrs.	Stewart	Stewart	Harper	1985-01-11	Stewart	97520164	PRIVATE RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
979	1977-08-24	Miss	Elaine	Elaine	Smith	1984-12-14	Elaine	97532758	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
980	1993-07-08	Dr.	Lynne	Lynne	Johnson	1984-12-07	Lynne	97624336	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
981	1994-04-19	Dr.	Leigh	Leigh	Gould	1985-01-11	Leigh	97626072	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
982	1982-11-11	Dr.	Gillian	Gillian	Hunt	1984-11-28	Gillian	97820067	HOUSING ASSOCIATION	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
983	1996-03-26	Mrs.	Victor	Victor	Smith	1984-11-27	Victor	97830937	OTHER			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
984	1973-06-12	Mrs.	Jamie	Jamie	Murray	1984-11-28	Jamie	97901626	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
985	1988-08-09	Miss	Jayne	Jayne	Collins	1984-12-14	Jayne	98013349	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
986	1982-08-28	Dr.	Paige	Paige	Mason	1984-12-13	Paige	9803605T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
987	1988-02-07	Dr.	Hannah	Hannah	Holmes	1984-12-03	Hannah	98036901	SUPERVISED SHELTERED			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
988	1970-10-14	Mr.	Marcus	Marcus	Wilson	1984-12-04	Marcus	98123544	OWN HOME			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
989	1979-12-14	Miss	Beverley	Beverley	Johnson	1985-01-02	Beverley	98141395	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
990	1992-04-16	Mr.	Tony	Tony	McCarthy	1984-11-29	Tony	9820277T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
991	1995-09-27	Mrs.	Iain	Iain	Knight	1985-01-03	Iain	98220297	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
992	1996-06-02	Miss	Diana	Diana	Lawson	1985-01-03	Diana	98239268	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Married		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
993	1979-10-16	Mrs.	Rita	Rita	Gordon	1985-01-08	Rita	98312347	COUNCIL RENTED	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
994	1980-12-19	Dr.	Ashleigh	Ashleigh	Lee	1985-01-22	Ashleigh	9833009T	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)			actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
995	1977-04-11	Ms.	Claire	Claire	Andrews	1985-02-13	Claire	9851336T	OWN HOME	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
996	1973-08-23	Mr.	Victoria	Victoria	Lawrence	1986-04-30	Victoria	98624482	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
997	1981-05-30	Dr.	Cameron	Cameron	Edwards	1991-10-24	Cameron	9916269T	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
998	1997-10-02	Mr.	Linda	Linda	Barker	1992-04-23	Linda	99262664	SUPPORTED LIVING	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
999	2012-05-29	Dr.	Graham	Graham	Jackson	1993-11-08	Graham	99314363	CARE/NURSING/RESIDENTIAL HOME (PRIVATE/LA/REGISTERED)	Single		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
1000	1998-06-04	Ms.	Carole	Carole	Hunt	1993-09-29	Carole	99328514	OWN HOME	Divorced		actor_client	True	False	False	Active	Todays date	False	False	False	False	False	False	False	False	False	10	Casrec	Todays date
\.


--
-- Data for Name: phonenumbers; Type: TABLE DATA; Schema: pre_migrate; Owner: casrec
--

COPY pre_migrate.phonenumbers (id, phone_number, c_case, type, is_default, updateddate, caserecnumber, person_id) FROM stdin;
1	01154960855	10000037	Home	False	Todays Date	10000037	1
2	0141 4960772	10000884	Home	False	Todays Date	10000884	2
3	(0116) 4960140	10001403	Home	False	Todays Date	10001403	3
4	+44(0)1174960053	10001668	Home	False	Todays Date	10001668	4
5	01184960761	10002199	Home	False	Todays Date	10002199	5
6	(0113) 4960022	10002625	Home	False	Todays Date	10002625	6
7	+44808 1570800	10003409	Home	False	Todays Date	10003409	7
8	(0114) 4960390	10004038	Home	False	Todays Date	10004038	8
9	0289018476	10004188	Home	False	Todays Date	10004188	9
10	+44(0)116 4960164	10004257	Home	False	Todays Date	10004257	10
11	(0131)4960373	10004263	Home	False	Todays Date	10004263	11
12	(0131)4960449	10004637	Home	False	Todays Date	10004637	12
13	+44(0)151 4960672	10004741	Home	False	Todays Date	10004741	13
14	(0114) 496 0455	10004879	Home	False	Todays Date	10004879	14
15	+44292018637	10005237	Home	False	Todays Date	10005237	15
16	+44161 4960565	10005243	Home	False	Todays Date	10005243	16
17	+44(0)117 4960313	10005433	Home	False	Todays Date	10005433	17
18	+44(0)28 9018 0612	10005928	Home	False	Todays Date	10005928	18
19	(0808) 1570245	10006315	Home	False	Todays Date	10006315	19
20	+441154960484	10006413	Home	False	Todays Date	10006413	20
21	0116 496 0817	10007163	Home	False	Todays Date	10007163	21
22	(0131) 496 0533	10007261	Home	False	Todays Date	10007261	22
23	+44191 496 0766	10007877	Home	False	Todays Date	10007877	23
24	(0131) 4960727	10008713	Home	False	Todays Date	10008713	24
25	(01632) 960 031	10009307	Home	False	Todays Date	10009307	25
26	09098790086	10009526	Home	False	Todays Date	10009526	26
27	(0161)4960820	10010274	Home	False	Todays Date	10010274	27
28	0117 4960465	10011951	Home	False	Todays Date	10011951	28
29	0808 157 0801	10012240	Home	False	Todays Date	10012240	29
30	+44(0)808 1570910	10012643	Home	False	Todays Date	10012643	30
31	+441614960778	10013116	Home	False	Todays Date	10013116	31
32	+44(0)131 4960754	10013560	Home	False	Todays Date	10013560	32
33	+44(0)116 496 0522	10013583	Home	False	Todays Date	10013583	33
34	0113 4960875	10013617	Home	False	Todays Date	10013617	34
35	(0115) 4960603	1001404T	Home	False	Todays Date	1001404T	35
36	(0161) 496 0407	10014200	Home	False	Todays Date	10014200	36
37	+44(0)115 496 0565	10015094	Home	False	Todays Date	10015094	37
38	0161 496 0434	10015105	Home	False	Todays Date	10015105	38
39	+44909 8790349	10015981	Home	False	Todays Date	10015981	39
40	+44(0)1184960596	10016195	Home	False	Todays Date	10016195	40
41	0909 879 0730	10016235	Home	False	Todays Date	10016235	41
42	(0306) 999 0183	10016431	Home	False	Todays Date	10016431	42
43	+44808 1570504	10016621	Home	False	Todays Date	10016621	43
44	(0191) 4960254	10016667	Home	False	Todays Date	10016667	44
45	(0141) 496 0865	10017181	Home	False	Todays Date	10017181	45
46	0141 4960088	10018420	Home	False	Todays Date	10018420	46
47	(020) 74960259	10018593	Home	False	Todays Date	10018593	47
48	(0808) 157 0869	10019377	Home	False	Todays Date	10019377	48
49	+44(0)1632960799	10020349	Home	False	Todays Date	10020349	49
50	+44(0)115 4960424	10020418	Home	False	Todays Date	10020418	50
51	+443069990800	10020597	Home	False	Todays Date	10020597	51
52	+441914960912	1002065T	Home	False	Todays Date	1002065T	52
53	0131 4960364	10020983	Home	False	Todays Date	10020983	53
54	(0808) 1570440	10021220	Home	False	Todays Date	10021220	54
55	+441314960057	10021744	Home	False	Todays Date	10021744	55
56	(01632) 960 994	10023226	Home	False	Todays Date	10023226	56
57	+44(0)289018322	10023232	Home	False	Todays Date	10023232	57
58	+44(0)1314960155	10023301	Home	False	Todays Date	10023301	58
59	+44306 999 0879	10023480	Home	False	Todays Date	10023480	59
60	(0118) 4960734	10023664	Home	False	Todays Date	10023664	60
61	+442074960043	10023877	Home	False	Todays Date	10023877	61
62	01134960182	10024391	Home	False	Todays Date	10024391	62
63	+441134960796	10024500	Home	False	Todays Date	10024500	63
64	(020) 74960957	13611727	Home	False	Todays Date	13611727	64
65	0116 4960352	10025630	Home	False	Todays Date	10025630	65
66	08081570196	10025751	Home	False	Todays Date	10025751	66
67	+44(0)808 157 0713	10025768	Home	False	Todays Date	10025768	67
68	(0808) 1570893	1002630T	Home	False	Todays Date	1002630T	68
69	0115 496 0940	10026374	Home	False	Todays Date	10026374	69
70	(0116) 496 0793	10027550	Home	False	Todays Date	10027550	70
71	+44(0)121 496 0242	10027832	Home	False	Todays Date	10027832	71
72	(0151) 496 0872	1002818T	Home	False	Todays Date	1002818T	72
73	01174960869	10028288	Home	False	Todays Date	10028288	73
74	029 2018 0727	10028340	Home	False	Todays Date	10028340	74
75	+44(0)161 4960680	10029078	Home	False	Todays Date	10029078	75
76	(01632)960910	10029084	Home	False	Todays Date	10029084	76
77	+44118 496 0924	10029245	Home	False	Todays Date	10029245	77
78	+44(0)117 4960307	10029556	Home	False	Todays Date	10029556	78
79	(0191)4960303	10029602	Home	False	Todays Date	10029602	79
80	(0118)4960797	1003019T	Home	False	Todays Date	1003019T	80
81	+44(0)191 496 0274	1003061T	Home	False	Todays Date	1003061T	81
82	(0116) 4960809	10030816	Home	False	Todays Date	10030816	82
83	01154960650	10030868	Home	False	Todays Date	10030868	83
84	+44(0)121 496 0770	10031042	Home	False	Todays Date	10031042	84
85	01144960202	10033048	Home	False	Todays Date	10033048	85
86	+44909 879 0234	10033250	Home	False	Todays Date	10033250	86
87	0292018786	10033561	Home	False	Todays Date	10033561	87
88	(0151)4960528	10033653	Home	False	Todays Date	10033653	88
89	029 2018 0922	10033837	Home	False	Todays Date	10033837	89
90	+44(0)115 4960987	10034253	Home	False	Todays Date	10034253	90
91	(0808)1570064	10034558	Home	False	Todays Date	10034558	91
92	+44(0)161 4960462	10034898	Home	False	Todays Date	10034898	92
93	+44(0)289018799	10035164	Home	False	Todays Date	10035164	93
94	(0117) 4960123	10036052	Home	False	Todays Date	10036052	94
95	+44141 4960641	10037026	Home	False	Todays Date	10037026	95
96	+44113 496 0390	10038450	Home	False	Todays Date	10038450	96
97	01414960255	10039522	Home	False	Todays Date	10039522	97
98	+44(0)1174960831	10040074	Home	False	Todays Date	10040074	98
99	+44(0)151 496 0407	10040794	Home	False	Todays Date	10040794	99
100	+441632 960105	10041002	Home	False	Todays Date	10041002	100
101	(0141) 496 0570	10041221	Home	False	Todays Date	10041221	101
102	+44306 999 0238	10041912	Home	False	Todays Date	10041912	102
103	(0113)4960254	10042691	Home	False	Todays Date	10042691	103
104	(0117)4960242	10042817	Home	False	Todays Date	10042817	104
105	+442074960148	10042909	Home	False	Todays Date	10042909	105
106	(028) 9018792	10043164	Home	False	Todays Date	10043164	106
107	0151 496 0490	10043855	Home	False	Todays Date	10043855	107
108	(0151) 4960255	10044150	Home	False	Todays Date	10044150	108
109	+44(0)289018318	10044547	Home	False	Todays Date	10044547	109
110	01632960184	10044553	Home	False	Todays Date	10044553	110
111	+44(0)808 1570195	10045118	Home	False	Todays Date	10045118	111
112	+44292018216	10045441	Home	False	Todays Date	10045441	112
113	+44114 496 0196	10045717	Home	False	Todays Date	10045717	113
114	0151 4960545	10046369	Home	False	Todays Date	10046369	114
115	+44(0)121 496 0792	1004731T	Home	False	Todays Date	1004731T	115
116	+44(0)1632 960084	10048151	Home	False	Todays Date	10048151	116
117	(0306) 9990450	10048168	Home	False	Todays Date	10048168	117
118	(0161)4960947	10050276	Home	False	Todays Date	10050276	118
119	+441214960382	10050512	Home	False	Todays Date	10050512	119
120	020 7946 0817	10051538	Home	False	Todays Date	10051538	120
121	+44(0)1214960483	10051890	Home	False	Todays Date	10051890	121
122	+44292018311	10052501	Home	False	Todays Date	10052501	122
123	(0141) 496 0497	10052743	Home	False	Todays Date	10052743	123
124	(01632) 960 572	10053032	Home	False	Todays Date	10053032	124
125	(0306)9990265	10053723	Home	False	Todays Date	10053723	125
126	(0191)4960443	10053746	Home	False	Todays Date	10053746	126
127	+441314960938	10054300	Home	False	Todays Date	10054300	127
128	0113 496 0939	10055096	Home	False	Todays Date	10055096	128
129	+44(0)118 496 0234	10055666	Home	False	Todays Date	10055666	129
130	+44(0)118 4960983	10056335	Home	False	Todays Date	10056335	130
131	+441314960534	10056410	Home	False	Todays Date	10056410	131
132	+44(0)1154960970	10056865	Home	False	Todays Date	10056865	132
133	+44(0)20 7496 0749	10056957	Home	False	Todays Date	10056957	133
134	+44(0)113 4960985	10057661	Home	False	Todays Date	10057661	134
135	020 74960499	10057995	Home	False	Todays Date	10057995	135
136	(028) 9018220	10058071	Home	False	Todays Date	10058071	136
137	+44(0)116 4960817	10058140	Home	False	Todays Date	10058140	137
138	+449098790079	10058508	Home	False	Todays Date	10058508	138
139	+44(0)1184960222	10058589	Home	False	Todays Date	10058589	139
140	(0131)4960127	10058917	Home	False	Todays Date	10058917	140
141	+44(0)1144960809	1005934T	Home	False	Todays Date	1005934T	141
142	+4420 74960778	10060501	Home	False	Todays Date	10060501	142
143	+44(0)1614960690	10062185	Home	False	Todays Date	10062185	143
144	+44808 157 0070	10062191	Home	False	Todays Date	10062191	144
145	(0909) 879 0542	1006312T	Home	False	Todays Date	1006312T	145
146	(029)2018349	10063257	Home	False	Todays Date	10063257	146
147	0808 1570506	10063614	Home	False	Todays Date	10063614	147
148	+44(0)161 496 0501	10064295	Home	False	Todays Date	10064295	148
149	+44(0)29 2018722	10064669	Home	False	Todays Date	10064669	149
150	+44114 496 0982	10065004	Home	False	Todays Date	10065004	150
151	+44(0)161 4960099	10065010	Home	False	Todays Date	10065010	151
152	(0151) 496 0043	10065632	Home	False	Todays Date	10065632	152
153	+449098790692	10065868	Home	False	Todays Date	10065868	153
154	+44(0)191 496 0355	10067863	Home	False	Todays Date	10067863	154
155	028 9018 0691	10068267	Home	False	Todays Date	10068267	155
156	+44141 496 0097	10069846	Home	False	Todays Date	10069846	156
157	+44(0)1314960173	1007033T	Home	False	Todays Date	1007033T	157
158	028 9018 0742	10070980	Home	False	Todays Date	10070980	158
159	(0118) 4960117	10071240	Home	False	Todays Date	10071240	159
160	+44131 496 0275	1007165T	Home	False	Todays Date	1007165T	160
161	+441914960050	10071919	Home	False	Todays Date	10071919	161
162	(0118)4960555	10072053	Home	False	Todays Date	10072053	162
163	+44(0)8081570984	10072180	Home	False	Todays Date	10072180	163
164	0306 9990292	10072548	Home	False	Todays Date	10072548	164
165	+44(0)151 496 0322	10072617	Home	False	Todays Date	10072617	165
166	0118 4960251	10072652	Home	False	Todays Date	10072652	166
167	+44(0)8081570276	10072905	Home	False	Todays Date	10072905	167
168	(0161) 496 0650	10075788	Home	False	Todays Date	10075788	168
169	01514960206	10075794	Home	False	Todays Date	10075794	169
170	(0116) 496 0579	10075892	Home	False	Todays Date	10075892	170
171	+44(0)115 4960300	10076307	Home	False	Todays Date	10076307	171
172	+449098790171	10076428	Home	False	Todays Date	10076428	172
173	+441914960222	10076618	Home	False	Todays Date	10076618	173
174	+44(0)151 496 0247	10077466	Home	False	Todays Date	10077466	174
175	(0141) 4960464	10077535	Home	False	Todays Date	10077535	175
176	01174960332	10077702	Home	False	Todays Date	10077702	176
177	(0113)4960513	10078014	Home	False	Todays Date	10078014	177
178	0161 4960918	10078498	Home	False	Todays Date	10078498	178
179	+44118 4960912	1008006T	Home	False	Todays Date	1008006T	179
180	(0118) 4960765	10080306	Home	False	Todays Date	10080306	180
181	01632 960379	10080698	Home	False	Todays Date	10080698	181
182	+44121 4960119	10080773	Home	False	Todays Date	10080773	182
183	+44(0)118 4960311	10080842	Home	False	Todays Date	10080842	183
184	+44(0)29 2018 0892	10081321	Home	False	Todays Date	10081321	184
185	0115 4960735	10081436	Home	False	Todays Date	10081436	185
186	(028) 9018 0086	10082290	Home	False	Todays Date	10082290	186
187	+44(0)909 8790025	10082629	Home	False	Todays Date	10082629	187
188	+44(0)1164960075	10084054	Home	False	Todays Date	10084054	188
189	(0114) 4960605	10085368	Home	False	Todays Date	10085368	189
190	0141 496 0372	10086377	Home	False	Todays Date	10086377	190
191	01314960913	10086803	Home	False	Todays Date	10086803	191
192	(0141) 496 0841	10087046	Home	False	Todays Date	10087046	192
193	+4429 2018230	10087121	Home	False	Todays Date	10087121	193
194	+44(0)116 4960770	10087207	Home	False	Todays Date	10087207	194
195	0306 999 0283	10087392	Home	False	Todays Date	10087392	195
196	0117 496 0794	10087622	Home	False	Todays Date	10087622	196
197	(029) 2018226	10088090	Home	False	Todays Date	10088090	197
198	+44(0)1632 960297	10088470	Home	False	Todays Date	10088470	198
199	+441154960020	10089346	Home	False	Todays Date	10089346	199
200	+44(0)114 4960742	10090422	Home	False	Todays Date	10090422	200
201	(0191) 496 0252	10090923	Home	False	Todays Date	10090923	201
202	+44114 496 0017	10090969	Home	False	Todays Date	10090969	202
203	(028) 9018026	10092221	Home	False	Todays Date	10092221	203
204	+441214960672	10093529	Home	False	Todays Date	10093529	204
205	(0191)4960160	10093996	Home	False	Todays Date	10093996	205
206	(0114) 496 0102	10094354	Home	False	Todays Date	10094354	206
207	+44(0)28 9018655	10094976	Home	False	Todays Date	10094976	207
208	(029) 2018264	10095259	Home	False	Todays Date	10095259	208
209	(0141) 496 0146	10096406	Home	False	Todays Date	10096406	209
210	+44(0)113 4960034	10097012	Home	False	Todays Date	10097012	210
211	+44(0)115 4960475	10097922	Home	False	Todays Date	10097922	211
212	(0113)4960646	10099491	Home	False	Todays Date	10099491	212
213	(0909)8790501	10099894	Home	False	Todays Date	10099894	213
214	0909 8790799	10101102	Home	False	Todays Date	10101102	214
215	+44(0)115 4960179	10101321	Home	False	Todays Date	10101321	215
216	+441184960810	10102566	Home	False	Todays Date	10102566	216
217	+44(0)1614960777	10102658	Home	False	Todays Date	10102658	217
218	+44121 4960942	1010391T	Home	False	Todays Date	1010391T	218
219	0131 4960066	10105028	Home	False	Todays Date	10105028	219
220	+44(0)1632 960438	10106020	Home	False	Todays Date	10106020	220
221	(0114) 4960480	10106095	Home	False	Todays Date	10106095	221
222	+44118 496 0886	10106665	Home	False	Todays Date	10106665	222
223	(0121) 496 0217	10107023	Home	False	Todays Date	10107023	223
224	(0161)4960978	10108458	Home	False	Todays Date	10108458	224
225	01154960292	10108700	Home	False	Todays Date	10108700	225
226	+44118 496 0715	10108815	Home	False	Todays Date	10108815	226
227	0909 879 0446	10109006	Home	False	Todays Date	10109006	227
228	0191 4960169	10109755	Home	False	Todays Date	10109755	228
229	+44(0)113 496 0681	1011017T	Home	False	Todays Date	1011017T	229
230	0191 498 0104	10114095	Home	False	Todays Date	10114095	230
231	0117 4960868	10114544	Home	False	Todays Date	10114544	231
232	+44(0)1914960800	10114901	Home	False	Todays Date	10114901	232
233	+44113 4960431	10117542	Home	False	Todays Date	10117542	233
234	+44(0)117 4960073	10117594	Home	False	Todays Date	10117594	234
235	(0909) 8790157	1011850T	Home	False	Todays Date	1011850T	235
236	01144960069	10118539	Home	False	Todays Date	10118539	236
237	+441314960469	10118706	Home	False	Todays Date	10118706	237
238	+44(0)808 1570047	10122279	Home	False	Todays Date	10122279	238
239	+44(0)1174960758	10123455	Home	False	Todays Date	10123455	239
240	(0191) 4960126	10125087	Home	False	Todays Date	10125087	240
241	+44909 8790353	10126044	Home	False	Todays Date	10126044	241
242	(0131) 496 0821	10126234	Home	False	Todays Date	10126234	242
243	0114 4960195	10126597	Home	False	Todays Date	10126597	243
244	(0141) 4960457	10129802	Home	False	Todays Date	10129802	244
245	+44(0)808 157 0241	10131138	Home	False	Todays Date	10131138	245
246	(0114)4960988	10131668	Home	False	Todays Date	10131668	246
247	+44(0)114 496 0112	10131979	Home	False	Todays Date	10131979	247
248	(0114) 496 0116	10132222	Home	False	Todays Date	10132222	248
249	+44151 4960026	10132683	Home	False	Todays Date	10132683	249
250	+44292018467	10133847	Home	False	Todays Date	10133847	250
251	09098790390	10134292	Home	False	Todays Date	10134292	251
252	(0808)1570770	10134672	Home	False	Todays Date	10134672	252
253	+44(0)29 2018734	10135295	Home	False	Todays Date	10135295	253
254	+44141 4960081	10135341	Home	False	Todays Date	10135341	254
255	(0116)4960922	10138356	Home	False	Todays Date	10138356	255
256	(0117) 4960917	10138460	Home	False	Todays Date	10138460	256
257	0909 879 0658	10138517	Home	False	Todays Date	10138517	257
258	+44(0)118 4960318	10139181	Home	False	Todays Date	10139181	258
259	(01632) 960 603	10139342	Home	False	Todays Date	10139342	259
260	+44(0)1184960426	10140700	Home	False	Todays Date	10140700	260
261	+44118 496 0854	10140913	Home	False	Todays Date	10140913	261
262	+44292018250	10141202	Home	False	Todays Date	10141202	262
263	+44306 9990223	10141254	Home	False	Todays Date	10141254	263
264	+44114 4960443	1014133T	Home	False	Todays Date	1014133T	264
265	+44(0)1414960382	10142038	Home	False	Todays Date	10142038	265
266	+4429 2018400	10142194	Home	False	Todays Date	10142194	266
267	020 74960066	1014265T	Home	False	Todays Date	1014265T	267
268	(01632) 960 706	10142729	Home	False	Todays Date	10142729	268
269	(0909) 8790326	10142856	Home	False	Todays Date	10142856	269
270	+44(0)2074960364	10143894	Home	False	Todays Date	10143894	270
271	+44113 496 0784	10146500	Home	False	Todays Date	10146500	271
272	+44(0)114 496 0812	10149066	Home	False	Todays Date	10149066	272
273	01314960328	10149878	Home	False	Todays Date	10149878	273
274	+44(0)118 496 0613	1015099T	Home	False	Todays Date	1015099T	274
275	(0808) 157 0400	10151208	Home	False	Todays Date	10151208	275
276	(0191) 4960754	10152488	Home	False	Todays Date	10152488	276
277	0909 8790748	10152868	Home	False	Todays Date	10152868	277
278	+44(0)1632 960 529	10153255	Home	False	Todays Date	10153255	278
279	0909 8790026	1015355T	Home	False	Todays Date	1015355T	279
280	+441134960380	10153802	Home	False	Todays Date	10153802	280
281	+44(0)141 4960362	10154051	Home	False	Todays Date	10154051	281
282	+44(0)141 4960618	10154097	Home	False	Todays Date	10154097	282
283	02074960443	10154500	Home	False	Todays Date	10154500	283
284	+44141 496 0548	10156034	Home	False	Todays Date	10156034	284
285	(0118)4960714	10156656	Home	False	Todays Date	10156656	285
286	+449098790185	10158403	Home	False	Todays Date	10158403	286
287	+44306 999 0219	10159625	Home	False	Todays Date	10159625	287
288	0116 496 0791	10159936	Home	False	Todays Date	10159936	288
289	+441614960348	10160321	Home	False	Todays Date	10160321	289
290	020 74960970	10160367	Home	False	Todays Date	10160367	290
291	(0121) 4960516	10160897	Home	False	Todays Date	10160897	291
292	(0131) 4960890	10160966	Home	False	Todays Date	10160966	292
293	(020)74960489	10162667	Home	False	Todays Date	10162667	293
294	+44114 4960971	10164063	Home	False	Todays Date	10164063	294
295	(0118) 496 0261	10164149	Home	False	Todays Date	10164149	295
296	+44(0)191 496 0858	10164178	Home	False	Todays Date	10164178	296
297	+44(0)115 496 0869	1016562T	Home	False	Todays Date	1016562T	297
298	(0909) 8790029	10166328	Home	False	Todays Date	10166328	298
299	+44(0)161 4960616	10181803	Home	False	Todays Date	10181803	299
300	+44121 496 0351	10181930	Home	False	Todays Date	10181930	300
301	01414960394	10182311	Home	False	Todays Date	10182311	301
302	(01632) 960164	10183078	Home	False	Todays Date	10183078	302
303	+44(0)909 879 0443	10184300	Home	False	Todays Date	10184300	303
304	0116 4960217	10185735	Home	False	Todays Date	10185735	304
305	0151 496 0101	10192899	Home	False	Todays Date	10192899	305
306	(0121)4960242	10192916	Home	False	Todays Date	10192916	306
307	(0117)4960494	10194709	Home	False	Todays Date	10194709	307
308	0115 4960621	10198244	Home	False	Todays Date	10198244	308
309	+44115 4960204	10199092	Home	False	Todays Date	10199092	309
310	+441154960244	10200679	Home	False	Todays Date	10200679	310
311	0131 496 0656	10200685	Home	False	Todays Date	10200685	311
312	01144960321	10200748	Home	False	Todays Date	10200748	312
313	+44292018112	10201193	Home	False	Todays Date	10201193	313
314	+44(0)1154960850	10201705	Home	False	Todays Date	10201705	314
315	0115 496 0919	10202386	Home	False	Todays Date	10202386	315
316	+44131 4960080	10494872	Home	False	Todays Date	10494872	316
317	(0161)4960170	10204496	Home	False	Todays Date	10204496	317
318	028 9018 0549	1020512T	Home	False	Todays Date	1020512T	318
319	(0115) 4960381	10206404	Home	False	Todays Date	10206404	319
320	+44(0)131 4960748	10207131	Home	False	Todays Date	10207131	320
321	+442074960024	10208946	Home	False	Todays Date	10208946	321
322	(0151) 4960536	10209045	Home	False	Todays Date	10209045	322
323	+441144960538	1021075T	Home	False	Todays Date	1021075T	323
324	(0117)4960388	10211717	Home	False	Todays Date	10211717	324
325	+4420 7496 0225	10213228	Home	False	Todays Date	10213228	325
326	(0306)9990264	10214807	Home	False	Todays Date	10214807	326
327	+44(0)151 4960004	10214940	Home	False	Todays Date	10214940	327
328	0117 4960586	10215183	Home	False	Todays Date	10215183	328
329	(0306) 9990336	10216508	Home	False	Todays Date	10216508	329
330	01632 960560	10221960	Home	False	Todays Date	10221960	330
331	01632 960 041	10222865	Home	False	Todays Date	10222865	331
332	0161 4960432	10228043	Home	False	Todays Date	10228043	332
333	+44(0)116 4960553	10231275	Home	False	Todays Date	10231275	333
334	(0191)4960580	10232094	Home	False	Todays Date	10232094	334
335	(0121)4960167	1023217T	Home	False	Todays Date	1023217T	335
336	+44(0)1164960422	10233264	Home	False	Todays Date	10233264	336
337	0114 4960360	10233327	Home	False	Todays Date	10233327	337
338	+44131 496 0592	10235783	Home	False	Todays Date	10235783	338
339	(020)74960243	10236953	Home	False	Todays Date	10236953	339
340	(0113) 496 0441	10238118	Home	False	Todays Date	10238118	340
341	+441184960453	1024055T	Home	False	Todays Date	1024055T	341
342	(0118) 4960046	10241932	Home	False	Todays Date	10241932	342
343	+44191 496 0164	10241990	Home	False	Todays Date	10241990	343
344	01134960896	10242970	Home	False	Todays Date	10242970	344
345	+44(0)116 4960772	10243443	Home	False	Todays Date	10243443	345
346	+4428 9018 0010	10243489	Home	False	Todays Date	10243489	346
347	+44(0)909 8790659	10244918	Home	False	Todays Date	10244918	347
348	(0117) 496 0411	10245530	Home	False	Todays Date	10245530	348
349	+441632 960 981	10245576	Home	False	Todays Date	10245576	349
350	(029) 2018 0744	10246308	Home	False	Todays Date	10246308	350
351	+44118 496 0793	10248689	Home	False	Todays Date	10248689	351
352	+44(0)118 4960504	10248787	Home	False	Todays Date	10248787	352
353	+44115 4960430	1025051T	Home	False	Todays Date	1025051T	353
354	+44(0)20 7496 0305	10250601	Home	False	Todays Date	10250601	354
355	+44191 4960797	10254153	Home	False	Todays Date	10254153	355
356	01164960967	10254942	Home	False	Todays Date	10254942	356
357	+44(0)1184960355	10255421	Home	False	Todays Date	10255421	357
358	(020) 74960689	10255945	Home	False	Todays Date	10255945	358
359	(0161) 4960687	10256741	Home	False	Todays Date	10256741	359
360	(0117)4960028	10259249	Home	False	Todays Date	10259249	360
361	0131 496 0537	10264165	Home	False	Todays Date	10264165	361
362	+44(0)8081570071	10264188	Home	False	Todays Date	10264188	362
363	+44(0)306 9990170	10264522	Home	False	Todays Date	10264522	363
364	(0161) 496 0612	10270815	Home	False	Todays Date	10270815	364
365	+441614960794	10272741	Home	False	Todays Date	10272741	365
366	+44115 496 0029	10273905	Home	False	Todays Date	10273905	366
367	(0114) 496 0584	10274494	Home	False	Todays Date	10274494	367
368	029 2018 0131	10277117	Home	False	Todays Date	10277117	368
369	0151 496 0109	1028453T	Home	False	Todays Date	1028453T	369
370	(01632)960228	10285929	Home	False	Todays Date	10285929	370
371	+441614960932	10287383	Home	False	Todays Date	10287383	371
372	(0121) 496 0952	10288046	Home	False	Todays Date	10288046	372
373	+44(0)20 7496 0889	10292742	Home	False	Todays Date	10292742	373
374	(0131) 496 0859	10293987	Home	False	Todays Date	10293987	374
375	+44(0)131 4960995	10295930	Home	False	Todays Date	10295930	375
376	+44114 4960926	10297297	Home	False	Todays Date	10297297	376
377	+44(0)8081570881	10297660	Home	False	Todays Date	10297660	377
378	+44306 9990387	10297913	Home	False	Todays Date	10297913	378
379	+44(0)1174960987	13611733	Home	False	Todays Date	13611733	379
380	+44(0)116 4960846	1029931T	Home	False	Todays Date	1029931T	380
381	0909 879 0927	1030110T	Home	False	Todays Date	1030110T	381
382	(0116) 4960872	10301750	Home	False	Todays Date	10301750	382
383	+44(0)1214960341	10302350	Home	False	Todays Date	10302350	383
384	+441632960051	10303376	Home	False	Todays Date	10303376	384
385	+44(0)28 9018010	10305935	Home	False	Todays Date	10305935	385
386	029 2018 0538	1030841T	Home	False	Todays Date	1030841T	386
387	+44(0)116 4960314	1030875T	Home	False	Todays Date	1030875T	387
388	(0808) 157 0528	10309533	Home	False	Todays Date	10309533	388
389	(028) 9018 0633	10315141	Home	False	Todays Date	10315141	389
390	(0191) 496 0752	10317585	Home	False	Todays Date	10317585	390
391	+443069990634	10318726	Home	False	Todays Date	10318726	391
392	+448081570617	10319067	Home	False	Todays Date	10319067	392
393	+44(0)114 4960619	10320788	Home	False	Todays Date	10320788	393
394	(0115) 4960910	10320955	Home	False	Todays Date	10320955	394
395	0114 4960364	10322725	Home	False	Todays Date	10322725	395
396	(0116) 496 0458	10324484	Home	False	Todays Date	10324484	396
397	+44(0)131 4960478	10325700	Home	False	Todays Date	10325700	397
398	+44(0)1514960758	10327234	Home	False	Todays Date	10327234	398
399	(0909) 879 0987	1032923T	Home	False	Todays Date	1032923T	399
400	(0114)4960265	11452767	Home	False	Todays Date	11452767	400
401	(0151) 496 0791	10332236	Home	False	Todays Date	10332236	401
402	0141 496 0352	10332461	Home	False	Todays Date	10332461	402
403	(0121)4960535	10334473	Home	False	Todays Date	10334473	403
404	+441174960825	10335568	Home	False	Todays Date	10335568	404
405	+44808 1570514	10336709	Home	False	Todays Date	10336709	405
406	+44121 496 0486	10337505	Home	False	Todays Date	10337505	406
407	(01632) 960 203	10337914	Home	False	Todays Date	10337914	407
408	03069990319	1033889T	Home	False	Todays Date	1033889T	408
409	+441632960162	10340294	Home	False	Todays Date	10340294	409
410	0131 4960962	1034037T	Home	False	Todays Date	1034037T	410
411	0118 4960925	10346606	Home	False	Todays Date	10346606	411
412	+44(0)114 496 0971	1034930T	Home	False	Todays Date	1034930T	412
413	+44(0)117 4960518	10349339	Home	False	Todays Date	10349339	413
414	(0116) 4960151	10352773	Home	False	Todays Date	10352773	414
415	01632960893	10353966	Home	False	Todays Date	10353966	415
416	+44117 496 0293	1035651T	Home	False	Todays Date	1035651T	416
417	(0113) 4960576	10356768	Home	False	Todays Date	10356768	417
418	(0121)4960306	10362036	Home	False	Todays Date	10362036	418
419	09098790841	10363460	Home	False	Todays Date	10363460	419
420	0115 4960421	10367766	Home	False	Todays Date	10367766	420
421	+44292018985	10369939	Home	False	Todays Date	10369939	421
422	01184960534	10370284	Home	False	Todays Date	10370284	422
423	(0131) 496 0372	10373086	Home	False	Todays Date	10373086	423
424	+44(0)292018176	10373495	Home	False	Todays Date	10373495	424
425	+44(0)115 496 0657	10381719	Home	False	Todays Date	10381719	425
426	+44(0)151 4960957	10382256	Home	False	Todays Date	10382256	426
427	+44(0)306 999 0124	10384821	Home	False	Todays Date	10384821	427
428	0808 1570996	10389088	Home	False	Todays Date	10389088	428
429	+44909 8790842	10397831	Home	False	Todays Date	10397831	429
430	0151 4960272	10403484	Home	False	Todays Date	10403484	430
431	0191 4960509	10409497	Home	False	Todays Date	10409497	431
432	(0114) 4960644	10410786	Home	False	Todays Date	10410786	432
433	+44(0)2074960212	1041194T	Home	False	Todays Date	1041194T	433
434	0131 4960217	10415698	Home	False	Todays Date	10415698	434
435	0141 496 0011	10420959	Home	False	Todays Date	10420959	435
436	0306 9990010	10423836	Home	False	Todays Date	10423836	436
437	+44113 496 0415	10424217	Home	False	Todays Date	10424217	437
438	+44(0)1214960790	10426794	Home	False	Todays Date	10426794	438
439	+44(0)131 496 0056	10429544	Home	False	Todays Date	10429544	439
440	+449098790652	10433249	Home	False	Todays Date	10433249	440
441	+44(0)1914960815	10434477	Home	False	Todays Date	10434477	441
442	(0118) 496 0014	10437636	Home	False	Todays Date	10437636	442
443	+44(0)1164960958	10439199	Home	False	Todays Date	10439199	443
444	0306 9990724	10441883	Home	False	Todays Date	10441883	444
445	+44118 496 0693	10442189	Home	False	Todays Date	10442189	445
446	09098790897	10445671	Home	False	Todays Date	10445671	446
447	+441134960994	10447090	Home	False	Todays Date	10447090	447
448	(0117) 4960093	10447959	Home	False	Todays Date	10447959	448
449	+4420 74960011	10454979	Home	False	Todays Date	10454979	449
450	(0115) 496 0104	10455268	Home	False	Todays Date	10455268	450
451	+44(0)1414960458	10456156	Home	False	Todays Date	10456156	451
452	+44(0)1414960916	10456162	Home	False	Todays Date	10456162	452
453	0191 498 0731	10456381	Home	False	Todays Date	10456381	453
454	+441632 960269	10460725	Home	False	Todays Date	10460725	454
455	+44(0)909 879 0934	10461469	Home	False	Todays Date	10461469	455
456	+44131 496 0029	10461498	Home	False	Todays Date	10461498	456
457	01614960934	10465735	Home	False	Todays Date	10465735	457
458	+44161 4960666	10468917	Home	False	Todays Date	10468917	458
459	01632960533	10469863	Home	False	Todays Date	10469863	459
460	020 74960276	10482836	Home	False	Todays Date	10482836	460
461	+44289018696	10484543	Home	False	Todays Date	10484543	461
462	+44(0)1214960749	1048587T	Home	False	Todays Date	1048587T	462
463	(0115)4960044	10486336	Home	False	Todays Date	10486336	463
464	0113 4960451	13402508	Home	False	Todays Date	13402508	464
465	+44(0)117 496 0625	11001537	Home	False	Todays Date	11001537	465
466	01314960109	11013596	Home	False	Todays Date	11013596	466
467	+44(0)114 4960515	11019897	Home	False	Todays Date	11019897	467
468	(0117)4960624	11021106	Home	False	Todays Date	11021106	468
469	+449098790408	11029206	Home	False	Todays Date	11029206	469
470	+44(0)116 496 0881	11034030	Home	False	Todays Date	11034030	470
471	+44(0)1184960069	1104342T	Home	False	Todays Date	1104342T	471
472	+44(0)28 9018841	11056262	Home	False	Todays Date	11056262	472
473	(028) 9018263	11063558	Home	False	Todays Date	11063558	473
474	+44191 496 0808	11068361	Home	False	Todays Date	11068361	474
475	+44(0)131 496 0062	11084044	Home	False	Todays Date	11084044	475
476	0191 498 0873	11084211	Home	False	Todays Date	11084211	476
477	+44(0)909 879 0870	11087791	Home	False	Todays Date	11087791	477
478	(0909) 8790994	11092050	Home	False	Todays Date	11092050	478
479	+44808 1570707	11100423	Home	False	Todays Date	11100423	479
480	0306 9990467	11102602	Home	False	Todays Date	11102602	480
481	+44(0)1214960294	11112194	Home	False	Todays Date	11112194	481
482	+44(0)114 4960181	11131468	Home	False	Todays Date	11131468	482
483	+44(0)191 496 0639	11138571	Home	False	Todays Date	11138571	483
484	0118 4960872	11149177	Home	False	Todays Date	11149177	484
485	+44(0)151 4960481	11153838	Home	False	Todays Date	11153838	485
486	+44(0)29 2018355	11166595	Home	False	Todays Date	11166595	486
487	(0161) 496 0701	11183886	Home	False	Todays Date	11183886	487
488	(0909) 8790422	1119959T	Home	False	Todays Date	1119959T	488
489	+44(0)909 879 0458	11203189	Home	False	Todays Date	11203189	489
490	+44(0)909 879 0037	11214567	Home	False	Todays Date	11214567	490
491	+44(0)1514960244	11214849	Home	False	Todays Date	11214849	491
492	(0118)4960311	11219796	Home	False	Todays Date	11219796	492
493	0191 498 0990	11223576	Home	False	Todays Date	11223576	493
494	+44191 4960674	11233248	Home	False	Todays Date	11233248	494
495	0191 4960502	11245969	Home	False	Todays Date	11245969	495
496	0292018068	11245975	Home	False	Todays Date	11245975	496
497	+44141 4960294	11247745	Home	False	Todays Date	11247745	497
498	(0909) 8790868	11251502	Home	False	Todays Date	11251502	498
499	(0114) 496 0207	11256558	Home	False	Todays Date	11256558	499
500	0306 999 0375	11259389	Home	False	Todays Date	11259389	500
501	+44(0)808 157 0732	11267055	Home	False	Todays Date	11267055	501
502	(028) 9018589	1126792T	Home	False	Todays Date	1126792T	502
503	+44(0)117 496 0342	11276657	Home	False	Todays Date	11276657	503
504	(0151) 4960083	11283988	Home	False	Todays Date	11283988	504
505	+44(0)121 4960475	1128889T	Home	False	Todays Date	1128889T	505
506	+441164960025	11291268	Home	False	Todays Date	11291268	506
507	+441632960603	1129192T	Home	False	Todays Date	1129192T	507
508	(01632)960443	11291942	Home	False	Todays Date	11291942	508
509	+44115 4960256	11308641	Home	False	Todays Date	11308641	509
510	(0115)4960784	11309454	Home	False	Todays Date	11309454	510
511	(0161)4960656	11314744	Home	False	Todays Date	11314744	511
512	0151 496 0421	11317742	Home	False	Todays Date	11317742	512
513	(020) 7496 0876	11321977	Home	False	Todays Date	11321977	513
514	+441164960072	11325016	Home	False	Todays Date	11325016	514
515	+44(0)151 4960728	11329259	Home	False	Todays Date	11329259	515
516	+441154960311	11336129	Home	False	Todays Date	11336129	516
517	+441914960007	11345121	Home	False	Todays Date	11345121	517
518	+441184960221	11348643	Home	False	Todays Date	11348643	518
519	09098790162	11356568	Home	False	Todays Date	11356568	519
520	(0113) 4960279	11377313	Home	False	Todays Date	11377313	520
521	+44(0)1914960930	11433199	Home	False	Todays Date	11433199	521
522	+44(0)3069990030	1143836T	Home	False	Todays Date	1143836T	522
523	+442074960062	1143889T	Home	False	Todays Date	1143889T	523
524	(0306) 9990299	11441562	Home	False	Todays Date	11441562	524
525	01214960476	11443384	Home	False	Todays Date	11443384	525
526	0289018548	11444871	Home	False	Todays Date	11444871	526
527	(0306) 9990115	11447460	Home	False	Todays Date	11447460	527
528	+44292018202	11452168	Home	False	Todays Date	11452168	528
529	01632 960230	11452329	Home	False	Todays Date	11452329	529
530	0808 157 0127	11462975	Home	False	Todays Date	11462975	530
531	(028)9018223	11466008	Home	False	Todays Date	11466008	531
532	+44131 4960668	11466112	Home	False	Todays Date	11466112	532
533	+44117 4960942	11466210	Home	False	Todays Date	11466210	533
534	(0117) 4960194	11467743	Home	False	Todays Date	11467743	534
535	+441914960323	11469818	Home	False	Todays Date	11469818	535
536	+44(0)292018851	11471903	Home	False	Todays Date	11471903	536
537	029 2018 0993	11472336	Home	False	Todays Date	11472336	537
538	+44(0)115 496 0781	11472365	Home	False	Todays Date	11472365	538
539	0161 4960238	11474279	Home	False	Todays Date	11474279	539
540	(0114) 4960259	11479865	Home	False	Todays Date	11479865	540
541	(020)74960422	11482204	Home	False	Todays Date	11482204	541
542	(0151)4960513	11482855	Home	False	Todays Date	11482855	542
543	(01632) 960 621	11484153	Home	False	Todays Date	11484153	543
544	0114 496 0200	11485012	Home	False	Todays Date	11485012	544
545	+44(0)3069990431	1148646T	Home	False	Todays Date	1148646T	545
546	(028)9018187	1148778T	Home	False	Todays Date	1148778T	546
547	(0909)8790560	11488252	Home	False	Todays Date	11488252	547
548	+44(0)131 4960872	11488465	Home	False	Todays Date	11488465	548
549	08081570853	11490233	Home	False	Todays Date	11490233	549
550	01314960820	11492297	Home	False	Todays Date	11492297	550
551	(0114) 4960744	11497854	Home	False	Todays Date	11497854	551
552	0909 879 0218	11499503	Home	False	Todays Date	11499503	552
553	+44(0)113 496 0174	11500820	Home	False	Todays Date	11500820	553
554	+44115 4960136	11501420	Home	False	Todays Date	11501420	554
555	(0116) 496 0566	11501823	Home	False	Todays Date	11501823	555
556	(020)74960286	11503075	Home	False	Todays Date	11503075	556
557	0117 496 0745	11503864	Home	False	Todays Date	11503864	557
558	+44131 4960918	11503933	Home	False	Todays Date	11503933	558
559	(0121)4960288	11504372	Home	False	Todays Date	11504372	559
560	01154960295	11505899	Home	False	Todays Date	11505899	560
561	01632 960022	11508154	Home	False	Todays Date	11508154	561
562	+44(0)191 496 0367	11508534	Home	False	Todays Date	11508534	562
563	+44(0)113 4960913	11511639	Home	False	Todays Date	11511639	563
564	+44115 4960946	11517353	Home	False	Todays Date	11517353	564
565	+44(0)20 7496 0728	11521916	Home	False	Todays Date	11521916	565
566	+44808 157 0233	11522637	Home	False	Todays Date	11522637	566
567	+44(0)1514960382	11522643	Home	False	Todays Date	11522643	567
568	+44117 4960748	11526707	Home	False	Todays Date	11526707	568
569	(0117) 4960825	11527215	Home	False	Todays Date	11527215	569
570	(0151) 496 0304	11530107	Home	False	Todays Date	11530107	570
571	+44(0)2074960671	11536092	Home	False	Todays Date	11536092	571
572	03069990624	11540897	Home	False	Todays Date	11540897	572
573	+443069990340	11545786	Home	False	Todays Date	11545786	573
574	01914960085	11546432	Home	False	Todays Date	11546432	574
575	0121 4960733	1155000T	Home	False	Todays Date	1155000T	575
576	0131 4960246	11550270	Home	False	Todays Date	11550270	576
577	+44(0)114 496 0703	11553037	Home	False	Todays Date	11553037	577
578	(028)9018888	11558554	Home	False	Todays Date	11558554	578
579	(028) 9018631	11560126	Home	False	Todays Date	11560126	579
580	0306 9990355	11563314	Home	False	Todays Date	11563314	580
581	+44191 4960730	11565044	Home	False	Todays Date	11565044	581
582	+44(0)151 4960965	1156889T	Home	False	Todays Date	1156889T	582
583	+44(0)131 496 0996	11569195	Home	False	Todays Date	11569195	583
584	(029) 2018586	11577229	Home	False	Todays Date	11577229	584
585	(020)74960823	11583718	Home	False	Todays Date	11583718	585
586	+44808 1570796	11584474	Home	False	Todays Date	11584474	586
587	+441174960714	11609075	Home	False	Todays Date	11609075	587
588	01144960945	11614970	Home	False	Todays Date	11614970	588
589	+44(0)121 496 0954	11615725	Home	False	Todays Date	11615725	589
590	(0118) 496 0534	11617864	Home	False	Todays Date	11617864	590
591	(0115)4960760	11623351	Home	False	Todays Date	11623351	591
592	+44113 4960033	11636695	Home	False	Todays Date	11636695	592
593	+441632960452	13611710	Home	False	Todays Date	13611710	593
594	(0808) 157 0879	11661807	Home	False	Todays Date	11661807	594
595	0141 4960093	11698923	Home	False	Todays Date	11698923	595
596	0306 9990103	11717534	Home	False	Todays Date	11717534	596
597	(0117) 496 0289	11742249	Home	False	Todays Date	11742249	597
598	+44(0)3069990053	11745967	Home	False	Todays Date	11745967	598
599	+44(0)191 496 0232	11757882	Home	False	Todays Date	11757882	599
600	01632 960 740	11760532	Home	False	Todays Date	11760532	600
601	0114 496 0265	11781162	Home	False	Todays Date	11781162	601
602	(029) 2018 0355	11784511	Home	False	Todays Date	11784511	602
603	(0151)4960998	11790827	Home	False	Todays Date	11790827	603
604	+441514960021	11798910	Home	False	Todays Date	11798910	604
605	+44(0)8081570308	11844790	Home	False	Todays Date	11844790	605
606	+44(0)306 9990074	11854986	Home	False	Todays Date	11854986	606
607	+44(0)306 999 0618	11866428	Home	False	Todays Date	11866428	607
608	0116 4960501	11886585	Home	False	Todays Date	11886585	608
609	+44(0)1632 960167	1194777T	Home	False	Todays Date	1194777T	609
610	(0151) 496 0319	11956501	Home	False	Todays Date	11956501	610
611	+44909 8790675	11957337	Home	False	Todays Date	11957337	611
612	+44117 496 0200	12006612	Home	False	Todays Date	12006612	612
613	+441214960432	1202119T	Home	False	Todays Date	1202119T	613
614	+44(0)116 496 0817	12021200	Home	False	Todays Date	12021200	614
615	+441134960191	12022071	Home	False	Todays Date	12022071	615
616	+44131 496 0382	12069348	Home	False	Todays Date	12069348	616
617	(0151)4960360	12080655	Home	False	Todays Date	12080655	617
618	+441632 960395	12120852	Home	False	Todays Date	12120852	618
619	+442074960491	12141476	Home	False	Todays Date	12141476	619
620	(0121) 496 0534	1216808T	Home	False	Todays Date	1216808T	620
621	(0191)4960775	12173962	Home	False	Todays Date	12173962	621
622	02074960045	12197359	Home	False	Todays Date	12197359	622
623	(020) 74960601	12217002	Home	False	Todays Date	12217002	623
624	+441632 960 668	12232172	Home	False	Todays Date	12232172	624
625	0115 496 0358	12233313	Home	False	Todays Date	12233313	625
626	020 74960031	12244697	Home	False	Todays Date	12244697	626
627	028 9018 0313	12269247	Home	False	Todays Date	12269247	627
628	0161 496 0452	12304250	Home	False	Todays Date	12304250	628
629	+441414960534	12308798	Home	False	Todays Date	12308798	629
630	+44(0)141 496 0430	12319047	Home	False	Todays Date	12319047	630
631	+44191 4960372	12322901	Home	False	Todays Date	12322901	631
632	+44121 4960271	12379718	Home	False	Todays Date	12379718	632
633	(0113) 4960793	12417667	Home	False	Todays Date	12417667	633
634	0121 496 0243	12422681	Home	False	Todays Date	12422681	634
635	+44(0)151 4960077	12441454	Home	False	Todays Date	12441454	635
636	(0141)4960165	12454585	Home	False	Todays Date	12454585	636
637	+44292018456	12455323	Home	False	Todays Date	12455323	637
638	(0161) 4960724	12485221	Home	False	Todays Date	12485221	638
639	+44(0)29 2018412	12488795	Home	False	Todays Date	12488795	639
640	+44(0)118 4960549	12500332	Home	False	Todays Date	12500332	640
641	+441154960130	12506230	Home	False	Todays Date	12506230	641
642	+449098790883	12509308	Home	False	Todays Date	12509308	642
643	+44141 496 0307	12515538	Home	False	Todays Date	12515538	643
644	0289018057	12566705	Home	False	Todays Date	12566705	644
645	+441144960877	12575599	Home	False	Todays Date	12575599	645
646	(0191) 4960876	12622608	Home	False	Todays Date	12622608	646
647	+44(0)118 4960497	12624632	Home	False	Todays Date	12624632	647
648	01614960297	12668301	Home	False	Todays Date	12668301	648
649	028 9018 0984	12670530	Home	False	Todays Date	12670530	649
650	+44(0)1632 960 600	12670887	Home	False	Todays Date	12670887	650
651	01314960674	1268922T	Home	False	Todays Date	1268922T	651
652	+44(0)114 496 0309	12693356	Home	False	Todays Date	12693356	652
653	+44121 496 0301	12693483	Home	False	Todays Date	12693483	653
654	(0141)4960569	12704013	Home	False	Todays Date	12704013	654
655	(0116) 4960425	12704474	Home	False	Todays Date	12704474	655
656	+44289018018	12709910	Home	False	Todays Date	12709910	656
657	(0121)4960909	12716400	Home	False	Todays Date	12716400	657
658	01632 960977	12725150	Home	False	Todays Date	12725150	658
659	+44(0)191 496 0376	12768501	Home	False	Todays Date	12768501	659
660	(020) 7496 0816	12768927	Home	False	Todays Date	12768927	660
661	+44(0)1514960634	1277117T	Home	False	Todays Date	1277117T	661
662	+44151 4960729	12777510	Home	False	Todays Date	12777510	662
663	(0115) 496 0692	12779384	Home	False	Todays Date	12779384	663
664	(01632) 960192	12784311	Home	False	Todays Date	12784311	664
665	+44(0)118 496 0127	12795770	Home	False	Todays Date	12795770	665
666	+44118 4960471	12797033	Home	False	Todays Date	12797033	666
667	+44(0)1614960479	1280494T	Home	False	Todays Date	1280494T	667
668	+441632 960491	12808842	Home	False	Todays Date	12808842	668
669	+441154960189	12826975	Home	False	Todays Date	12826975	669
670	+44113 496 0477	12839812	Home	False	Todays Date	12839812	670
671	+441914960518	12844958	Home	False	Todays Date	12844958	671
672	01164960302	12855789	Home	False	Todays Date	12855789	672
673	+44(0)1214960541	1285669T	Home	False	Todays Date	1285669T	673
674	(020) 7496 0815	12878552	Home	False	Todays Date	12878552	674
675	0141 4960200	1288073T	Home	False	Todays Date	1288073T	675
676	+44(0)28 9018 0187	12882401	Home	False	Todays Date	12882401	676
677	0909 8790620	12885508	Home	False	Todays Date	12885508	677
678	01184960269	12886984	Home	False	Todays Date	12886984	678
679	+44(0)116 496 0159	12898213	Home	False	Todays Date	12898213	679
680	+441174960756	12912465	Home	False	Todays Date	12912465	680
681	(0808)1570621	12925832	Home	False	Todays Date	12925832	681
682	+441164960384	12936323	Home	False	Todays Date	12936323	682
683	+44118 496 0432	1294953T	Home	False	Todays Date	1294953T	683
684	(0113)4960474	12952628	Home	False	Todays Date	12952628	684
685	+4429 2018007	12986199	Home	False	Todays Date	12986199	685
686	0161 496 0395	13005455	Home	False	Todays Date	13005455	686
687	(0191) 4960943	13006913	Home	False	Todays Date	13006913	687
688	(0191)4960389	13034690	Home	False	Todays Date	13034690	688
689	+44141 4960076	13044788	Home	False	Todays Date	13044788	689
690	+44118 4960831	13045198	Home	False	Todays Date	13045198	690
691	(0131)4960866	13058640	Home	False	Todays Date	13058640	691
692	+44118 496 0273	13076410	Home	False	Todays Date	13076410	692
693	(0306)9990113	13082997	Home	False	Todays Date	13082997	693
694	(0909) 8790359	13093845	Home	False	Todays Date	13093845	694
695	+44113 4960281	13110922	Home	False	Todays Date	13110922	695
696	01184960985	13131258	Home	False	Todays Date	13131258	696
697	+44(0)114 4960913	13137156	Home	False	Todays Date	13137156	697
698	+44117 496 0112	13140618	Home	False	Todays Date	13140618	698
699	+44(0)306 9990110	13157543	Home	False	Todays Date	13157543	699
700	+44115 496 0514	13174794	Home	False	Todays Date	13174794	700
701	0909 8790057	13193711	Home	False	Todays Date	13193711	701
702	+44289018693	13195959	Home	False	Todays Date	13195959	702
703	+44(0)141 496 0093	13198030	Home	False	Todays Date	13198030	703
704	029 2018 0901	13218462	Home	False	Todays Date	13218462	704
705	+44306 9990479	13233643	Home	False	Todays Date	13233643	705
706	01214960105	13258619	Home	False	Todays Date	13258619	706
707	+441134960164	13259818	Home	False	Todays Date	13259818	707
708	01632 960 561	13260762	Home	False	Todays Date	13260762	708
709	(0151)4960636	13262336	Home	False	Todays Date	13262336	709
710	(01632)960884	13263316	Home	False	Todays Date	13263316	710
711	+44(0)191 496 0042	13272728	Home	False	Todays Date	13272728	711
712	+44(0)1144960215	13273645	Home	False	Todays Date	13273645	712
713	+44116 496 0398	1327533T	Home	False	Todays Date	1327533T	713
714	+44(0)1134960470	13280481	Home	False	Todays Date	13280481	714
715	0141 496 0630	13305888	Home	False	Todays Date	13305888	715
716	020 74960745	1330853T	Home	False	Todays Date	1330853T	716
717	+44141 496 0231	13318495	Home	False	Todays Date	13318495	717
718	+44(0)3069990077	13323382	Home	False	Todays Date	13323382	718
719	(0117) 4960995	13384618	Home	False	Todays Date	13384618	719
720	+44(0)28 9018444	1339115T	Home	False	Todays Date	1339115T	720
721	(0151) 496 0305	13391270	Home	False	Todays Date	13391270	721
722	+44(0)115 4960504	13392486	Home	False	Todays Date	13392486	722
723	(0115)4960254	13397421	Home	False	Todays Date	13397421	723
724	(028)9018352	13399214	Home	False	Todays Date	13399214	724
725	(0121) 496 0847	13400122	Home	False	Todays Date	13400122	725
726	01214960494	13402641	Home	False	Todays Date	13402641	726
727	(0306) 999 0092	13404388	Home	False	Todays Date	13404388	727
728	(0114)4960792	13404808	Home	False	Todays Date	13404808	728
729	+44(0)29 2018018	13409133	Home	False	Todays Date	13409133	729
730	(0161)4960645	13410324	Home	False	Todays Date	13410324	730
731	(0114) 496 0430	13411120	Home	False	Todays Date	13411120	731
732	(0151) 496 0914	13417375	Home	False	Todays Date	13417375	732
733	+441632960446	13419744	Home	False	Todays Date	13419744	733
734	(0113) 4960377	13420267	Home	False	Todays Date	13420267	734
735	029 2018 0130	13420388	Home	False	Todays Date	13420388	735
736	+44(0)116 496 0162	13432648	Home	False	Todays Date	13432648	736
737	(0151)4960866	13442384	Home	False	Todays Date	13442384	737
738	(01632) 960983	13448593	Home	False	Todays Date	13448593	738
739	+44116 496 0351	13448996	Home	False	Todays Date	13448996	739
740	+441632960462	1345321T	Home	False	Todays Date	1345321T	740
741	+44(0)1174960619	13456190	Home	False	Todays Date	13456190	741
742	0808 1570894	13465129	Home	False	Todays Date	13465129	742
743	020 7946 0768	13465498	Home	False	Todays Date	13465498	743
744	028 9018 0205	1346927T	Home	False	Todays Date	1346927T	744
745	+44(0)113 496 0426	13474979	Home	False	Todays Date	13474979	745
746	(0117) 4960607	13480535	Home	False	Todays Date	13480535	746
747	(0131)4960265	13481135	Home	False	Todays Date	13481135	747
748	0808 157 0086	13482478	Home	False	Todays Date	13482478	748
749	+44(0)161 4960463	13487465	Home	False	Todays Date	13487465	749
750	0117 4960794	13493919	Home	False	Todays Date	13493919	750
751	+441154960676	13493983	Home	False	Todays Date	13493983	751
752	+441184960736	13496762	Home	False	Todays Date	13496762	752
753	(0306)9990095	13498215	Home	False	Todays Date	13498215	753
754	+44(0)191 4960491	13500437	Home	False	Todays Date	13500437	754
755	+44(0)289018064	13503032	Home	False	Todays Date	13503032	755
756	(0161) 4960742	13506940	Home	False	Todays Date	13506940	756
757	029 2018645	13509840	Home	False	Todays Date	13509840	757
758	+44(0)116 496 0684	13511527	Home	False	Todays Date	13511527	758
759	(0909) 8790637	1351233T	Home	False	Todays Date	1351233T	759
760	+44(0)131 496 0613	13518100	Home	False	Todays Date	13518100	760
761	+44(0)117 496 0547	13522329	Home	False	Todays Date	13522329	761
762	+44117 4960619	13524445	Home	False	Todays Date	13524445	762
763	+44117 4960715	13526405	Home	False	Todays Date	13526405	763
764	+44(0)306 9990543	13526463	Home	False	Todays Date	13526463	764
765	(0306) 9990327	13526774	Home	False	Todays Date	13526774	765
766	+4428 9018 0205	13527247	Home	False	Todays Date	13527247	766
767	(0121)4960672	13528607	Home	False	Todays Date	13528607	767
768	+44(0)909 8790195	13538372	Home	False	Todays Date	13538372	768
769	+44(0)1914960085	13538591	Home	False	Todays Date	13538591	769
770	+4429 2018450	13538619	Home	False	Todays Date	13538619	770
771	+44141 4960280	13539594	Home	False	Todays Date	13539594	771
772	+44(0)117 496 0796	13544204	Home	False	Todays Date	13544204	772
773	0306 999 0290	13546297	Home	False	Todays Date	13546297	773
774	+44116 496 0152	13546798	Home	False	Todays Date	13546798	774
775	+44(0)116 496 0248	13546936	Home	False	Todays Date	13546936	775
776	01144960882	13547559	Home	False	Todays Date	13547559	776
777	01614960661	13547686	Home	False	Todays Date	13547686	777
778	+44(0)141 496 0889	13547801	Home	False	Todays Date	13547801	778
779	(029) 2018 0438	13548551	Home	False	Todays Date	13548551	779
780	(0114) 496 0061	13554746	Home	False	Todays Date	13554746	780
781	+44(0)28 9018194	13556332	Home	False	Todays Date	13556332	781
782	+44115 4960093	13558995	Home	False	Todays Date	13558995	782
783	+44(0)121 4960049	13559860	Home	False	Todays Date	13559860	783
784	+44(0)909 879 0954	13560544	Home	False	Todays Date	13560544	784
785	0114 496 0687	13560636	Home	False	Todays Date	13560636	785
786	(0121)4960627	13560918	Home	False	Todays Date	13560918	786
787	0118 496 0290	13561524	Home	False	Todays Date	13561524	787
788	+44(0)118 4960541	13561639	Home	False	Todays Date	13561639	788
789	0151 4960227	13562090	Home	False	Todays Date	13562090	789
790	+44(0)121 4960712	13562654	Home	False	Todays Date	13562654	790
791	(029) 2018542	13565957	Home	False	Todays Date	13565957	791
792	(020) 7496 0058	13567376	Home	False	Todays Date	13567376	792
793	(0191)4960430	13567497	Home	False	Todays Date	13567497	793
794	(0117) 4960981	13567819	Home	False	Todays Date	13567819	794
795	+44(0)29 2018845	1356793T	Home	False	Todays Date	1356793T	795
796	(0808)1570292	13568016	Home	False	Todays Date	13568016	796
797	+44(0)118 4960024	13568114	Home	False	Todays Date	13568114	797
798	020 7946 0841	13568552	Home	False	Todays Date	13568552	798
799	+44(0)292018863	13569866	Home	False	Todays Date	13569866	799
800	(0113)4960713	13570660	Home	False	Todays Date	13570660	800
801	(0141) 4960917	13570798	Home	False	Todays Date	13570798	801
802	+44117 4960460	13570896	Home	False	Todays Date	13570896	802
803	0191 498 0659	13570994	Home	False	Todays Date	13570994	803
804	(0151) 496 0782	13571496	Home	False	Todays Date	13571496	804
805	0116 4960271	13571726	Home	False	Todays Date	13571726	805
806	+44118 496 0478	13571974	Home	False	Todays Date	13571974	806
807	0118 496 0201	13572067	Home	False	Todays Date	13572067	807
808	+44161 4960006	13572165	Home	False	Todays Date	13572165	808
809	+441614960590	13572211	Home	False	Todays Date	13572211	809
810	+44191 496 0675	13572764	Home	False	Todays Date	13572764	810
811	(0116)4960400	13572856	Home	False	Todays Date	13572856	811
812	(028)9018824	13573295	Home	False	Todays Date	13573295	812
813	0121 496 0634	13573410	Home	False	Todays Date	13573410	813
814	+441414960208	13573715	Home	False	Todays Date	13573715	814
815	+44(0)116 496 0356	13578754	Home	False	Todays Date	13578754	815
816	(0121)4960534	13581220	Home	False	Todays Date	13581220	816
817	+44(0)121 496 0999	13583192	Home	False	Todays Date	13583192	817
818	+44151 4960613	13611704	Home	False	Todays Date	13611704	818
819	0141 496 0200	1361174T	Home	False	Todays Date	1361174T	819
820	(029) 2018878	13611756	Home	False	Todays Date	13611756	820
821	+441144960017	13611762	Home	False	Todays Date	13611762	821
822	0292018113	13611779	Home	False	Todays Date	13611779	822
823	+44(0)1614960031	13611785	Home	False	Todays Date	13611785	823
824	+44121 4960141	13611791	Home	False	Todays Date	13611791	824
825	02074960568	13611802	Home	False	Todays Date	13611802	825
826	(0161)4960269	13611819	Home	False	Todays Date	13611819	826
827	(0161) 4960938	13611825	Home	False	Todays Date	13611825	827
828	+448081570748	13611831	Home	False	Todays Date	13611831	828
829	(028) 9018 0153	13611848	Home	False	Todays Date	13611848	829
830	(0909) 8790196	13611854	Home	False	Todays Date	13611854	830
831	+44(0)141 496 0244	13611860	Home	False	Todays Date	13611860	831
832	+44131 496 0780	13611917	Home	False	Todays Date	13611917	832
833	+44(0)28 9018694	13612552	Home	False	Todays Date	13612552	833
834	0113 496 0711	13612569	Home	False	Todays Date	13612569	834
835	+44118 496 0148	13612575	Home	False	Todays Date	13612575	835
836	0808 157 0912	13612581	Home	False	Todays Date	13612581	836
837	(0118) 496 0016	13612598	Home	False	Todays Date	13612598	837
838	(0151)4960695	13612609	Home	False	Todays Date	13612609	838
839	(0808) 157 0682	13612615	Home	False	Todays Date	13612615	839
840	+44(0)1184960933	13612621	Home	False	Todays Date	13612621	840
841	+44(0)29 2018197	13612638	Home	False	Todays Date	13612638	841
842	(0113)4960669	13612644	Home	False	Todays Date	13612644	842
843	01632 960483	13612650	Home	False	Todays Date	13612650	843
844	+44(0)909 8790005	94000393	Home	False	Todays Date	94000393	844
845	(0115) 496 0800	94000738	Home	False	Todays Date	94000738	845
846	+441144960352	94001471	Home	False	Todays Date	94001471	846
847	(0113) 4960630	94003667	Home	False	Todays Date	94003667	847
848	(0116) 4960548	9400409T	Home	False	Todays Date	9400409T	848
849	0115 4960808	94004169	Home	False	Todays Date	94004169	849
850	(0808) 157 0250	94004780	Home	False	Todays Date	94004780	850
851	+44289018232	94006227	Home	False	Todays Date	94006227	851
852	09098790211	94007582	Home	False	Todays Date	94007582	852
853	(0909) 879 0660	94007697	Home	False	Todays Date	94007697	853
854	0115 496 0260	9400971T	Home	False	Todays Date	9400971T	854
855	(0161) 496 0717	94009939	Home	False	Todays Date	94009939	855
856	09098790096	94012175	Home	False	Todays Date	94012175	856
857	0118 4960828	94012682	Home	False	Todays Date	94012682	857
858	0121 4960232	9401326T	Home	False	Todays Date	9401326T	858
859	0808 1570246	94013627	Home	False	Todays Date	94013627	859
860	(0121)4960242	94016032	Home	False	Todays Date	94016032	860
861	+44292018163	94016314	Home	False	Todays Date	94016314	861
862	+4429 2018 0613	94017507	Home	False	Todays Date	94017507	862
863	(0808) 157 0046	94017513	Home	False	Todays Date	94017513	863
864	(0161)4960929	94019859	Home	False	Todays Date	94019859	864
865	+441632 960834	94020031	Home	False	Todays Date	94020031	865
866	+44(0)1134960420	94020895	Home	False	Todays Date	94020895	866
867	+44(0)141 496 0934	94021339	Home	False	Todays Date	94021339	867
868	+44(0)9098790474	9402145T	Home	False	Todays Date	9402145T	868
869	01614960639	94023680	Home	False	Todays Date	94023680	869
870	(0141) 4960464	94024510	Home	False	Todays Date	94024510	870
871	+44808 1570908	94026142	Home	False	Todays Date	94026142	871
872	+44(0)131 4960328	94026637	Home	False	Todays Date	94026637	872
873	+44116 496 0852	94026885	Home	False	Todays Date	94026885	873
874	01164960105	94028799	Home	False	Todays Date	94028799	874
875	+44(0)113 496 0187	94029163	Home	False	Todays Date	94029163	875
876	(0115) 4960012	94029226	Home	False	Todays Date	94029226	876
877	03069990196	94029255	Home	False	Todays Date	94029255	877
878	0909 8790876	94029318	Home	False	Todays Date	94029318	878
879	+44808 1570147	94029762	Home	False	Todays Date	94029762	879
880	+44(0)306 9990721	94031017	Home	False	Todays Date	94031017	880
881	+448081570735	94031196	Home	False	Todays Date	94031196	881
882	02074960412	94031806	Home	False	Todays Date	94031806	882
883	+44(0)161 496 0258	94032032	Home	False	Todays Date	94032032	883
884	(0113) 496 0360	94032199	Home	False	Todays Date	94032199	884
885	0113 496 0163	94033219	Home	False	Todays Date	94033219	885
886	+44141 496 0813	94033571	Home	False	Todays Date	94033571	886
887	+4420 74960618	94034044	Home	False	Todays Date	94034044	887
888	0161 496 0593	94034453	Home	False	Todays Date	94034453	888
889	+44(0)3069990476	94035617	Home	False	Todays Date	94035617	889
890	(020) 7496 0536	94035842	Home	False	Todays Date	94035842	890
891	(0161) 496 0777	94036511	Home	False	Todays Date	94036511	891
892	+44(0)118 496 0818	94036528	Home	False	Todays Date	94036528	892
893	(0121) 496 0927	94036747	Home	False	Todays Date	94036747	893
894	+44161 4960992	94036868	Home	False	Todays Date	94036868	894
895	+441214960170	94037589	Home	False	Todays Date	94037589	895
896	+44(0)306 9990988	94039929	Home	False	Todays Date	94039929	896
897	+44808 1570834	94040677	Home	False	Todays Date	94040677	897
898	029 2018 0632	94041104	Home	False	Todays Date	94041104	898
899	(0117) 496 0476	94041225	Home	False	Todays Date	94041225	899
900	+44(0)8081570898	9404167T	Home	False	Todays Date	9404167T	900
901	(0121) 496 0118	94041801	Home	False	Todays Date	94041801	901
902	+44(0)1632 960 770	94042580	Home	False	Todays Date	94042580	902
903	+44(0)1214960370	94044102	Home	False	Todays Date	94044102	903
904	+44(0)1914960290	9404438T	Home	False	Todays Date	9404438T	904
905	+44121 4960786	94044586	Home	False	Todays Date	94044586	905
906	+44(0)29 2018 0930	94044718	Home	False	Todays Date	94044718	906
907	+44(0)117 4960209	94047244	Home	False	Todays Date	94047244	907
908	+44(0)191 4960547	94051698	Home	False	Todays Date	94051698	908
909	(0115) 4960172	94055780	Home	False	Todays Date	94055780	909
910	+44(0)1514960178	94056875	Home	False	Todays Date	94056875	910
911	+44(0)114 4960213	94058138	Home	False	Todays Date	94058138	911
912	(01632)960851	94061819	Home	False	Todays Date	94061819	912
913	+44(0)141 496 0342	94064587	Home	False	Todays Date	94064587	913
914	+44161 4960264	94071048	Home	False	Todays Date	94071048	914
915	01314960177	9407151T	Home	False	Todays Date	9407151T	915
916	+44808 157 0043	94074213	Home	False	Todays Date	94074213	916
917	+44(0)191 4960778	94074985	Home	False	Todays Date	94074985	917
918	020 7946 0622	94076375	Home	False	Todays Date	94076375	918
919	+441214960002	94078030	Home	False	Todays Date	94078030	919
920	029 2018 0103	94078554	Home	False	Todays Date	94078554	920
921	0909 8790881	94079626	Home	False	Todays Date	94079626	921
922	0808 1570041	94079655	Home	False	Todays Date	94079655	922
923	(0114) 4960558	94082311	Home	False	Todays Date	94082311	923
924	+442074960183	94087154	Home	False	Todays Date	94087154	924
925	+4420 74960319	94090910	Home	False	Todays Date	94090910	925
926	+44114 496 0174	95000256	Home	False	Todays Date	95000256	926
927	(0118) 4960925	95000400	Home	False	Todays Date	95000400	927
928	+44(0)118 496 0939	9500122T	Home	False	Todays Date	9500122T	928
929	0116 4960063	95002441	Home	False	Todays Date	95002441	929
930	(0306)9990293	9500544T	Home	False	Todays Date	9500544T	930
931	(020) 7496 0613	95006822	Home	False	Todays Date	95006822	931
932	(0115)4960894	95010297	Home	False	Todays Date	95010297	932
933	+44(0)131 4960200	95014298	Home	False	Todays Date	95014298	933
934	+44(0)292018157	95017676	Home	False	Todays Date	95017676	934
935	(0151) 4960529	95018760	Home	False	Todays Date	95018760	935
936	+44(0)9098790297	95028213	Home	False	Todays Date	95028213	936
937	+44909 8790423	95030119	Home	False	Todays Date	95030119	937
938	+44(0)1514960954	95032391	Home	False	Todays Date	95032391	938
939	(0909) 879 0054	95032638	Home	False	Todays Date	95032638	939
940	(01632)960091	95035544	Home	False	Todays Date	95035544	940
941	028 9018931	9504667T	Home	False	Todays Date	9504667T	941
942	+441144960273	95046732	Home	False	Todays Date	95046732	942
943	(0306)9990443	95046778	Home	False	Todays Date	95046778	943
944	(0115) 4960510	95049033	Home	False	Todays Date	95049033	944
945	(0115) 4960281	95049684	Home	False	Todays Date	95049684	945
946	(028) 9018314	95050028	Home	False	Todays Date	95050028	946
947	0161 4960478	95050777	Home	False	Todays Date	95050777	947
948	(0121)4960587	95053308	Home	False	Todays Date	95053308	948
949	+441614960152	95053648	Home	False	Todays Date	95053648	949
950	0141 4960151	95054248	Home	False	Todays Date	95054248	950
951	+441134960892	95054605	Home	False	Todays Date	95054605	951
952	+44(0)1154960527	95056617	Home	False	Todays Date	95056617	952
953	+44151 4960806	95062876	Home	False	Todays Date	95062876	953
954	+441514960839	95064335	Home	False	Todays Date	95064335	954
955	+44121 4960322	95065851	Home	False	Todays Date	95065851	955
956	+44117 4960675	95072099	Home	False	Todays Date	95072099	956
957	+441184960123	95073534	Home	False	Todays Date	95073534	957
958	02074960724	95088769	Home	False	Todays Date	95088769	958
959	(0114) 4960206	95089035	Home	False	Todays Date	95089035	959
960	0306 9990051	95095271	Home	False	Todays Date	95095271	960
961	(0114)4960856	95095697	Home	False	Todays Date	95095697	961
962	+44(0)808 157 0681	9509575T	Home	False	Todays Date	9509575T	962
963	+44(0)9098790172	95096988	Home	False	Todays Date	95096988	963
964	+44306 999 0777	95101131	Home	False	Todays Date	95101131	964
965	+4428 9018 0233	9510511T	Home	False	Todays Date	9510511T	965
966	0141 496 0833	95107490	Home	False	Todays Date	95107490	966
967	0114 4960504	95110088	Home	False	Todays Date	95110088	967
968	0909 879 0763	9511251T	Home	False	Todays Date	9511251T	968
969	+44(0)28 9018 0441	95708936	Home	False	Todays Date	95708936	969
970	0114 4960222	95907481	Home	False	Todays Date	95907481	970
971	+44(0)117 496 0296	96300648	Home	False	Todays Date	96300648	971
972	+441134960602	96400946	Home	False	Todays Date	96400946	972
973	+44131 496 0976	96505010	Home	False	Todays Date	96505010	973
974	+441632960595	97009936	Home	False	Todays Date	97009936	974
975	+44131 4960216	97111265	Home	False	Todays Date	97111265	975
976	(0151)4960388	97200058	Home	False	Todays Date	97200058	976
977	+44(0)115 4960666	97432184	Home	False	Todays Date	97432184	977
978	+44(0)1314960650	97520164	Home	False	Todays Date	97520164	978
979	(0116) 496 0448	97532758	Home	False	Todays Date	97532758	979
980	+442074960035	97624336	Home	False	Todays Date	97624336	980
981	01154960758	97626072	Home	False	Todays Date	97626072	981
982	+44(0)191 496 0392	97820067	Home	False	Todays Date	97820067	982
983	(0117)4960638	97830937	Home	False	Todays Date	97830937	983
984	+44909 879 0540	97901626	Home	False	Todays Date	97901626	984
985	01314960402	98013349	Home	False	Todays Date	98013349	985
986	+44(0)117 496 0190	9803605T	Home	False	Todays Date	9803605T	986
987	+44(0)20 74960491	98036901	Home	False	Todays Date	98036901	987
988	+44113 496 0534	98123544	Home	False	Todays Date	98123544	988
989	(0306) 999 0993	98141395	Home	False	Todays Date	98141395	989
990	+44(0)2074960773	9820277T	Home	False	Todays Date	9820277T	990
991	(01632) 960 119	98220297	Home	False	Todays Date	98220297	991
992	0113 496 0694	98239268	Home	False	Todays Date	98239268	992
993	+44(0)29 2018 0655	98312347	Home	False	Todays Date	98312347	993
994	+44114 496 0807	9833009T	Home	False	Todays Date	9833009T	994
995	+44(0)1614960862	9851336T	Home	False	Todays Date	9851336T	995
996	(0151)4960857	98624482	Home	False	Todays Date	98624482	996
997	+44117 496 0549	9916269T	Home	False	Todays Date	9916269T	997
998	+44(0)20 7496 0403	99262664	Home	False	Todays Date	99262664	998
999	(020) 74960650	99314363	Home	False	Todays Date	99314363	999
1000	+44(0)306 999 0247	99328514	Home	False	Todays Date	99328514	1000
\.


--
-- PostgreSQL database dump complete
--

