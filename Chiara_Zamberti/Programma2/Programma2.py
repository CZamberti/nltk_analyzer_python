#-*- coding: utf-8 -*- 
import sys
import codecs
import nltk
import re
import math
from nltk import sent_tokenize, word_tokenize, pos_tag, FreqDist, trigrams, bigrams

#Definisco la funzione che tokenizza il testo, crea una lista pulita di tokens (senza punteggiatura), assegna il POS, trova le NE PERSON e le GPE)
def TokenizzazioneEPOS(frasi):
	#definisco le liste (vuote)
	tokensTOT = []
	tokensTOTPOS= []
	CleanTokList = []
	#divido le frasi in tokens
	for frase in frasi:
		tokens = nltk.word_tokenize(frase)
		tokensTOT = tokensTOT+tokens
		#calcolo il numero totale di tokens nel testo
		TOTlen = len(tokensTOT)
		#scorro la lista tokensTOT e vedo se il token non è un segno di punteggiatura
		for tok in tokens:
			if not (tok in [".", ",", ";", ":", "!", "?", "'", '"']):
				#inserisco come ultimo elemento della lista il token trovato (che non è segno di punteggiatura)
				CleanTokList.append(tok)
				#assegno la POS ad ogni token e creo la lista tokensTOTPOS
		tokensTOTPOS = nltk.pos_tag(tokensTOT)
		#analizzo la categoria delle NE del token
		analisi=nltk.ne_chunk(tokensTOTPOS)
		
#creo due liste vuote per raggruppare tutti i tokens con NE PERSON e GPE
	NEPERSON=[]
	NEGPE=[]
#scorro i nodi in analisi (secondo la struttura ad albero)
	for nodo in analisi:
		NE=''
				#controllo se nodo è un nodo intermedio o una foglia
		if hasattr(nodo, 'node'):
				#trovo ogni nodo con PERSON
			if nodo.node in "PERSON":
				#scorro le foglie del nodo selezionato, per ottenere le liste delle foglie del nodo intermedio
				for partNE in nodo.leaves():
					NE=NE+' '+partNE[0]
				NEPERSON.append(NE)
				     
						#trovo ogni nodo con GPE
			elif nodo.node in "GPE":
				for partNE in nodo.leaves():
					NE=NE+' '+partNE[0]
				NEGPE.append(NE)

	return tokensTOT, tokensTOTPOS, CleanTokList, TOTlen, NEPERSON, NEGPE

#Definisco la funzione che trova i 20 tokens più frequenti (senza punteggiatura)
def VentiTokensFrequenti(CleanTokList):
	distribuzioneTokens=CleanTokList.keys()
	#assegno la frequenza ad ogni token, in un range da 0 a 20
	for token in distribuzioneTokens[0:20]:
		#stampo il token e la frequenza relativa
		print token, "----> con frequenza di:", CleanTokList[token]

#Funzione che prende in input i bigrammi e restituisce una lista con le POS
def POS (testoAnalizzatoPOS):
	#creo una lista vuota
	listaPOS = []
	#scorro i bigrammi nel testo annotato
	for bigramma in testoAnalizzatoPOS:
		#aggiungo i bigrammi a listaPOS
		listaPOS.append(bigramma[1])
		#restituisco la listaPOS
	return listaPOS

#Definisco la funzione che calcola i 10 POS più frequenti
def DistribuzionePOS(listaPOS):
	#seleziono le chiavi di listaPOS
	ListaDistrPOS=listaPOS.keys()
	#scorro all'intero della lista, in un range da 0 a 10
	for i in ListaDistrPOS[0:10]:
		#stampo il token e il POS con la frequenza 
		print i, "----> con frequenza di:", listaPOS[i]

