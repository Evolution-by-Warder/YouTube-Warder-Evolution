HOME_SKIN = """
<screen name="WarderYouTubeHome" position="0,0" size="1920,1080" title="YouTube Warder Evolution" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;44" foregroundColor="#FFFFFF" transparent="1" zPosition="4"/>
  <widget name="version" position="0,0" size="1,1" font="Regular;27" foregroundColor="#6CCBFF" transparent="1" halign="right" zPosition="4"/>
  <eLabel position="22,173" size="351,805" backgroundColor="#122C47"/>
  <eLabel position="22,173" size="351,5" backgroundColor="#087EC7"/>
  <widget name="nav_focus0" position="35,191" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav0" position="120,199" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus1" position="35,269" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav1" position="120,277" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus2" position="35,347" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav2" position="120,355" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus3" position="35,425" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav3" position="120,433" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus4" position="35,503" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav4" position="120,512" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus5" position="35,581" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav5" position="120,590" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus6" position="35,659" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav6" position="120,668" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="nav_focus7" position="35,737" size="328,72" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_focus.png" alphatest="on" zPosition="2"/>
  <widget name="nav7" position="120,746" size="234,55" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <!-- Eight small native picons (shared on all language settings). -->
  <ePixmap position="48,194" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_0.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,273" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_1.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,351" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_2.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,429" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_3.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,507" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_4.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,585" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_5.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,663" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_6.png" alphatest="on" zPosition="5"/>
  <ePixmap position="48,741" size="64,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/nav_7.png" alphatest="on" zPosition="5"/>
  <eLabel position="394,173" size="1490,805" backgroundColor="#10263E"/>
  <eLabel position="394,173" size="1490,5" backgroundColor="#087EC7"/>
  <widget name="heading" position="0,0" size="1,1" font="Regular;45" foregroundColor="#FFFFFF" transparent="1" zPosition="4"/>
  <widget name="subtitle" position="427,198" size="1090,42" font="Regular;27" foregroundColor="#6CCBFF" transparent="1" zPosition="4"/>
  <widget name="page_info" position="1560,198" size="300,42" font="Regular;24" foregroundColor="#62D9F8" transparent="1" halign="right" zPosition="4"/>
  <widget name="preview_focus0" position="413,251" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel0" position="415,253" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb0" position="446,261" size="410,230" zPosition="4"/>
  <widget name="preview_title0" position="427,486" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel0" position="427,543" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus1" position="902,251" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel1" position="904,253" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb1" position="935,261" size="410,230" zPosition="4"/>
  <widget name="preview_title1" position="916,486" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel1" position="916,543" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus2" position="1391,251" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel2" position="1393,253" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb2" position="1424,261" size="410,230" zPosition="4"/>
  <widget name="preview_title2" position="1405,486" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel2" position="1405,543" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus3" position="413,601" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel3" position="415,603" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb3" position="446,610" size="410,230" zPosition="4"/>
  <widget name="preview_title3" position="427,836" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel3" position="427,893" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus4" position="902,601" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel4" position="904,603" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb4" position="935,610" size="410,230" zPosition="4"/>
  <widget name="preview_title4" position="916,836" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel4" position="916,893" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_focus5" position="1391,601" size="477,324" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/video_focus.png" alphatest="on" zPosition="8"/>
  <widget name="preview_panel5" position="1393,603" size="473,320" font="Regular;22" foregroundColor="#142C47" backgroundColor="#142C47" transparent="0" zPosition="3"/>
  <widget name="preview_thumb5" position="1424,610" size="410,230" zPosition="4"/>
  <widget name="preview_title5" position="1405,836" size="444,56" font="Regular;22" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="preview_channel5" position="1405,893" size="444,20" font="Regular;19" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1" zPosition="4"/>
  <widget name="detail0" position="449,256" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail1" position="449,349" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail2" position="449,443" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail3" position="449,565" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail4" position="449,658" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="detail5" position="449,752" size="1350,76" font="Regular;30" foregroundColor="#FFFFFF" backgroundColor="#10263E" transparent="1" zPosition="4"/>
  <widget name="preview_message" position="450,254" size="1360,350" font="Regular;32" foregroundColor="#C6DCEE" transparent="1" zPosition="4"/>
  <widget name="status" position="427,939" size="1410,28" font="Regular;20" foregroundColor="#6CCBFF" transparent="1" zPosition="4"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="22,173" size="351,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="22,976" size="351,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="22,173" size="2,805" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="371,173" size="2,805" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="394,173" size="1490,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="394,976" size="1490,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="394,173" size="2,805" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1882,173" size="2,805" backgroundColor="#168BAF" zPosition="2"/>

  <widget name="preview_border0" position="413,251" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <widget name="preview_border1" position="902,251" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <widget name="preview_border2" position="1391,251" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <widget name="preview_border3" position="413,601" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <widget name="preview_border4" position="902,601" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <widget name="preview_border5" position="1391,601" size="477,324" foregroundColor="#0D5273" backgroundColor="#0D5273" transparent="0" zPosition="1"/>
  <!-- Search system keyboard is rendered inside Home; no modal/overlay. -->
  <!-- Reuse system VirtualKeyBoard eListboxPythonMultiContent + Input, NOT Warder-made letter buttons. -->
  <widget name="kb_system_input" position="479,264" size="1325,59" font="Regular;32" foregroundColor="#FFFFFF" backgroundColor="#0C2038" transparent="0" zPosition="6"/>
  <widget name="kb_system_list" position="780,372" size="718,405" scrollbarMode="showNever" transparent="1" zPosition="6"/>
  <widget name="kb_hint" position="480,780" size="1340,42" font="Regular;24" foregroundColor="#76CFF2" transparent="1" zPosition="6"/>
  <widget name="kb_feedback" position="480,838" size="1340,42" font="Regular;23" foregroundColor="#55DEFF" transparent="1" zPosition="6"/>
</screen>
"""


