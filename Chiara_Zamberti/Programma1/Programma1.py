#-*- coding: utf-8 -*- 

import sys
import codecs
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk import pos_tag


#Definisco la funzione per la tokenizzazione e che restituisce la lunghezza totale dei tokens
def Tokenizer(frasi):
	#inizializzo le liste e i valori
	LunghezzaTOT = 0.0
	tokensTOT = []
	#creo un ciclo che scorre tutte le frasi del testo
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		#aggiungo tutti i token alla lista tokensTOT
		tokensTOT = tokensTOT+tokens
		#calcolo la lunghezza totale del testo
	LunghezzaTOT = len(tokensTOT)
	return LunghezzaTOT, tokensTOT

#Definisco la funzione che trova la lunghezza media dei tokens (in termini di caratteri, senza punteggiatura)
def LunghezzaMediaTokChar(testotokenizzato):
	#inizializzo i valori
	average=0.0
	totCaratteri=0.0
	#creo una variabile che toglie la punteggiatura dal testo
	rimuoviPunt = re.compile('.*[A-Za-z0-9]*.')
	#tolgo la punteggiatura dal testo tokenizzato
	testotokenizzatoNoPunt = [word for word in testotokenizzato if rimuoviPunt.match(word)]
	#creo un ciclo che scorre il testo tokenizzato senza punteggiatura
	for tok in testotokenizzatoNoPunt:
		totCaratteri=totCaratteri+len(tok)	
	#calcolo la lunghezza media dei tokens in termini di caratteri
	average = float(totCaratteri)/len(testotokenizzatoNoPunt)
	return average

#Definisco la funzione che trova la lunghezza media delle frasi in termini di tokens
def AverageRawLength(testoTok, frasi):
	#calcolo la lunghezza media delle frasi in termini di token
	media = float(len(testoTok)) / float(len(frasi))
	return media

#Definizione della funzione per calcolare la lunghezza del Vocabolario
def Vocabolario(testotokenizzato):
	#calcolo il vocabolario del testo già tokenizzato, restituendo la lista dei tokens
	vocabolario = set(testotokenizzato)
	#calcolo il voc cioè il numero dei tokens del vocabolario
	voc = len(vocabolario)
	#restituisco l'insieme dei token del vocabolario
	return voc, vocabolario

 #Definizione della funzione per calcolare la distribuzione degli hapax sui primi 3000 tokens del testo
def distribuzioneHapax(testotokenizzato):
	#definisco una lista
	hapax=[]
	#scorro i primi 3000 tokens del testo tokenizzato
	for token in testotokenizzato[:3000]:
		#creo un contatore che conta tutti gli hapax, ovvero i tokens con occorrenza=1
		if testotokenizzato.count(token)== 1:
			#aggiungo gli hapax alla lista creata
			hapax = testotokenizzato+hapax
			#aggiungo i token trovati in coda alla lista hapax
			hapax.append(token)
			#calcolo la distribuzione degli hapax sui primi 3000 tokens
	Distrhapax = len(hapax)/3000
	#
	return Distrhapax

#Definisco la funzione che calcola la ricchezza lessicale attraverso la Type Token Ratio sui primi 3000 tokens del testo
def TTR(testotokenizzato):
	#creo una variabile che imposta a testotokenizzato un range di 3000 tokens
	tokens3000 = set(testotokenizzato[:3000])
	#calcolo la TTR
	ttr = float(len(tokens3000))/3000
	return ttr

#Definisco la funzione che assegna a ciascuna parte del testo il POS tagging
def POSTag(testotokenizzato):
	#definisco una variabile che applica il POS Tagging al testo tokenizzato
	tokensPOSTot = pos_tag(word_tokenize(testotokenizzato))
	return tokensPOSTot


