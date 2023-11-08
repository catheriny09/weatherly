import requests
import openai
import tools
import wx

# Put this on a timer with a ui that refreshes every minute?

class Weather_Frame(wx.Frame):    
    def __init__(self):
        self.openai_key, self.weather_key = tools.fetchKeys()
        
        super().__init__(parent=None, title='Weatherly')
        panel = wx.Panel(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel, size=(250, -1), style=wx.TE_CENTRE, pos=(5, 5))
        sizer.Add(self.text_ctrl, 0, wx.ALL | wx.CENTER, 5)
        
        button = wx.Button(panel, label='Select', pos=(5, 5))
        button.Bind(wx.EVT_BUTTON, self.on_press)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 5) 
        
        self.w_text_ctrl = wx.TextCtrl(panel, size=(300, 300), style=wx.TE_READONLY, pos=(5,5)) 
        sizer.Add(self.w_text_ctrl, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(sizer)
        
        self.CreateStatusBar()

        self.Show()
        
    def on_press(self, event):
        city = self.text_ctrl.GetValue()
        
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_key}'
        openai.api_key = self.openai_key

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            temp = temp - 273.15
            temp = "{0:.2f}".format(temp)
                
            desc = data['weather'][0]['description']
                
            prompt = f'Temperature: {temp} C Description: {desc}\n'
                
            response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"What should I wear in this weather? Please give a short list:{prompt}",
                    max_tokens=1024,
                    temperature=0.5,
                )
                
            res = response.choices[0].text
            output = (f'Temperature: {temp} C\nDescription: {desc}\n\n {res}')
            self.w_text_ctrl.SetLabelText(output)
                
        else:
            print('Error fetching weather data')

def app():
    window = wx.App()
    frame = Weather_Frame()
    window.MainLoop()
        
app()