SEARCH_SKIN = """
<screen name="WarderYouTubeSearch" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="query" position="65,184" size="1755,60" font="Regular;31" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="44,233" size="1832,621" backgroundColor="#122C47"/>
  <widget name="results" position="68,265" size="1778,564" font="Regular;28" foregroundColor="#FFFFFF" backgroundColor="#122C47" foregroundColorSelected="#FFFFFF" backgroundColorSelected="#126BA5" transparent="0" itemHeight="60" scrollbarMode="showOnDemand" zPosition="3"/>
  <widget name="details" position="65,870" size="1730,44" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="status" position="65,923" size="1780,42" font="Regular;25" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="44,233" size="1832,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="44,852" size="1832,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="44,233" size="2,621" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1874,233" size="2,621" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""

SETTINGS_SKIN = """
<screen name="WarderYouTubeSettings" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Settings" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="description" position="61,178" size="1762,80" font="Regular;31" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="49,269" size="878,361" backgroundColor="#122C47"/>
  <eLabel position="949,269" size="920,361" backgroundColor="#122C47"/>
  <eLabel position="49,269" size="878,5" backgroundColor="#087EC7"/>
  <eLabel position="949,269" size="920,5" backgroundColor="#137A77"/>
  <widget name="section_search" position="76,294" size="830,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="key_state" position="76,376" size="812,110" font="Regular;31" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="section_playback" position="976,294" size="842,55" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="quality" position="976,376" size="845,66" font="Regular;32" foregroundColor="#65C7FF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="resolver_state" position="976,466" size="824,110" font="Regular;26" foregroundColor="#C6DCEE" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="49,653" size="1820,227" backgroundColor="#10263E"/>
  <eLabel position="49,653" size="1820,5" backgroundColor="#8B6F40"/>
  <widget name="section_privacy" position="77,673" size="1640,53" font="Regular;32" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="warning" position="77,733" size="1657,105" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="status" position="56,910" size="1775,56" font="Regular;26" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="49,269" size="878,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,628" size="878,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,269" size="2,361" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="925,269" size="2,361" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="949,269" size="920,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="949,628" size="920,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="949,269" size="2,361" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1867,269" size="2,361" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="49,653" size="1820,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,878" size="1820,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="49,653" size="2,227" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1867,653" size="2,227" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


