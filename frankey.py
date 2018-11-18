# -*- coding: utf-8 -*-

from LineAPI.linepy import *
from gtts import gTTS
from bs4 import BeautifulSoup
from datetime import datetime
from googletrans import Translator
import ast, codecs, json, os, pytz, re, random, requests, sys, time, urllib.parse

client = LINE()
#client = LINE("AuthToken")
clientMid = client.profile.mid
clientStart = time.time()
clientPoll = OEPoll(client)

welcome = []

languageOpen = codecs.open("language.json","r","utf-8")
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("setting.json","r","utf-8")
unsendOpen = codecs.open("unsend.json","r","utf-8")

language = json.load(languageOpen)
read = json.load(readOpen)
settings = json.load(settingsOpen)
unsend = json.load(unsendOpen)

def restartBot():
	print ("[ INFO ] BOT RESETTED")
	python = sys.executable
	os.execl(python, python, *sys.argv)

def logError(text):
    client.log("[ ERROR ] {}".format(str(text)))
    tz = pytz.timezone("Asia/Makassar")
    timeNow = datetime.now(tz=tz)
    timeHours = datetime.strftime(timeNow,"(%H:%M)")
    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    inihari = datetime.now(tz=tz)
    hr = inihari.strftime('%A')
    bln = inihari.strftime('%m')
    for i in range(len(day)):
        if hr == day[i]: hasil = hari[i]
    for k in range(0, len(bulan)):
        if bln == str(k): bln = bulan[k-1]
    time = "{}, {} - {} - {} | {}".format(str(hasil), str(inihari.strftime('%d')), str(bln), str(inihari.strftime('%Y')), str(inihari.strftime('%H:%M:%S')))
    with open("errorLog.txt","a") as error:
        error.write("\n[{}] {}".format(str(time), text))

def timeChange(secs):
	mins, secs = divmod(secs,60)
	hours, mins = divmod(mins,60)
	days, hours = divmod(hours,24)
	weeks, days = divmod(days,7)
	months, weeks = divmod(weeks,4)
	text = ""
	if months != 0: text += "%02d Bulan" % (months)
	if weeks != 0: text += " %02d Minggu" % (weeks)
	if days != 0: text += " %02d Hari" % (days)
	if hours !=  0: text +=  " %02d Jam" % (hours)
	if mins != 0: text += " %02d Menit" % (mins)
	if secs != 0: text += " %02d Detik" % (secs)
	if text[0] == " ":
		text = text[1:]
	return text

def welcomeMembers(to, mid):
    try:
        arrData = ""
        textx = "? Auto Welcome ?\nHallo ".format(str(len(mid)))
        arr = []
        no = 1
        num = 2
        for i in mid:
            ginfo = client.getGroup(to)
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention+settings["welcome"]+" Di "+str(ginfo.name)
            if no < len(mid):
                no += 1
                textx += "%i " % (num)
                num=(num+1)
            else:
                try:
                    no = "\n?ÄÄ[ {} ]".format(str(client.getGroup(to).name))
                except:
                    no = "\n?ÄÄ[ Success ]"
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def leaveMembers(to, mid):
    try:
        arrData = ""
        textx = "? Respon Leave ?\nBaper Ya Kak ".format(str(len(mid)))
        arr = []
        no = 1
        num = 2
        for i in mid:
            ginfo = client.getGroup(to)
            mention = "@x\n"
            slen = str(len(textx))
            elen = str(len(textx) + len(mention) - 1)
            arrData = {'S':slen, 'E':elen, 'M':i}
            arr.append(arrData)
            textx += mention+settings["leave"]
            if no < len(mid):
                no += 1
                textx += "%i " % (num)
                num=(num+1)
            else:
                try:
                    no = "\n?ÄÄ[ {} ]".format(str(client.getGroup(to).name))
                except:
                    no = "\n?ÄÄ[ Success ]"
        client.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
    except Exception as error:
        client.sendMessage(to, "[ INFO ] Error :\n" + str(error))

def command(text):
	pesan = text.lower()
	if settings["setKey"] == True:
		if pesan.startswith(settings["keyCommand"]):
			cmd = pesan.replace(settings["keyCommand"],"")
		else:
			cmd = "Undefined command"
	else:
		cmd = text.lower()
	return cmd

