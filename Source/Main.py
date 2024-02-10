import pandas as pd
import TankBattle
import PySimpleGUI as sg
from psg_reskinner import animated_reskin


#TODO: Add pushguns and ac's with guns on them to the CSV
#TODO: enable save settings
#TODO: actual settings
        #number of iterations to run (be sure to set max)
#TODO: add range as a factor (remember that some ammo like arpg doesn't take range into account)
#TODO: enable user to add custom tanks temporarily/permanently


#imports the csv containing tank stats, turns that into a list, vehicle_1 and vehicle_2 are the currently selected tanks.
#can probably initilalize those somewhere else

# to build the exe run pyinstaller --onefile --noconsole --icon=Source/Vehicle_Combat_Simulator.ico --name=VCS Source/Main.py  in console
# remember to move the vehicle_stats.csv and Vehicle_Combat_Simulator to dist folder
window_name = 'Foxhole Vehicle Combat Simulator v0.1'
icon = 'Vehicle_Combat_Simulator.ico'
stats_file = 'vehicle_stats.csv'
tank_stats_csv = pd.read_csv(stats_file)
vehicle_1 = tank_stats_csv.to_dict('records')[19]
vehicle_2 = tank_stats_csv.to_dict('records')[16]
tank_name_list = tank_stats_csv['name'].tolist()
#starting theme for the window
sg.theme('DarkBlue')
#the list of tanks the user can select from in the gui is selected here
lst1 = sg.Listbox(tank_name_list, size=(40, 7), select_mode='single', key='tank 1', enable_events = True)
lst2 = sg.Listbox(tank_name_list, size=(40, 7), select_mode='single', key='tank 2', enable_events= True)
answer = 'please select your tanks '
menu_def = [
   ['Settings', ['Theme',['Colonial', 'Warden']]],
]



#TODO move the whole GUI aspect to a different python file tbh
#builds the various layout elements that then make up the window
col1 = [
    [sg.Text('Tank 1:', pad=(0,(0,5)))],
    [lst1],
    [sg.Text('Starting Armor %:', pad=(0,(19,0))), sg.Slider(range = (1, 100), default_value= 100, key = 'slider1', orientation='h', size= (20,10), enable_events=True)],
    [sg.HSep()],
    [sg.Text(f'Name: ', key='name1')],
    [sg.Text('Faction:', key='faction1')],
    [sg.Text(f'Hp: ', key='hp1')],
    [sg.Text('Armour:', key='armor1')],
    [sg.Text('Reload time:', key='rof1_a'), sg.Text('Reload time gun 2:', key='rof1_b')],
    [sg.Text('Damage:', key='dmg1_a'), sg.Text('Damage gun 2:', key='dmg1_b')],
    [sg.Text('Pen multiplier', key='penmulti1_a'), sg.Text('Pen multiplier gun 2:', key='penmulti1_b')],
    [sg.Text('Pen chance:', key='penchance1_a'), sg.Text('Pen Chance gun 2:', key='penchance1_b')],
    ]
col2 = [
    [sg.Text('Tank 2:',pad=(0,(0,5)))],
    [lst2],
    [sg.Text('Starting Armor %:', pad=(0,(19,0))), sg.Slider(range = (1, 100), default_value= 100, key = 'slider2', orientation='h', size= (20,10), enable_events=True)],
    [sg.HSep()],
    [sg.Text(f'Name: ', key='name2')],
    [sg.Text('Faction:', key='faction2')],
    [sg.Text(f'Hp: ', key='hp2')],
    [sg.Text('Armour:', key='armor2')],
    [sg.Text('Reload time:', key='rof2_a'), sg.Text('Reload time gun 2:', key='rof2_b')],
    [sg.Text('Damage:', key='dmg2_a'), sg.Text('Damage gun 2:', key='dmg2_b')],
    [sg.Text('Pen multiplier', key = 'penmulti2_a'), sg.Text('Pen multiplier gun 2:', key = 'penmulti2_b')],
    [sg.Text('Pen chance:', key = 'penchance2_a'), sg.Text('Pen Chance gun 2:', key='penchance2_b')],
]

