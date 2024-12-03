import re
import requests

# 定义输入 URL 和输出文件
input_url = 'https://jasonml.xyz/m3u/aptv.m3u'
output_file = 'MediaBrowser.Channels.IPTV.xml'

# 初始化 XML 文件内容
xml_content = '''<?xml version="1.0"?>
<PluginConfiguration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <Bookmarks>
'''

# 从 URL 获取 M3U 文件内容
response = requests.get(input_url)
lines = response.text.splitlines()

# 解析 M3U 文件并转换为 XML
for i in range(len(lines)):
    if lines[i].startswith('#EXTINF'):
        name_match = re.search(r'tvg-name="([^"]+)"', lines[i])
        logo_match = re.search(r'tvg-logo="([^"]+)"', lines[i])
        if name_match and logo_match:
            name = name_match.group(1)
            logo = logo_match.group(1)
            path = lines[i + 1].strip()
            
            # 替换 & 为 &amp;
            name = name.replace('&', '&amp;')
            logo = logo.replace('&', '&amp;')
            path = path.replace('&', '&amp;')
            
            xml_content += f'''    <Bookmark>
      <Name>{name}</Name>
      <Image>{logo}</Image>
      <Path>{path}</Path>
      <Protocol>Http</Protocol>
      <UserId>bba9781c0268471fbcc5b47cc9a2cd30</UserId>
    </Bookmark>
'''

# 结束 XML 文件内容
xml_content += '''  </Bookmarks>
</PluginConfiguration>
'''

# 写入 XML 文件
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(xml_content)

print(f"转换完成，输出文件为 {output_file}")