GRID_SKIN = """
<screen name="WarderYouTubeGrid" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Videos" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;41" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="heading" position="1045,173" size="814,48" font="Regular;29" foregroundColor="#36B9FF" transparent="1" halign="right" zPosition="3"/>
  <eLabel position="0,173" size="321,826" backgroundColor="#102A45"/>
  <eLabel position="18,177" size="288,6" backgroundColor="#087EC7"/>
  <eLabel position="18,352" size="288,2" backgroundColor="#315676"/>
  <eLabel position="18,648" size="288,2" backgroundColor="#315676"/>
  <eLabel position="322,173" size="2,826" backgroundColor="#315676"/>
  
    <widget name="side0" position="26,193" size="274,54" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side1" position="26,252" size="272,54" font="Regular;27" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side2" position="26,375" size="271,51" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side3" position="26,431" size="272,190" font="Regular;25" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side4" position="26,672" size="270,50" font="Regular;27" foregroundColor="#6CCBFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side5" position="26,730" size="270,77" font="Regular;26" foregroundColor="#FFFFFF" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  
    <widget name="side6" position="26,838" size="273,109" font="Regular;24" foregroundColor="#C6DCEE" backgroundColor="#102A45" transparent="1" zPosition="3"/>
  <eLabel position="355,216" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus0" position="355,216" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb0" position="362,223" size="476,249" zPosition="2"/>
  <widget name="title0" position="364,471" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel0" position="364,543" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="868,216" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus1" position="868,216" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb1" position="875,223" size="476,249" zPosition="2"/>
  <widget name="title1" position="877,471" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel1" position="877,543" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="1381,216" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus2" position="1381,216" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb2" position="1388,223" size="476,249" zPosition="2"/>
  <widget name="title2" position="1390,471" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel2" position="1390,543" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="355,585" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus3" position="355,585" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb3" position="362,591" size="476,249" zPosition="2"/>
  <widget name="title3" position="364,839" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel3" position="364,911" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="868,585" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus4" position="868,585" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb4" position="875,591" size="476,249" zPosition="2"/>
  <widget name="title4" position="877,839" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel4" position="877,911" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <eLabel position="1381,585" size="491,355" backgroundColor="#142C47"/>
  <widget name="focus5" position="1381,585" size="491,364" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/grid_focus.png" alphatest="on" zPosition="8"/>
  <widget name="thumb5" position="1388,591" size="476,249" zPosition="2"/>
  <widget name="title5" position="1390,839" size="473,72" font="Regular;26" foregroundColor="#FFFFFF" transparent="1" zPosition="2"/>
  <widget name="channel5" position="1390,911" size="473,25" font="Regular;20" foregroundColor="#B9D9F5" transparent="1" zPosition="2"/>
  <widget name="status" position="358,953" size="1460,43" font="Regular;25" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <eLabel position="0,999" size="1920,81" backgroundColor="#08182D"/>
  <widget name="footer" position="28,1014" size="1880,52" font="Regular;24" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="355,216" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="355,569" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="355,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="844,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>

  <eLabel position="355,585" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="355,938" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="355,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="844,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>

  <eLabel position="868,216" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="868,569" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="868,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1357,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>

  <eLabel position="868,585" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="868,938" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="868,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1357,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>

  <eLabel position="1381,216" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1381,569" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1381,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1870,216" size="1,355" backgroundColor="#0D536F" zPosition="5"/>

  <eLabel position="1381,585" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1381,938" size="491,1" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1381,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
  <eLabel position="1870,585" size="1,355" backgroundColor="#0D536F" zPosition="5"/>
</screen>
"""


UPDATE_CHECK_SKIN = """
<screen name="WarderYouTubeUpdateCheck" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Updates" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <eLabel position="43,223" size="1834,729" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="status" position="72,248" size="1750,110" font="Regular;37" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="detail" position="72,399" size="1750,185" font="Regular;30" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#08182D"/>
  <widget name="footer" position="42,1013" size="1820,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,223" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

UPDATE_SKIN = """
<screen name="WarderYouTubeUpdateProgress" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Update progress" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <eLabel position="43,223" size="1834,729" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="version" position="72,257" size="1650,64" font="Regular;36" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="phase" position="72,344" size="1670,67" font="Regular;32" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="progress" position="72,455" size="1550,34" borderWidth="1" zPosition="3"/>
  <widget name="percentage" position="1660,440" size="160,62" font="Regular;31" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="detail" position="72,555" size="1720,170" font="Regular;30" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#08182D"/>
  <widget name="footer" position="42,1013" size="1830,54" font="Regular;27" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,223" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

