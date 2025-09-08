import pandas as pd 
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
  df = pd.read_csv("aircrashes-copy.csv")
  # clean data

  df.columns = df.columns.str.strip().str.replace(" ", "_").str.replace\
    (r"[^A-Za-z0-9_]", "")
  
  #### REPLACING EMPTY COLUMNS WITH UNKNOWN/Missing
  df["Country/Region"] = df["Country/Region"].fillna("Unspecified")
  df["Operator"] = df["Operator"].fillna("Unspecified")

  #### CLEAN COUNTRY/REGION COLUMN
  ###### Unknown are empty columns, Unspecified are unclear regions.
  country_corrections = {
    ' Alaska':'Alaska','Belgian':'Belgium','Brazil/tAmazonaves':'Brazil','British':'Britain','Cameroons':'Cameroon',
    'China?':'China','Democratic':'DRC','Equatorial':'Equitorial Guinea','French':'France','Hong':'Hong Kong','India\tPawan':'India',
    'near':'California','New':'New York','North':'North Korea','Northern':'Northern Ireland','Norway\tCHC':'Norway','ON':'Ontario Canada',
    'Papua':'Papua New Guinea','Puerto':'Puerto Rico','Saudi':'Saudi Arabia','SK':'Canada','South-West':'South Africa','Sri':'Sri Lanka',
    'Tennesee':'Tennessee','USSRAeroflot':'Russia','100':'Unspecified','BC':'British Columbia Canada','Bias':'China','Brazil\tLoide':'Brazil',
    'miles':'Miles','Spain\r\n\t\r\nMoron':'Spain','United':'UAE','Airlines':'Unspecified','Coloado':'Colorado','D.C.Capital':'Washington DC','Florida?':'Florida',
    'off':'Angola','The':'Netherlands','Argentinade':'Argentina','California?':'California','D.C.Air':'Florida','El':'El Salvador','Indonesia\r\n\t\r\nSarmi':'Indonesia',
    'NSW':'Australia','UARMisrair':'EgyptAir (UAR era)','Minnesota46826/109':'Minnesota','Qld':'Australia','U.S.':'United States',
    '325':'Unspecified','110':'Unspecified','116':'Unspecified','18':'Unspecified','570':'Unspecified','Germany?':'Germany','Azerbaijan\r\n\t\r\nBakou':'Azerbaijan',
    'USSRBalkan':'Balkan Bulgarian Airlines (USSR era)','Brazil\r\nFlorianopolis':'Brazil','Chile\tAerolineas':'Chile','Honduras?':'Honduras','US':'United States','Afghanstan':'Afghanistan',
    'USSRMilitary':'USSR Military Aviation','800':'Unspecified','Tajikistan\tMilitary':'Tajikistan','USSRAerflot':'Russia','Djibouti\r\n\tDjibouti':'Dijibouti',
    'France?':'France','UAEGulf':'UAE','Virginia.American':'Virginia America',"'-":"Unspecified",'10':'Unspecified','Unkown':'Unspecified'}
  df["Country/Region"] = df["Country/Region"].replace(country_corrections)

  #### CLEAN AIRCRAFT MANUFACTURERS COLUMN
  # Dictionary of corrections for Aircraft manufacturers
  manufacturer_corrections = {
    "Doublas": "Douglas","MD Douglas": "McDonnell Douglas","Mc Donnell Douglas": "McDonnell Douglas","De Havilland": "de Havilland",
    "de Havilland  Canada": "De Havilland Canada","Hadley Page 137Jetstream I": "Handley Page Jetstream","Lisnov": "Lisunov","C": "Cessna",
    "Fokke": "Focke-Wulf","B17G Flying": "Boeing B-17G Flying Fortress","Lockheed 14 Super": "Lockheed 14 Super Electra","Lockheed 188C": "Lockheed L-188C Electra",
    "Aerospatiale Caravelle": "Aérospatiale Caravelle","OFM": "OFM Aircraft","??": "Unknown","Swallow?": "Swallow","Embraer 110EJ Band./Embraer 110P": "Embraer 110 Bandeirante",
    "Embraer 110P1": "Embraer 110 Bandeirante","Pilatus Britten Norman": "Pilatus Britten-Norman","NAMC": "Nihon Aircraft Manufacturing Corporation",
    "Britten Norman": "Britten-Norman","Lockheed Super": "Lockheed Super Constellation","Lockheed 14": "Lockheed Model 14","Lockheed 18": "Lockheed Model 18 Lodestar",
    "Lockheed Hudson": "Lockheed Hudson","Vickers 610 Viking": "Vickers Viking 610","Vickers Viking 1B & Soviet": "Vickers Viking 1B","Vickers Valetta": "Vickers Valetta",
    "Vickers Viscount": "Vickers Viscount","Vickers Wellington": "Vickers Wellington","Vickers Vanguard": "Vickers Vanguard","Avro 685 York": "Avro 685 York",
    "Avro Shackleton": "Avro Shackleton","Handley Page": "Handley Page","Hawker Siddeley HS": "Hawker Siddeley","Hawker Siddeley Trident": "Hawker Siddeley Trident","British Aerospace BAe": "British Aerospace",
    "British Aerospace BAe": "British Aerospace","Cams": "CAMS","Hadley Page": "Handley Page","Messerschmidt": "Messerschmitt","Pilgrim": "Fairchild Pilgrim",
    "Aerocomp Comp Air": "Aerocomp Comp Air","Eurocopter EC225LP Super Puma M2+": "Eurocopter EC225LP Super Puma","Bell 212FAC": "Bell 212",
    "Bell 205": "Bell 205","Bell": "Bell","Stearman": "Stearman Aircraft","Stinson Model": "Stinson","Farman": "Farman Aviation Works",
    "Swallow\r\nSwallow?":"Swallow","Sikorsky S43 (flying":"Sikorsky S43 (flying)","Unknown /":"Unknown","Short Sandringham (flying":"Short Sandringham (flying)",
    "Avro 691 Lancastrian (flying":"Avro 691 Lancastrian (flying)","Short Sandringham 5 (flying":"Short Sandringham 5 (flying)",
    "Latécoère 23 (flying":"Latécoère 23 (flying)","Latécoère 300 (float":"Latécoère 300 (float)","Latecoere 301 (flying":"Latecoere 301 (flying)",
    "Helicopter?":"Helicopter","Short Sandringham 2 (flying":"Short Sandringham 2 (flying)","CMASA Wal (flying":"CMASA Wal (flying)",
    "Fairchild packet (C119 flying":"Fairchild packet (C119 flying)","Domier Delphin III (flying":"Domier Delphin III (flying)","Airship?":"Airship",
    'Latecoere 631 (sea':'Latecoere 631 (sea)','Aeromarine Model 85 (flying':'Aeromarine Model 85 (flying)','Vickers Viscount 745D /':'Vickers Viscount 745D',
    "Stinson?":"Stinson","?42":"42","?VP":"VP","Short Calcutta (flying":"Short Calcutta (flying)","Rutan Long EZ (experimental":"Rutan Long EZ (experimental)",
    "Hawker Siddeley Trident 2E /":"Hawker Siddeley Trident 2E",

 }
  df["Aircraft_Manufacturer"] = df["Aircraft_Manufacturer"].replace(manufacturer_corrections)
  df["Aircraft_Manufacturer"] = df["Aircraft_Manufacturer"].replace("?", " ")

  #### CLEANING AIRCRAFT COLUMN
  # Dictionary of corrections for Aircraft
  aircraft_corrections = {
    "Douglas DC 4?": "Douglas DC-4","Doublas Dc 3?": "Douglas DC-3","Antonov AN 26?": "Antonov An-26","Antonov AN 32?": "Antonov An-32",
    "Mi  8 helicopter?": "Mil Mi-8","Mi  8?": "Mil Mi-8","Mil Mi 8?": "Mil Mi-8","Curtiss seaplane?": "Curtiss Seaplane","Zeppelin L 59 (airship)?": "Zeppelin LZ 59",
    "Curtiss C 46 Commando?": "Curtiss C-46 Commando","??": "Unknown","?VH  TAT": "Unknown","\"Swallow\nSwallow?\"": "Swallow","Zeppelin L 70 (airship)?": "Zeppelin L 70 (airship)",
    "UH  60 Blackhawk helilcopter?": "UH-60 Black Hawk helicopter","Caproni Ca.48?": "Caproni Ca.48","Unknown / Unknown?": "Unknown","Antonov AN 22?": "Antonov AN 22",
    "Siebel Si 204?": "Siebel Si 204","Zeppelin L 23 (airship)?": "Zeppelin L 23 (airship)","Lockheed 18 56 Lodestar?": "Lockheed 18-56 Lodestar",
    "Consolidated B 24?": "Consolidated B-24","Mc Donnell Dougals DC 9?": "McDonnell Douglas DC-9","Fokker Universal F 14?": "Fokker Universal F-14",
    "Douglas C47?": "Douglas C-47","Dirigible Roma (airship)?": "Dirigible Roma (Airship)","Mil Mi 17?": "Mil Mi-17","Helicopter?": "Helicopter (Unspecified)",
    "Douglas DC 3?": "Douglas DC-3","Curtiss C 46?": "Curtiss C-46","Lisunov Li 2?": "Lisunov Li-2","Black Hawk helicopter?": "Sikorsky UH-60 Black Hawk",
    "Mil Mi 8 (helicopter)?": "Mil Mi-8 Helicopter","Mil Mi 8 / Mil Mi": "Mil Mi-8","Douglas C 47?": "Douglas C-47","Fairchild packet (C119 flying boxcar)?": "Fairchild C-119 Flying Boxcar",
    "Farman F 40?": "Farman F.40","Tupolev ANT 9?": "Tupolev ANT-9","Mi  17?": "Mil Mi-17","Boeing RC 135E?": "Boeing RC-135E","Douglas DC 5?": "Douglas DC-5",
    "PBY Catalina?": "Consolidated PBY Catalina","KJ  2000?": "KJ-2000","FD Type Dirigible?": "Dirigible (Type FD)","Pitcairn PA 6 Mailwing?": "Pitcairn PA-6 Mailwing",
    "LVG C VI?": "LVG C.VI","Sukhoi Su 2742": "Sukhoi Su-27 (42)","Loening C W Air Yaht?": "Loening CW Air Yacht","?NC21V": "NC21V",
    "Mil Mi 8T (helicopter)?": "Mil Mi-8T helicopter","Douglas DC 3 (C": "Douglas DC-3","Douglas DC C": "Douglas DC-3","Five Grumman TBM Avengers?": "Grumman TBM Avenger (5 units)",
    "Antonov AN 12?": "Antonov An-12","Fairchild Pilgrim 100A?": "Fairchild Pilgrim 100A","KB  50?": "Boeing KB-50","Boeing Vertol CH 47 (helicopter)?": "Boeing Vertol CH-47 Chinook",
    "Boeing Vertol CH 47 (helilcopter)?": "Boeing Vertol CH-47 Chinook","Fairchild C 123?": "Fairchild C-123 Provider","Fairchild?": "Fairchild (unspecified model)",
    "Twin Apache?": "Curtiss-Wright XP-60 'Twin Apache'","Ilyushin II 14?": "Ilyushin Il-14","Lockheed 18 08 Lodestar	N410M": "Lockheed 18-08 Lodestar N410M",
    "Lockheed 049 ConsellationNC86505": "Lockheed 049 Constellation NC86505","MI 172 V5 helicopter?": "Mil Mi-172 (helicopter)","Zeppelin L 43 (airship)?": "Zeppelin LZ-43 (airship)",
    "L  Hudson?": "Lockheed Hudson","Fairchild C 199G?": "Fairchild C-119G","Pitcairns PA 6?": "Pitcairn PA-6","Aeromarine Model 85 (flying boat)?": "Aeromarine Model 85 (flying boat)",
    "McDonnel F 4E Phantom II?": "McDonnell F-4E Phantom II","Sepecat Jaguar A?": "SEPECAT Jaguar A","Junkers JU 86?": "Junkers Ju-86",
    "?139": "Unknown","Airship?": "Airship","C  46?": "Curtiss C-46","H  21B?": "Piasecki H-21B","MiG  23?": "Mikoyan-Gurevich MiG-23",
    "MiG  15 UTI?": "Mikoyan-Gurevich MiG-15 UTI","Douglas C 54 Skymaster?": "Douglas C-54 Skymaster","Douglas C 54?": "Douglas C-54",
    "Stinson?": "Stinson","Zeppelin L 22 (airship)?": "Zeppelin L-22 (airship)","Super Zeppelin (airship)?": "Zeppelin (Super airship)",
    "Zeppelin L 34 (airship)?": "Zeppelin L-34 (airship)","Ilyushin IL 18?": "Ilyushin Il-18","Kalinin K 7?": "Kalinin K-7",
    "Boeing Vertol CH47A (helicopter)?": "Boeing Vertol CH-47A (helicopter)","?42  52196": "Douglas C-42 52196","Budd RB 1 Conestoga?": "Budd RB-1 Conestoga",
    "Li  2 / Li": "Lisunov Li-2","Lockheed Hudson?": "Lockheed Hudson","Tempest?": "Hawker Tempest","Ford Tri motor 5?": "Ford Trimotor 5",
    "Douglas A 3D Skywarrior?": "Douglas A-3D Skywarrior","De Havilland DH 4?": "de Havilland DH-4",
    "Zeppelin L 31 (airship)?": "Zeppelin L-31 (Airship)",
 }


  df["Aircraft"] = df["Aircraft"].replace(aircraft_corrections)

  ######## CLEANING LOCATION COLUMN
  # Dictionary of corrections for Location
  location_corrections = {
    "Shanghi China": "Shanghai China","Ningpo Bay China": "Ningbo Bay China","Near Shensi China?": "Near Shaanxi China","Pao Ting Fou China?": "Baoding (Pao Ting Fu) China",
    "Baranquilla Colombia": "Barranquilla Colombia","Rio de Janerio Brazil": "Rio de Janeiro Brazil","Near Belem Brazil\tLoide": "Near Belem Brazil (Loide)",
    "Manaus Brazil\tAmazonaves": "Manaus Brazil (Amazonaves)","Coen Australila": "Coen Australia","Sorta Norway\tCHC": "Sortland Norway (CHC)",
    "Russian Mission Alaksa": "Russian Mission Alaska","Tamanraset Algeria": "Tamanrasset Algeria","Near Konigs Wusterausen East": "Near Königs Wusterhausen East Germany",
    "Sagone India": "Sangone India","Jirkouk Iraq": "Kirkuk Iraq","Near Alma-Ata Kazakastan": "Near Alma-Ata Kazakhstan","Chrisinau Moldova": "Chisinau Moldova",
    "Ixtaccihuati Mexico": "Iztaccihuatl Mexico","Cerro Lilio Mexico": "Cerro del Lilio Mexico","Benito Bolivia": "Beníto Bolivia","Colorado Bolivia": "Colorada Bolivia",
    "Kupe Mountains Cameroons": "Kupe Mountains Cameroon","Massamba Democratic": "Massamba Congo (Democratic Republic)","Mugogo Democratic": "Mugogo Congo (Democratic Republic)",
    "Bukavu Democratic": "Bukavu Congo (Democratic Republic)","Kongolo Democratic": "Kongolo Congo (Democratic Republic)","Nganga Lingolo Congo": "Nganga Lingolo Congo (DRC)",
    "Bundeena Australia": "Bundeena New South Wales Australia","Chilang Point Bias": "Chilang Point Bissau Guinea-Bissau","Hangow China": "Hangzhou China",
    "Fort Hertz China": "Fort Hertz (Putao) Myanmar","Wangmoon China": "Wangmo China","Sakiya Saugye Japan": "Sakiyama Sogyo Japan","Montnago Italy": "Montagnano Italy",
    "Off Stromboli Italy": "Near Stromboli Italy","Near Ardinello di Amaseno Italy": "Near Ardielle di Amaseno Italy",
    "Kabassaak Turkey": "Kabasakal Turkey","Zaporozhye Ukraine": "Zaporizhzhia Ukraine","Belgrad Yugoslavia": "Belgrade Yugoslavia",
    "?Deutsche Lufthansa": "Deutsche Lufthansa","Belgrade Yugosalvia": "Belgrade Yugoslavia","Green Grove Florida?": "Green Grove Florida",
    "Nnear Albuquerque New": "Near Albuquerque New Mexico","Wroctaw Poland": "Wroclaw Poland","Nnear Yuzhno-Sakhalinsk Russia": "Near Yuzhno-Sakhalinsk Russia",
    "Near Havlien Pakistan": "Near Havellian Pakistan","Preswick Scotland": "Prestwick Scotland","Gazni Afghanistan": "Ghazni Afghanistan",
    "Kranoyarsk Russia": "Krasnoyarsk Russia","Fond-du-Lac Saskatchewan": "Fond du Lac Saskatchewan","Catherham Surrey": "Caterham Surrey",
    "Nurnberg Germany": "Nürnberg Germany","Eubeoa Greece": "Euboea Greece","Hati": "Haiti","Mendotta Minnisota": "Mendota Minnesota","Wisconson": "Wisconsin",
    "Off Venice California?": "Off Venice California","Guaderrama Spain": "Guadarrama Spain","UARMisrair": "UAR Misrair","Horwich Lancs": "Horwich Lancashire",
    "Caravelas Bay Brazil": "Caravelas Brazil","Lapadrera Colombia": "La Pedrera Colombia","Gibraltar?": "Gibraltar","Nnear Kuybyshev Russia": "Near Kuybyshev Russia",
    "Near Syktyvar Russia": "Near Syktyvkar Russia","Khartoom Sudan": "Khartoum Sudan","Near Rijeka Yugoslavia": "Near Rijeka Yugoslavia",
    "Bakou Azerbaijan\n\t\nBakou": "Baku Azerbaijan","San Diego CADuncan": "San Diego CA","Near Wawona Cailifornia": "Near Wawona California",
    "Nacias Nguema Equatorial": "Nacias Nguema Equatorial Guinea","Off Rasal United": "Off Rasal United Kingdom","Torysa Czechoslovakia": "Torysa Czechoslovakia",
    "Burbank Calilfornia": "Burbank California","San Barbra Honduras?": "San Barbara Honduras","Boston Massachutes": "Boston Massachusetts",
    "Near Cuidad de Valles Mexic": "Near Ciudad de Valles Mexico","Zamboanga Philipines": "Zamboanga Philippines","Near Amiens Picrdie": "Near Amiens Picardie",
    "Dearborn Minnesota": "Dearborn Michigan","Near Walsenberg Colorado": "Near Walsenburg Colorado","Off Mar del Plata Aregntina": "Off Mar del Plata Argentina",
    "Guatamala City  Guatemala": "Guatemala City Guatemala","San Salvador El": "San Salvador El Salvador","La Poyatta Colombia": "La Hoyada Colombia",
    "Stephenville Newfoundlandu.s.": "Stephenville Newfoundland U.S.","Near Jalalogori West": "Near Jalalogori West","Near Sarowbi Afghanistan": "Near Sarobi Afghanistan",
    "Near Bagram Afghanstan": "Near Bagram Afghanistan","Luassingua Angola": "Luassingua Angola","Techachapi Mountains California": "Tehachapi Mountains California",
    "Off Cape Mendocino CAMilitary": "Off Cape Mendocino CA Military","Landsdowne House Canada": "Lansdowne House Canada","Ste. Therese de Blainville Canada": "Sainte-Thérèse-de-Blainville Canada",
    "Near Petrich bulgaria": "Near Petrich Bulgaria","Novia Scotia Canada": "Nova Scotia Canada","Between Shanghi and Canton China": "Between Shanghai and Canton China",
    "Near Kindu Congo": "Near Kindu DR Congo","Near Bugulumisa Congo": "Near Bugulma Congo","Near Hasna Egypt": "Near Aswan Egypt",
    "Near Point Alert Ellesmere": "Near Alert Ellesmere","Near Trevelez Granada": "Near Trevélez Granada","Near Chiringa India": "Near Cherringa India",
    "Chiraz Iran": "Shiraz Iran","Venice Italyde": "Venice Italy","Abidjan Ivory": "Abidjan Ivory Coast","Barskoon Kirghizia": "Barskoon Kyrgyzstan",
    "Almelund Minnisota": "Almelund Minnesota","La Rache Morocco": "Larache Morocco","Near Lonkin Myanmar": "Near Lonkin Burma (Myanmar)",
    "Over the Carribean SeaLACSA": "Over the Caribbean Sea LACSA","Juvisy-sur-Orge France?": "Juvisy-sur-Orge France","Isiro Democtratic": "Isiro Democratic Republic of Congo",
    "Near Nador Morroco": "Near Nador Morocco","Centeral Afghanistan": "Central Afghanistan","Kharkov. Ukraine Russia": "Kharkov Ukraine",
    "Georgian SSR USSRAerflot": "Georgian SSR USSR Aeroflot","Gulf of Sivash USSRAeroflot": "Gulf of Sivash USSR Aeroflot",
    "Off St. Petersburg USSRAeroflot": "Off St. Petersburg USSR Aeroflot","Petropavlosk USSRAeroflot": "Petropavlovsk USSR Aeroflot",
    "Near Leningrad USSRAeroflot": "Near Leningrad USSR Aeroflot","Near Khabarovsk USSRAeroflot": "Near Khabarovsk USSR Aeroflot",
    "New York New":"New York"
   }

  df["Location"] = df["Location"].replace(location_corrections)

  ##### CLEANING OPERATORS COLUMN
  # Dictionary of corrections for Operators
  operator_corrections = {
    "Airways??": "Airways","N/A":"Unknown","GuineaTrans New?": "Guinea Trans New","Nevada      Vegas Las of SW miles United Air Lines /": "Nevada Las Vegas - United Air Lines",
    "Airlines Australia GuineaTrans New": "Airlines Australia - Guinea Trans New","(UK) Airlines International SwitzerlandInvicta": "(UK) Airlines International - Switzerland Invicta",
    "Alaska Air Fuel": "Alaska Air (Fuel Service)","USSRAeroflot": "USSR Aeroflot","Airlines Airlines/Alliance Indian": "Airlines Alliance Indian",
    "Force Air OceanIndian": "Force Air Ocean Indian","England Walcot Air Line": "England Walcott Air Line","Airways) Nigeria by (chartered ArabiaNationair": "Airways Nigeria (chartered by Arabia Nationair)",
    "Amercia Air": "America Air","Foundation Reasearch Purdue - GuineaPrivate": "Foundation Research Purdue - Guinea Private",
    "Airlines Duch Royal KLM": "Airlines Dutch Royal KLM","Force Air US - Militiary": "Force Air US - Military","GuineaAeroflot": "Guinea Aeroflot",
    "Inc. Flight InaguaAgape": "Inc. Flight Inagua Agape","KarkinitskyAeroflot of": "Karkinitsky Aeroflot","Italila Eurojet": "Italia Eurojet",
    "Ivorie CoastAir": "Ivory Coast Air","Airlilnes LeoneParamount": "Airlines Leone Paramount","Aviaition Ababeel": "Aviation Ababeel",
    "Airlines Dutch Royal NetherlandsKLM": "Airlines Dutch Royal Netherlands KLM","UzbekistanAeroflot": "Uzbekistan Aeroflot",
    "Aéreo Taxi AéreoBahia Taxi AéreoBahia Taxi Bahia": "Aéreo Taxi Bahia","Airways Overseas KongPacific": "Airways Overseas Hong Kong Pacific",
    "Service Mail Aerial JerseyUS": "Service Mail Aerial Jersey US","Airways National Zealand ZealandNew": "Airways National New Zealand",
    "Canada Miami Aviaition/Air Manila": "Canada Miami Aviation / Air Manila","Airways) Orient (Filipinas Fairways": "Airways Orient (Filipinas Fairways)",
    "Romane) Aeriene (Transporturile Tarom": "Romane Aeriene (Transporturile Tarom)","Airlines ArabiaVnukovo": "Airlines Arabia Vnukovo",
    "LeoneHelicsa": "Leone Helicsa","Azur VietnamAigle": "Azur Vietnam Aigle","Vietnam) (South Vietnam VietnamAir": "South Vietnam Airlines",
    "Force Air Lankan Sri - LankaMilitary": "Force Air Sri Lankan - Military","Force Air Royal - LankaMilitary": "Force Air Royal Sri Lanka - Military",
    "Airways EmiratesSterling Arab": "Airways Emirates Sterling Arab","KingdomLoganair": "Kingdom Loganair","Singapore Airllines": "Singapore Airlines",
    "Airways Guiena": "Airways Guinea","Lines Air ElalatPhilippine of island Philippine the": "Lines Air El Alat Philippine of the Philippine Island",
    "Air Bay GuineaMilne New": "Air Bay Guinea Milne New","Forces Air Army U.S. - GuineaMilitary": "Forces Air Army U.S. - Guinea Military",
    "Helicopter York  YorkNew": "Helicopter York New York","Reederei Zeppelin JerseyDeutsche": "Reederei Zeppelin Jersey Deutsche",
    "Airlines Cargo JerseyRegina": "Airlines Cargo Jersey Regina","Airways W JerseyFlying": "Airways W Jersey Flying",
    "Private / Airways YorkGreylock": "Private / Airways York Greylock","Force Air U.S. - MexicoMilitary": "Force Air U.S. - Mexico Military",
    "Airlines Ukranian-Mediterranean": "Airlines Ukrainian-Mediterranean","France Indian National Airlines": "Indian Airlines (France Mislabel)",
    "Air Western and Continental Trans": "Air Western & Continental Transport","California          Angeles Continental Airlines": "California Los Angeles Continental Airlines",
    "Airlines VirginiaCapital": "Virginia Capital Airlines","New York          York American Airlines": "New York American Airlines",
    "Airlines YorkMohawk": "Mohawk Airlines New York","New York          York USAir": "New York USAir",
    "Airlines Western JerseyColonial": "Colonial Airlines Western Jersey","Airlines JerseyCentral": "Central Jersey Airlines",
    "Airlines YorkContinental": "Continental Airlines New York","African RepublicUnion Aeromaritime": "African Republic Union Aeromaritime Transport",
    "Aviati Mustang": "Mustang Aviation","Force Air Argentine - RicaMilitary": "Argentine Air Force / Costa Rica Military (Mislabel)",
    "India          Bengal British Overseas Airways": "British Overseas Airways Bengal India","England Bristop Aeroplane Company": "England Bristol Aeroplane Company",
    "USSRAeroflot / Soviet Air Force": "USSR Aeroflot / Soviet Air Force","Aviation Cap Wehite": "Cap White Aviation","Indiaèkoda (India) Ltd": "Indaèkoda (India) Ltd.",
    "Air Paukn": "Air Paukn","York?": "York Airways","Nordchurchaid": "Nord Church Aid","Charter - Aerocontroctors": "Aerocontractors Charter",
    "Flamence RicoAir": "Flamenco Air Puerto Rico","Russian - /Military Aeroflot": "Aeroflot (Russian Military)",
    "Brazil          Paulo Total  Air Lines": "Total Air Lines São Paulo Brazil","service guard border Kazakhstan - KazakistanMilitary": "Kazakhstan Border Guard Service - Military",
    "Airways HampshireNortheast": "Northeast Airlines (New Hampshire)","Airways JerseySaturn": "Saturn Airways (NJ)","CarolinaStratofreight": "Stratofreight (North Carolina)",
    "Indonesia          Sulawesi Eastindo": "Eastindo Aviation (Sulawesi, Indonesia)","Flyveselksap Wideroe's": "Flyveselskap Widerøe",
    "Canada          Scotia MK Airlines": "Scotia MK Airlines Canada","Aviation Costal": "Coastal Aviation","Unied Kingdom Air Union": "United Kingdom Air Union",
    "Connection) (American Airlines Corporate": "American Airlines Corporate Connection","Air Divi AntillesDivi": "Divi Divi Air (Netherlands Antilles)",
    "Airlines Dutch Royal IndiesKLM": "KLM Royal Dutch Airlines (Netherlands Indies)","Corp. Aviation Paramount - Taxi JerseyAir": "Paramount Aviation Corp. - Air Taxi (NJ)",
    "Airways York YorkNew": "New York Airways","Zealand New Freight ZealandAir": "New Zealand Air Freight",
    "Service Flying YorkChamberlin": "Chamberlin Flying Service (NY)","WNBC - YorkPrivate": "WNBC Private Flight (NY)",
    "Airlines HampshireNortheast": "Northeast Airlines (New Hampshire)",
  }


  df["Operator"] = df["Operator"].replace(operator_corrections)

  # In some cases, fatalities were greater than the number aboard (illogical).
  # Such rows were removed.
  df = df[df["Fatalities_(air)"] <= df["Aboard"]]

  # reset index
  df = df.reset_index(drop=True)

  return df