def backupData():
	try:
		backup = read
		f = codecs.open('read.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = settings
		f = codecs.open('setting.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		backup = unsend
		f = codecs.open('unsend.json','w','utf-8')
		json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
		return True
	except Exception as error:
		logError(error)
		return False

def menuHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuHelp =	"?ÄÄ[ Help Message ]" + "\n" + \
				"³ " + key + "Help" + "\n" + \
                                "³ " + key + "Help Status" + "\n" + \
                                "³ " + key + "Help settings" + "\n" + \
                                "³ " + key + "Help self" + "\n" + \
                                "³ " + key + "Help group" + "\n" + \
                                "³ " + key + "Help special" + "\n" + \
                                "³ " + key + "Help media" + "\n" + \
                                "³ " + key + "Translate" + "\n" + \
				"³ " + key + "TextToSpeech" + "\n" + \
				"?ÄÄ[ Frakenstien ]"
	return menuHelp

def menuStatusHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuStatusHelp =	"?ÄÄ[ Status Command ]" + "\n" + \
				"³ MyKey" + "\n" + \
				"³ " + key + "ÍÍ¡" + "\n" + \
				"³ " + key + "ÃÕ" + "\n" + \
				"³ " + key + "ÃÑ¹" + "\n" + \
				"³ " + key + "àª¤" + "\n" + \
				"³ " + key + "stt" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuStatusHelp

def menuSettingsHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuSettingsHelp =	"?ÄÄ[ Settings Command ]" + "\n" + \
				"³ SetKey ?On/Off?" + "\n" + \
                                "³ " + key + "Welcome ?On/Off?" + "\n" + \
				"³ " + key + "AutoAdd ?On/Off?" + "\n" + \
				"³ " + key + "AutoJoin ?On/Off?" + "\n" + \
				"³ " + key + "AutoJoinTicket ?On/Off?" + "\n" + \
				"³ " + key + "AutoRead ?On/Off?" + "\n" + \
				"³ " + key + "AutoRespon ?On/Off?" + "\n" + \
				"³ " + key + "CheckContact ?On/Off?" + "\n" + \
				"³ " + key + "CheckPost ?On/Off?" + "\n" + \
				"³ " + key + "CheckSticker ?On/Off?" + "\n" + \
				"³ " + key + "DetectUnsend ?On/Off?" + "\n" + \
				"³ " + key + "SetKey: ?text?" + "\n" + \
				"³ " + key + "SetAutoAddMessage: ?text?" + "\n" + \
				"³ " + key + "SetAutoResponMessage: ?text?" + "\n" + \
				"³ " + key + "SetAutoJoinMessage: ?Text?" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuSettingsHelp

def menuSelfHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuSelfHelp =	        "?ÄÄ[ Self Command ]" + "\n" + \
				"³ " + key + "ChangeName: ?Text?" + "\n" + \
				"³ " + key + "ChangeBio: ?Text?" + "\n" + \
				"³ " + key + "Me" + "\n" + \
				"³ " + key + "MyMid" + "\n" + \
				"³ " + key + "MyName" + "\n" + \
				"³ " + key + "MyBio" + "\n" + \
				"³ " + key + "MyPicture" + "\n" + \
				"³ " + key + "MyVideoProfile" + "\n" + \
				"³ " + key + "MyCover" + "\n" + \
				"³ " + key + "MyProfile" + "\n" + \
				"³ " + key + "GetMid @Mention" + "\n" + \
				"³ " + key + "GetName @Mention" + "\n" + \
				"³ " + key + "GetBio @Mention" + "\n" + \
				"³ " + key + "GetPicture @Mention" + "\n" + \
				"³ " + key + "GetVideoProfile @Mention" + "\n" + \
				"³ " + key + "GetCover @Mention" + "\n" + \
				"³ " + key + "CloneProfile @Mention" + "\n" + \
				"³ " + key + "RestoreProfile" + "\n" + \
				"³ " + key + "BackupProfile" + "\n" + \
				"³ " + key + "FriendList" + "\n" + \
				"³ " + key + "FriendInfo ?Number?" + "\n" + \
				"³ " + key + "BlockList" + "\n" + \
				"³ " + key + "FriendBroadcast" + "\n" + \
				"³ " + key + "ChangePictureProfile" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuSelfHelp

def menuGroupHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuGroupHelp =	        "?ÄÄ[ Group Command ]" + "\n" + \
				"³ " + key + "ChangeGroupName: ?Text?" + "\n" + \
				"³ " + key + "GroupCreator" + "\n" + \
				"³ " + key + "GroupID" + "\n" + \
				"³ " + key + "GroupName" + "\n" + \
				"³ " + key + "GroupPicture" + "\n" + \
				"³ " + key + "OpenQR" + "\n" + \
				"³ " + key + "CloseQR" + "\n" + \
				"³ " + key + "GroupList" + "\n" + \
				"³ " + key + "MemberList" + "\n" + \
				"³ " + key + "PendingList" + "\n" + \
				"³ " + key + "GroupInfo" + "\n" + \
				"³ " + key + "GroupBroadcast: ?Text?" + "\n" + \
				"³ " + key + "ChangeGroupPicture" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuGroupHelp

def menuSpecialHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuSpecialHelp =	"?ÄÄ[ Special Command ]" + "\n" + \
				"³ " + key + "Mimic ?On/Off?" + "\n" + \
				"³ " + key + "MimicList" + "\n" + \
				"³ " + key + "MimicAdd @Mention" + "\n" + \
				"³ " + key + "MimicDel @Mention" + "\n" + \
				"³ " + key + "Mentionall" + "\n" + \
				"³ " + key + "Lurking ?On/Off?" + "\n" + \
				"³ " + key + "Lurking" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuSpecialHelp


def menuMediaHelp():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuMediaHelp =   	"?ÄÄ[ Media Command ]" + "\n" + \
				"³ " + key + "InstaInfo ?Username?" + "\n" + \
				"³ " + key + "InstaStory ?Username?" + "\n" + \
				"³ " + key + "Quotes" + "\n" + \
				"³ " + key + "SearchImage ?Search?" + "\n" + \
				"³ " + key + "SearchMusic ?Search?" + "\n" + \
				"³ " + key + "SearchLyric ?Search?" + "\n" + \
				"³ " + key + "SearchYoutube ?Search?" + "\n" + \
				"?ÄÄ[ Frankenstien ]"
	return menuMediaHelp

def menuTextToSpeech():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTextToSpeech =	"?ÄÄ[ Text To Speech ]" + "\n" + \
						"³ " + key + "af : Afrikaans" + "\n" + \
						"³ " + key + "sq : Albanian" + "\n" + \
						"³ " + key + "ar : Arabic" + "\n" + \
						"³ " + key + "hy : Armenian" + "\n" + \
						"³ " + key + "bn : Bengali" + "\n" + \
						"³ " + key + "ca : Catalan" + "\n" + \
						"³ " + key + "zh : Chinese" + "\n" + \
						"³ " + key + "zh-cn : Chinese (Mandarin/China)" + "\n" + \
						"³ " + key + "zh-tw : Chinese (Mandarin/Taiwan)" + "\n" + \
						"³ " + key + "zh-yue : Chinese (Cantonese)" + "\n" + \
						"³ " + key + "hr : Croatian" + "\n" + \
						"³ " + key + "cs : Czech" + "\n" + \
						"³ " + key + "da : Danish" + "\n" + \
						"³ " + key + "nl : Dutch" + "\n" + \
						"³ " + key + "en : English" + "\n" + \
						"³ " + key + "en-au : English (Australia)" + "\n" + \
						"³ " + key + "en-uk : English (United Kingdom)" + "\n" + \
						"³ " + key + "en-us : English (United States)" + "\n" + \
						"³ " + key + "eo : Esperanto" + "\n" + \
						"³ " + key + "fi : Finnish" + "\n" + \
						"³ " + key + "fr : French" + "\n" + \
						"³ " + key + "de : German" + "\n" + \
						"³ " + key + "el : Greek" + "\n" + \
						"³ " + key + "hi : Hindi" + "\n" + \
						"³ " + key + "hu : Hungarian" + "\n" + \
						"³ " + key + "is : Icelandic" + "\n" + \
						"³ " + key + "id : Indonesian" + "\n" + \
						"³ " + key + "it : Italian" + "\n" + \
						"³ " + key + "ja : Japanese" + "\n" + \
						"³ " + key + "km : Khmer (Cambodian)" + "\n" + \
						"³ " + key + "ko : Korean" + "\n" + \
						"³ " + key + "la : Latin" + "\n" + \
						"³ " + key + "lv : Latvian" + "\n" + \
						"³ " + key + "mk : Macedonian" + "\n" + \
						"³ " + key + "no : Norwegian" + "\n" + \
						"³ " + key + "pl : Polish" + "\n" + \
						"³ " + key + "pt : Portuguese" + "\n" + \
						"³ " + key + "ro : Romanian" + "\n" + \
						"³ " + key + "ru : Russian" + "\n" + \
						"³ " + key + "sr : Serbian" + "\n" + \
						"³ " + key + "si : Sinhala" + "\n" + \
						"³ " + key + "sk : Slovak" + "\n" + \
						"³ " + key + "es : Spanish" + "\n" + \
						"³ " + key + "es-es : Spanish (Spain)" + "\n" + \
						"³ " + key + "es-us : Spanish (United States)" + "\n" + \
						"³ " + key + "sw : Swahili" + "\n" + \
						"³ " + key + "sv : Swedish" + "\n" + \
						"³ " + key + "ta : Tamil" + "\n" + \
						"³ " + key + "th : Thai" + "\n" + \
						"³ " + key + "tr : Turkish" + "\n" + \
						"³ " + key + "uk : Ukrainian" + "\n" + \
						"³ " + key + "vi : Vietnamese" + "\n" + \
						"³ " + key + "cy : Welsh" + "\n" + \
						"?ÄÄ[ Jangan Typo ]"
	return menuTextToSpeech

def menuTranslate():
	if settings['setKey'] == True:
		key = settings['keyCommand']
	else:
		key = ''
	menuTranslate =	"?ÄÄ[ Translate ]" + "\n" + \
					"³ " + key + "af : afrikaans" + "\n" + \
					"³ " + key + "sq : albanian" + "\n" + \
					"³ " + key + "am : amharic" + "\n" + \
					"³ " + key + "ar : arabic" + "\n" + \
					"³ " + key + "hy : armenian" + "\n" + \
					"³ " + key + "az : azerbaijani" + "\n" + \
					"³ " + key + "eu : basque" + "\n" + \
					"³ " + key + "be : belarusian" + "\n" + \
					"³ " + key + "bn : bengali" + "\n" + \
					"³ " + key + "bs : bosnian" + "\n" + \
					"³ " + key + "bg : bulgarian" + "\n" + \
					"³ " + key + "ca : catalan" + "\n" + \
					"³ " + key + "ceb : cebuano" + "\n" + \
					"³ " + key + "ny : chichewa" + "\n" + \
					"³ " + key + "zh-cn : chinese (simplified)" + "\n" + \
					"³ " + key + "zh-tw : chinese (traditional)" + "\n" + \
					"³ " + key + "co : corsican" + "\n" + \
					"³ " + key + "hr : croatian" + "\n" + \
					"³ " + key + "cs : czech" + "\n" + \
					"³ " + key + "da : danish" + "\n" + \
					"³ " + key + "nl : dutch" + "\n" + \
					"³ " + key + "en : english" + "\n" + \
					"³ " + key + "eo : esperanto" + "\n" + \
					"³ " + key + "et : estonian" + "\n" + \
					"³ " + key + "tl : filipino" + "\n" + \
					"³ " + key + "fi : finnish" + "\n" + \
					"³ " + key + "fr : french" + "\n" + \
					"³ " + key + "fy : frisian" + "\n" + \
					"³ " + key + "gl : galician" + "\n" + \
					"³ " + key + "ka : georgian" + "\n" + \
					"³ " + key + "de : german" + "\n" + \
					"³ " + key + "el : greek" + "\n" + \
					"³ " + key + "gu : gujarati" + "\n" + \
					"³ " + key + "ht : haitian creole" + "\n" + \
					"³ " + key + "ha : hausa" + "\n" + \
					"³ " + key + "haw : hawaiian" + "\n" + \
					"³ " + key + "iw : hebrew" + "\n" + \
					"³ " + key + "hi : hindi" + "\n" + \
					"³ " + key + "hmn : hmong" + "\n" + \
					"³ " + key + "hu : hungarian" + "\n" + \
					"³ " + key + "is : icelandic" + "\n" + \
					"³ " + key + "ig : igbo" + "\n" + \
					"³ " + key + "id : indonesian" + "\n" + \
					"³ " + key + "ga : irish" + "\n" + \
					"³ " + key + "it : italian" + "\n" + \
					"³ " + key + "ja : japanese" + "\n" + \
					"³ " + key + "jw : javanese" + "\n" + \
					"³ " + key + "kn : kannada" + "\n" + \
					"³ " + key + "kk : kazakh" + "\n" + \
					"³ " + key + "km : khmer" + "\n" + \
					"³ " + key + "ko : korean" + "\n" + \
					"³ " + key + "ku : kurdish (kurmanji)" + "\n" + \
					"³ " + key + "ky : kyrgyz" + "\n" + \
					"³ " + key + "lo : lao" + "\n" + \
					"³ " + key + "la : latin" + "\n" + \
					"³ " + key + "lv : latvian" + "\n" + \
					"³ " + key + "lt : lithuanian" + "\n" + \
					"³ " + key + "lb : luxembourgish" + "\n" + \
					"³ " + key + "mk : macedonian" + "\n" + \
					"³ " + key + "mg : malagasy" + "\n" + \
					"³ " + key + "ms : malay" + "\n" + \
					"³ " + key + "ml : malayalam" + "\n" + \
					"³ " + key + "mt : maltese" + "\n" + \
					"³ " + key + "mi : maori" + "\n" + \
					"³ " + key + "mr : marathi" + "\n" + \
					"³ " + key + "mn : mongolian" + "\n" + \
					"³ " + key + "my : myanmar (burmese)" + "\n" + \
					"³ " + key + "ne : nepali" + "\n" + \
					"³ " + key + "no : norwegian" + "\n" + \
					"³ " + key + "ps : pashto" + "\n" + \
					"³ " + key + "fa : persian" + "\n" + \
					"³ " + key + "pl : polish" + "\n" + \
					"³ " + key + "pt : portuguese" + "\n" + \
					"³ " + key + "pa : punjabi" + "\n" + \
					"³ " + key + "ro : romanian" + "\n" + \
					"³ " + key + "ru : russian" + "\n" + \
					"³ " + key + "sm : samoan" + "\n" + \
					"³ " + key + "gd : scots gaelic" + "\n" + \
					"³ " + key + "sr : serbian" + "\n" + \
					"³ " + key + "st : sesotho" + "\n" + \
					"³ " + key + "sn : shona" + "\n" + \
					"³ " + key + "sd : sindhi" + "\n" + \
					"³ " + key + "si : sinhala" + "\n" + \
					"³ " + key + "sk : slovak" + "\n" + \
					"³ " + key + "sl : slovenian" + "\n" + \
					"³ " + key + "so : somali" + "\n" + \
					"³ " + key + "es : spanish" + "\n" + \
					"³ " + key + "su : sundanese" + "\n" + \
					"³ " + key + "sw : swahili" + "\n" + \
					"³ " + key + "sv : swedish" + "\n" + \
					"³ " + key + "tg : tajik" + "\n" + \
					"³ " + key + "ta : tamil" + "\n" + \
					"³ " + key + "te : telugu" + "\n" + \
					"³ " + key + "th : thai" + "\n" + \
					"³ " + key + "tr : turkish" + "\n" + \
					"³ " + key + "uk : ukrainian" + "\n" + \
					"³ " + key + "ur : urdu" + "\n" + \
					"³ " + key + "uz : uzbek" + "\n" + \
					"³ " + key + "vi : vietnamese" + "\n" + \
					"³ " + key + "cy : welsh" + "\n" + \
					"³ " + key + "xh : xhosa" + "\n" + \
					"³ " + key + "yi : yiddish" + "\n" + \
					"³ " + key + "yo : yoruba" + "\n" + \
					"³ " + key + "zu : zulu" + "\n" + \
					"³ " + key + "fil : Filipino" + "\n" + \
					"³ " + key + "he : Hebrew" + "\n" + \
					"?ÄÄ[ Jangan Typo ]"
	return menuTranslate

def clientBot(op):
	try:
		if op.type == 0:
			return

		if op.type == 5:
			if settings["autoAdd"] == True:
				client.findAndAddContactsByMid(op.param1)
			client.sendMention(op.param1, settings["autoAddMessage"], [op.param1])

		if op.type == 13:
			if settings["autoJoin"] and clientMid in op.param3:
				client.acceptGroupInvitation(op.param1)
				client.sendMention(op.param1, settings["autoJoinMessage"], [op.param2])

		if op.type == 17:
			if op.param1 in welcome:
				ginfo = client.getGroup(op.param1)
				contact = client.getContact(op.param2).picturePath
				image = 'http://dl.profile.line.naver.jp'+contact
				welcomeMembers(op.param1, [op.param2])
				client.sendImageWithURL(op.param1, image)
		if op.type == 15:
			if op.param1 in welcome:
				ginfo = client.getGroup(op.param1)
				leaveMembers(op.param1, [op.param2])

		if op.type == 25:
			try:
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				cmd = command(text)
				setKey = settings["keyCommand"].title()
				if settings["setKey"] == False:
					setKey = ''
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if msg.contentType == 0:
						if cmd == "ÍÍ¡":
							client.sendMessage(to, "Berhasil mematikan selfbot")
							sys.exit("[ INFO ] BOT SHUTDOWN")
							return
						elif cmd == "restart":
							client.sendMessage(to, "Berhasil mereset bot")
							restartBot()
						elif cmd == "àª¤":
							start = time.time()
							client.sendMessage(to, "Menghitung kecepatan...")
							elapsed_time = time.time() - start
							client.sendMessage(to, "Kecepatan mengirim pesan {} detik".format(str(elapsed_time)))
						elif cmd == "ÃÑ¹":
							timeNow = time.time()
							runtime = timeNow - clientStart
							runtime = timeChange(runtime)
							client.sendMessage(to, "Selfbot telah aktif selama {}".format(str(runtime)))
						elif cmd.startswith("setkey: "):
							sep = text.split(" ")
							key = text.replace(sep[0] + " ","")
							if " " in key:
								client.sendMessage(to, "Key tidak bisa menggunakan spasi")
							else:
								settings["keyCommand"] = str(key).lower()
								client.sendMessage(to, "Berhasil mengubah set key command menjadi : ?{}?".format(str(key).lower()))
						elif cmd == "¤ÓÊÑè§":
							helpMessage = menuHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§2":
							helpStatusMessage = menuStatusHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpStatusMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§3":
							helpSettingsMessage = menuSettingsHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpSettingsMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§4":
							helpSelfMessage = menuSelfHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpSelfMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§5":
							helpGroupMessage = menuGroupHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpGroupMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§6":
							helpSpecialMessage = menuSpecialHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpSpecialMessage, icon, name, link)
						elif cmd == "¤ÓÊÑè§7":
							helpMediaMessage = menuMediaHelp()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpMediaMessage, icon, name, link)
						elif cmd == "texttospeech":
							helpTextToSpeech = menuTextToSpeech()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpTextToSpeech, icon, name, link)
						elif cmd == "translate":
							helpTranslate = menuTranslate()
							contact = client.getContact(sender)
							icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							name = contact.displayName
							link = "http://line.me/ti/p/%40has6814j"
							client.sendFooter(to, helpTranslate, icon, name, link)


						elif cmd == "status":
							try:
								ret_ = "?ÄÄ[ Status ]"
								if settings["autoAdd"] == True: ret_ += "\n³ Auto Add : ON"
								else: ret_ += "\n³ Auto Add : OFF"
								if settings["autoJoin"] == True: ret_ += "\n³ Auto Join : ON"
								else: ret_ += "\n³ Auto Join : OFF"
								if settings["autoJoin"] == True: ret_ += "\n³ Auto Join Ticket : ON"
								else: ret_ += "\n³ Auto Join Ticket : OFF"
								if settings["autoRead"] == True: ret_ += "\n³ Auto Read : ON"
								else: ret_ += "\n³ Auto Read : OFF"
								if settings["autoRespon"] == True: ret_ += "\n³ Auto Respon : ON"
								else: ret_ += "\n³ Auto Respon : OFF"
								if settings["checkContact"] == True: ret_ += "\n³ Check Contact : ON"
								else: ret_ += "\n³ Check Contact : OFF"
								if settings["checkPost"] == True: ret_ += "\n³ Check Post : ON"
								else: ret_ += "\n³ Check Post : OFF"
								if settings["checkSticker"] == True: ret_ += "\n³ Check Sticker : ON"
								else: ret_ += "\n³ Check Sticker : OFF"
								if settings["detectUnsend"] == True: ret_ += "\n³ Detect Unsend : ON"
								else: ret_ += "\n³ Detect Unsend : OFF"
								if settings["setKey"] == True: ret_ += "\n³ Set Key : ON"
								else: ret_ += "\n³ Set Key : OFF"
								ret_ +="\n³ Auto Add Message : {}".format(settings["autoAddMessage"])
								ret_ +="\n³ Auto Join Message : {}".format(settings["autoJoinMessage"])
								ret_ +="\n³ Auto Respon Message : {}".format(settings["autoResponMessage"])
								ret_ +="\n³ Welcome Message : {}".format(settings["welcome"])
								ret_ +="\n³ Leave Message : {}".format(settings["leave"])
								ret_ += "\n?ÄÄ[ Status ]"
								icon = "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								name = contact.displayName
								link = "http://line.me/ti/p/%40has6814j"
								client.sendFooter(to, str(ret_), icon, name, link)
							except Exception as error:
								logError(error)
						elif cmd == "autoadd on":
							if settings["autoAdd"] == True:
								client.sendMessage(to, "Auto add telah aktif")
							else:
								settings["autoAdd"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto add")
						elif cmd == "autoadd off":
							if settings["autoAdd"] == False:
								client.sendMessage(to, "Auto add telah nonaktif")
							else:
								settings["autoAdd"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto add")
						elif cmd == "autojoin on":
							if settings["autoJoin"] == True:
								client.sendMessage(to, "Auto join telah aktif")
							else:
								settings["autoJoin"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto join")
						elif cmd == "autojoin off":
							if settings["autoJoin"] == False:
								client.sendMessage(to, "Auto join telah nonaktif")
							else:
								settings["autoJoin"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto join")
						elif cmd == "autojointicket on":
							if settings["autoJoinTicket"] == True:
								client.sendMessage(to, "Auto join ticket telah aktif")
							else:
								settings["autoJoinTicket"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto join ticket")
						elif cmd == "autojointicket off":
							if settings["autoJoinTicket"] == False:
								client.sendMessage(to, "Auto join ticket telah nonaktif")
							else:
								settings["autoJoinTicket"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto join ticket")
						elif cmd == "autoread on":
							if settings["autoRead"] == True:
								client.sendMessage(to, "Auto read telah aktif")
							else:
								settings["autoRead"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto read")
						elif cmd == "autoread off":
							if settings["autoRead"] == False:
								client.sendMessage(to, "Auto read telah nonaktif")
							else:
								settings["autoRead"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto read")
						elif cmd == "autorespon on":
							if settings["autoRespon"] == True:
								client.sendMessage(to, "Auto respon telah aktif")
							else:
								settings["autoRespon"] = True
								client.sendMessage(to, "Berhasil mengaktifkan auto respon")
						elif cmd == "autorespon off":
							if settings["autoRespon"] == False:
								client.sendMessage(to, "Auto respon telah nonaktif")
							else:
								settings["autoRespon"] = False
								client.sendMessage(to, "Berhasil menonaktifkan auto respon")
						elif cmd == "checkcontact on":
							if settings["checkContact"] == True:
								client.sendMessage(to, "Check details contact telah aktif")
							else:
								settings["checkContact"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details contact")
						elif cmd == "checkcontact off":
							if settings["checkContact"] == False:
								client.sendMessage(to, "Check details contact telah nonaktif")
							else:
								settings["checkContact"] = False
								client.sendMessage(to, "Berhasil menonaktifkan Check details contact")
						elif cmd == "checkpost on":
							if settings["checkPost"] == True:
								client.sendMessage(to, "Check details post telah aktif")
							else:
								settings["checkPost"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details post")
						elif cmd == "checkpost off":
							if settings["checkPost"] == False:
								client.sendMessage(to, "Check details post telah nonaktif")
							else:
								settings["checkPost"] = False
								client.sendMessage(to, "Berhasil menonaktifkan check details post")
						elif cmd == "checksticker on":
							if settings["checkSticker"] == True:
								client.sendMessage(to, "Check details sticker telah aktif")
							else:
								settings["checkSticker"] = True
								client.sendMessage(to, "Berhasil mengaktifkan check details sticker")
						elif cmd == "checksticker off":
							if settings["checkSticker"] == False:
								client.sendMessage(to, "Check details sticker telah nonaktif")
							else:
								settings["checkSticker"] = False
								client.sendMessage(to, "Berhasil menonaktifkan check details sticker")
						elif cmd == "detectunsend on":
							if settings["detectUnsend"] == True:
								client.sendMessage(to, "Detect unsend telah aktif")
							else:
								settings["detectUnsend"] = True
								client.sendMessage(to, "Berhasil mengaktifkan detect unsend")
						elif cmd == "detectunsend off":
							if settings["detectUnsend"] == False:
								client.sendMessage(to, "Detect unsend telah nonaktif")
							else:
								settings["detectUnsend"] = False
								client.sendMessage(to, "Berhasil menonaktifkan detect unsend")
						elif cmd.startswith("setautoaddmessge: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoAddMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto add menjadi : ?{}?".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto add")
						elif cmd.startswith("setautoresponmessage: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoResponMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto respon menjadi : ?{}?".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto respon")
						elif cmd.startswith("setautojoinmessage: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["autoJoinMessage"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan auto join menjadi : ?{}?".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan auto join")

						elif 'Setwelcomemessage: ' in msg.text:
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["welcome"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan welcome menjadi : ?{}?".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan welcome")

						elif 'Setleavemessage: ' in msg.text:
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							try:
								settings["welcome"] = txt
								client.sendMessage(to, "Berhasil mengubah pesan leave menjadi : ?{}?".format(txt))
							except:
								client.sendMessage(to, "Gagal mengubah pesan leave")

						elif 'Welcome ' in msg.text:
							spl = msg.text.replace('Welcome ','')
							if spl == 'on':
								if msg.to in welcome:
									msgs = "Welcome Msg sudah aktif"
								else:
									welcome.append(msg.to)
									ginfo = client.getGroup(msg.to)
									msgs = "Status : [ ON ]\nDi Group : " +str(ginfo.name)
								client.sendMessage(msg.to, "? Status Welcome ?\n" + msgs)
							elif spl == 'off':
                                                           	if msg.to in welcome:
                                                                	welcome.remove(msg.to)
                                                                	ginfo = client.getGroup(msg.to)
                                                                	msgs = "Status : [ OFF ]\nDi Group : " +str(ginfo.name)
                                                           	else:
                                                                	msgs = "Welcome Msg sudah tidak aktif"
                                                           	client.sendMessage(msg.to, "? Status Welcome ?\n" + msgs)

						elif cmd.startswith("changename: "):
							sep = text.split(" ")
							name = text.replace(sep[0] + " ","")
							if len(name) <= 20:
								profile = client.getProfile()
								profile.displayName = name
								client.updateProfile(profile)
								client.sendMessage(to, "Berhasil mengubah nama menjadi : {}".format(name))
						elif cmd.startswith("changebio: "):
							sep = text.split(" ")
							bio = text.replace(sep[0] + " ","")
							if len(bio) <= 500:
								profile = client.getProfile()
								profile.displayName = bio
								client.updateProfile(profile)
								client.sendMessage(to, "Berhasil mengubah bio menjadi : {}".format(bio))
						elif cmd == "me":
							client.sendMention(to, "@!", [sender])
							client.sendContact(to, sender)
						elif cmd == "myprofile":
							contact = client.getContact(sender)
							cover = client.getProfileCoverURL(sender)
							result = "?ÄÄ[ Details Profile ]"
							result += "\n³ Display Name : @!"
							result += "\n³ Mid : {}".format(contact.mid)
							result += "\n³ Status Message : {}".format(contact.statusMessage)
							result += "\n³ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
							result += "\n³ Cover : {}".format(str(cover))
							result += "\n?ÄÄÄÄÄÄÄÄÄÄ"
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
							client.sendMention(to, result, [sender])
						elif cmd == "mymid":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.mid), [sender])
						elif cmd == "myname":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.displayName), [sender])
						elif cmd == "mybio":
							contact = client.getContact(sender)
							client.sendMention(to, "@!: {}".format(contact.statusMessage), [sender])
						elif cmd == "mypicture":
							contact = client.getContact(sender)
							client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd == "myvideoprofile":
							contact = client.getContact(sender)
							if contact.videoProfile == None:
								return client.sendMessage(to, "Anda tidak memiliki video profile")
							client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd == "mycover":
							cover = client.getProfileCoverURL(sender)
							client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("getmid "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.sendMention(to, "@!: {}".format(ls), [ls])
						elif cmd.startswith("getname "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.displayName), [ls])
						elif cmd.startswith("getbio "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendMention(to, "@!: {}".format(contact.statusMessage), [ls])
						elif cmd.startswith("getpicture "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
						elif cmd.startswith("getvideoprofile "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									contact = client.getContact(ls)
									if contact.videoProfile == None:
										return client.sendMention(to, "@!tidak memiliki video profile", [ls])
									client.sendVideoWithURL(to, "http://dl.profile.line-cdn.net/{}/vp".format(contact.pictureStatus))
						elif cmd.startswith("getcover "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									cover = client.getProfileCoverURL(ls)
									client.sendImageWithURL(to, str(cover))
						elif cmd.startswith("cloneprofile "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									client.cloneContactProfile(ls)
									client.sendContact(to, sender)
									client.sendMessage(to, "Berhasil clone profile")
						elif cmd == "restoreprofile":
							try:
								clientProfile = client.getProfile()
								clientProfile.displayName = str(settings["myProfile"]["displayName"])
								clientProfile.statusMessage = str(settings["myProfile"]["statusMessage"])
								clientPictureStatus = client.downloadFileURL("http://dl.profile.line-cdn.net/{}".format(str(settings["myProfile"]["pictureStatus"])), saveAs="LineAPI/tmp/backupPicture.bin")
								coverId = str(settings["myProfile"]["coverId"])
								client.updateProfile(clientProfile)
								client.updateProfileCoverById(coverId)
								client.updateProfilePicture(clientPictureStatus)
								client.sendMessage(to, "Berhasil restore profile")
								client.sendContact(to, sender)
								client.deleteFile(clientPictureStatus)
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal restore profile")
						elif cmd == "backupprofile":
							try:
								clientProfile = client.getProfile()
								settings["myProfile"]["displayName"] = str(clientProfile.displayName)
								settings["myProfile"]["statusMessage"] = str(clientProfile.statusMessage)
								settings["myProfile"]["pictureStatus"] = str(clientProfile.pictureStatus)
								coverId = client.getProfileDetail()["result"]["objectId"]
								settings["myProfile"]["coverId"] = str(coverId)
								client.sendMessage(to, "Berhasil backup profile")
							except Exception as error:
								logError(error)
								client.sendMessage(to, "Gagal backup profile")
						elif cmd == "friendlist":
							contacts = client.getAllContactIds()
							num = 0
							result = "?ÄÄ[ Friend List ]"
							for listContact in contacts:
								contact = client.getContact(listContact)
								num += 1
								result += "\n³ {}. {}".format(num, contact.displayName)
							result += "\n?ÄÄ[ Total {} Friend ]".format(len(contacts))
							client.sendMessage(to, result)
						elif cmd.startswith("friendinfo "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							contacts = client.getAllContactIds()
							try:
								listContact = contacts[int(query)-1]
								contact = client.getContact(listContact)
								cover = client.getProfileCoverURL(listContact)
								result = "?ÄÄ[ Details Profile ]"
								result += "\n³ Display Name : @!"
								result += "\n³ Mid : {}".format(contact.mid)
								result += "\n³ Status Message : {}".format(contact.statusMessage)
								result += "\n³ Picture Profile : http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus)
								result += "\n³ Cover : {}".format(str(cover))
								result += "\n?ÄÄÄÄÄÄÄÄÄÄ"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(contact.pictureStatus))
								client.sendMention(to, result, [contact.mid])
							except Exception as error:
								logError(error)
						elif cmd == "blocklist":
							blockeds = client.getBlockedContactIds()
							num = 0
							result = "?ÄÄ[ List Blocked ]"
							for listBlocked in blockeds:
								contact = client.getContact(listBlocked)
								num += 1
								result += "\n³ {}. {}".format(num, contact.displayName)
							result += "\n?ÄÄ[ Total {} Blocked ]".format(len(blockeds))
							client.sendMessage(to, result)
						elif cmd.startswith("friendbroadcast: "):
                                                        sep = text.split(" ")
                                                        txt = text.replace(sep[0] + " ","")
                                                        contacts = client.getAllContactIds()
                                                        for contact in contacts:
                                                                client.sendMessage(contact, "[ Broadcast ]\n{}".format(str(txt)))
                                                        client.sendMessage(to, "Berhasil broadcast ke {} teman".format(str(len(contacts))))

						elif cmd.startswith("changegroupname: "):
							if msg.toType == 2:
								sep = text.split(" ")
								groupname = text.replace(sep[0] + " ","")
								if len(groupname) <= 20:
									group = client.getGroup(to)
									group.name = groupname
									client.updateGroup(group)
									client.sendMessage(to, "Berhasil mengubah nama group menjadi : {}".format(groupname))
						elif cmd == "openqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = False
								client.updateGroup(group)
								groupUrl = client.reissueGroupTicket(to)
								client.sendMessage(to, "Berhasil membuka QR Group\n\nGroupURL : line://ti/g/{}".format(groupUrl))
						elif cmd == "closeqr":
							if msg.toType == 2:
								group = client.getGroup(to)
								group.preventedJoinByTicket = True
								client.updateGroup(group)
								client.sendMessage(to, "Berhasil menutup QR Group")
						elif cmd == "grouppicture":
							if msg.toType == 2:
								group = client.getGroup(to)
								groupPicture = "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus)
								client.sendImageWithURL(to, groupPicture)
						elif cmd == "groupname":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "Nama Group : {}".format(group.name))
						elif cmd == "groupid":
							if msg.toType == 2:
								group = client.getGroup(to)
								client.sendMessage(to, "Group ID : {}".format(group.id))
						elif cmd == "grouplist":
							groups = client.getGroupIdsJoined()
							ret_ = "?ÄÄ[ Group List ]"
							no = 0
							for gid in groups:
								group = client.getGroup(gid)
								no += 1
								ret_ += "\n³ {}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
							ret_ += "\n?ÄÄ[ Total {} Groups ]".format(str(len(groups)))
							client.sendMessage(to, str(ret_))
						elif cmd == "memberlist":
							if msg.toType == 2:
								group = client.getGroup(to)
								num = 0
								ret_ = "?ÄÄ[ List Member ]"
								for contact in group.members:
									num += 1
									ret_ += "\n³ {}. {}".format(num, contact.displayName)
								ret_ += "\n?ÄÄ[ Total {} Members]".format(len(group.members))
								client.sendMessage(to, ret_)
						elif cmd == "pendinglist":
							if msg.toType == 2:
								group = client.getGroup(to)
								ret_ = "?ÄÄ[ Pending List ]"
								no = 0
								if group.invitee is None or group.invitee == []:
									return client.sendMessage(to, "Tidak ada pendingan")
								else:
									for pending in group.invitee:
										no += 1
										ret_ += "\n³ {}. {}".format(str(no), str(pending.displayName))
									ret_ += "\n?ÄÄ[ Total {} Pending]".format(str(len(group.invitee)))
									client.sendMessage(to, str(ret_))
						elif cmd == "groupinfo":
							group = client.getGroup(to)
							try:
								try:
									groupCreator = group.creator.mid
								except:
									groupCreator = "Tidak ditemukan"
								if group.invitee is None:
									groupPending = "0"
								else:
									groupPending = str(len(group.invitee))
								if group.preventedJoinByTicket == True:
									groupQr = "Tertutup"
									groupTicket = "Tidak ada"
								else:
									groupQr = "Terbuka"
									groupTicket = "https://line.me/R/ti/g/{}".format(str(client.reissueGroupTicket(group.id)))
								ret_ = "?ÄÄ[ Group Information ]"
								ret_ += "\n³ Nama Group : {}".format(group.name)
								ret_ += "\n³ ID Group : {}".format(group.id)
								ret_ += "\n³ Pembuat : @!"
								ret_ += "\n³ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n³ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n³ Group Qr : {}".format(groupQr)
								ret_ += "\n³ Group Ticket : {}".format(groupTicket)
								ret_ += "\n?ÄÄ[ Success ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMention(to, str(ret_), [groupCreator])
							except:
								ret_ = "?ÄÄ[ Group Information ]"
								ret_ += "\n³ Nama Group : {}".format(group.name)
								ret_ += "\n³ ID Group : {}".format(group.id)
								ret_ += "\n³ Pembuat : {}".format(groupCreator)
								ret_ += "\n³ Jumlah Member : {}".format(str(len(group.members)))
								ret_ += "\n³ Jumlah Pending : {}".format(groupPending)
								ret_ += "\n³ Group Qr : {}".format(groupQr)
								ret_ += "\n³ Group Ticket : {}".format(groupTicket)
								ret_ += "\n?ÄÄ[ Success ]"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(group.pictureStatus))
								client.sendMessage(to, str(ret_))
						elif cmd.startswith("groupbroadcast: "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							groups = client.getGroupIdsJoined()
							for group in groups:
								client.sendMessage(group, "[ Broadcast ]\n{}".format(str(txt)))
							client.sendMessage(to, "Berhasil broadcast ke {} group".format(str(len(groups))))


						elif cmd == 'á·¤':
							group = client.getGroup(to)
							midMembers = [contact.mid for contact in group.members]
							midSelect = len(midMembers)//20
							for mentionMembers in range(midSelect+1):
								no = 0
								ret_ = "?ÄÄ[ Mention Members ]"
								dataMid = []
								for dataMention in group.members[mentionMembers*20 : (mentionMembers+1)*20]:
									dataMid.append(dataMention.mid)
									no += 1
									ret_ += "\n³ {}. @!".format(str(no))
								ret_ += "\n?ÄÄ[ Total {} Members]".format(str(len(dataMid)))
								client.sendMention(to, ret_, dataMid)
						elif cmd == "à»Ô´áÍº":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to in read['readPoint']:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "Lurking telah diaktifkan")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								read['readPoint'][to] = msg_id
								read['readMember'][to] = []
								client.sendMessage(to, "Set reading point : \n{}".format(readTime))
						elif cmd == "»Ô´áÍº":
							tz = pytz.timezone("Asia/Makassar")
							timeNow = datetime.now(tz=tz)
							day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
							hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
							bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
							hr = timeNow.strftime("%A")
							bln = timeNow.strftime("%m")
							for i in range(len(day)):
								if hr == day[i]: hasil = hari[i]
							for k in range(0, len(bulan)):
								if bln == str(k): bln = bulan[k-1]
							readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
							if to not in read['readPoint']:
								client.sendMessage(to,"Lurking telah dinonaktifkan")
							else:
								try:
									del read['readPoint'][to]
									del read['readMember'][to]
								except:
									pass
								client.sendMessage(to, "Delete reading point : \n{}".format(readTime))
						elif cmd == "ÍèÒ¹":
							if to in read['readPoint']:
								if read["readMember"][to] == []:
									return client.sendMessage(to, "Tidak Ada Sider")
								else:
									no = 0
									result = "?ÄÄ[ Reader ]"
									for dataRead in read["readMember"][to]:
										no += 1
										result += "\n³ {}. @!".format(str(no))
									result += "\n?ÄÄ[ Total {} Sider ]".format(str(len(read["readMember"][to])))
									client.sendMention(to, result, read["readMember"][to])
									read['readMember'][to] = []
						elif cmd == "changepictureprofile":
							settings["changePictureProfile"] = True
							client.sendMessage(to, "Silahkan kirim gambarnya")
						elif cmd == "changegrouppicture":
							if msg.toType == 2:
								if to not in settings["changeGroupPicture"]:
									settings["changeGroupPicture"].append(to)
								client.sendMessage(to, "Silahkan kirim gambarnya")
						elif cmd == "mimic on":
							if settings["mimic"]["status"] == True:
								client.sendMessage(to, "Reply message telah aktif")
							else:
								settings["mimic"]["status"] = True
								client.sendMessage(to, "Berhasil mengaktifkan reply message")
						elif cmd == "mimic off":
							if settings["mimic"]["status"] == False:
								client.sendMessage(to, "Reply message telah nonaktif")
							else:
								settings["mimic"]["status"] = False
								client.sendMessage(to, "Berhasil menonaktifkan reply message")
						elif cmd == "mimiclist":
							if settings["mimic"]["target"] == {}:
								client.sendMessage(to, "Tidak Ada Target")
							else:
								no = 0
								result = "?ÄÄ[ Mimic List ]"
								target = []
								for mid in settings["mimic"]["target"]:
									target.append(mid)
									no += 1
									result += "\n³ {}. @!".format(no)
								result += "\n?ÄÄ[ Total {} Mimic ]".format(str(len(target)))
								client.sendMention(to, result, target)
						elif cmd.startswith("mimicadd "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls in settings["mimic"]["target"]:
											client.sendMessage(to, "Target sudah ada dalam list")
										else:
											settings["mimic"]["target"][ls] = True
											client.sendMessage(to, "Berhasil menambahkan target")
									except:
										client.sendMessage(to, "Gagal menambahkan target")
						elif cmd.startswith("mimicdel "):
							if 'MENTION' in msg.contentMetadata.keys()!= None:
								names = re.findall(r'@(\w+)', text)
								mention = ast.literal_eval(msg.contentMetadata['MENTION'])
								mentionees = mention['MENTIONEES']
								lists = []
								for mention in mentionees:
									if mention["M"] not in lists:
										lists.append(mention["M"])
								for ls in lists:
									try:
										if ls not in settings["mimic"]["target"]:
											client.sendMessage(to, "Target sudah tida didalam list")
										else:
											del settings["mimic"]["target"][ls]
											client.sendMessage(to, "Berhasil menghapus target")
									except:
										client.sendMessage(to, "Gagal menghapus target")


						elif cmd.startswith("instainfo"):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/instainfo/{}?key=betakey".format(txt))
							data = url.json()
							icon = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Instagram_icon.png/599px-Instagram_icon.png"
							name = "Instagram"
							link = "https://www.instagram.com/{}".format(data["result"]["username"])
							result = "?ÄÄ[ Instagram Info ]"
							result += "\n³ Name : {}".format(data["result"]["name"])
							result += "\n³ Username: {}".format(data["result"]["username"])
							result += "\n³ Bio : {}".format(data["result"]["bio"])
							result += "\n³ Follower : {}".format(data["result"]["follower"])
							result += "\n³ Following : {}".format(data["result"]["following"])
							result += "\n³ Private : {}".format(data["result"]["private"])
							result += "\n³ Post : {}".format(data["result"]["mediacount"])
							result += "\n?ÄÄÄÄÄÄÄÄÄÄ"
							client.sendImageWithURL(to, data["result"]["url"])
							client.sendFooter(to, result, icon, name, link)
						elif cmd.startswith("instastory "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							if len(cond) == 2:
								url = requests.get("http://rahandiapi.herokuapp.com/instastory/{}?key=betakey".format(search))
								data = url.json()
								num = int(cond[1])
								if num <= len(data["url"]):
									search = data["url"][num - 1]
									if search["tipe"] == 1:
										client.sendImageWithURL(to, str(search["link"]))
									elif search["tipe"] == 2:
										client.sendVideoWithURL(to, str(search["link"]))
						elif cmd == "quotes":
							url = requests.get("https://botfamily.faith/api/quotes/?apikey=beta")
							data = url.json()
							result = "?ÄÄ[ Quotes ]"
							result += "\n³ Author : {}".format(data["result"]["author"])
							result += "\n³ Category : {}".format(data["result"]["category"])
							result += "\n³ Quote : {}".format(data["result"]["quote"])
							result += "\n?ÄÄÄÄÄÄÄÄÄÄ"
							client.sendMessage(to, result)
						elif cmd.startswith("say-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("say-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "say-" + lang + " ","")
							if lang not in language["gtts"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							tts = gTTS(text=txt, lang=lang)
							tts.save("line/tmp/tts-{}.mp3".format(lang))
							client.sendAudio(to, "line/tmp/tts-{}.mp3".format(lang))
							client.deleteFile("line/tmp/tts-{}.mp3".format(lang))
						elif cmd.startswith("searchyoutube "):
							sep = text.split(" ")
							txt = msg.text.replace(sep[0] + " ","")
							cond = txt.split("|")
							search = cond[0]
							url = requests.get("http://api.w3hills.com/youtube/search?keyword={}&api_key=86A7FCF3-6CAF-DEB9-E214-B74BDB835B5B".format(search))
							data = url.json()
							if len(cond) == 1:
								no = 0
								result = "?ÄÄ[ Youtube Search ]"
								for anu in data["videos"]:
									no += 1
									result += "\n³ {}. {}".format(str(no),str(anu["title"]))
								result += "\n?ÄÄ[ Total {} Result ]".format(str(len(data["videos"])))
								client.sendMessage(to, result)
							elif len(cond) == 2:
								num = int(str(cond[1]))
								if num <= len(data):
									search = data["videos"][num - 1]
									ret_ = "?ÄÄ[ Youtube Info ]"
									ret_ += "\n³ Channel : {}".format(str(search["publish"]["owner"]))
									ret_ += "\n³ Title : {}".format(str(search["title"]))
									ret_ += "\n³ Release : {}".format(str(search["publish"]["date"]))
									ret_ += "\n³ Viewers : {}".format(str(search["stats"]["views"]))
									ret_ += "\n³ Likes : {}".format(str(search["stats"]["likes"]))
									ret_ += "\n³ Dislikes : {}".format(str(search["stats"]["dislikes"]))
									ret_ += "\n³ Rating : {}".format(str(search["stats"]["rating"]))
									ret_ += "\n³ Description : {}".format(str(search["description"]))
									ret_ += "\n?ÄÄ[ {} ]".format(str(search["webpage"]))
									client.sendImageWithURL(to, str(search["thumbnail"]))
									client.sendMessage(to, str(ret_))
						elif cmd.startswith("searchimage "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							url = requests.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(txt))
							data = url.json()
							client.sendImageWithURL(to, random.choice(data["result"]))
						elif cmd.startswith("searchmusic "):
							sep = text.split(" ")
							query = text.replace(sep[0] + " ","")
							cond = query.split("|")
							search = str(cond[0])
							url = requests.get("http://api.ntcorp.us/joox/search?q={}".format(str(search)))
							data = url.json()
							if len(cond) == 1:
								num = 0
								ret_ = "?ÄÄ[ Result Music ]"
								for music in data["result"]:
									num += 1
									ret_ += "\n³ {}. {}".format(str(num), str(music["single"]))
								ret_ += "\n?ÄÄ[ Total {} Music ]".format(str(len(data["result"])))
								ret_ += "\n\nUntuk mengirim music, silahkan gunakan command {}SearchMusic {}|?number?".format(str(setKey), str(search))
								client.sendMessage(to, str(ret_))
							elif len(cond) == 2:
								num = int(cond[1])
								if num <= len(data["result"]):
									music = data["result"][num - 1]
									url = requests.get("http://api.ntcorp.us/joox/song_info?sid={}".format(str(music["sid"])))
									data = url.json()
									ret_ = "?ÄÄ[ Music ]"
									ret_ += "\n³ Title : {}".format(str(data["result"]["song"]))
									ret_ += "\n³ Album : {}".format(str(data["result"]["album"]))
									ret_ += "\n³ Size : {}".format(str(data["result"]["size"]))
									ret_ += "\n³ Link : {}".format(str(data["result"]["mp3"][0]))
									ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
									client.sendImageWithURL(to, str(data["result"]["img"]))
									client.sendMessage(to, str(ret_))
									client.sendAudioWithURL(to, str(data["result"]["mp3"][0]))
						elif cmd.startswith("searchlyric "):
							sep = text.split(" ")
							txt = text.replace(sep[0] + " ","")
							cond = txt.split("|")
							query = cond[0]
							with requests.session() as web:
								web.headers["user-agent"] = "Mozilla/5.0"
								url = web.get("https://www.musixmatch.com/search/{}".format(urllib.parse.quote(query)))
								data = BeautifulSoup(url.content, "html.parser")
								result = []
								for trackList in data.findAll("ul", {"class":"tracks list"}):
									for urlList in trackList.findAll("a"):
										title = urlList.text
										url = urlList["href"]
										result.append({"title": title, "url": url})
								if len(cond) == 1:
									ret_ = "?ÄÄ[ Musixmatch Result ]"
									num = 0
									for title in result:
										num += 1
										ret_ += "\n³ {}. {}".format(str(num), str(title["title"]))
									ret_ += "\n?ÄÄ[ Total {} Lyric ]".format(str(len(result)))
									ret_ += "\n\nUntuk melihat lyric, silahkan gunakan command {}SearchLyric {}|?number?".format(str(setKey), str(query))
									client.sendMessage(to, ret_)
								elif len(cond) == 2:
									num = int(cond[1])
									if num <= len(result):
										data = result[num - 1]
										with requests.session() as web:
											web.headers["user-agent"] = "Mozilla/5.0"
											url = web.get("https://www.musixmatch.com{}".format(urllib.parse.quote(data["url"])))
											data = BeautifulSoup(url.content, "html5lib")
											for lyricContent in data.findAll("p", {"class":"mxm-lyrics__content "}):
												lyric = lyricContent.text
												client.sendMessage(to, lyric)
						elif cmd.startswith("tr-"):
							sep = text.split("-")
							sep = sep[1].split(" ")
							lang = sep[0]
							if settings["setKey"] == False:
								txt = text.lower().replace("tr-" + lang + " ","")
							else:
								txt = text.lower().replace(settings["keyCommand"] + "tr-" + lang + " ","")
							if lang not in language["googletrans"]:
								return client.sendMessage(to, "Bahasa {} tidak ditemukan".format(lang))
							translator = Translator()
							result = translator.translate(txt, dest=lang)
							client.sendMessage(to, result.text)
						if text.lower() == "mykey":
							client.sendMessage(to, "Keycommand yang diset saat ini : ?{}?".format(str(settings["keyCommand"])))
						elif text.lower() == "setkey on":
							if settings["setKey"] == True:
								client.sendMessage(to, "Setkey telah aktif")
							else:
								settings["setKey"] = True
								client.sendMessage(to, "Berhasil mengaktifkan setkey")
						elif text.lower() == "setkey off":
							if settings["setKey"] == False:
								client.sendMessage(to, "Setkey telah nonaktif")
							else:
								settings["setKey"] = False
								client.sendMessage(to, "Berhasil menonaktifkan setkey")
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
					elif msg.contentType == 1:
						if settings["changePictureProfile"] == True:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cpp.bin".format(time.time()))
							settings["changePictureProfile"] = False
							client.updateProfilePicture(path)
							client.sendMessage(to, "Berhasil mengubah foto profile")
							client.deleteFile(path)
						if msg.toType == 2:
							if to in settings["changeGroupPicture"]:
								path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-cgp.bin".format(time.time()))
								settings["changeGroupPicture"].remove(to)
								client.updateGroupPicture(to, path)
								client.sendMessage(to, "Berhasil mengubah foto group")
								client.deleteFile(path)
					elif msg.contentType == 7:
						if settings["checkSticker"] == True:
							stk_id = msg.contentMetadata['STKID']
							stk_ver = msg.contentMetadata['STKVER']
							pkg_id = msg.contentMetadata['STKPKGID']
							ret_ = "?ÄÄ[ Sticker Info ]"
							ret_ += "\n³ STICKER ID : {}".format(stk_id)
							ret_ += "\n³ STICKER PACKAGES ID : {}".format(pkg_id)
							ret_ += "\n³ STICKER VERSION : {}".format(stk_ver)
							ret_ += "\n³ STICKER URL : line://shop/detail/{}".format(pkg_id)
							ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
							client.sendMessage(to, str(ret_))
					elif msg.contentType == 13:
						if settings["checkContact"] == True:
							try:
								contact = client.getContact(msg.contentMetadata["mid"])
								cover = client.getProfileCoverURL(msg.contentMetadata["mid"])
								ret_ = "?ÄÄ[ Details Contact ]"
								ret_ += "\n³ Nama : {}".format(str(contact.displayName))
								ret_ += "\n³ MID : {}".format(str(msg.contentMetadata["mid"]))
								ret_ += "\n³ Bio : {}".format(str(contact.statusMessage))
								ret_ += "\n³ Gambar Profile : http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus))
								ret_ += "\n³ Gambar Cover : {}".format(str(cover))
								ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
								client.sendImageWithURL(to, "http://dl.profile.line-cdn.net/{}".format(str(contact.pictureStatus)))
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Kontak tidak valid")
					elif msg.contentType == 16:
						if settings["checkPost"] == True:
							try:
								ret_ = "?ÄÄ[ Details Post ]"
								if msg.contentMetadata["serviceType"] == "GB":
									contact = client.getContact(sender)
									auth = "\n³ Penulis : {}".format(str(contact.displayName))
								else:
									auth = "\n³ Penulis : {}".format(str(msg.contentMetadata["serviceName"]))
								purl = "\n³ URL : {}".format(str(msg.contentMetadata["postEndUrl"]).replace("line://","https://line.me/R/"))
								ret_ += auth
								ret_ += purl
								if "mediaOid" in msg.contentMetadata:
									object_ = msg.contentMetadata["mediaOid"].replace("svc=myhome|sid=h|","")
									if msg.contentMetadata["mediaType"] == "V":
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n³ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
											murl = "\n³ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n³ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
											murl = "\n³ Media URL : https://obs-us.line-apps.com/myhome/h/download.nhn?{}".format(str(object_))
										ret_ += murl
									else:
										if msg.contentMetadata["serviceType"] == "GB":
											ourl = "\n³ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(msg.contentMetadata["mediaOid"]))
										else:
											ourl = "\n³ Objek URL : https://obs-us.line-apps.com/myhome/h/download.nhn?tid=612w&{}".format(str(object_))
									ret_ += ourl
								if "stickerId" in msg.contentMetadata:
									stck = "\n³ Stiker : https://line.me/R/shop/detail/{}".format(str(msg.contentMetadata["packageId"]))
									ret_ += stck
								if "text" in msg.contentMetadata:
									text = "\n³ Tulisan : {}".format(str(msg.contentMetadata["text"]))
									ret_ += text
								ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
								client.sendMessage(to, str(ret_))
							except:
								client.sendMessage(to, "Post tidak valid")
			except Exception as error:
				logError(error)


		if op.type == 26:
			try:
				msg = op.message
				text = str(msg.text)
				msg_id = msg.id
				receiver = msg.to
				sender = msg._from
				if msg.toType == 0 or msg.toType == 1 or msg.toType == 2:
					if msg.toType == 0:
						if sender != client.profile.mid:
							to = sender
						else:
							to = receiver
					elif msg.toType == 1:
						to = receiver
					elif msg.toType == 2:
						to = receiver
					if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
						if msg.contentType == 0:
							client.sendMessage(to, text)
						elif msg.contentType == 1:
							path = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-mimic.bin".format(time.time()))
							client.sendImage(to, path)
							client.deleteFile(path)
					if msg.contentType == 0:
						if settings["autoRead"] == True:
							client.sendChatChecked(to, msg_id)
						if sender not in clientMid:
							if msg.toType != 0 and msg.toType == 2:
								if 'MENTION' in msg.contentMetadata.keys()!= None:
									names = re.findall(r'@(\w+)', text)
									mention = ast.literal_eval(msg.contentMetadata['MENTION'])
									mentionees = mention['MENTIONEES']
									for mention in mentionees:
										if clientMid in mention["M"]:
											if settings["autoRespon"] == True:
												client.sendMention(sender, settings["autoResponMessage"], [sender])
											break
						if text is None: return
						if "/ti/g/" in msg.text.lower():
							if settings["autoJoinTicket"] == True:
								link_re = re.compile('(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?')
								links = link_re.findall(text)
								n_links = []
								for l in links:
									if l not in n_links:
										n_links.append(l)
								for ticket_id in n_links:
									group = client.findGroupByTicket(ticket_id)
									client.acceptGroupInvitationByTicket(group.id,ticket_id)
									client.sendMessage(to, "Berhasil masuk ke group %s" % str(group.name))
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								unsend[msg_id] = {"text": text, "from": sender, "time": unsendTime}
							except Exception as error:
								logError(error)
					if msg.contentType == 1:
						if settings["detectUnsend"] == True:
							try:
								unsendTime = time.time()
								image = client.downloadObjectMsg(msg_id, saveAs="LineAPI/tmp/{}-image.bin".format(time.time()))
								unsend[msg_id] = {"from": sender, "image": image, "time": unsendTime}
							except Exception as error:
								logError(error)
			except Exception as error:
				logError(error)

		if op.type == 55:
			if op.param1 in read["readPoint"]:
				if op.param2 not in read["readMember"][op.param1]:
					read["readMember"][op.param1].append(op.param2)


		if op.type == 65:
			try:
				if settings["detectUnsend"] == True:
					to = op.param1
					sender = op.param2
					if sender in unsend:
						unsendTime = time.time()
						contact = client.getContact(unsend[sender]["from"])
						if "text" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "?ÄÄ[ Unsend Message ]"
								ret_ += "\n³ Sender : @!"
								ret_ += "\n³ Time : {} yang lalu".format(sendTime)
								ret_ += "\n³ Type : Text"
								ret_ += "\n³ Text : {}".format(unsend[sender]["text"])
								ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
								client.sendMention(to, ret_, [contact.mid])
								del unsend[sender]
							except:
								del unsend[sender]
						elif "image" in unsend[sender]:
							try:
								sendTime = unsendTime - unsend[sender]["time"]
								sendTime = timeChange(sendTime)
								ret_ = "?ÄÄ[ Unsend Message ]"
								ret_ += "\n³ Sender : @!"
								ret_ += "\n³ Time : {} yang lalu".format(sendTime)
								ret_ += "\n³ Type : Image"
								ret_ += "\n³ Text : None"
								ret_ += "\n?ÄÄÄÄÄÄÄÄÄÄ"
								client.sendMention(to, ret_, [contact.mid])
								client.sendImage(to, unsend[sender]["image"])
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
							except:
								client.deleteFile(unsend[sender]["image"])
								del unsend[sender]
					else:
						client.sendMessage(to, "Data unsend tidak ditemukan")
			except Exception as error:
				logError(error)
		backupData()
	except Exception as error:
		logError(error)

def run():
	while True:
		ops = clientPoll.singleTrace(count=50)
		if ops != None:
			for op in ops:
				try:
					clientBot(op)
				except Exception as error:
					logError(error)
				clientPoll.setRevision(op.revision)

if __name__ == "__main__":
	run()