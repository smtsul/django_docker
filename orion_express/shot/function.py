from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from TimeWithFrames import TimeWithFrames
import os


def test(path, name):
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'xml')
    bxf_data_elements = soup.find_all('BxfData')
    schedule_name_element = soup.find('ScheduleName')
    schedule_name_value = schedule_name_element.text if schedule_name_element else 'shot_error'  # TODO обрезать
    print(schedule_name_value)
    ''' готовим основу для xml'''
    playlist = ET.Element("Playlist")
    playlist.set("Name", name + schedule_name_value)
    playlist.set("Version", "7.1")
    playlist.set("xsi:noNamespaceSchemaLocation", "APPlayList.xsd")
    playlist.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    playlist.set("xmlns:xsd", "http://www.w3.org/2001/XMLSchema")
    content = ET.SubElement(playlist, "Content")
    comment = ET.SubElement(content, "Comment")
    comment.set("Name", name)
    for bxf_data in bxf_data_elements:
        action = bxf_data.get('action')
        scheduled_event_elements = bxf_data.find_all('ScheduledEvent')
        for scheduled_event in scheduled_event_elements:
            event_type = scheduled_event.find('EventData').get('eventType')
            if event_type == 'Primary':
                layer = 1  # идеальное место для обнуления слоя
                # print(scheduled_event)
                clip = ET.SubElement(content, "Clip")
                clip.set("Name", scheduled_event.find('EventTitle'))  # ToDO Надо ли ставить urn:uuid?
                clip.set('StartType', 'UNLOCK')  # TODO разобраться когда ставить unlock, когда HardDateTime
                clip.set('StartDate', scheduled_event.find('StartDateTime').find('SmpteDateTime').get('broadcastDate'))
                clip.set('StartTime', scheduled_event.find('StartDateTime').find('SmpteTimeCode').text)
                temp_time_clip = TimeWithFrames(scheduled_event.find('StartDateTime').find('SmpteTimeCode').text)#сразу переводим в мой класс, чтобы после отнять
                clip.set('Duration', scheduled_event.find('SmpteDuration').find('SmpteTimeCode').text)
                # tc_in = event_data.find('SOM').find('SmpteTimeCode').text
                smpte_time_code = scheduled_event.find('StartDateTime').find('SmpteTimeCode').text
                clip.set('TCIn',scheduled_event.find('Media').find('MediaLocation').find('SOM').find('SmpteTimeCode').text)
                clip.set('Logo', 'On')  # TODO разобраться когда ставить on, когда off
                clip.set('ExtID', 'shot_' + scheduled_event.find('ContentId').find('HouseNumber').text)
                # print('ExtID', scheduled_event.find('ContentId').find('HouseNumber').text)
            if event_type == 'NonPrimary': # ToDO разобраться с переходной графикой почему она в некоторых местах отрицательная?
                graphics = ET.SubElement(clip, 'Graphics')
                graphics.set('OffsetType',
                             "Start")  # TODO разобраться когда старт, когда end, возможно если есть params->end
                temp_time_graphics = TimeWithFrames(scheduled_event.find('StartDateTime').find('SmpteTimeCode').text)
                temp_time_graphics.subtract_time(temp_time_clip)
                graphics.set('Offset', str(temp_time_graphics))
                graphics.set('Layer', str(layer))
                layer += 1
                if layer > 5: layer = 1
                graphics.set('Duration', scheduled_event.find('SmpteDuration').find('SmpteTimeCode').text)
                temp_ext_id=scheduled_event.find('ContentId').find('HouseNumber').text
                if temp_ext_id=='shot_shotsmoking.tga': #ToDo возможно тут идет обращение к БД
                    graphics.set('ExtID','Shot_NoSmoke')
                elif temp_ext_id=='shot_+18.tga':
                    graphics.set('ExtID', 'Shot_18+')
                elif temp_ext_id=='shottv_next.tga':
                    graphics.set('ExtID','shot_nextmark_2022')
                    # params = ET.SubElement('ExtID','Params')
                    print(scheduled_event.find('NonPrimaryEvent').findall('Macros').text)
                    # params.set(scheduled_event.findall('Macros').find('MacroParameterString').text)
                    # params.set(scheduled_event.find('Macros').find('MacroParameterString').text)
                else:
                    graphics.set('ExtID', 'shot_' + scheduled_event.find('ContentId').find('HouseNumber').text)
                graphics.set('Name', scheduled_event.find('EventTitle'))


    tree = ET.ElementTree(playlist)
    xml_str = ET.tostring(playlist, encoding="utf-8").decode("utf-8")

    # Сохранение XML в файл
    path_out = r'C:\Users\User\PycharmProjects\django_docker\orion_express\shot\temp\output\\' #TODO в проде изменить путь
    if not os.path.exists(path_out):
        try:
            os.makedirs(path_out)
        except OSError as e:
            print("Ошибка при создании пути:", str(e))
    else:
        with open(path_out + '\\' + schedule_name_value + ".xml", "w", encoding="utf-8") as file:
            file.write(xml_str)


if __name__ == '__main__':
    path = r'C:\Users\User\PycharmProjects\django_docker\orion_express\shot\temp\input\\' #TODO в проде изменить путь
    playlist = r'2024_02_29_ESAIR.XML'
    test(path + playlist, 'Shot')
