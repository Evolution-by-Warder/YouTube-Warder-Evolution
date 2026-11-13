HOME_SKIN = """
<screen name="WarderYouTubeHome" position="0,0" size="1920,1080" title="YouTube Warder Evolution" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;44" foregroundColor="#FFFFFF" transparent="1" zPosition="4"/>
  <widget name="version" position="0,0" size="1,1" font="Regular;27" foregroundColor="#6CCBFF" transparent="1" halign="right" zPosition="4"/>
  <eLabel position="22,153" size="351,825" backgroundColor="#122C47"/>
  <eLabel position="22,153" size="351,5" backgroundColor="#087EC7"/>
  <widget name="nav_focus0" position="35,171" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav0" position="120,180" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus1" position="35,251" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav1" position="120,260" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus2" position="35,331" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav2" position="120,340" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus3" position="35,411" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav3" position="120,420" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus4" position="35,491" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav4" position="120,500" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus5" position="35,571" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav5" position="120,580" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus6" position="35,651" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav6" position="120,660" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus7" position="35,731" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav7" position="120,740" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <!-- Eight small native picons (shared on all language settings). -->
  <ePixmap position="48,175" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_0.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,255" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_1.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,335" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_2.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,415" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_3.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,495" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_4.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,575" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_5.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,655" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_6.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,735" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_7.png" alphatest="on" zPosition="5"/>
  <eLabel position="394,153" size="1490,825" backgroundColor="#10263E"/>
  <eLabel position="394,153" size="1490,5" backgroundColor="#087EC7"/>
  <widget name="heading" position="426,167" size="1050,63" font="Regular;45" foregroundColor="#FFFFFF" transparent="1" zPosition="4"/>
  <widget name="subtitle" position="427,231" size="1324,45" font="Regular;27" foregroundColor="#6CCBFF" transparent="1" zPosition="4"/>
  <widget name="preview_focus0" position="413,285" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel0" position="418,290" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb0" position="446,295" size="410,230" zPosition="4"/>
  <widget name="preview_title0" position="427,529" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel0" position="427,581" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus1" position="902,285" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel1" position="907,290" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb1" position="935,295" size="410,230" zPosition="4"/>
  <widget name="preview_title1" position="916,529" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel1" position="916,581" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus2" position="1391,285" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel2" position="1396,290" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb2" position="1424,295" size="410,230" zPosition="4"/>
  <widget name="preview_title2" position="1405,529" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel2" position="1405,581" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus3" position="413,615" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel3" position="418,620" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb3" position="446,625" size="410,230" zPosition="4"/>
  <widget name="preview_title3" position="427,859" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel3" position="427,911" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus4" position="902,615" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel4" position="907,620" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb4" position="935,625" size="410,230" zPosition="4"/>
  <widget name="preview_title4" position="916,859" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel4" position="916,911" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus5" position="1391,615" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel5" position="1396,620" size="467,314" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb5" position="1424,625" size="410,230" zPosition="4"/>
  <widget name="preview_title5" position="1405,859" size="444,52" font="Regular;23" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel5" position="1405,911" size="444,22" font="Regular;20" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="detail0" position="449,290" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail1" position="449,386" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail2" position="449,482" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail3" position="449,578" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail4" position="449,674" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail5" position="449,770" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="preview_message" position="450,300" size="1360,350" font="Regular;32" foregroundColor="#C6DCEE" transparent="1" zPosition="4"/>
  <widget name="status" position="427,938" size="1410,28" font="Regular;20" foregroundColor="#6CCBFF" transparent="1" zPosition="4"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="22,153" size="351,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="22,976" size="351,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="22,153" size="2,825" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="371,153" size="2,825" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="394,153" size="1490,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="394,976" size="1490,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="394,153" size="2,825" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1882,153" size="2,825" backgroundColor="#168BAF" zPosition="2"/>

  <widget name="preview_border0" position="413,285" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
  <widget name="preview_border1" position="902,285" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
  <widget name="preview_border2" position="1391,285" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
  <widget name="preview_border3" position="413,615" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
  <widget name="preview_border4" position="902,615" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
  <widget name="preview_border5" position="1391,615" size="477,324" foregroundColor="#188EAB" backgroundColor="#188EAB" transparent="0" zPosition="1"/>
</screen>
"""