LIBRARY_SKIN = """
<screen name="WarderYouTubeLibrary" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Saved videos" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <eLabel position="43,223" size="1834,729" backgroundColor="#122C47" zPosition="0"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="title" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <widget name="subtitle" position="55,173" size="1740,45" font="Regular;32" foregroundColor="#36B9FF" transparent="1" zPosition="3"/>
  <widget name="results" position="50,236" size="1810,625" font="Regular;30" itemHeight="62" foregroundColor="#FFFFFF" backgroundColor="#142C47" foregroundColorSelected="#FFFFFF" backgroundColorSelected="#126BA5" transparent="0" scrollbarMode="showOnDemand" zPosition="3"/>
  <widget name="status" position="55,876" size="1790,93" font="Regular;28" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#08182D"/>
  <widget name="footer" position="38,1013" size="1840,54" font="Regular;25" foregroundColor="#FFFFFF" transparent="1" zPosition="0"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;22" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;22" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="43,223" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,950" size="1834,2" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="43,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
  <eLabel position="1875,223" size="2,729" backgroundColor="#1886AD" zPosition="2"/>
</screen>
"""

KEYBOARD_SKIN = """
<screen name="WarderYouTubeKeyboard" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Keyboard" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <eLabel position="197,173" size="1526,154" backgroundColor="#122C47"/>
  <eLabel position="197,173" size="1526,5" backgroundColor="#087EC7"/>
  <widget name="title" position="229,188" size="1456,62" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="input" position="235,265" size="1410,51" font="Regular;31" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="hint" position="210,342" size="1490,44" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="197,394" size="1526,493" backgroundColor="#10263E"/>
  <eLabel position="221,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus0" position="221,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter0" position="225,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus1" position="370,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter1" position="374,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus2" position="519,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter2" position="523,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus3" position="668,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter3" position="672,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus4" position="817,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter4" position="821,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus5" position="966,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter5" position="970,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus6" position="1115,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter6" position="1119,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus7" position="1264,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter7" position="1268,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus8" position="1413,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter8" position="1417,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,419" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus9" position="1562,419" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter9" position="1566,427" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus10" position="221,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter10" position="225,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus11" position="370,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter11" position="374,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus12" position="519,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter12" position="523,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus13" position="668,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter13" position="672,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus14" position="817,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter14" position="821,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus15" position="966,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter15" position="970,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus16" position="1115,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter16" position="1119,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus17" position="1264,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter17" position="1268,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus18" position="1413,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter18" position="1417,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,510" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus19" position="1562,510" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter19" position="1566,517" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus20" position="221,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter20" position="225,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus21" position="370,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter21" position="374,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus22" position="519,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter22" position="523,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus23" position="668,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter23" position="672,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus24" position="817,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter24" position="821,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus25" position="966,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter25" position="970,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus26" position="1115,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter26" position="1119,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus27" position="1264,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter27" position="1268,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus28" position="1413,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter28" position="1417,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,600" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus29" position="1562,600" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter29" position="1566,608" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus30" position="221,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter30" position="225,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus31" position="370,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter31" position="374,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus32" position="519,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter32" position="523,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus33" position="668,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter33" position="672,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus34" position="817,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter34" position="821,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus35" position="966,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter35" position="970,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus36" position="1115,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter36" position="1119,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus37" position="1264,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter37" position="1268,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus38" position="1413,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter38" position="1417,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,691" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus39" position="1562,691" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter39" position="1566,699" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="221,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus40" position="221,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter40" position="225,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="370,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus41" position="370,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter41" position="374,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="519,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus42" position="519,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter42" position="523,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="668,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus43" position="668,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter43" position="672,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="817,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus44" position="817,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter44" position="821,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="966,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus45" position="966,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter45" position="970,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1115,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus46" position="1115,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter46" position="1119,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1264,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus47" position="1264,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter47" position="1268,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1413,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus48" position="1413,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter48" position="1417,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <eLabel position="1562,782" size="132,76" backgroundColor="#142C47"/>
  <widget name="focus49" position="1562,782" size="132,76" font="Regular;33" foregroundColor="#FFFFFF" backgroundColor="#087EC7" transparent="0" zPosition="2"/>
  <widget name="letter49" position="1566,790" size="124,58" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" halign="center" valign="center" zPosition="3"/>
  <widget name="legend" position="205,913" size="1580,56" font="Regular;26" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="197,173" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,325" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,173" size="2,154" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1721,173" size="2,154" backgroundColor="#168BAF" zPosition="2"/>

  <eLabel position="197,394" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,885" size="1526,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="197,394" size="2,493" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1721,394" size="2,493" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


CONTEXT_SKIN = """
<screen name="WarderYouTubeContext" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Actions" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <eLabel position="288,175" size="1345,759" backgroundColor="#122C47"/>
  <eLabel position="288,175" size="1345,6" backgroundColor="#087EC7"/>
  <widget name="heading" position="333,212" size="1260,76" font="Regular;44" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1" zPosition="3"/>
  <widget name="video" position="337,300" size="1250,123" font="Regular;29" foregroundColor="#6CCBFF" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <widget name="context_focus0" position="334,445" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus1" position="334,515" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus2" position="334,586" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus3" position="334,656" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="context_focus4" position="334,726" size="1250,72" font="Regular;27" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
    <widget name="context_row0" position="354,452" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row1" position="354,522" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row2" position="354,592" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row3" position="354,663" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="context_row4" position="354,733" size="1200,55" font="Regular;31" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="hint" position="336,829" size="1230,60" font="Regular;28" foregroundColor="#B9D9F5" backgroundColor="#142C47" transparent="1"  zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;22" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;22" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="288,175" size="1345,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="288,932" size="1345,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="288,175" size="2,759" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1631,175" size="2,759" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""



