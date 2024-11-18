import multiprocessing
import os
import json
import time
from lxml import etree

wb_data = """<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank updated="yes">2</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank updated="yes">5</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank updated="yes">69</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>"""

if __name__ == "__main__":
    html = etree.HTML(wb_data)
    html_data = html.xpath('//*[@name="Panama"]')

    for i in range(len(html_data)):
        print(etree.tostring(html_data[0], pretty_print=True, encoding='utf8').decode('utf8'))
