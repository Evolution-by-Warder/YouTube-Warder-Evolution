# -*- coding: utf-8 -*-
"""Flat, native Enigma2 screens; no images, animation or custom renderer."""
HOME_SKIN = """
<screen name="WarderYouTubeHome" position="0,0" size="1920,1080" title="YouTube Warder Evolution" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,108" backgroundColor="#142C47"/>
  <eLabel position="0,106" size="1920,3" backgroundColor="#087EC7"/>
  <widget name="brand" position="43,21" size="1200,64" font="Regular;44" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="2"/>
  <widget name="version" position="1250,32" size="620,48" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" halign="right" zPosition="2"/>
  <eLabel position="24,135" size="362,843" backgroundColor="#122C47"/>
  <eLabel position="24,135" size="362,6" backgroundColor="#087EC7"/>
  <widget name="nav_title" position="47,158" size="310,55" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <widget name="menu" position="38,229" size="332,699" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" itemHeight="67" scrollbarMode="showOnDemand"/>
  <eLabel position="414,137" size="1470,410" backgroundColor="#10263E"/>
  <eLabel position="414,137" size="8,410" backgroundColor="#087EC7"/>
  <widget name="overline" position="452,162" size="1320,49" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <widget name="heading" position="452,218" size="1350,81" font="Regular;52" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="description" position="452,316" size="1335,158" font="Regular;32" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1" />
  <eLabel position="414,569" size="476,329" backgroundColor="#122C47"/>
  <eLabel position="912,569" size="476,329" backgroundColor="#122C47"/>
  <eLabel position="1410,569" size="474,329" backgroundColor="#122C47"/>
  <eLabel position="435,587" size="435,5" backgroundColor="#087EC7"/>
  <eLabel position="933,587" size="435,5" backgroundColor="#137A77"/>
  <eLabel position="1431,587" size="433,5" backgroundColor="#8B6F40"/>
  <widget name="card1_title" position="447,612" size="420,62" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="card1_body" position="447,680" size="415,166" font="Regular;27" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <widget name="card2_title" position="945,612" size="420,62" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="card2_body" position="945,680" size="415,166" font="Regular;27" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <widget name="card3_title" position="1443,612" size="420,62" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="card3_body" position="1443,680" size="415,166" font="Regular;27" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <widget name="status" position="430,916" size="1435,46" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <widget name="footer" position="40,947" size="1810,38" font="Regular;23" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

SEARCH_SKIN = """
<screen name="WarderYouTubeSearch" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,108" backgroundColor="#142C47"/>
  <eLabel position="0,106" size="1920,3" backgroundColor="#087EC7"/>
  <widget name="title" position="45,22" size="1700,66" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="query" position="65,145" size="1755,57" font="Regular;35" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1" />
  <eLabel position="44,215" size="1832,636" backgroundColor="#122C47"/>
  <widget name="results" position="68,240" size="1778,570" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" itemHeight="60" scrollbarMode="showOnDemand"/>
  <widget name="details" position="65,868" size="1730,44" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1" />
  <widget name="status" position="65,922" size="1780,42" font="Regular;25" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

SETTINGS_SKIN = """
<screen name="WarderYouTubeSettings" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Settings" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,108" backgroundColor="#142C47"/>
  <eLabel position="0,106" size="1920,3" backgroundColor="#087EC7"/>
  <widget name="title" position="44,22" size="1760,65" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="description" position="61,144" size="1762,80" font="Regular;31" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1" />
  <eLabel position="49,251" size="878,370" backgroundColor="#122C47"/>
  <eLabel position="949,251" size="920,370" backgroundColor="#122C47"/>
  <eLabel position="49,251" size="878,5" backgroundColor="#087EC7"/>
  <eLabel position="949,251" size="920,5" backgroundColor="#137A77"/>
  <widget name="section_search" position="76,277" size="830,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="key_state" position="76,361" size="812,110" font="Regular;31" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1" />
  <widget name="section_playback" position="976,277" size="842,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="quality" position="976,361" size="845,66" font="Regular;32" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1" />
  <widget name="resolver_state" position="976,453" size="824,110" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1" />
  <eLabel position="49,645" size="1820,233" backgroundColor="#10263E"/>
  <eLabel position="49,645" size="1820,5" backgroundColor="#8B6F40"/>
  <widget name="section_privacy" position="77,666" size="1640,53" font="Regular;32" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="warning" position="77,727" size="1657,105" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <widget name="status" position="56,909" size="1775,56" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""


GRID_SKIN = """
<screen name="WarderYouTubeGrid" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Videos" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,104" backgroundColor="#142C47"/>
  <widget name="brand" position="36,20" size="1010,61" font="Regular;41" foregroundColor="#FFFFFF" transparent="1"/>
  <widget name="heading" position="1038,28" size="815,54" font="Regular;29" foregroundColor="#36B9FF" transparent="1" halign="right"/>
  <eLabel position="0,104" size="321,895" backgroundColor="#102A45"/>
  <eLabel position="18,155" size="288,6" backgroundColor="#087EC7"/>
  <eLabel position="18,337" size="288,2" backgroundColor="#315676"/>
  <eLabel position="18,640" size="288,2" backgroundColor="#315676"/>
  <eLabel position="322,104" size="2,895" backgroundColor="#315676"/>
  
    <widget name="side0" position="26,174" size="274,54" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side1" position="26,234" size="272,54" font="Regular;27" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side2" position="26,360" size="271,51" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side3" position="26,417" size="272,190" font="Regular;25" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side4" position="26,665" size="270,50" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side5" position="26,724" size="270,77" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" />
  
    <widget name="side6" position="26,835" size="273,109" font="Regular;24" foregroundColor="#C6DCEE" backgroundColor="#102A45" transparent="1" />
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
  <widget name="status" position="358,953" size="1460,43" font="Regular;25" foregroundColor="#36B9FF" transparent="1"/>
  <eLabel position="0,999" size="1920,81" backgroundColor="#142C47"/>
  <widget name="footer" position="28,1014" size="1880,52" font="Regular;24" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""