#Definizione della funzione che estrae i bigrammi dal testo annotato e restituisce una lista di bigrammi
def EstraiBigrammi(tokensTOTPOS):
	#creo una lista vuota
	Bigrammi=[]
	#divido il testo in bigrammi con la funzione "bigrams" di nltk
	BigrammiPOS = list(bigrams(tokensTOTPOS))
	#scorro ogni bigramma in BigrammiPOS
	for bigramma in BigrammiPOS:
		#seleziono i bigrammi contenenti le NE riportate e con frequenza maggiore di 3 e li aggiungo alla lista se soddifano le condizioni
		if ((bigramma[0][1]in["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NPS"]) and (bigramma [1][1]in["JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NPS"]) and (tokensTOTPOS.count(bigramma[0])>3) and (tokensTOTPOS.count(bigramma[1])>3)):
			Bigrammi.append(bigramma)
	#restituisco i bigrammi
	return Bigrammi


#Funzione che estrae i trigrammi dal testo annotato e restituisce una lista di trigrammi (di token e POS)
def EstraiTrigrammi(tokensTOTPOS):
	#creo una lista vuota
	Trigrammi = []
#divido il testo in trigrammi con la funzione trigrams di nltk
	TrigrammiPOS = list(trigrams(tokensTOTPOS))
	#scorro ogni trigramma in TrigrammiPOS
	for trigramma in TrigrammiPOS:
		#elimino la punteggiatura dalla lista di trigrammi e aggiungo il trigramma che soddisfano le condizioni alla lista.
		if not ((trigramma[0][1] in [".", ",", ";", ":", "!", "?", "'", '"', '"', "CC", "IN"]) or (trigramma[1][1] in [".", ",", ";", ":", "!", "?", "'", '"', '"', "CC", "IN"]) or (trigramma[2][1] in [".", ",", ";", ":", "!", "?", "'", '"', '"', "CC", "IN"])):
			Trigrammi.append(trigramma)
			#restituisco i trigrammi
	return Trigrammi



def Dizionario(Trigrammi, Bigrammi, tokensTOTPOS, TOTlen, NEPERSON, NEGPE):
	#inizializzo i dizionari
	DizTrigrammi = {}
	DizBigrammi = {}
	DizionarioProbCondizionata = {}
	DizionarioLMI = {}
	DizionarioGPE = {}
	DizionarioPERSON = {}
	DizionarioBigrammi = {}
	#definisco le liste
	ListaTrigrammi = set(Trigrammi)
	ListaBigrammi = set(Bigrammi)
	TypeNEPERSON = set(NEPERSON)
	TypeNEGPE = set(NEGPE)
	#creo un ciclo che scorre la lista trigrammi e ne calcola la frequenza 
	for trigramma in ListaTrigrammi:
		FreqTrigrammi=Trigrammi.count(trigramma)
		DizTrigrammi[trigramma]=FreqTrigrammi
	for bigramma in Bigrammi:
		freq=Bigrammi.count(bigramma)
		DizionarioBigrammi[bigramma]=freq
	#creo un ciclo che scorre la lista bigrammi e ne calcola la frequenza
	for bigramma in ListaBigrammi:
		#definisco le frequenze delle parole nei bigrammi
		frequenzaAB=Bigrammi.count(bigramma)
		frequenzaA=tokensTOTPOS.count(bigramma[0])*1.0
		frequenzaB=tokensTOTPOS.count(bigramma[1])*1.0
		#calcolo la probabilità condizionata
		ProbabilitaCondizionata=frequenzaAB/frequenzaA
		#calcolo la Local Mutual Information
		LMI=frequenzaAB*math.log((frequenzaAB*TOTlen*1.0)/(frequenzaA*frequenzaB*1.0), 2)
		#definisco i dizionari
		DizionarioProbCondizionata[bigramma]=ProbabilitaCondizionata
		DizionarioLMI[bigramma]=LMI
		#creo un ciclo che scorre le NE e conta le occorrenze delle NE di tipo PERSON
	for tok in TypeNEPERSON:
		frequenza=NEPERSON.count(tok)
		DizionarioPERSON[tok]=frequenza

		#creo un ciclo che scorre le NE e conta le occorrenze delle NE di tipo GPE	
	for tok in TypeNEGPE:
		frequenza=NEGPE.count(tok)
		DizionarioGPE[tok]=frequenza
		#restituisco i dizionari
	return DizionarioBigrammi, DizTrigrammi, DizionarioProbCondizionata, DizionarioLMI, DizionarioPERSON, DizionarioGPE