SEARCH_SKIN = """
<screen name="WarderYouTubeSearch" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="query" position="65,160" size="1755,57" font="Regular;35" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="44,215" size="1832,636" backgroundColor="#122C47"/>
  <widget name="results" position="68,240" size="1778,570" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" itemHeight="60" scrollbarMode="showOnDemand" zPosition="3"/>
  <widget name="details" position="65,868" size="1730,44" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="status" position="65,922" size="1780,42" font="Regular;25" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="44,215" size="1832,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="44,849" size="1832,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="44,215" size="2,636" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1874,215" size="2,636" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""

SETTINGS_SKIN = """
<screen name="WarderYouTubeSettings" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Settings" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="description" position="61,158" size="1762,80" font="Regular;31" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="49,251" size="878,370" backgroundColor="#122C47"/>
  <eLabel position="949,251" size="920,370" backgroundColor="#122C47"/>
  <eLabel position="49,251" size="878,5" backgroundColor="#087EC7"/>
  <eLabel position="949,251" size="920,5" backgroundColor="#137A77"/>
  <widget name="section_search" position="76,277" size="830,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="key_state" position="76,361" size="812,110" font="Regular;31" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="section_playback" position="976,277" size="842,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="quality" position="976,361" size="845,66" font="Regular;32" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="resolver_state" position="976,453" size="824,110" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="49,645" size="1820,233" backgroundColor="#10263E"/>
  <eLabel position="49,645" size="1820,5" backgroundColor="#8B6F40"/>
  <widget name="section_privacy" position="77,666" size="1640,53" font="Regular;32" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="warning" position="77,727" size="1657,105" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="status" position="56,909" size="1775,56" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="49,251" size="878,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,619" size="878,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,251" size="2,370" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="925,251" size="2,370" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="949,251" size="920,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="949,619" size="920,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="949,251" size="2,370" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1867,251" size="2,370" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="49,645" size="1820,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,876" size="1820,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,645" size="2,233" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1867,645" size="2,233" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


GRID_SKIN = """
<screen name="WarderYouTubeGrid" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Videos" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;41" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="heading" position="1045,148" size="814,48" font="Regular;29" foregroundColor="#36B9FF" transparent="1" halign="right" zPosition="3"/>
  <eLabel position="0,153" size="321,846" backgroundColor="#102A45"/>
  <eLabel position="18,157" size="288,6" backgroundColor="#087EC7"/>
  <eLabel position="18,337" size="288,2" backgroundColor="#315676"/>
  <eLabel position="18,640" size="288,2" backgroundColor="#315676"/>
  <eLabel position="322,153" size="2,846" backgroundColor="#315676"/>
  
    <widget name="side0" position="26,174" size="274,54" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side1" position="26,234" size="272,54" font="Regular;27" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side2" position="26,360" size="271,51" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side3" position="26,417" size="272,190" font="Regular;25" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side4" position="26,665" size="270,50" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side5" position="26,724" size="270,77" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side6" position="26,835" size="273,109" font="Regular;24" foregroundColor="#C6DCEE" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  <eLabel position="355,197" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus0" position="355,197" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb0" position="362,204" size="476,249" zPosition="2"/>
  <widget name="title0" position="364,466" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel0" position="364,527" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="868,197" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus1" position="868,197" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb1" position="875,204" size="476,249" zPosition="2"/>
  <widget name="title1" position="877,466" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel1" position="877,527" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="1381,197" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus2" position="1381,197" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb2" position="1388,204" size="476,249" zPosition="2"/>
  <widget name="title2" position="1390,466" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel2" position="1390,527" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="355,575" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus3" position="355,575" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb3" position="362,582" size="476,249" zPosition="2"/>
  <widget name="title3" position="364,844" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel3" position="364,905" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="868,575" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus4" position="868,575" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb4" position="875,582" size="476,249" zPosition="2"/>
  <widget name="title4" position="877,844" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel4" position="877,905" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="1381,575" size="491,364" backgroundColor="#142C47"/>
  <widget name="focus5" position="1381,575" size="491,364" backgroundColor="#087EC7" zPosition="1"/>
  <widget name="thumb5" position="1388,582" size="476,249" zPosition="2"/>
  <widget name="title5" position="1390,844" size="473,57" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel5" position="1390,905" size="473,28" font="Regular;22" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <widget name="status" position="358,953" size="1460,43" font="Regular;25" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <eLabel position="0,999" size="1920,81" backgroundColor="#142C47"/>
  <widget name="footer" position="28,1014" size="1880,52" font="Regular;24" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="355,197" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="355,559" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="355,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="844,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>

  <eLabel position="355,575" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="355,937" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="355,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="844,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>

  <eLabel position="868,197" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="868,559" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="868,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1357,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>

  <eLabel position="868,575" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="868,937" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="868,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1357,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>

  <eLabel position="1381,197" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1381,559" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1381,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1870,197" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>

  <eLabel position="1381,575" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1381,937" size="491,2" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1381,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
  <eLabel position="1870,575" size="2,364" backgroundColor="#1AB4D5" zPosition="5"/>
</screen>
"""


