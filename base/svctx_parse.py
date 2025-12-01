import xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx
from utils.logger_util import logger


def parse_event_record(xml_str):
    root = ET.fromstring(xml_str)
    # 定义命名空间
    ns = {
        "ns": "http://schemas.microsoft.com/win/2004/08/events/event"
    }

    system = root.find("ns:System", ns)
    event_id = system.find("ns:EventID", ns).text
    level = system.find("ns:Level", ns).text if system.find("ns:Level", ns) is not None else "N/A"
    time_created = system.find("ns:TimeCreated", ns).attrib["SystemTime"]
    provider = system.find("ns:Provider", ns).attrib["Name"]

    # 可选：提取事件描述（在 EventData 中，但不一定有可读消息）
    # 实际消息通常需要事件模板（来自系统），这里仅展示原始数据
    event_data = root.find("ns:EventData", ns)
    data = {}
    if event_data is not None:
        for data_item in event_data.findall("ns:Data", ns):
            name = data_item.attrib.get("Name", "Unknown")
            data[name] = data_item.text or ""

    return {
        "TimeCreated": time_created,
        "EventID": event_id,
        "Level": level,
        "Provider": provider,
        "EventData": data
    }

if __name__ == '__main__':
    # 使用示例
    evtx_path = r"D:\System.evtx"
    match_id = False
    match_Provider = False
    match_case_3 = False
    with Evtx(evtx_path) as log:
        for i, record in enumerate(log.records()):
            if i >= 10:  # 仅显示前10条
                pass
            try:
                parsed = parse_event_record(record.xml())
                # print(f"Time: {parsed['TimeCreated']}")
                # print(f"EventID: {parsed['EventID']}")
                # print(f"Level: {parsed['Level']}")
                # print(f"Provider: {parsed['Provider']}")
                # print("-" * 50)
                if '41' in parsed['EventID']:
                    match_id = True
                if 'BugcheckCode:0x0' in parsed['Provider']:
                    match_Provider = True
                if match_id and match_Provider:
                    match_case_3 = True
                    break

            except Exception as e:
                logger.info(f"解析错误: {e}")

    logger.info(f'match_case_3:{match_case_3}')