#Definisco la funzione che calcola la distribuzione (in termini percentuali) di sostantivi, aggettivi, verbi e preposizioni e la densità lessicale, (tra sostantivi, verbi, avverbi e aggettivi, tranne "." e ",") 
def SVAP(testotokenizzato, lunghezza):
	#definisco le liste
	sostantivi = [word + "/" + tag for (word, tag) in testotokenizzato if tag.startswith('N')]
	aggettivi = [word + "/" + tag for (word, tag) in testotokenizzato if tag.startswith('JJ')]
	verbi = [word + "/" + tag for (word, tag) in testotokenizzato if tag.startswith('V')]
	preposizioni = [word + "/" + tag for (word, tag) in testotokenizzato if tag.startswith('IN')]
	avverbi = [word + "/" + tag for (word,tag) in testotokenizzato if tag.startswith('RB')]
	virgola = [word + "/" + tag for (word,tag) in testotokenizzato if tag.startswith(',')]
	punto = [word + "/" + tag for (word,tag) in testotokenizzato if tag.startswith('.')]
	#calcolo le distribuzioni
	rapportosostantivi = 100*(float(len(sostantivi))/len(testotokenizzato))
	rapportoaggettivi = 100*(float(len(aggettivi))/len(testotokenizzato))
	rapportoverbi = 100*(float(len(verbi))/len(testotokenizzato))
	rapportopreposizioni = 100*(float(len(preposizioni))/len(testotokenizzato))
	distribuzionevirgola = (float(len(virgola)))
	distribuzionepunto = (float(len(punto)))
	#calcolo la somma delle distribuzioni di "." e ","
	somma = distribuzionepunto + distribuzionevirgola
	#calcolo la somma definitiva
	sommadef= somma+(float(lunghezza))
	#calcolo il totale
	tot = (float(len(sostantivi))+(len(aggettivi))+(len(verbi))+(len(avverbi)))
	return rapportosostantivi, rapportoaggettivi, rapportoverbi, rapportopreposizioni, sommadef,tot