#Definisco una funzione che, attraverso un modello di Markov di ordine I, estrae la frase con probabilità più alta, lunga almeno 10 token e con frequenza maggiore di 3
def Markov(frasi, lunghezza,tokensTOT, bigrammiTOT):
#inizializzo le variabili
	contaparole=0
	probigMAX=0
	fraseMAX=""
	#creo un ciclo che scorre le frasi
	for frase in frasi:
		#creo un contatore, che si resetta per ogni frase
		contaparole=0
		#tokenizzazione delle frasi
		tokens=nltk.word_tokenize(frase)
		#creazione delle tuple di bigrammi
		bigrammi=bigrams(tokens)
		#calcolo la probabilità del primo elemento del bigramma
		markov=(tokensTOT.count(tokens[0])*1.0)/(lunghezza*1.0)
		#controllo se il numero dei tokens della frase è maggiore di 9
		if len(tokens)>9:
			#scorro i tokens nella lista tokens
			for tok in tokens:
				bigramma=[]
				conteggioTok=tokensTOT.count(tok)
				#controllo se la frequenza del token è maggiore di 3
				if conteggioTok>3:
					contaparole+=1
					#imposto il contatore uguale alla lunghezza dei tokens
			if contaparole==len(tokens):
				#creo un ciclo che scorre i bigrammi della frase nella lista
				for big in bigramma:
					probigramma=(bigrammiTOT.count(big)*1.0)/(tokensTOT.count(big[0])*1.0)
					#calcolo la probabilità di markov
					markov=probigramma*markov
					#controllo se la probabilità è la massima
				if markov>probigMAX:
					#assegno a "frase" la frase con probabilità massima
					fraseMAX=frase
					#imposto la probabilità massima alla probabilità di markov
					probigMAX=markov
	return fraseMAX, probigMAX

#ordino i valori di una lista di tuple, in ordine decrescente per valore (rispetto al secondo elemento della tupla).
def Sort(dizionario):
	return sorted(dizionario.items(), key=lambda x: x[1], reverse=True)


