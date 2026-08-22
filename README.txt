AETHER 3D DESKTOP SIMULATION
============================

Isi:
- aether_simulation.py : program utama
- run_aether.bat       : launcher Windows
- requirements.txt     : dependency Python

CARA JALANKAN - WINDOWS
-----------------------
1. Install Python 3.10+ dari python.org.
   Saat install, centang "Add Python to PATH".
2. Extract folder ini.
3. Double-click: run_aether.bat

Launcher akan otomatis mencoba meng-install:
- numpy
- matplotlib

Alternatif lewat terminal:
    pip install -r requirements.txt
    python aether_simulation.py

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

CATATAN FISIKA
--------------
Simulasi ini adalah visualisasi konsep AETHER, bukan validasi bahwa medan
magnet Bumi akan otomatis membuat magnet di dalam satelit berputar 1 kali
setiap 1 orbit.

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
