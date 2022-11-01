from tkinter import *
import tkinter.font
import time
from time import strftime
from darksky import forecast
from datetime import date, timedelta
import pandas as pd
from newsapi.articles import Articles
import datetime
import pickle #알아보기
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import math
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import calendar

WIDTH  = 1920
HEIGHT = 1080

# Weather API credentials
key = '93a522f375502ea4e4a091c06d034ff1' # 그 접근할 수 있는 비밀번호 토큰, 비밀번호
ORANGE = 36.27, (126.90)

# News API credentials
apikey = '455e01c84ca44ff387187f10f202bed3'
a = Articles(API_KEY=apikey)

# Calendar SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.largeFont = tkinter.font.Font(family="Piboto", size=70)
        self.mediumFont = tkinter.font.Font(family="Piboto", size=40)
        self.normalFont = tkinter.font.Font(family="Piboto Light", size=20)

    def setupGUI(self): #설치 또는 실행을 검은색 화면을...
        self.grid(row=0, column=0)

        # Weather & news frame to contain weather/news info
        #  날씨와 뉴스의 틀은 날씨와 뉴스의 정보를 포함한다.
        # For weather, column 0 = info, column 1 = icon
        # 날씨에서는 컬럼0= 날씨의 정보 -> 컬럼1은 = 아이콘
        today_weather_frame = Frame(self, width=900, height=1000, bg='black')
        today_weather_frame.grid(row=0, column=0, sticky=W)
        GUI.weather_label1 = Label(today_weather_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.mediumFont, justify=LEFT)
        GUI.weather_label1.grid(row=0, column=0, sticky=NW)
        #행렬 행 열
            #row=가로 , column= 세로
        # Frame and labels to hold the forecast
        weather_news_frame = Frame(self, width=200, height=500, bg='black')
        weather_news_frame.grid(row=1, column=0, sticky=W)

        GUI.weather_label2 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label2.grid(row=1, column=0, sticky=W)
        GUI.weather_label3 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label3.grid(row=2, column=0, sticky=W)
        GUI.weather_label4 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label4.grid(row=3, column=0, sticky=W)
        GUI.weather_label5 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label5.grid(row=4, column=0, sticky=W)
        GUI.weather_label6 = Label(weather_news_frame, text="Loading weather...",fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label6.grid(row=5, column=0, sticky=W)
        GUI.weather_label7 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label7.grid(row=6, column=0, sticky=W)
        GUI.weather_label8 = Label(weather_news_frame, text="Loading weather...", fg='white', bg='black',
                                   font=self.normalFont, justify=LEFT)
        GUI.weather_label8.grid(row=7, column=0, sticky=W)

        icon = PhotoImage(file="weather_icons/partly-cloudy-day.gif")
        icon = icon.subsample(10)

        # Set up labels to hold weather icons
        GUI.icon_label = Label(today_weather_frame, borderwidth=0, image=icon)
        GUI.icon_label.photo = icon
        GUI.icon_label.grid(row=0, column=1, sticky=W)
        GUI.icon_label2 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label2.grid(row=1, column=1, sticky=W)
        GUI.icon_label3 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label3.grid(row=2, column=1, sticky=W)
        GUI.icon_label4 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label4.grid(row=3, column=1, sticky=W)
        GUI.icon_label5 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label5.grid(row=4, column=1, sticky=W)
        GUI.icon_label6 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label6.grid(row=5, column=1, sticky=W)
        GUI.icon_label7 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label7.grid(row=6, column=1, sticky=W)
        GUI.icon_label8 = Label(weather_news_frame, borderwidth=0, image=icon)
        GUI.icon_label8.grid(row=7, column=1, sticky=W)

        # Labels to hold news info
        news_frame = Frame(self, width=400, height=500, bg='black')
        news_frame.grid(row=2, column=0, sticky=W)

        GUI.news_today = Label(news_frame, text="\n오늘의 주요 뉴스:", fg='white', bg='black',
                               font=self.mediumFont, justify=LEFT)
        GUI.news_today.grid(row=0, column=0, sticky=W)

        GUI.news_label1 = Label(news_frame, text="Loading headlines...", fg='white', bg='black',
                                font=self.normalFont, justify=LEFT)
        GUI.news_label1.grid(row=1, column=0, sticky=W)

        GUI.news_label2 = Label(news_frame, text="Loading headlines...", fg='white', bg='black',
                                font=self.normalFont, justify=LEFT)
        GUI.news_label2.grid(row=2, column=0, sticky=W)
        GUI.news_label3 = Label(news_frame, text="Loading headlines...", fg='white', bg='black',
                                font=self.normalFont, justify=LEFT)
        GUI.news_label3.grid(row=3, column=0, sticky=W)
        GUI.news_label4 = Label(news_frame, text="Loading headlines...", fg='white', bg='black',
                                font=self.normalFont, justify=LEFT)
        GUI.news_label4.grid(row=4, column=0, sticky=W)
        GUI.news_label5 = Label(news_frame, text="Loading headlines...", fg='white', bg='black',
                                font=self.normalFont, justify=LEFT)
        GUI.news_label5.grid(row=5, column=0, sticky=W)        


        # Adjust this width for spacing
        frame_placeholder = Frame(self, width=WIDTH/2.8, height=10, bg='black')
        frame_placeholder.grid(row=0, column=1)
        frame_placeholder1 = Frame(self, width=WIDTH/2.8, height=10, bg='black')
        frame_placeholder1.grid(row=1, column=1)

        # Time frame to hold time & date in grid
        time_frame = Frame(self, width=400, height=500, bg='black')
        time_frame.grid(row=0, column=3, sticky=NE)
        GUI.time_label = Label(time_frame, text=strftime("%I:%M %p", time.localtime()), fg='white', bg='black',
                               font=self.largeFont)
        GUI.time_label.grid(row=0, column=0, sticky=NE)

        GUI.date_label = Label(time_frame, text=strftime("%A, %B %d", time.localtime()), fg='white', bg='black',
                               font=self.normalFont)
        GUI.date_label.grid(row=1, column=0, sticky=NE)

        # Frame for calendar info
        calendar_frame = Frame(self, width=400, height=500, bg='black')
        calendar_frame.grid(row=1, column=3, sticky=NE)
        GUI.calendar_label0 = Label(calendar_frame, text='\n일정\n===========', fg='white', bg='black',
                                    font=self.mediumFont)
        GUI.calendar_label0.grid(row=0, column=0, sticky=NE)
        GUI.calendar_label1 = Label(calendar_frame, text='Loading calendar events...', fg='white', bg='black',
                                    font=self.normalFont)
        GUI.calendar_label1.grid(row=1, column=0, sticky=NE)
        GUI.calendar_label2 = Label(calendar_frame, text='Loading calendar events...', fg='white', bg='black',
                                    font=self.normalFont)
        GUI.calendar_label2.grid(row=2, column=0, sticky=NE)
        GUI.calendar_label3 = Label(calendar_frame, text='Loading calendar events...', fg='white', bg='black',
                                    font=self.normalFont)
        GUI.calendar_label3.grid(row=3, column=0, sticky=NE)
        GUI.calendar_label4 = Label(calendar_frame, text='Loading calendar events...', fg='white', bg='black',
                                    font=self.normalFont)
        GUI.calendar_label4.grid(row=4, column=0, sticky=NE)
        GUI.calendar_label5 = Label(calendar_frame, text='Loading calendar events...', fg='white', bg='black',
                                    font=self.normalFont)
        GUI.calendar_label5.grid(row=5, column=0, sticky=NE)

        self.configure(background='black')

    def updateGUI(self):
        # Constantly updates the time until the program is stopped
        GUI.time_label.configure(text=strftime("%I:%M %p", time.localtime()))
        GUI.date_label.configure(text=strftime("%A, %B %d", time.localtime()))

        window.after(1000, mirror.updateGUI)

    def updateWeather(self):
        # Updates the weather information
        weekday = date.today()
        daily_summary = ''
        weather_today = ''
        weather_list = []
        today_icon = ''
        icons_list = []

        # Gets weather info
        # 날씨 정보 얻기
        # 숫자 세기
        counter = 0
        
        with forecast(key, *ORANGE) as orange:
            daily_summary += orange.daily.summary
            for day in orange.daily: #매일 매일 반복 업데이트
                day = dict(day=date.strftime(weekday, '%a'),
                           sum=day.summary,
                           #최저온도
                           tempMin=math.trunc((day.temperatureMin-32)*(5/9)),
                           #최고온도
                           tempMax=math.trunc((day.temperatureMax-32)*(5/9)),
                           icon=day.icon
                           )
                # Save each of these in a list to display to GUI
                if counter == 0:
                    weather_today += ('Today: HIGH {tempMax}°C | Low {tempMin}°C'.format(**day))

                    today_icon = ('{icon}'.format(**day))
                    weekday += timedelta(days=1)
                    counter += 1
                else:
                    # t = ['월','화','']
                    # weekdays= calendar.weekday(datetime.datetime.now(day))
    
                    weather_list.append('========================\n{day}: High {tempMax}°C | Low {tempMin}°C'.format(**day)) #incoding -> decoding / incoding -> decoding
                    icons_list.append('{icon}'.format(**day))
                    weekday += timedelta(days=1)
                    counter += 1 #월요일 여기 쪼개보기

        GUI.weather_label1.configure(text=weather_today)

        # Set icon for weather today
        #아이콘의 경로 설정, 형식 설정
        icon_path = 'weather_icons/' #아이콘 이미지 경로
        today_icon += '.gif' #아이콘을 더해서 갖다 넣는다?
        icon_path += today_icon # 'weather_icons/today_icon'
        icon = PhotoImage(file=icon_path)
        #subsample 아이콘 크기 수정 x,y에대한 픽셀 값
        icon = icon.subsample(9)
        #이미지를 화면에 띄우는 작업
        GUI.icon_label.configure(image=icon)
        GUI.icon_label.photo = icon

        # Push updated weather info to each label along with icons
        for x in range(0, len(weather_list)):
            temp_icon_path = 'weather_icons/'
            temp_icon_name = icons_list[x]
            temp_icon_name += '.gif' 
            temp_icon_path += temp_icon_name
            temp_icon = PhotoImage(file=temp_icon_path)
            temp_icon = temp_icon.subsample(15)

            if x == 0:
                GUI.weather_label2.configure(text='•'+weather_list[x])
                GUI.icon_label2.configure(image=temp_icon)
                GUI.icon_label2.photo = temp_icon
            if x == 1:
                GUI.weather_label3.configure(text='•'+weather_list[x])
                GUI.icon_label3.configure(image=temp_icon)
                GUI.icon_label3.photo = temp_icon
            if x == 2:
                GUI.weather_label4.configure(text='•'+weather_list[x])
                GUI.icon_label4.configure(image=temp_icon)
                GUI.icon_label4.photo = temp_icon
            if x == 3:
                GUI.weather_label5.configure(text='•'+weather_list[x])
                GUI.icon_label5.configure(image=temp_icon)
                GUI.icon_label5.photo = temp_icon
            if x == 4:
                GUI.weather_label6.configure(text='•'+weather_list[x])
                GUI.icon_label6.configure(image=temp_icon)
                GUI.icon_label6.photo = temp_icon
            if x == 5:
                GUI.weather_label7.configure(text='•'+weather_list[x])
                GUI.icon_label7.configure(image=temp_icon)
                GUI.icon_label7.photo = temp_icon
            if x == 6:
                GUI.weather_label8.configure(text='•'+weather_list[x])
                GUI.icon_label8.configure(image=temp_icon)
                GUI.icon_label8.photo = temp_icon

        window.after(50000000, mirror.updateWeather)

    def updateNews(self):

        url = 'https://media.naver.com/press/052/ranking?type=popular'

        response = requests.get(url)
        title_new_list = []

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            ul = soup.select_one('ul.press_ranking_list')
            titles = ul.select('li>a>div>strong')
            counter = 0
            for title in titles:
                
                counter +=1
                print(str(counter)+". "+title.get_text())
                title_new_list.append(title.get_text())
        


        else : 
            print(response.status_code)
        
        GUI.news_label1.configure(text='•'+title_new_list[0])
        GUI.news_label2.configure(text='•'+title_new_list[1])
        GUI.news_label3.configure(text='•'+title_new_list[2])
        GUI.news_label4.configure(text='•'+title_new_list[3])
        GUI.news_label5.configure(text='•'+title_new_list[4])


        window.after(50000000, mirror.updateNews)

    def updateCalendar(self):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=7, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        event_list = []
        if not events:
            print('정보가 발견되지 않았습니다.')
        for event in events:
            event_str = ''
            start = event['start'].get('dateTime', event['start'].get('date')) # 시작하는 날짜 얻기
            start = start[0:10] # Remove unnecessary characters at end of string # 날짜 데이터 슬라이싱
            print
            year = start.find('-') # year찾기
            start_day = datetime.datetime.strptime(start, '%Y-%m-%d').strftime('%a %b %d') #
            event_date = start[year + 1:year + 6]
            summary = event['summary'] # Remove emojis
            event_str += summary + ' | ' + start_day
            event_list.append(event_str)


        # Update calendar text
        GUI.calendar_label1.configure(text=event_list[0])
        GUI.calendar_label2.configure(text=event_list[1])
        GUI.calendar_label3.configure(text=event_list[2])
        GUI.calendar_label4.configure(text=event_list[3])
        GUI.calendar_label5.configure(text=event_list[4])

        window.after(500000000, mirror.updateCalendar)

def close_escape(event=None):
    print('Smart mirror closed')
    window.destroy()


window = Tk()
window.title("Smart Mirror")
window.geometry('1920x1080')
window.configure(background='black') #bg

#Removes borders from GUI and implements quit via esc
window.overrideredirect(1)
window.overrideredirect(0)
window.attributes("-fullscreen", True)
window.wm_attributes("-topmost", 1)
window.focus_set()

window.bind("<Escape>", close_escape)

mirror = GUI(window)
mirror.setupGUI()
window.after(1000, mirror.updateGUI)
window.after(1000, mirror.updateWeather)
window.after(1000, mirror.updateNews())
window.after(1000, mirror.updateCalendar())
window.mainloop()
