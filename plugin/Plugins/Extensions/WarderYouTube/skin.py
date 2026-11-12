# -*- coding: utf-8 -*-
"""Flat, native Enigma2 screens; no images, animation or custom renderer."""
HOME_SKIN = """
<screen name="WarderYouTubeHome" position="0,0" size="1920,1080" title="YouTube - Warder Evolution" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,110" backgroundColor="#142C47"/>
  <widget name="brand" position="42,23" size="1100,60" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
  <widget name="version" position="1260,28" size="595,52" font="Regular;28" foregroundColor="#36B9FF" backgroundColor="#142C47" halign="right" transparent="1"/>
  <widget name="menu" position="28,157" size="320,730" font="Regular;30" itemHeight="66" backgroundColor="#142C47" foregroundColor="#FFFFFF" scrollbarMode="showOnDemand"/>
  <widget name="heading" position="405,166" size="1350,70" font="Regular;46" foregroundColor="#FFFFFF" transparent="1"/>
  <eLabel position="403,265" size="1350,3" backgroundColor="#087EC7"/>
  <widget name="description" position="405,320" size="1335,220" font="Regular;31" foregroundColor="#B9D9F5" transparent="1"/>
  <widget name="status" position="405,615" size="1330,100" font="Regular;27" foregroundColor="#36B9FF" transparent="1"/>
  <eLabel position="0,996" size="1920,84" backgroundColor="#142C47"/>
  <widget name="footer" position="45,1014" size="1780,54" font="Regular;27" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
</screen>
"""

SEARCH_SKIN = """
<screen name="WarderYouTubeSearch" position="0,0" size="1920,1080" title="YouTube - Warder Evolution / Search" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,105" backgroundColor="#142C47"/>
  <widget name="title" position="45,23" size="1640,62" font="Regular;43" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
  <widget name="query" position="55,134" size="1760,62" font="Regular;37" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="results" position="50,225" size="1805,610" font="Regular;31" itemHeight="60" foregroundColor="#FFFFFF" backgroundColor="#142C47" scrollbarMode="showOnDemand"/>
  <widget name="details" position="55,849" size="1780,52" font="Regular;27" foregroundColor="#B9D9F5" transparent="1"/>
  <widget name="status" position="55,913" size="1780,56" font="Regular;28" foregroundColor="#36B9FF" transparent="1"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="40,1011" size="1860,54" font="Regular;25" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
</screen>
"""

SETTINGS_SKIN = """
<screen name="WarderYouTubeSettings" position="0,0" size="1920,1080" title="YouTube - Warder Evolution / Settings" flags="wfNoBorder" backgroundColor="#08182D">
  <eLabel position="0,0" size="1920,105" backgroundColor="#142C47"/>
  <widget name="title" position="48,26" size="1750,62" font="Regular;42" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
  <widget name="description" position="75,185" size="1760,150" font="Regular;35" foregroundColor="#B9D9F5" transparent="1"/>
  <widget name="key_state" position="75,385" size="1740,72" font="Regular;39" foregroundColor="#36B9FF" transparent="1"/>
  <widget name="warning" position="75,555" size="1730,150" font="Regular;29" foregroundColor="#B9D9F5" transparent="1"/>
  <eLabel position="0,997" size="1920,83" backgroundColor="#142C47"/>
  <widget name="footer" position="42,1013" size="1840,53" font="Regular;27" foregroundColor="#FFFFFF" backgroundColor="#142C47" transparent="1"/>
</screen>
"""