CONFIRM_SKIN = """
<screen name="WarderYouTubeConfirm" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Confirm" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="274,194" size="1372,708" backgroundColor="#122C47"/>
  <eLabel position="274,194" size="1372,5" backgroundColor="#087EC7"/>
  <widget name="heading" position="327,229" size="1260,72" font="Regular;43" foregroundColor="#6CCBFF" transparent="1" zPosition="3"/>
  <widget name="question" position="327,332" size="1250,175" font="Regular;32" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
    <widget name="confirm_focus0" position="550,580" size="830,70" font="Regular;30" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="confirm_row0" position="574,588" size="780,54" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="confirm_focus1" position="550,650" size="830,70" font="Regular;30" backgroundColor="#126BA5" transparent="0" zPosition="3"/>
  <widget name="confirm_row1" position="574,658" size="780,54" font="Regular;34" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="5"/>
  <widget name="hint" position="335,829" size="1200,49" font="Regular;28" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="274,194" size="1372,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="274,900" size="1372,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="274,194" size="2,708" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1644,194" size="2,708" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""


INFO_SKIN = """
<screen name="WarderYouTubeInfo" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Details" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="brand" position="0,0" size="1,1" font="Regular;42" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="72,181" size="1775,737" backgroundColor="#122C47"/>
  <eLabel position="72,181" size="1775,5" backgroundColor="#087EC7"/>
  <widget name="title" position="116,216" size="1690,68" font="Regular;42" foregroundColor="#6CCBFF" transparent="1" zPosition="3"/>
  <widget name="body" position="116,313" size="1660,580" font="Regular;30" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="3" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="3" halign="center"/>

  <eLabel position="72,181" size="1775,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="72,916" size="1775,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="72,181" size="2,737" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1845,181" size="2,737" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""