layout = [
    [sg.Menu(menu_def)],
    [sg.Column(col1), sg.VSeperator(), sg.Column(col2, vertical_alignment='t'), sg.VSeperator()],
    [sg.HSep()],
    [sg.Text('Range (m):', pad=(0,(19,0))),
     sg.Slider(range = (0, 50), default_value= 50, key = 'range slider', orientation='h', size= (25,15), enable_events=True),
     sg.Button('Simulate', pad=((150,0),(15,0)))],
    [sg.HSep()],
    [sg.Text(answer, key='Answer')],
          ]
#actual window
window = sg.Window(title=window_name, layout=layout, icon=icon)
armor_start_percent1 = 100
armor_start_percent2 = 100

#these events handle updating various GUI elements as the program recieves imputs.
def event_simulate():
    try:
        tk1_ph = values['tank 1']
        tk2_ph = values['tank 2']
        vehicle_1 = tank_stats_csv.to_dict('records')[tank_name_list.index(tk1_ph[0])]
        vehicle_2 = tank_stats_csv.to_dict('records')[tank_name_list.index(tk2_ph[0])]
        tank_calculation_returns = TankBattle.vehicle_1v1(vehicle_1, vehicle_2, values['range slider'], 1000, values['slider1'],
                                                          values['slider2'], )
        tank1wins = tank_calculation_returns[0]
        tank2wins = tank_calculation_returns[1]
        avgtime = tank_calculation_returns[2]
        tank1_winrate = round((tank1wins/(tank1wins+tank2wins))*100, 2)
        tank2_winrate = round(100 - tank1_winrate, 2)
        window['Answer'].update(
            f'{vehicle_1['name']} winrate: {tank1_winrate}%, {vehicle_2['name']} winrate: {tank2_winrate}%, avg time per fight: {round((avgtime), 1)} s')
    except:
        sg.popup('something went wrong.')
def event_tank_1():
    tk1_ph = values['tank 1']
    vehicle_1 = tank_stats_csv.to_dict('records')[tank_name_list.index(tk1_ph[0])]
    window['name1'].update(f'Name: {vehicle_1['name']}')
    window['hp1'].update(f'Hp: {vehicle_1['hp']}')
    window['armor1'].update(
        f'Armour: {vehicle_1['armor']}, {vehicle_1['base penchance']}%-{vehicle_1['max penchance']}%')
    window['rof1_a'].update(f'Reload time: {vehicle_1['reload+firing']}')
    window['dmg1_a'].update(f'Damage: {vehicle_1['damage']}')
    window['faction1'].update(f'Faction: {vehicle_1['Faction']}')
    window['rof1_b'].update(f'reload time gun 2: {vehicle_1['reload+firing gun 2']}')
    window['dmg1_b'].update(f'Damage gun 2: {vehicle_1['damage gun 2']}')
    if vehicle_1['pen multiplier'] == 5:
        window['penmulti1_a'].update(f'Pen multiplier: 0')
        window['penmulti1_b'].update(f'Pen multiplier gun 2: 0')
    else:
        window['penmulti1_a'].update(f'Pen multiplier: {vehicle_1['pen multiplier']}')
        window['penmulti1_b'].update(f'Pen multiplier gun 2: {vehicle_1['pen multiplier gun 2']}')
    return vehicle_1
def event_tank_2():
    tk2_ph = values['tank 2']
    vehicle_2 = tank_stats_csv.to_dict('records')[tank_name_list.index(tk2_ph[0])]
    window['name2'].update(f'Name: {vehicle_2['name']}')
    window['hp2'].update(f'Hp: {vehicle_2['hp']}')
    window['armor2'].update(
        f'Armour: {vehicle_2['armor']}, {vehicle_2['base penchance']}%-{vehicle_2['max penchance']}%')
    window['rof2_a'].update(f'Reload time: {vehicle_2['reload+firing']}')
    window['dmg2_a'].update(f'Damage: {vehicle_2['damage']}')
    window['faction2'].update(f'Faction: {vehicle_2['Faction']}')
    window['rof2_b'].update(f'reload time gun 2: {vehicle_2['reload+firing gun 2']}')
    window['dmg2_b'].update(f'Damage gun 2: {vehicle_2['damage gun 2']}')
    if vehicle_2['pen multiplier'] == 5:
        window['penmulti2_a'].update(f'Pen multiplier: 0')
        window['penmulti2_b'].update(f'Pen multiplier gun 2: 0')
    else:
        window['penmulti2_a'].update(f'Pen multiplier: {vehicle_2['pen multiplier']}')
        window['penmulti2_b'].update(f'Pen multiplier gun 2: {vehicle_2['pen multiplier gun 2']}')
    return vehicle_2