UPDATE_CHECK_SKIN = """
<screen name="WarderYouTubeUpdateCheck" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Updates" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <eLabel position="43,204" size="1834,748" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="status" position="72,230" size="1750,110" font="Regular;37" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="detail" position="72,385" size="1750,185" font="Regular;30" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="42,1013" size="1820,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,204" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

UPDATE_SKIN = """
<screen name="WarderYouTubeUpdateProgress" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Update progress" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <eLabel position="43,204" size="1834,748" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="version" position="72,180" size="1650,62" font="Regular;37" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="phase" position="72,290" size="1670,66" font="Regular;33" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="progress" position="72,405" size="1550,34" borderWidth="1" zPosition="3"/>
  <widget name="percentage" position="1660,390" size="160,62" font="Regular;31" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="detail" position="72,510" size="1720,170" font="Regular;30" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="42,1013" size="1830,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,204" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

LIBRARY_SKIN = """
<screen name="WarderYouTubeLibrary" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Saved videos" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <eLabel position="43,204" size="1834,748" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <widget name="subtitle" position="55,153" size="1740,45" font="Regular;32" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="results" position="50,218" size="1810,625" font="Regular;30" itemHeight="62" foregroundColor="#FFFFFF" backgroundColor="#142C47" scrollbarMode="showOnDemand" zPosition="3"/>
  <widget name="status" position="55,874" size="1790,93" font="Regular;28" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="38,1013" size="1840,54" font="Regular;25" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,204" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,204" size="2,748" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

KEYBOARD_SKIN = """
<screen name="WarderYouTubeKeyboard" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Keyboard" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <eLabel position="197,153" size="1526,158" backgroundColor="#122C47"/>
  <eLabel position="197,153" size="1526,5" backgroundColor="#087EC7"/>
  <widget name="title" position="229,168" size="1456,62" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="input" position="235,247" size="1410,51" font="Regular;31" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="hint" position="210,326" size="1490,44" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="197,380" size="1526,505" backgroundColor="#10263E"/>
  <eLabel position="221,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus0" position="221,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter0" position="225,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus1" position="370,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter1" position="374,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus2" position="519,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter2" position="523,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus3" position="668,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter3" position="672,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus4" position="817,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter4" position="821,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus5" position="966,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter5" position="970,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus6" position="1115,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter6" position="1119,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus7" position="1264,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter7" position="1268,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus8" position="1413,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter8" position="1417,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,405" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus9" position="1562,405" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter9" position="1566,413" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus10" position="221,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter10" position="225,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus11" position="370,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter11" position="374,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus12" position="519,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter12" position="523,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus13" position="668,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter13" position="672,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus14" position="817,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter14" position="821,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus15" position="966,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter15" position="970,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus16" position="1115,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter16" position="1119,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus17" position="1264,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter17" position="1268,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus18" position="1413,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter18" position="1417,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,498" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus19" position="1562,498" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter19" position="1566,506" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus20" position="221,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter20" position="225,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus21" position="370,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter21" position="374,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus22" position="519,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter22" position="523,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus23" position="668,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter23" position="672,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus24" position="817,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter24" position="821,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus25" position="966,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter25" position="970,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus26" position="1115,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter26" position="1119,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus27" position="1264,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter27" position="1268,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus28" position="1413,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter28" position="1417,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,591" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus29" position="1562,591" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter29" position="1566,599" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus30" position="221,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter30" position="225,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus31" position="370,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter31" position="374,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus32" position="519,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter32" position="523,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus33" position="668,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter33" position="672,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus34" position="817,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter34" position="821,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus35" position="966,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter35" position="970,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus36" position="1115,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter36" position="1119,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus37" position="1264,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter37" position="1268,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus38" position="1413,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter38" position="1417,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,684" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus39" position="1562,684" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter39" position="1566,692" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus40" position="221,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter40" position="225,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus41" position="370,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter41" position="374,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus42" position="519,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter42" position="523,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus43" position="668,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter43" position="672,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus44" position="817,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter44" position="821,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus45" position="966,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter45" position="970,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus46" position="1115,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter46" position="1119,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus47" position="1264,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter47" position="1268,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus48" position="1413,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter48" position="1417,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,777" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus49" position="1562,777" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter49" position="1566,785" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <widget name="legend" position="205,912" size="1580,56" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="197,153" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,309" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,153" size="2,158" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1721,153" size="2,158" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="197,380" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,883" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,380" size="2,505" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1721,380" size="2,505" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


