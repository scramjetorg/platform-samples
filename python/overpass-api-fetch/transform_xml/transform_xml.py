import xml.etree.ElementTree as ET


def transform_xml_data(xml_string):
    tags_to_keep = ['bounds', 'nd']
    attr_to_keep = ['height', 'building']
    xml = ET.fromstring(xml_string)

    for way in xml.findall('way'):
        # remove all 'ref=' elements
        for nd in way.findall('nd'):
            del nd.attrib['ref']

        # remove all other tags except the specified ones
        for tag in way.findall('tag'):
            if tag.attrib.get('k') not in attr_to_keep:
                way.remove(tag)
            else:
                tags_to_keep.append(tag.tag)

        for tag in way:
            if tag.tag not in tags_to_keep:
                way.remove(tag)

    # convert the modified XML to string
    out_xml = ET.tostring(xml, encoding='utf-8')
    return out_xml
