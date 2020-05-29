'''
Név
Email
Github
Referencia
Végzettség
Kompetenciák
Egyéb
'''

import PySimpleGUI as sg
import sqlite3

#SQL
conn = sqlite3.Connection('project.db')
c = conn.cursor()
c.execute('''
         CREATE TABLE IF NOT EXISTS tb (
                                       Név TEXT,
                                       Email TEXT,
                                       Github TEXT,
                                       Referencia TEXT,
                                       Végzettség TEXT,
                                       Kompetenciák TEXT,
                                       Egyéb TEXT
                                       )
         ''')
conn.commit()

#Grafikus felület
def bevitel(be):
    return [sg.Text(f'{be}:',  size=(15,1)), sg.Input(key=be)]
col1 = sg.Column([
                 [sg.Text()],
                 bevitel('Név'),
                 bevitel('Email'),
                 bevitel('Github'),
                 bevitel('Referencia'),
                 bevitel('Végzettség'),
                 bevitel('Kompetenciák'),
                 bevitel('Egyéb'),
                 [sg.Text()],
                 [sg.Button('Ment'), sg.Button('Keres'),sg.Button('Töröl')]
                 ])
col2 = sg.Column([
                  [sg.Listbox([], size=(30,15), key='eredmény')],
                 ])

layout = [[col1, col2]]
window = sg.Window('Project', layout, font = 'Helvetica 14', default_element_size = (20,1),auto_size_buttons=False)

#Főhurok
while True:
    event, values = window.read()
    if event == None:
        break
    Név          = values['Név']
    Email        = values['Email']
    Github       = values['Github']
    Referencia   = values['Referencia']
    Végzettség   = values['Végzettség']
    Kompetenciák = values['Kompetenciák']
    Egyéb        = values['Egyéb']
    
    if event in ('Ment'):
        if Név and Email:
            c.execute('SELECT Email FROM tb WHERE Email LIKE ?', (Email,))
            x = c.fetchall()
            if x == [(Email,)]:
                window['eredmény'].update([f'{Email} cím már létezik'])
            else:
                c.execute('INSERT INTO tb VALUES (?,?,?,?,?,?,?)', (Név,Email,Github,Referencia,Végzettség,Kompetenciák,Egyéb))
                conn.commit()
                window['Név'].update('')
                window['Email'].update('')
                window['Github'].update('')
                window['Referencia'].update('')
                window['Végzettség'].update('')
                window['Kompetenciák'].update('')
                window['Egyéb'].update('')
            
    if event in ('Keres'):
        Név          = '%' if not Név else '%'+Név+'%'
        Email        = '%' if not Email else '%'+Email+'%'
        Github       = '%' if not Github else '%'+Github+'%'
        Referencia   = '%' if not Referencia else '%'+Referencia+'%'
        Végzettség   = '%' if not Végzettség else '%'+Végzettség+'%'
        Kompetenciák = '%' if not Kompetenciák else '%'+Kompetenciák+'%'
        Egyéb        = '%' if not Egyéb else '%'+Egyéb+'%'
        c.execute('''SELECT * FROM tb WHERE Név LIKE ?
                                        AND Email LIKE ?
                                        AND Github LIKE ?
                                        AND Referencia LIKE ?
                                        AND Végzettség LIKE ?
                                        AND Kompetenciák LIKE ?
                                        AND Egyéb LIKE ?'''
                                        ,(Név,Email,Github,Referencia,Végzettség,Kompetenciák,Egyéb))
        x = c.fetchall()
        window['eredmény'].update(x)