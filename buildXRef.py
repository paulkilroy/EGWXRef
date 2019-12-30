import scrapy
import time
import re
import json

# Need to fix to make the book chapter name 1Corinthians 1 -> 1 Corinthians 1
# further commented XXX BUG below

class QuotesSpider(scrapy.Spider):
	name = "quotes"
	baseURL = "https://m.egwwritings.org/"

	bookMap = {
		"Genesis": "Gen",
		"Exodus": "Exod",
		"Leviticus": "Lev",
		"Numbers": "Num",
		"Deuteronomy": "Deut",
		"Joshua": "Josh",
		"Judges": "Judg",
		"Ruth": "Ruth",
		"1Samuel": "1Sam",
		"2Samuel": "2Sam",
		"1Kings": "1Kgs",
		"2Kings": "2Kgs",
		"1Chronicles": "1Chr",
		"2Chronicles": "2Chr",
		"Ezra": "Ezra",
		"Nehemiah": "Neh",
		"Esther": "Esth",
		"Job": "Job",
		"Psalms": "Ps",
		"Proverbs": "Prov",
		"Ecclesiastes": "Eccl",
		"SongofSolomon": "Song",
		"Isaiah": "Isa",
		"Jeremiah": "Jer",
		"Lamentations": "Lam",
		"Ezekiel": "Ezek",
		"Daniel": "Dan",
		"Hosea": "Hos",
		"Joel": "Joel",
		"Amos": "Amos",
		"Obadiah": "Obad",
		"Jonah": "Jonah",
		"Micah": "Mic",
		"Nahum": "Nah",
		"Habakkuk": "Hab",
		"Zephaniah": "Zeph",
		"Haggai": "Hag",
		"Zechariah": "Zach",
		"Malachi": "Mal",
		"Matthew": "Matt",
		"Mark": "Mark",
		"Luke": "Luke",
		"John": "John",
		"Acts": "Acts",
		"Romans": "Rom",
		"1Corinthians": "1Cor",
		"2Corinthians": "1Cor",
		"Galatians": "Gal",
		"Ephesians": "Eph",
		"Philippians": "Phil",
		"Colossians": "Col",
		"1Thessalonians": "1Thes",
		"2Thessalonians": "2Thes",
		"1Timothy": "1Tim",
		"2Timothy": "2Tim",
		"Titus": "Titus",
		"Philemon": "Phlm",
		"Hebrews": "Heb",
		"James": "Jas",
		"1Peter": "1Pet",
		"2Peter": "2Pet",
		"1John": "1John",
		"2John": "2John",
		"3John": "3John",
		"Jude": "Jude",
		"Revelation": "Rev",
	}


	def start_requests(self):
		#with open('xref.js', 'w') as f:
		#	f.write('var crossref = {\n')

		#url = 'https://m.egwwritings.org/en/book/2778.1' #Genesis 1
		#startId = 3
		url = 'https://m.egwwritings.org/en/book/2778.13187#13187' #Genesis 1
		startId = 13187
		yield scrapy.Request(url=url, callback=self.parse, meta={'startId': startId})

	def parse(self, response):
		startId = int(response.meta['startId'])

		print("StartId:" +str(startId))
		if not bool(re.match( '^\w+\W+\d+$', response.selector.xpath('//*[@id="'+str(startId)+'"]/span//text()').get())):
			startId += 1

		print("NEW StartId:" +str(startId))
		bookAndChapter = response.selector.xpath('//*[@id="'+str(startId)+'"]/span/text()').get()
		# XXX BUG need to fix "1Samuel 1"  into "1 Samuel 1" etc..
		# XXX BUG basically if the first character is a number, insert a space after it
		if not bookAndChapter is None:
			print("bookAndChapter:", bookAndChapter)
			book, chapter = re.split('\W+', bookAndChapter)
			print("book:",book,"#")
			print("chapter: ", chapter)

		id = startId + 1
		while True:
			idText = response.selector.xpath('//*[@id="'+str(id)+'"]/span//text()').get()
			# Either this is a bunch of book names and pages or a list of chapters in the current book to xref
			print("idText", idText )
			if idText is None or re.match("^[\s\d\-\,]+$",idText):
				break;
			else:
				id = id + 1

		print("id:", id)
		xrefs = {}
		xrefs[bookAndChapter] = {}
		#xrefs[bookAndChapter].append([]) # Add this chapter to the book, assume they are all in order
		while True:
			spans = response.selector.xpath('//*[@id="'+str(id)+'"]/span')
			if len(spans) == 0:
				break

			verseList = spans[0].xpath('./text()').get() # comma and dash separated list of verses
			print("id:", id, " verseList:", verseList)

			verseList = verseList.replace(' ', '')
			verseArray = verseList.split(',')
			verseInts = []
			for verseList in verseArray:
				if "-" in verseList:
					verseRange = verseList.split('-')
					verseInts += range(int(verseRange[0]), int(verseRange[1]) + 1)
				else:
					verseInts.append(int(verseList))

			print("id:", id, " verseInts:", verseInts)
			#print(type(verseList))
			for verseInt in verseInts:
				verse = str(verseInt)
				spans = response.selector.xpath('//*[@id="'+str(id+1)+'"]/span')
				if len(spans) == 0:
					break

				egw = ""
				for a in spans[0].xpath('.//a'):
					xref = {}
					text = a.xpath('./text()').get()
					xr = text.split()
					if len(xr) == 1:
						page = xr[0]
					else:
						egw = xr[0]
						page = xr[1]
					href = a.xpath('./@href').get()
					print("book:"+book+"verse:", verse, "egw:",egw, "page:", page, "href:", href)
					xref['name']=text
					xref['link']=href
					bgVerse = self.bookMap[book] + "-" + chapter + "-" + verse;
					#if len(xrefs[book][0]) < int(verse):
					if bgVerse not in xrefs[bookAndChapter]:
						xrefs[bookAndChapter][bgVerse] = [xref]
					else:
						xrefs[bookAndChapter][bgVerse].append(xref)
					#print("xref:", xrefs[book]);
			id += 2

		if not bookAndChapter is None:
			with open('xref.js', 'a') as f:
				# if id is low, we're in genesis 1
				if id > 100:
					print("writing comma")
					f.write(',')
				f.write('"'+bookAndChapter+'": ')
				f.write(json.dumps(xrefs[bookAndChapter],indent=2))
				f.write('\n')

		#Go On to next chapter
		nextLink = response.selector.xpath("//a[text()='Next']/@href").get()
		print("nextLink:", nextLink)
		t = nextLink.split('.')
		if( len(t) > 1 ):
			startId = int( t[1].split("/")[0] )
			time.sleep(2.34)
			yield scrapy.Request(url="https://m.egwwritings.org/"+nextLink, callback=self.parse, meta={'startId': startId})
		else:
			print("Nothing more to do... exiting")
			with open('xref.js', 'a') as f:
				f.write("}\n")
