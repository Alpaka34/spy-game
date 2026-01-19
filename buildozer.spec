[app]

# Uygulamanın adı (telefonda görünecek isim)
title = Casus Oyunu

# Paket adı (benzersiz olmalı, noktalı yazılır)
package.name = casusoyunu
package.domain = org.hayati

# Kaynak dosyaların olduğu yer (genelde . demek kök demek)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Kivy sürümü + python (2026'da stabil olan)
requirements = python3,kivy==2.2.1,buildozer,cython==0.29.37

# Telefonu dik tutsun
orientation = portrait

# Tam ekran olmasın (isteğe bağlı)
fullscreen = 0

# Android ayarları (bunları değiştirme şimdilik)
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

# İkon eklemek istersen sonra buraya yazarsın (şimdilik boş bırak)
#icon.filename = icon.png

p4a.branch = master
android.api = 33
android.minapi = 21