def update_pen_2():
    #try:
    currarm_1a = (vehicle_2['armor']*(values['slider2']/100))
    stripped_1 = 100-((currarm_1a/vehicle_2['armor'])*100)
    pch1 = round((TankBattle.pen_calculator(vehicle_2['base penchance'], stripped_1, vehicle_2['max penchance'], vehicle_1['pen multiplier'], values['range slider'])), 1)
    window['penchance1_a'].update(f'Pen chance:{pch1}%')
    #except:
        #window['penchance1_a'].update(f'Pen chance:')
    if vehicle_1['pen multiplier gun 2'] > 0:
        currarm_1b = (vehicle_2['armor'] * (values['slider2'] / 100))
        stripped_1a = 100 - ((currarm_1b / vehicle_2['armor']) * 100)
        pch1 = round((TankBattle.pen_calculator(vehicle_2['base penchance'], stripped_1, vehicle_2['max penchance'],
                                                vehicle_1['pen multiplier gun 2'], values['range slider'])), 1)
        window['penchance1_b'].update(f'Pen chance gun 2:{pch1}%')
    else:
        window['penchance1_b'].update(f'Pen chance gun 2:0')
def update_pen_1():
    #try:
    currarm_2a = (vehicle_1['armor']*(values['slider1']/100))
    stripped_2 = 100-((currarm_2a/vehicle_2['armor'])*100)
    pch1 = round((TankBattle.pen_calculator(vehicle_1['base penchance'], stripped_2, vehicle_1['max penchance'], vehicle_2['pen multiplier'], values['range slider'])), 1)

    window['penchance2_a'].update(f'Pen chance:{pch1}%')
    #except:
        #window['penchance2_a'].update(f'Pen chance:')
    if vehicle_2['pen multiplier gun 2'] > 0:
        currarm_2b = (vehicle_1['armor']*(values['slider1']/100))
        stripped_2 = 100-((currarm_2b/vehicle_2['armor'])*100)
        pch1 = round((TankBattle.pen_calculator(vehicle_1['base penchance'], stripped_2, vehicle_1['max penchance'], vehicle_2['pen multiplier gun 2'], values['range slider'])), 1)
        window['penchance2_b'].update(f'Pen chance gun 2:{pch1}%')
    else:
        window['penchance2_b'].update(f'Pen chance gun 2:0')
            #window['penchance2_b'].update(f'Pen chance gun 2:')
#taken psg_reskinner a library, allows chaning the theme of the gui while program is running
def reskin_job(newtheme):
    animated_reskin(
        window=window,
        new_theme=newtheme,
        theme_function=sg.theme,
        lf_table=sg.LOOK_AND_FEEL_TABLE,
    )
    window.TKroot


#for some reason reskinning to current theme makes the theme switcher more stable
reskin_job('DarkBlue')
#print(tank_name_list[0])
#main program loop




while True:
    event, values = window.read()
    if event == 'Simulate':
        event_simulate()
    if event == 'tank 1':
        vehicle_1 = event_tank_1()
        update_pen_1()
        update_pen_2()
    if event == 'tank 2':
        vehicle_2 = event_tank_2()
        update_pen_1()
        update_pen_2()
    if event == 'slider2':
        update_pen_2()
    if event == 'slider1':
        update_pen_1()
    if event == 'range slider':
        update_pen_1()
        update_pen_2()
    if event == 'Colonial':
        sg.theme('DarkGreen')
        reskin_job('DarkGreen')

    if event == 'Warden':
        sg.theme('DarkBlue')
        reskin_job('DarkBlue')
    if event in (None, 'Exit'):
        break
