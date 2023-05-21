import datetime as dt
import datetime

class weatherObject:
    units = "" #standard, metric, imperial
    array=[]
    date_table={}
    table ={}
    jsonData=""
    timezone_shift = ""

    def __init__(self):
        self.current_temp=""
        self.humidity=""
        self.weather=""
        self.weatherDescription=""
        self.wind=""
        self.date="" 
        
    def __init__(self,current_temp,humidty,weather,wd,wind,date,id):
        self.temp=current_temp
        self.humidity=humidty
        self.weather=weather
        self.weatherDescription=wd
        self.wind=wind
        self.date=date
        self.id = id
        
    def jsonParse():
        weatherObject.array=[]
        weatherObject.timezone_shift = weatherObject.jsonData["city"]["timezone"]
        for i,v in enumerate (weatherObject.jsonData["list"]):
            #temp=str(round(v["main"]["temp"]))+ chr(176)+Api.get_metric() #temp
            temp=round(v["main"]["temp"])
            id = (v["weather"][0]["id"])
            humidity=str(v["main"]["humidity"]) # humidity
            weather=(v["weather"][0]["main"]) #description
            weatherDescription=(v["weather"][0]["description"]) #description
            wind=str(round(v["wind"]["speed"])) #wind speed
            date=str(v["dt_txt"]) #date
            d =dt.datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
            d=d + dt.timedelta(0,weatherObject.timezone_shift)
            node = weatherObject(temp,humidity,weather,weatherDescription,wind,d,id)
            #print(type(node.temp),type(node.humidity),type(node.weather),type(node.weatherDescription),type(node.wind),type(node.date),'\n',node)
            weatherObject.array.append(node) 
        weatherObject.dateSort()
        return
    
    def get_date(offset):
        now = datetime.datetime.now().date()
        try:
            n=(list(weatherObject.table.keys())[offset],"dates")
            p = n[0]
            p=datetime.datetime.strptime(p,"%Y-%m-%d")
            p= p.strftime("%b %#d")
            return p
        except: 
            now = now + datetime.timedelta(days = offset + 1)
            return now.strftime("%b %#d")
        
    
    """
    @staticmethod
    def convert_time(date):
    #expressed as 24 hour clock
    #get time from date
    #convert to 12hour clock am/pm
        time = dt.datetime.strftime(date,"%H:%M")
        hour=int(time[0:2])
        if hour > 12:
            postfix = "PM"
            hour = int(hour%12)
        else:
            postfix = "AM"
        res = str(hour) + " " + postfix
        return res
       """ 
        

    @staticmethod
    def dateSort():
        #group nodes by date
        #grab nodes
        arr=[]
        main = []
        weatherObject.date_table={}
        current = weatherObject.array[0].date
        current = dt.datetime.strftime(current,'%Y-%m-%d')

        for i in weatherObject.array:
            date = dt.datetime.strftime(i.date,'%Y-%m-%d')
            if date == current:
                arr.append(i)
            else:
                current = date
                main.append(arr)
                arr = []
            
            if date not in weatherObject.date_table:
                weatherObject.date_table[date]=[i]
            else:weatherObject.date_table[date].append(i)
        main.append(arr)
        count = 0
        weatherObject.table = weatherObject.date_table
        
        arr = []
        for i,v in weatherObject.date_table.items():
            #print(i,"\n",weatherObject.date_table[i],"\n"
            #)
            arr.append(weatherObject.table[i])

            count +=1
        #print("printing arr", arr[0])
        pass
        #after date table made
        #make another table
        #index as keys
        pass

    def __str__(self):
        return f"\nTemp: {self.temp} \nHumidty: {self.humidity} \nDescription: {self.weather} \nDescription2: {self.weatherDescription} \nWind: {self.wind}\nDate:{self.date}\nID:{self.id}\n"
    def __repr__(self):
            return f"\nTemp: {self.temp} \nHumidty: {self.humidity} \nDescription: {self.weather} \nDescription2: {self.weatherDescription} \nWind: {self.wind}\nDate:{self.date}\nID: {self.id}\n"
    pass