CONTEXT_SKIN = """
<screen name="WarderYouTubeContext" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Actions" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <eLabel position="288,155" size="1345,778" backgroundColor="#122C47"/>
  <eLabel position="288,155" size="1345,6" backgroundColor="#087EC7"/>
  <widget name="heading" position="333,193" size="1260,76" font="Regular;44" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <widget name="video" position="337,283" size="1250,123" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="context_focus0" position="334,432" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus1" position="334,504" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus2" position="334,576" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus3" position="334,648" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus4" position="334,720" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
    <widget name="context_row0" position="354,439" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row1" position="354,511" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row2" position="354,583" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row3" position="354,655" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row4" position="354,727" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="hint" position="336,825" size="1230,60" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="288,155" size="1345,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="288,931" size="1345,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="288,155" size="2,778" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1631,155" size="2,778" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""



CONFIRM_SKIN = """
<screen name="WarderYouTubeConfirm" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Confirm" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="274,175" size="1372,725" backgroundColor="#122C47"/>
  <eLabel position="274,175" size="1372,5" backgroundColor="#087EC7"/>
  <widget name="heading" position="327,210" size="1260,72" font="Regular;43" foregroundColor="#6CCBFF" transparent="1" zPosition="3"/>
  <widget name="question" position="327,316" size="1250,175" font="Regular;32" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
    <widget name="confirm_focus0" position="550,570" size="830,70" font="Regular;30" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="confirm_row0" position="574,578" size="780,54" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="confirm_focus1" position="550,642" size="830,70" font="Regular;30" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="confirm_row1" position="574,650" size="780,54" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="hint" position="335,825" size="1200,49" font="Regular;28" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="274,175" size="1372,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="274,898" size="1372,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="274,175" size="2,725" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1644,175" size="2,725" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


INFO_SKIN = """
<screen name="WarderYouTubeInfo" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Details" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="72,161" size="1775,756" backgroundColor="#122C47"/>
  <eLabel position="72,161" size="1775,5" backgroundColor="#087EC7"/>
  <widget name="title" position="116,197" size="1690,68" font="Regular;42" foregroundColor="#6CCBFF" transparent="1" zPosition="3"/>
  <widget name="body" position="116,297" size="1660,556" font="Regular;30" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="3" halign="center"/>

  <eLabel position="72,161" size="1775,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="72,915" size="1775,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="72,161" size="2,756" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1845,161" size="2,756" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""



# Only the outer shell is Warder-specific. The "list" is Enigma2's real
# VirtualKeyBoardList and retains its firmware-defined keys and navigation.
# This screen never replaces VirtualKeyBoard globally in the active GUI skin.
NATIVE_SEARCH_KEYBOARD_SKIN = """
<screen name="WarderNativeSearchKeyboard" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1125,28" size="245,42" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_date" position="1090,88" size="280,36" font="Regular;22" foregroundColor="#C2DDF8" transparent="1" halign="right" zPosition="8"/>
  <widget name="hdr_clock" position="1398,38" size="261,86" font="Regular;51" valign="bottom" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version_label" position="1682,28" size="214,37" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_version" position="1670,88" size="235,39" font="Regular;26" foregroundColor="#55DEFF" transparent="1" halign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <widget name="warder_brand" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="warder_caption" position="0,0" size="1,1" font="Regular;30" foregroundColor="#6CCBFF" transparent="1" halign="right" zPosition="3"/>
  <eLabel position="168,153" size="1584,803" backgroundColor="#122C47"/>
  <eLabel position="168,153" size="1584,6" backgroundColor="#087EC7"/>
  <widget name="prompt" position="206,175" size="1500,65" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <eLabel position="206,256" size="1502,76" backgroundColor="#0C2038"/>
  <widget name="text" position="228,263" size="1455,64" font="Regular;37" foregroundColor="#FFFFFF" backgroundColor="#0C2038" transparent="1" zPosition="3"/>
  <widget name="list" position="487,414" size="945,350" font="Regular;29" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="0" zPosition="3" scrollbarMode="showNever"/>
  <widget name="mode" position="477,847" size="103,46" font="Regular;25" foregroundColor="#6CCBFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="locale" position="590,847" size="530,46" font="Regular;24" foregroundColor="#B9D9F5" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="language" position="1135,847" size="552,46" font="Regular;24" foregroundColor="#B9D9F5" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="warder_key_hint" position="490,918" size="1200,42" font="Regular;23" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="150,1003" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="warder_key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1003" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="warder_key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1003" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="warder_key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1003" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="warder_key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#10283F" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="168,153" size="1584,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="168,954" size="1584,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="168,153" size="2,803" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1750,153" size="2,803" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""