#Definizione della funzione principale, con 2 valori, i due files
def main(file1, file2):
	#leggo i file in input (con codifica UTF-8)
	fileInput1 = codecs.open(file1, "r", "utf-8")
	fileInput2 = codecs.open(file2, "r", "utf-8")
	#leggo i testi in input
	raw1 = fileInput1.read()
	raw2 = fileInput2.read()
	#importo il tokenizzatore NLTK
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	#divido i corpora in frasi
	frasi1 = sent_tokenizer.tokenize(raw1)
	frasi2 = sent_tokenizer.tokenize(raw2)
	#applico la tokenizzazione e l'analisi POS el testo diviso in frasi
	testoTokenizzato1, tokensTOTPOS1, CleanTokList1, TOTlen1, NEPERSON1, NEGPE1 = TokenizzazioneEPOS(frasi1)
	testoTokenizzato2, tokensTOTPOS2, CleanTokList2, TOTlen2, NEPERSON2, NEGPE2 = TokenizzazioneEPOS(frasi2)
	#definisco i trigrammi per i due files
	Trigrammi1 = EstraiTrigrammi(tokensTOTPOS1)
	Trigrammi2 = EstraiTrigrammi(tokensTOTPOS2)
	#definisco i bigrammi per i due files
	Bigrammi1 = EstraiBigrammi(tokensTOTPOS1)
	Bigrammi2 = EstraiBigrammi(tokensTOTPOS2)


	#definisco i dizionari dei bigrammi, dei trigrammi, della probabiltà condizionata, della LMI e delle NE PERSON GPE
	DizionarioBigrammi1, DizTrigrammi1, DizionarioProbCondizionata1, DizionarioLMI1, DizionarioPERSON1, DizionarioGPE1 = Dizionario(Trigrammi1, Bigrammi1, tokensTOTPOS1, TOTlen1, NEPERSON1, NEGPE1)
	DizionarioBigrammi2, DizTrigrammi2, DizionarioProbCondizionata2, DizionarioLMI2, DizionarioPERSON2, DizionarioGPE2 = Dizionario(Trigrammi2, Bigrammi2, tokensTOTPOS2, TOTlen2, NEPERSON2, NEGPE2)
 
	#definisco le liste distribuzione pos (com il FreqDist)
	ListaDistrPOS1=nltk.FreqDist(tokensTOTPOS1)
	ListaDistrPOS2=nltk.FreqDist(tokensTOTPOS2)

	#definisco le liste di 20 tokens più frequenti
	VentiTokensFrequenti1=nltk.FreqDist(CleanTokList1)
	VentiTokensFrequenti2=nltk.FreqDist(CleanTokList2)
	#definisco le liste di bigrammi sul testo tokenizzato
	BigrammiTok1=list(bigrams(testoTokenizzato1))
	BigrammiTok2=list(bigrams(testoTokenizzato2))
	#restituisco la frase più frequente e la relativa probabilità di Markov
	Markov1, probabilitamarkov1=Markov(frasi1, TOTlen1, testoTokenizzato1, BigrammiTok1)
	Markov2, probabilitamarkov2=Markov(frasi2, TOTlen2, testoTokenizzato2, BigrammiTok2)


	#titolo programma 2

	print "Programma 2 - Per ognuno dei due corpora il programma deve estrarre le seguenti informazioni:\n"

	print "•Estrarre ed ordinare in ordine di frequenza decrescente, indicando anche la relativa frequenza:"
	print "\n"
	print "-I 20 token più frequenti escludendo la punteggiatura di", file1, "sono:\n", VentiTokensFrequenti(VentiTokensFrequenti1)
	print "\n"
	print "-I 20 token più frequenti escludendo la punteggiatura di", file2, "sono:\n", VentiTokensFrequenti(VentiTokensFrequenti2)
	print "\n"
	print "------------------------------------"
	print "\n"
	print "-Le 10 PoS più frequenti (Part-of-Speech) di", file1, "sono:\n", DistribuzionePOS(ListaDistrPOS1)
	print "\n"
	print "-Le 10 PoS più frequenti (Part-of-Speech) di", file2, "sono:\n",DistribuzionePOS(ListaDistrPOS2)
	print "\n"
	print "------------------------------------"
	print "\n"
	print "-I 10 trigrammi di PoS più frequenti che non contengono punteggiatura e congiunzioni di", file1,	"sono:\n"
	TupleDizTrigrammi1=Sort(DizTrigrammi1)
	for elemento in TupleDizTrigrammi1[0:10]:
		print elemento[0], "con frequenza di:", elemento[1], "\n"
	print "\n"

	print "-I 10 trigrammi di PoS più frequenti che non contengono punteggiatura e congiunzioni di", file2, "sono:","\n", 
	TupleDizTrigrammi2=Sort(DizTrigrammi2)
	for elemento in TupleDizTrigrammi2[0:10]:
		print elemento[0], "con frequenza di:", elemento[1], "\n"

	print "************************************"
	print "\n"
	print "•Estrarre ed ordinare i 20 bigrammi composti solo di Aggettivi e Sostantivi (dove ogni token deve avere una frequenza maggiore di 3):"
	print "\n"

	print "-I 20 bigrammi con frequenza massima di", file1, "sono (contando la frequenza dei bigrammi e dei token che lo compongono):\n"
	bigrammifreqmax1=Sort(DizionarioBigrammi1)
	for elemento in bigrammifreqmax1[0:20]:
		print elemento[0], "con frequenza di:", elemento[1], elemento[0][0], (tokensTOTPOS1.count(elemento[0][0])), elemento[0][1], (tokensTOTPOS1.count(elemento[0][1])), "\n"
	print "\n"

	print "-I 20 bigrammi con frequenza massima di", file2, "sono (contando la frequenza dei bigrammi e dei token che lo compongono):","\n"
	bigrammifreqmax2=Sort(DizionarioBigrammi2)
	for elemento in bigrammifreqmax2[0:20]:
		print elemento[0], "con frequenza di:", elemento[1], elemento[0][0], (tokensTOTPOS2.count(elemento[0][0])), elemento[0][1], (tokensTOTPOS2.count(elemento[0][1])), "\n"
	print "\n"
	print "------------------------------------"
	print "\n"
	print "-La probabilità condizionata massima di", file1, "è di:"
	TupleDizionarioBigrammi1=Sort(DizionarioProbCondizionata1)    
	for elemento in TupleDizionarioBigrammi1[0:20]:
		print elemento[0], "con probabilità di:", elemento[1]
	print "\n"

	print "-La probabilità condizionata massima di", file2, "è di:"
	TupleDizionarioBigrammi2=Sort(DizionarioProbCondizionata2)    
	for elemento in TupleDizionarioBigrammi2[0:20]:
		print elemento[0], "con probabilità di:", elemento[1]
	print "\n"
	print "------------------------------------"
	print "\n"
	print "-La forza associativa massima (calcolata in termini di Local Mutual Information) di", file1, "è:"
	ListatupleDizionarioLMI1=Sort(DizionarioLMI1)
	for elemento in ListatupleDizionarioLMI1[0:20]:
		print elemento[0], "con forza associativa di:", elemento[1]
	print "\n"
	print "-La forza associativa massima (calcolata in termini di Local Mutual Information) di", file2, "è:"
	ListatupleDizionarioLMI2=Sort(DizionarioLMI2)
	for elemento in ListatupleDizionarioLMI2[0:20]:
		print elemento[0], "con forza associativa di:", elemento[1]
	print "\n"
	print "************************************"
	print "\n"
	print "•Trovare la frase con probabilità più alta. La frase deve essere lunga almeno 10 token e ogni token deve avere una frequenza maggiore di 3. La probabilità deve essere calcolata attraverso un modello di Markov di ordine 1 che sfrutta statistiche estratte dal corpus che contiene la frase."
	print "\n"
	print "-La frase con probabilità più alta di", file1,"è:\n", Markov1, "con probabilità di:", probabilitamarkov1
	print "-La frase con probabilità più alta di", file2, "è:\n", Markov2, "con probabilità di:", probabilitamarkov2
	print "\n"
	print "************************************"
	print "•Estrarre, dopo aver individuato e classificato le Entità Nominate (NE) presenti nel testo:"
	print "\n"
	print "-I 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza di:", file1, "sono:"
	ListatupleDizionarioPERSON1=Sort(DizionarioPERSON1)
	for elemento in ListatupleDizionarioPERSON1[0:20]:
		print elemento[0], "con frequenza di:", elemento[1]
	print "\n"
	print "-I 20 nomi propri di persona più frequenti (tipi), ordinati per frequenza di:", file2, "sono:"
	ListatupleDizionarioPERSON2=Sort(DizionarioPERSON2)
	for elemento in ListatupleDizionarioPERSON2[0:20]:
		print elemento[0], "con frequenza di:", elemento[1]
	print "\n"
	print "------------------------------------"
	print "\n"
	print "-I 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza di:", file1, "sono:"
	ListatupleDizionarioGPE1=Sort(DizionarioGPE1)
	for elemento in ListatupleDizionarioGPE1[0:20]:
		print elemento[0], "con frequenza di:", elemento[1]
	print "\n"
	print "-I 20 nomi propri di luogo più frequenti (tipi), ordinati per frequenza di:", file2, "sono:"
	ListatupleDizionarioGPE2=Sort(DizionarioGPE2)
	for elemento in ListatupleDizionarioGPE2[0:20]:
		print elemento[0], "con frequenza di:", elemento[1]



main(sys.argv[1], sys.argv[2])