#Definizione della funzione principale, con 2 valori, i due files
def main(file1, file2):
	#creo due variabili che aprono i due files in input, con codifica in utf-8
	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	#creo due variabili che leggono i files
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#carico il tokenizzatore per la divisione in frasi
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	#tokenizzo le frasi dei due files
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)


 
	#stabilisco il numero dei tokens nei testi (lunghezza) e la liste liste di tokens.
	lunghezza1, testoTokenizzato1 = Tokenizer(frasi1)
	lunghezza2, testoTokenizzato2 = Tokenizer(frasi2)

	#creo due variabili per il calcolo della lunghezza media delle frasi in tokens 
	media1 = AverageRawLength(testoTokenizzato1, frasi1)
	media2 = AverageRawLength(testoTokenizzato2, frasi2)
	
	#creo due variabili per il calcolo della lunghezza media token in termini di caratteri (senza punteggiatura)
	average1 = LunghezzaMediaTokChar(testoTokenizzato1)
	average2 = LunghezzaMediaTokChar(testoTokenizzato2)

	#creo due variabili per il calcolo della lunghezza del vocabolario e la lista delle parole tipo nei testi
	voc1, vocabolario1 = Vocabolario(testoTokenizzato1)
	voc2, vocabolario2 = Vocabolario(testoTokenizzato2)

	#calcolo della distribuzione degli hapax nei testi sui primi 3000 tokens
	hapax1 = distribuzioneHapax(testoTokenizzato1)
	hapax2 = distribuzioneHapax(testoTokenizzato2)

	#calcolo la Type Token Ratio
	ttr1 = TTR(testoTokenizzato1)
	ttr2 = TTR(testoTokenizzato2)

	#applico il POS Tagging ai due testi
	tokensPOStot1 = POSTag(raw1)
	tokensPOStot2 = POSTag(raw2)


	#calcolo la distribuzione in termini percentuali dei due corpora, dopo aver definito le rispettive somme
	sommadef1 = SVAP(tokensPOStot1, lunghezza1) 
	tot1= SVAP(tokensPOStot1,lunghezza1)

	sommadef2 = SVAP(tokensPOStot1, lunghezza2) 
	tot2= SVAP(tokensPOStot1,lunghezza2)    

	#calcolo la densità lessicale dei due files
	rapportosostantivi1, rapportoaggettivi1, rapportopreposizioni1, rapportoverbi1, sommadef1, tot1 = SVAP(tokensPOStot1, lunghezza1)
	rapportosostantivi2, rapportoaggettivi2, rapportopreposizioni2, rapportoverbi2,sommadef2, tot2 = SVAP(tokensPOStot2, lunghezza2)

   
	#Titolo programma 1
	print "Programma 1 - Confrontare i due testi sulla base delle seguenti informazioni statistiche:"
	print "\n"
	#stampo i vari risultati e effettuo i dovuti confronti tra i due files in imput
	print "▶Numero tokens:"
	print "\n"
	print "•Il corpus", file1, "è lungo", lunghezza1, "tokens"
	print "\n"
	print "•Il corpus", file2, "è lungo", lunghezza2, "tokens"
	print "\n"
	if lunghezza1<lunghezza2:
			print "-Il corpus", file2, "è più lungo di", file1
	elif lunghezza1>lunghezza2:
			print "-Il corpus", file1, "è più lungo di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno la stessa lunghezza."
	print "\n"
	print "************************************************"
	print "\n"
	print "▶Lunghezza media dei token in termini di caratteri (escludendo la punteggiatura):"
	print "\n"
	 #mediachar
	print "•La lunghezza media di token in termini di caratteri di", file1, "è di", average1
	print "\n"
	print "•La lunghezza media di token in termini di caratteri di", file2, "è di", average2
	print "\n"
	if average1<average2:
			print "-I tokens di", file2, "sono più lunghi di quelli di", file1
	elif average1>average2:
			print "-I tokens di", file1, "sono più lunghi di quelli di", file2
	else:
			print "-I tokens di ", file1, "e", file2, "hanno lo stesso numero di caratteri."
	print "\n"
	print "************************************************"
	print "\n"
	print "▶Lunghezza media delle frasi in termini di token:"
	print "\n"
	print "•La lunghezza media delle frasi in termini di token di", file1, "è di", media1
	print "\n"
	print "•La lunghezza media delle frasi in termini di token di", file2, "è di", media2
	print "\n"	
	if media1<media2:
			print "-I tokens di", file2, "sono più lunghi di quelli di", file1
	elif media1>media2:
			print "-I tokens di", file1, "sono più lunghi di quelli di", file2
	else:
			print "-I tokens di ", file1, "e", file2, "hanno lo stesso numero di caratteri."
	print "\n"
	print "************************************************"
	print "\n"
	print "▶Grandezza del vocabolario del testo:"
	print "\n"

	print "•Il vocabolario di", file1, "contiene",  voc1, "parole tipo"
	print "\n"
	print "•Il vocabolario di", file2, "contiene",  voc2, "parole tipo"
	print "\n"

	if voc1<voc2:
			print "-Il corpus", file2, "ha il vocabolario più grande di", file1
	elif voc1>voc2:
			print "-Il corpus", file1, "ha il vocabolario più grande di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno il vocabolario della stessa dimensione."
	print "\n"
	print "************************************************"
	print "\n"

	print "▶Distribuzione degli hapax sui primi 3000 token:"
	print "\n"

	print "•La distribuzione degli hapax sui primi 3000 tokens di", file1, "è di", hapax1, "hapax"
	print "\n"
	print "•La distribuzione degli hapax sui primi 3000 tokens di", file2, "è di", hapax2, "hapax"
	print "\n"

	if hapax1<hapax2:
			print "-Il corpus", file2, "ha sui primi 3000 tokens una frequenza degli hapax più alta di", file1
	elif hapax1>hapax2:
			print "-Il corpus", file1, "ha  sui primi 3000 tokens una frequenza dei hapax più alta di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno sui primi 3000 tokens la stessa distribuzione di hapax."
	print "\n"
	print "************************************************"
	print "\n"

	print "▶Ricchezza lessicale calcolata attraverso la Type Token Ratio (TTR) sui primi 3000 token:"
	print "\n"
	print "•La ricchezza lessicale, sui primi 3000 tokens di", file1, "è di:", ttr1
	print "\n"
	print "•La ricchezza lessicale, sui primi 3000 tokens di", file2, "è di:", ttr2
	print "\n"
	
	if ttr1<ttr2:
			print "-Il corpus",file2, "ha sui primi 3000 tokens una ricchezza lessicale più alta rispetto a", file1
	elif ttr1>ttr2:
			print "-Il corpus", file1, "ha sui primi 3000 tokens una ricchezza lessicale più alta rispetto a", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno sui primi 3000 tokens la stessa ricchezza lessicale."

	print "\n"
	print "************************************************"
	print "\n"

	print "▶Distribuzione (in termini percentuali) di Sostantivi, Aggettivi, Verbi e Preposizioni:"
	print "\n"
	print "•La distribuzione in termini di sostantivi, aggettivi, verbi e preposizioni nel file", file1, "è del:", "\n", "-",rapportosostantivi1,"%","per i sostantivi","\n", "-",rapportoaggettivi1, "%","per gli aggettivi","\n", "-",rapportoverbi1, "%","per i verbi","\n", "-",rapportopreposizioni1, "%","per le preposizioni","\n"
	print "\n"	
	print "•La distribuzione in termini di sostantivi, aggettivi, verbi e preposizioni nel file", file2, "è del:", "\n", "-",rapportosostantivi2,"%","per i sostantivi","\n", "-",rapportoaggettivi2, "%","per gli aggettivi","\n", "-",rapportoverbi2, "%","per i verbi","\n", "-",rapportopreposizioni2, "%","per le preposizioni", "\n"
	print "\n"	
	if rapportosostantivi1<rapportosostantivi2:
			print "-Il corpus", file2, "ha una distribuzione in termini di sostantivi maggiore di", file1
	elif rapportosostantivi1>rapportosostantivi2:
			print "-Il corpus", file1, "ha una distribuzione in termini di sostantivi maggiore di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno la stessa distribuzione in termini di sostantivi."

	print "\n"

	if rapportoaggettivi1<rapportoaggettivi2:
			print "-Il corpus", file2, "ha una distribuzione in termini di aggettivi maggiore di", file1
	elif rapportoaggettivi1>rapportoaggettivi2:
			print "-Il corpus", file1, "ha una distribuzione in termini di aggettivi maggiore di", file2
	else:
			print "-I corpora",file1, "e", file2, "hanno la stessa distribuzione in termini di aggettivi."

	print "\n"

	if rapportoverbi1<rapportoverbi2:
			print "-Il corpus",file2, "ha una distribuzione in termini di verbi maggiore di", file1
	elif rapportoverbi1>rapportoverbi2:
			print "-Il corpus", file1, "ha una distribuzione in termini di verbi maggiore di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno la stessa distribuzione in termini di verbi."

	print "\n"

	if rapportopreposizioni1<rapportopreposizioni2:
			print "-Il corpus", file2, "ha una distribuzione in termini di preposizioni maggiore di", file1
	elif rapportopreposizioni1>rapportopreposizioni2:
			print "-Il corpus", file1, "ha una distribuzione in termini di preposizioni maggiore di", file2
	else:
			print "-I corpora", file1, "e", file2, "hanno la stessa distribuzione in termini di preposizioni."

	print "\n"
	print "************************************************"
	print "\n"

	print '▶Densità lessicale, calcolata come il rapporto tra il numero totale di occorrenze nel testo di Sostantivi, Verbi, Avverbi, Aggettivi e il numero totale di parole nel testo (ad esclusione dei segni di punteggiatura marcati con POS "," "."):'
	print "\n"

	print "•La densità lessicale in termini di sostantivi, verbi, avverbi e aggettivi di", file1, "è di", tot1/sommadef1
	print "\n"
	print "•La densità lessicale in termini di sostantivi, verbi, avverbi e aggettivi di", file2, "è di", tot2/sommadef2
	print "\n"
	if tot1/sommadef1<tot2/sommadef2:
			print "-La densità lessicale in termini di sostantivi, verbi, avverbi e aggettivi di", file2, "è maggiore di quella di", file1
	elif tot1/sommadef1>tot2/sommadef2:
			print "-La densità lessicale in termini di sostantivi, verbi, avverbi e aggettivi di", file1, "è maggiore di quella di", file2
	else:
			print "-Le densità lessicali in termini di sostantivi, verbi, avverbi e aggettivi di", file1, "e", file2, "sono uguali."

	"\n"
	print "************************************************"
	"\n"
main(sys.argv[1], sys.argv[2])