try:
  df = load_data()

  st.title("Aircraft Crashes Full Data")


  #filters = { 
  #"Location": df["Location"].unique(),
  #"Country/Region": df["Country/Region"].unique(),
  #"Aircraft_Manufacturer":df["Aircraft_Manufacturer"].unique(),
  #"Aircraft":df["Aircraft"].unique(),
  #"Operator":df["Operator"].unique(),}

  # filters
  filters = { 
    "Location": df["Location"].value_counts().head(5).index.tolist(),
    "Country/Region": df["Country/Region"].value_counts().head(5).index.tolist(),
    "Aircraft_Manufacturer": df["Aircraft_Manufacturer"].value_counts().head(5).index.tolist(),
    "Aircraft": df["Aircraft"].value_counts().head(5).index.tolist(),
    "Operator": df["Operator"].value_counts().head(5).index.tolist(),
 }
  # Store selection
  selected_filters = {}

  # generate multi-select widgets dynamically
  for key,options in filters.items():
    selected_filters[key] = st.sidebar.multiselect(key,options)

  #take a copy of the data 
  filtered_df = df.copy()
   
  #apply filter selection to the data
  for key,selected_values in selected_filters.items():
    if selected_values:
      filtered_df = filtered_df[filtered_df[key].isin(selected_values)]

  #display the data
  #st.dataframe(filtered_df)

  #display a quick overview using matrix
  st.write("## Quick Overview")


  # CALCULATIONS/METRICS
  year_highest_accidents = df['Year'].value_counts().idxmax()   # 1. Year with highest accident
  total_fatalities_aboard = df['Fatalities_(air)'].sum()        # 2. Total fatalities: aboard 
  total_fatalities_ground = df['Ground'].sum()                  # 3. Total fatalities: ground
  top_country = df['Country/Region'].value_counts().idxmax()  # 4. countries/regions with the most accidents
  top_location = df['Location'].value_counts().idxmax()        # 5. location with the most accidents
  top_manufacturer = df['Aircraft_Manufacturer'].value_counts().idxmax() # 6. manufacturer with most accident
  


    # streamlit column components
  #col1,col2,col3,col4,col5 = st.columns(5)

  #with col1:
    #st.metric("Country/Region: ",top_countries)

  #with col2:
    #st.metric("Location: ", top_locations)

  #with col3:
    #st.metric("Aircraft Manufacturer: ",top_manufacturers)

  #with col4:
    #st.metric("Operator: ", top_operator)

  #with col5:
    #st.metric("Aircraft: ", top_aircraft)



  col1, col2 = st.columns(2)

  with col1:
    st.write("### Table Metrics")

        # Section 1 (like a sub-column on top)
    with st.container():
        st.write("Country/Region with highest accident: ")
        st.write("####",top_country)

        # Section 2 (like a sub-column below)
    with st.container():
        st.write("Location with highest accident: ")
        st.write("####",top_location)

            # Section 3 
    with st.container():
        st.write("Aircraft Manufacturer with highest accident: ")
        st.write("####",top_manufacturer)
    




  with col2:
    st.write("### EDAs")

    with st.container():
        st.write("Year with highest accident: ")
        st.write("####",year_highest_accidents)
    
    with st.container():
        st.write("Total fatalities(aboard): ")
        st.write("####",total_fatalities_aboard)

    with st.container():
        st.write("Total fatalities(ground): ")
        st.write("####",total_fatalities_ground)
  
  ####### Research Questions
  st.subheader("Analysis Findings")

  
  ### Q1. Top 10 countries/regions with highest accidents
  st.write("##### Q1. Top 10 countries/regions with highest accidents")
  temp1 = filtered_df['Country/Region'].value_counts().head(10).reset_index()
  temp1.columns = ["Country/Region", "Total Accidents"]

  st.dataframe(temp1)
  #### Graph 1
  chart1= alt.Chart(temp1).mark_bar().encode(
  y='Total Accidents:Q',
  x=alt.X('Country/Region:N', sort='-y'),
  color=alt.Color("Country/Region:N",legend=None),
  tooltip=['Country/Region', 'Total Accidents']
  ).properties(height=400).interactive()

  st.altair_chart(chart1,use_container_width=True)


  ## Q2. Aircraft manufacturer with most accidents
  st.write("##### Q2. Top 10 Aircraft Manufacturers with highest accidents")
  temp2= filtered_df['Aircraft_Manufacturer'].value_counts().head(10).reset_index()
  temp2.columns =["Aircraft Manufacturers","Total Accidents"]
  st.dataframe(temp2)

  ### Graph 2
  chart2, ax = plt.subplots(figsize=(10, 6))
  sns.reset_defaults()
  sns.set_theme()
  sns.barplot(x='Total Accidents', y='Aircraft Manufacturers', data=temp2, ax=ax)
  ax.set_title('Top 10 Aircraft Manufacturers by Number of Accidents')
  ax.set_xlabel('Number of Accidents')
  ax.set_ylabel('Aircraft Manufacturers')
  st.pyplot(chart2) 


  ### Q3. Average fatalities aboard per aircraft type
  st.write("##### Q3. Average fatalities aboard per aircraft type")
  temp3 = filtered_df.groupby('Aircraft')['Fatalities_(air)'].mean().sort_values(ascending=False).head(10).reset_index()
  temp3.columns = ["Aircrafts", "Average Fatalities"]

  st.dataframe(temp3, use_container_width=True)

  # Create bar chart
  chart3, ax = plt.subplots(figsize=(12,7))
  ax.barh(temp3['Aircrafts'], temp3['Average Fatalities'], color='orange')
  ax.set_title('Average Fatalities by Aircraft', fontsize=16)
  ax.set_xlabel('Average Fatalities', fontsize=14)
  ax.set_ylabel('Aircrafts', fontsize=14)
  ax.tick_params(axis='x', labelrotation=45,labelsize=12)  # Rotate & enlarge x-axis labels
  ax.tick_params(axis='y', labelsize=12)
  st.pyplot(chart3)


  ### Q4. year with highest number of aircraft accidents
  st.write("##### Q4. Accidents Trend by Year")

  temp4 = filtered_df['Year'].value_counts().sort_index().reset_index()
  temp4.columns = ['Year', 'Total Accidents']

  st.dataframe(temp4, use_container_width=True)
  
  chart4 = alt.Chart(temp4).mark_line(point=True).encode(
      x=alt.X('Year:O', title='Year'),
      y=alt.Y('Total Accidents:Q', title='Total Accidents'),
      tooltip=['Year', alt.Tooltip('Total Accidents:Q', format='.2%')]
  ).properties(
      title='Accidents Trend by Year',
      width=700,
      height=400
  ).interactive()
  st.altair_chart(chart4, use_container_width=True)

  
  ### Q5. What percentage of fatalities occurred on the ground vs. aboard?

  ground_total = filtered_df['Ground'].sum()
  aboard_total = filtered_df['Fatalities_(air)'].sum()

  # Create DataFrame for display
  st.write("##### Q5. Fatalities Summary")
  temp5 = pd.DataFrame({
     'Category': ['Ground', 'Aboard'],
     'Total Fatalities': [ground_total, aboard_total]
  })
  st.table(temp5)

  # Create Pie Chart
  if ground_total == 0 and aboard_total == 0:
    st.warning("No fatalities data available to plot. Please check the dataset.")
  else:
    chart5, ax = plt.subplots(figsize=(3,2))
    ax.pie([ground_total, aboard_total], labels=['Ground', 'Aboard'], autopct='%1.1f%%', startangle=90)
    ax.set_title('Fatalities: Ground vs. Aboard', fontsize=8)
    st.pyplot(chart5, use_container_width=False)



  #### Q6. Survival Rate overtime
  st.write("##### Q6.Average Survival Rate by Year")
  filtered_df['SurvivalRate'] = (filtered_df['Aboard'] - filtered_df['Fatalities_(air)']) / filtered_df['Aboard']
  filtered_df['SurvivalRate'] = filtered_df['SurvivalRate'].fillna(0)

  # Group by year
  temp6 = filtered_df.groupby('Year')['SurvivalRate'].mean().reset_index()

  # Display table
  st.dataframe(temp6, use_container_width=True)

  # Altair line chart
  chart6 = alt.Chart(temp6).mark_line(point=True).encode(
      x=alt.X('Year:O', title='Year'),
      y=alt.Y('SurvivalRate:Q', title='Average Survival Rate'),
      tooltip=['Year', alt.Tooltip('SurvivalRate:Q', format='.2%')]
  ).properties(
      title='Average Survival Rate Over Time',
      width=700,
      height=400
  ).interactive()
  st.altair_chart(chart6, use_container_width=True)



  ####### QUESTION 7
  # 6.. Top 10 locations with the most accidents
  st.write("##### Q7.Top 10 Location with highest accidents")
  temp7 = filtered_df['Location'].value_counts().head(10).reset_index()
  temp7.columns = ["Location","Total Accidents"]

  st.dataframe(temp7, use_container_width=True)

  #### Graph 7
  chart7= alt.Chart(temp7).mark_bar().encode(
  x='Total Accidents:Q',
  y=alt.Y('Location:N', sort='-x'),
  color=alt.Color("Location:N",legend=None),
  tooltip=['Location', 'Total Accidents']
  ).properties(height=300).interactive()

  st.altair_chart(chart7,use_container_width=True)

  
  ####### QUESTION 8
  # 8. Top operators with the most accidents
  st.write("##### Q8.Top 10 Operators with highest accidents")
  temp8 = filtered_df['Operator'].value_counts().head(10).reset_index()
  temp8.columns=["Operator","Total Accidents"]

  st.dataframe(temp8,use_container_width=True)

  #### Graph 8
  chart8= alt.Chart(temp8).mark_bar().encode(
  x='Total Accidents:Q',
  y=alt.Y('Operator:N', sort='-x'),
  color=alt.Color("Operator:N",legend=None),
  tooltip=['Operator', 'Total Accidents']
  ).properties(height=300).interactive()

  st.altair_chart(chart8,use_container_width=True)


  ###### QUESTION 9
  ##### 9. Accident trend by Quater

  st.write("##### Q9. Accidents Trend by Quarter")

  temp9 = filtered_df['Quarter'].value_counts().sort_index().reset_index()
  temp9.columns = ['Quarter', 'Total Accidents']

  st.dataframe(temp9, use_container_width=True)
  
  chart9 = alt.Chart(temp9).mark_bar(point=True).encode(
      y='Total Accidents:Q',
      x=alt.X('Quarter:N', sort='-y'),
      tooltip=['Quarter', 'Total Accidents']
  ).properties(height=300).interactive()

  st.altair_chart(chart9, use_container_width=True)


  ###### Question 10
  ##### Q10. Aircraft Manufacturers and Total Accidents per Decade
  st.write("##### Q10. Aircraft Manufacturers and Total Accidents per Decade")

  # Create Decade column
  filtered_df['Decade'] = (filtered_df['Year'] // 10) * 10

  # Group by decade and calculate metrics
  temp10 = (
      filtered_df.groupby('Decade')
          .agg(
              Unique_Manufacturers=('Aircraft_Manufacturer', 'nunique'),
              Total_Accidents=('Aircraft_Manufacturer', 'count')
          )
          .reset_index()
          .sort_values('Decade')
  )
  temp10.columns = ['Decade','Aircraft Manufacturers','Total Accidents']
  st.dataframe(temp10, use_container_width=True, height=len(temp10) * 35 + 50)

  #### Graph 10
  # Bar chart for Total Accidents
  bars = alt.Chart(temp10).mark_bar(color="skyblue").encode(
      x=alt.X("Decade:O", title="Decade"),
      y=alt.Y("Total Accidents:Q", title="Total Accidents")
  )
  # Line chart for Aircraft Manufacturers
  line = alt.Chart(temp10).mark_line(color="red", point=True).encode(
      x="Decade:O",
      y=alt.Y("Aircraft Manufacturers:Q", title="Aircraft Manufacturers")
  )

  # Combine charts with dual axis
  chart10 = alt.layer(bars, line).resolve_scale(
      y='independent'  # allows two separate y-axes
  ).properties(
      title="Aircraft Manufacturers and Total Accidents per Decade",
      width=700,
      height=400
  )

  st.altair_chart(chart10, use_container_width=True)


  st.write("##### Notes: ")
  st.write("'Unspecified' is used in empty rows or rows with unclear entries as left by the original dataset")






except Exception as e:
  st.error("Error: check error details")

  with st.expander("Error Details"):
    st.code(str(e))
    # st.code(traceback.format_exc())