UPDATE_CHECK_SKIN = """
<screen name="WarderYouTubeUpdateCheck" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Updates" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,105" backgroundColor="#142C47"/>
  <widget name="title" position="45,23" size="1800,62" font="Regular;42" foregroundColor="#FFFFFF" transparent="1"/>
  <widget name="status" position="72,230" size="1750,110" font="Regular;37" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="detail" position="72,385" size="1750,185" font="Regular;30" foregroundColor="#B9D9F5" transparent="1"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="42,1013" size="1820,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

UPDATE_SKIN = """
<screen name="WarderYouTubeUpdateProgress" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Update progress" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,105" backgroundColor="#142C47"/>
  <widget name="title" position="45,23" size="1770,62" font="Regular;42" foregroundColor="#FFFFFF" transparent="1"/>
  <widget name="version" position="72,180" size="1650,62" font="Regular;37" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="phase" position="72,290" size="1670,66" font="Regular;33" foregroundColor="#FFFFFF" transparent="1"/>
  <widget name="progress" position="72,405" size="1550,34" borderWidth="1"/>
  <widget name="percentage" position="1660,390" size="160,62" font="Regular;31" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="detail" position="72,510" size="1720,170" font="Regular;30" foregroundColor="#B9D9F5" transparent="1"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="42,1013" size="1830,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

LIBRARY_SKIN = """
<screen name="WarderYouTubeLibrary" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Saved videos" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,105" backgroundColor="#142C47"/>
  <widget name="title" position="45,23" size="1750,62" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
  <widget name="subtitle" position="55,132" size="1740,65" font="Regular;32" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="results" position="50,218" size="1810,625" font="Regular;30" itemHeight="62" foregroundColor="#FFFFFF" backgroundColor="#142C47" scrollbarMode="showOnDemand"/>
  <widget name="status" position="55,874" size="1790,93" font="Regular;28" foregroundColor="#B9D9F5" transparent="1"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="38,1013" size="1840,54" font="Regular;25" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

KEYBOARD_SKIN = """
<screen name="WarderYouTubeKeyboard" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Keyboard" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,108" backgroundColor="#142C47"/>
  <eLabel position="0,106" size="1920,3" backgroundColor="#087EC7"/>
  <widget name="brand" position="46,24" size="1770,62" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <eLabel position="197,141" size="1526,170" backgroundColor="#122C47"/>
  <eLabel position="197,141" size="1526,5" backgroundColor="#087EC7"/>
  <widget name="title" position="229,168" size="1456,62" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="input" position="235,247" size="1410,51" font="Regular;31" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <widget name="hint" position="210,326" size="1490,44" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
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
  <widget name="legend" position="205,912" size="1580,56" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""


CONTEXT_SKIN = """
<screen name="WarderYouTubeContext" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Actions" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,108" backgroundColor="#142C47"/>
  <eLabel position="0,106" size="1920,3" backgroundColor="#087EC7"/>
  <widget name="brand" position="47,24" size="1700,62" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <eLabel position="288,155" size="1345,778" backgroundColor="#122C47"/>
  <eLabel position="288,155" size="1345,6" backgroundColor="#087EC7"/>
  <widget name="heading" position="333,193" size="1260,76" font="Regular;44" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" />
  <widget name="video" position="337,283" size="1250,123" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1" />
  <widget name="menu" position="334,432" size="1250,314" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" itemHeight="72" scrollbarMode="showOnDemand"/>
  <widget name="hint" position="336,825" size="1230,60" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" />
  <eLabel position="0,993" size="1920,87" backgroundColor="#10283F"/>
  <eLabel position="40,1005" size="415,58" backgroundColor="#A32B3C"/>
  <widget name="key_red" position="56,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#A32B3C" transparent="1" zPosition="6"/>
  <eLabel position="510,1005" size="415,58" backgroundColor="#167A55"/>
  <widget name="key_green" position="526,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#167A55" transparent="1" zPosition="6"/>
  <eLabel position="980,1005" size="415,58" backgroundColor="#9E7516"/>
  <widget name="key_yellow" position="996,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#9E7516" transparent="1" zPosition="6"/>
  <eLabel position="1450,1005" size="415,58" backgroundColor="#155EA1"/>
  <widget name="key_blue" position="1466,1011" size="381,48" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#155EA1" transparent="1" zPosition="6"/>
</screen>
"""

