ORBITAL 3D DESKTOP SIMULATION
=============================

ORBITAL
Orbital Renewable Energy Harvesting and Laser-based Transmission

Integrating Solar and Geomagnetic Energy for Space-to-Earth Power Transfer


ISI
---
- orbital_simulation.py : program utama
- run_orbital.bat       : launcher Windows
- requirements.txt      : dependency Python


CARA JALANKAN - WINDOWS
-----------------------
1. Install Python 3.10+ dari python.org.
   Saat install, centang "Add Python to PATH".

2. Extract folder ini.

3. Double-click:
   run_orbital.bat

Launcher akan otomatis mencoba meng-install:
- numpy
- matplotlib


ALTERNATIF LEWAT TERMINAL
-------------------------
    pip install -r requirements.txt
    python orbital_simulation.py


FITUR
-----
- Model 3D Bumi.
- Orbit satelit.
- Visualisasi medan magnet Bumi.
- Kutub N dan S.
- Dua solar panel.
- Magnet internal yang divisualisasikan 1 rotasi per 1 orbit.
- Dynamo sebagai model konseptual.
- Charging baterai dari solar + dynamo.
- Auto power-beaming laser ke receiver ketika baterai penuh.
- Pause / Resume.
- Reset.
- Slider kecepatan simulasi.
- Mouse drag pada plot Matplotlib untuk mengubah sudut pandang.
- Scroll/zoom bawaan Matplotlib dapat digunakan tergantung backend.


ALUR KONSEP
-----------
1. Satelit mengorbit Bumi.
2. Solar panel menghasilkan energi.
3. Medan magnet Bumi direpresentasikan dalam simulasi.
4. Magnet internal divisualisasikan berotasi mengikuti orbit.
5. Rotasi menggerakkan model dynamo konseptual.
6. Energi solar dan dynamo digunakan untuk mengisi baterai.
7. Ketika baterai penuh, energi dipancarkan menggunakan laser
   menuju ground receiver.


CATATAN FISIKA
--------------
Simulasi ini adalah visualisasi konsep ORBITAL, bukan validasi bahwa
medan magnet Bumi akan otomatis membuat magnet di dalam satelit
berputar 1 kali setiap orbit.

Untuk desain fisik nyata perlu dihitung:

- torsi magnetik m × B,
- attitude/orientasi satelit,
- momentum dan reaction torque,
- generator efficiency dan mechanical losses,
- solar irradiance serta eclipse,
- battery capacity,
- laser conversion efficiency,
- atmospheric transmission,
- pointing/tracking receiver,
- thermal management,
- keseluruhan energy balance.


DISCLAIMER
----------
Komponen dynamo dan mekanisme rotasi magnet dalam simulasi merupakan
model konseptual untuk memvisualisasikan prinsip sistem.

Performa dan kelayakan sistem nyata memerlukan analisis fisika,
rekayasa, serta perhitungan energy balance secara menyeluruh.