# Only the outer shell is Warder-specific. The "list" is Enigma2's real
# VirtualKeyBoardList and retains its firmware-defined keys and navigation.
# This screen never replaces VirtualKeyBoard globally in the active GUI skin.
NATIVE_SEARCH_KEYBOARD_SKIN = """
<screen name="WarderNativeSearchKeyboard" position="0,0" size="1920,1080" title="YouTube Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">

  <widget name="hdr_day" position="1110,20" size="270,35" font="Regular;25" foregroundColor="#E2EFF8" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_date" position="980,55" size="400,35" font="Regular;24" foregroundColor="#D9E6EF" transparent="1" halign="right" valign="center" zPosition="8"/>
  <widget name="hdr_clock" position="1398,20" size="190,70" font="Regular;60" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="center" zPosition="8"/>
  <widget name="hdr_seconds" position="1590,39" size="66,51" font="Regular;38" valign="center" foregroundColor="#FFFFFF" transparent="1" halign="left" zPosition="8"/>
  <widget name="hdr_version_label" position="1680,20" size="210,35" font="Regular;25" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>
  <widget name="hdr_version" position="1680,55" size="210,35" font="Regular;24" foregroundColor="#55DEFF" transparent="1" halign="center" valign="center" zPosition="8"/>

  <ePixmap position="0,0" size="1920,152" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/WarderYouTube/images/warder_header.png" zPosition="0"/>
  <eLabel position="0,150" size="1920,3" backgroundColor="#1BEFF0" zPosition="10"/>
  <eLabel position="1392,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <eLabel position="1664,22" size="2,83" backgroundColor="#19C9FF" zPosition="7"/>
  <widget name="warder_brand" position="0,0" size="1,1" font="Regular;43" foregroundColor="#FFFFFF" transparent="1" zPosition="3"/>
  <widget name="warder_caption" position="0,0" size="1,1" font="Regular;30" foregroundColor="#6CCBFF" transparent="1" halign="right" zPosition="3"/>
  <eLabel position="168,173" size="1584,783" backgroundColor="#122C47"/>
  <eLabel position="168,173" size="1584,6" backgroundColor="#087EC7"/>
  <widget name="prompt" position="206,194" size="1500,65" font="Regular;36" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <eLabel position="206,273" size="1502,76" backgroundColor="#0C2038"/>
  <widget name="text" position="228,280" size="1455,64" font="Regular;37" foregroundColor="#FFFFFF" backgroundColor="#0C2038" transparent="1" zPosition="3"/>
  <widget name="list" position="487,428" size="945,350" font="Regular;29" foregroundColor="#FFFFFF" backgroundColor="#122C47" transparent="0" zPosition="3" scrollbarMode="showNever"/>
  <widget name="mode" position="477,850" size="103,46" font="Regular;25" foregroundColor="#6CCBFF" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="locale" position="590,850" size="530,46" font="Regular;24" foregroundColor="#B9D9F5" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="language" position="1135,850" size="552,46" font="Regular;24" foregroundColor="#B9D9F5" backgroundColor="#122C47" transparent="1" zPosition="3"/>
  <widget name="warder_key_hint" position="490,919" size="1200,42" font="Regular;23" foregroundColor="#B9D9F5" transparent="1" zPosition="3"/>
  <eLabel position="0,993" size="1920,87" backgroundColor="#08182D"/>
  <eLabel position="150,1070" size="195,3" backgroundColor="#FF526A" zPosition="5"/>
  <widget name="warder_key_red" position="56,1020" size="381,45" font="Regular;29" foregroundColor="#FE637D" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="620,1070" size="195,3" backgroundColor="#36E884" zPosition="5"/>
  <widget name="warder_key_green" position="526,1020" size="381,45" font="Regular;29" foregroundColor="#4CE58B" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1090,1070" size="195,3" backgroundColor="#FFE065" zPosition="5"/>
  <widget name="warder_key_yellow" position="996,1020" size="381,45" font="Regular;29" foregroundColor="#FFD367" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>
  <eLabel position="1560,1070" size="195,3" backgroundColor="#60BCFF" zPosition="5"/>
  <widget name="warder_key_blue" position="1466,1020" size="381,45" font="Regular;29" foregroundColor="#5EBEFF" backgroundColor="#08182D" transparent="1" zPosition="6" halign="center"/>

  <eLabel position="168,173" size="1584,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="168,954" size="1584,2" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="168,173" size="2,783" backgroundColor="#168BAF" zPosition="2"/>
  <eLabel position="1750,173" size="2,783" backgroundColor="#168BAF" zPosition="2"/>
</screen>
"""
