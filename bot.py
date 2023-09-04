import logging
import telebot
import mysql.connector
import random
from telebot import types
import time

API_TOKEN = '6197957152:AAHl7CsqiBfdsGNoaHbT62t5aoeEjOpaR_Q'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot
bot = telebot.TeleBot(API_TOKEN)

DB_HOST = 'localhost'
DB_NAME = 'st35380_userdbtelegram'
DB_USER = 'st35380_userdbtelegram'
DB_PASSWORD = 'Xalid1234'

# Create a MySQL connection
db = mysql.connector.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    connect_timeout=60 
)

cursor = db.cursor()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Check if the user is already registered
    check_sql = "SELECT * FROM userdb2 WHERE id = %s"
    check_val = (chat_id,)
    cursor.execute(check_sql, check_val)
    result = cursor.fetchone()

    if result:
        # Create a keyboard with the commands
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
        # Add buttons without emojis
        markup.add(
            types.KeyboardButton("/profil"),
            types.KeyboardButton("/match"),
            types.KeyboardButton("/info"),
            types.KeyboardButton("/haqqımızda"),
            types.KeyboardButton("/mesaj"),
            types.KeyboardButton("/VIP"),
            types.KeyboardButton("/versiya"),
            types.KeyboardButton("/trade"),
            types.KeyboardButton("/socialmedia")
        )
    
        # Create the message to send
        welcome_message = (
            "Salam, Heart2Heart-ə Xoş Gəldin!\n"
            "Sənə dost, flört və ya sevgili tapmağına kömək etmək üçün buradayam☺️\n"
            "Əylənəcəyinə inanıram🌹\n"
            "⚠️ UNUTMA bot yenidir ⚠️ Bəzən connection problemləri yaşa bilərsən. Bot cavab verməzsə 10 saniyə gözlə və KOMUTU yenidən yaz.\n\n"
            "/profil📜 - Profilinə baxa vəya məlumatlarını dəyişdirə bilərsən.\n\n"
            "/match🔍 - Qarşı cinsin ilə eşleşmə başlata bilərsən.\n\n"
            "/info🧾 - Komutlar haqqında məlumat ala bilərsən(Əvvəlcə buranı oxusan sistemi daha yaxşı anlaya bilərsən).\n\n"
            "/haqqimizda⚒️ - Heart2Heart qurucuları haqqında ümumi məlumat.\n\n"
            "/mesaj📝 - Adminə mesaj göndərə bilərsən.\n\n"
            "/VIP🌐 - Ödəniş edərək daha çox eşleşə və eşleşdiyin kişiyə 1 dəfəlik bir mesaj göndərə bilərsən.(Yaxın zamanda aktiv olacaq)\n\n"
            "/versiya📂 - Əlavə olunacaq və ya əlavə olunan bütün məlumatlara baxa bilərsən.\n\n"
            "/trade🛍️ - Sizlərə sunduğumuz online Market. Burada ən ucuz və qarantiyalı panel sifarişi və ya music, film platformalarının premium hesablarını sifariş edə bilərsiniz.\n\n"
            "/socialmedia🃏 - Heart2Heart sosial media hesablarına baxa bilərsiniz."
        )

    # Send the message with the keyboard
        bot.send_message(chat_id, welcome_message, reply_markup=markup)
    else:
        bot.reply_to(message, "Salam, Heart2Heart telegram botuna xoş gəldin. \nBu botun əsas məqsədi səni qarşı cinsin ilə ünsiyyət qurdurmağa çalışmaq. \nQeydiyyatdan keçdikdən sonra sənin məlumatların qarşı cinsə göstərilir. Əgər qarşı tərəf səni bəyənərsə, sənə bəyənən kişinin məlumatları gəlir. Əgər səndə bəyənsən bir biriniz ilə mesajlaşa bilirsiniz. Eyni şəkildə sənədə qarşı cinsinin məlumatları göstərilir. Və dediklərim təkrar olunur. İstifadəçi sayı az olduğu üçün 24 saat ərzində sadəcə 3 dəfə bəyənmə limitin var. \n\nBaşlamadan əvvəl qeydiyyatdan keçməlisən. /qeydiyyat yazaraq qeydiyyatdan keç.\n\nBot @heart2heart_telegram(instagram) tərəfindən düzəldilmişdir. Hər hansı bir problemdə @heart2heart_telegram(instagram) hesabına mesaj göndərin.\n\n\nİstifadəçi artarsa bir çox funksiya əlavə olunacaqdır.")

@bot.message_handler(commands=['match'])
def start_matching(message):
    chat_id = message.chat.id
    user = bot.get_chat(chat_id)
    usernamesend = user.username
  
    # Kullanıcının bəyənmə limitini kontrol edin
    check_likeing_sql = "SELECT likeing FROM userdb2 WHERE id = %s"
    check_likeing_val = (chat_id,)
    cursor.execute(check_likeing_sql, check_likeing_val)
    user_likeing_result = cursor.fetchone()
    
    if user_likeing_result is not None:
        user_likeing = user_likeing_result[0]
        
        if user_likeing == 0:
            bot.reply_to(message, "Bağışlayın, günlük bəyənmə limitiniz doldu. 00:00-da limitlər sıfırlanacaq.")
            return
    else:
      bot.reply_to(message, "Qeydiyyatdan keçin")  

    # Kullanıcının cinsiyetini al
    check_sql = "SELECT gender FROM userdb2 WHERE id = %s"
    check_val = (chat_id,)
    cursor.execute(check_sql, check_val)
    result = cursor.fetchone()

    if result:
        user_gender = result[0]

        # Kullanıcının daha önce eşleştiği kişilerin ID'lerini al
        history_sql = "SELECT history FROM userdb2 WHERE id = %s"
        history_val = (chat_id,)
        cursor.execute(history_sql, history_val)
        history_result = cursor.fetchone()
        
        if history_result and history_result[0]:
          history_data = history_result[0]
        else:
          history_data = ""
          

        # Seçilen cinsiyete uygun bir kullanıcıyı veritabanından seçin
        select_sql = (
            "SELECT id, username, age, region, info, foto1 "
            "FROM userdb2 "
            "WHERE gender != %s AND id NOT IN (" + ",".join(["%s"] * len(history_data.split(','))) + ") "
            "ORDER BY RAND() LIMIT 1"
        )
        select_val = (user_gender,) + tuple(history_data.split(','))
        cursor.execute(select_sql, select_val)
        match_result = cursor.fetchone()
        

        if match_result:
          match_id, match_username, match_age, match_region, match_info, match_foto1 = match_result

          markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
          markup.add(types.KeyboardButton("❤️"), types.KeyboardButton("👎")) 
          # Kullanıcıya karşı cinsin bilgilerini ve profil fotoğrafını gönderin
          bot.send_photo(chat_id, match_foto1, caption=f"{match_username} - {match_age}, {match_region}\n{match_info}", reply_markup=markup)
          
          # Kullanıcının cevabına göre işlem yapın
          bot.register_next_step_handler(message, handle_matching_response, match_id, match_username, usernamesend)


          update_sql = "UPDATE userdb2 SET likeing = likeing - 1 WHERE id = %s"
          update_val = (chat_id,)
          cursor.execute(update_sql, update_val)
          db.commit()
        else:
          bot.reply_to(message, "Bağışlayın, sizə görə birisi tapılmadı😞.")
    else:
      bot.reply_to(message, "Başlamadan əvvəl /qeydiyyat yazaraq qeydiyyatdan keçin.")


def handle_matching_response(message, match_id, match_username, usernamesend):
    chat_id = message.chat.id
    response = message.text
    
    update_sql = f"UPDATE userdb2 SET history = CONCAT(history, ',{match_id}') WHERE id = '{chat_id}'"
    cursor.execute(update_sql)
    db.commit()

    if response == "❤️":
        #update_sql = "UPDATE userdb2 SET likeing = likeing - 1 WHERE id = %s"
        #update_val = (chat_id,)
        #cursor.execute(update_sql, update_val)
        #db.commit()

        # Get the photo of the user who liked you
        user_photo_sql = "SELECT foto1 FROM userdb2 WHERE id = %s"
        user_photo_val = (chat_id,)
        cursor.execute(user_photo_sql, user_photo_val)
        user_photo = cursor.fetchone()[0]

        user_info = get_user_info(chat_id, usernamesend)  # Kullanıcının kendi bilgilerini alın

        try:
            bot.send_photo(match_id, user_photo, caption=f"Biri səni bəyəndi! İşte onun haqqında daha çox məlumat:\n{user_info}")
        except telebot.apihelper.ApiTelegramException as e:
            if e.result.status_code == 403:
                pass  # Engellendiyse hatayı görmezden gel
              
        start_matching(message)

    elif response == "👎":
        start_matching(message)
        #update_sql = "UPDATE userdb2 SET likeing = likeing - 1 WHERE id = %s"
        #update_val = (chat_id,)
        #cursor.execute(update_sql, update_val)
        #db.commit()
    else:
        bot.reply_to(message, "Sadəcə ❤️ vəya 👎 işarəsi qoyun.")

@bot.message_handler(commands=['info'])
def send_info(message):
    chat_id = message.chat.id

    info_message = (
        "Əvvəlcə bunu deyim. Başda qeydiyyatdan keçdiyin zaman, yazdığın və göndərdiyin bütün məlumatların qarşı cinsə görsənəcək. "
        "Əgər şəklin vəya istifadəçi adın pisdirsə, /profil yazıb bunları düzəldə bilərsən⚙️. "
        "Əsasən özün haqqında bir şəkil qoysan qarşı cinslərin səni bəyənə bilərlər.\n\n"
        "Bəs necə mesajlaşa bilərsən? 💌 - Səni əgər birisi bəyənərsə avtomatik sənə bildiriş gəlir. "
        "Bildirişin sonunda isə mesaj ata biləmən üçün bəyənən kişinin istifadəçi adı yazılır. "
        "Onun üzərinə basaraq mesaj göndərə bilərsən.\n\n"
        "/match nə işə yarayır? 📇 - Eyni şəkildə onlar necə səni bəyənə bilirsə, səndə onları bəyənə bilərsən. "
        "Onların xoşuna gəlsən mesaj ata bilərlər.\n\n"
        "/mesaj nə işə yarayır? 🧰 - Bu komut ilə adminlə mesajlaşa bilərsən. "
        "Hər hansı bir sualın və ya cinsini səhv seçmisənsə sənə kömək edə biləcək tək admin vardır.\n\n"
        "/VIP nə işə yarayır? 💸 - Bildiyiniz kimi eşleşmələrdə günlük limit var. "
        "Bu limit günlük 6-dır. Limit sizə bəs etmirsə VIP istifadəçi alaraq limitinizi 24 edə bilərsiniz. "
        "Bununlada bitmir, eşleşdiyiniz kişilərə istərsəniz bir dəfəlik mesaj göndərə bilərsiniz. "
        "Qarşı cinsiniz sizin göndərdiyiniz mesaja qarşılıq verə bilər.\n\n"
        "/versiya nə işə yarayır? 🗃️ - Buradan bot-da nələr əlavə olunduğunu haqqında ətraflı məlumat ala bilərsiniz.\n\n"
        "/trade nə işə yarayır? 🛍️ - Sizlərə Azərbaycanın ən ucuz və qarantiyalı servislərini sunuruq 🎉. "
        "100% güvənilirdir, onlayn ödəmə edə bilərsiniz. Maksimum 24 saat ərzində sifarişləriniz tamamlanır.\n\n"
        "/socialmedia nə işə yarayır? 🎭 - Heart2Heart bot-un aktiv sosial media hesablarını buradan əldə edə bilərsiniz."
    )

    bot.send_message(chat_id, info_message)

@bot.message_handler(commands=['versiya'])
def send_version_info(message):
    chat_id = message.chat.id

    version_info = (
        "Heart2Heart Versiyaları:\n\n"
        "Heart2Heart V1 Beta - Əlavə olunanlar:\n"
        "1. /qeydiyyat\n"
        "2. /profil\n\n"
        "Heart2Heart V1.1 Beta - Əlavə olunanlar:\n"
        "1. /qeydiyyat\n"
        "2. /profil\n"
        "3. /match\n"
        "4. /mesaj\n\n"
        "Heart2Heart V2 Aktiv versiya - Əlavə olunanlar:\n"
        "1. /qeydiyyat\n"
        "2. /profil📜\n"
        "3. /match🔍\n"
        "4. /info🧾\n"
        "5. /haqqimizda⚒️\n"
        "6. /mesaj📝\n"
        "7. /VIP🌐\n"
        "8. /versiya📂\n"
        "9. /trade🛍️\n"
        "10. /socialmedia🃏"
    )

    bot.send_message(chat_id, version_info)
  
@bot.message_handler(commands=['haqqimizda'])
def send_about_us_info(message):
    chat_id = message.chat.id

    about_us_info = (
        "Salam, biz Heart2Heart Company. Sənə xidmət verə bilməyimiz üçün Heart2Heart adı altında bir bot düzəltdiq. "
        "Əsas məqsidimiz Azərbaycanda ən böyük telegram botlarından birini düzəltmək.\n\n"
        "Bəs Heart2Heart-ün qurucusu kimdir? - Heart2Heart-ün qurucusu Zadeh nickname-li bir programistdir. "
        "Deyə biləcəyim bir çox şeyi dedim. Sualın varsa /mesaj yazaraq adminə(yəni mənə) mesajını göndərə bilərsən. "
        "Bot aktiv deyilsə Heart2Heart-ün instagram səhifəsinə (heart2heart_telegram) və ya şəxsi instagram səhifəmə (i._zadeh) mesaj göndərə bilərsən."
    )
    bot.send_message(chat_id, about_us_info)

@bot.message_handler(commands=['VIP'])
def send_vip_info(message):
    chat_id = message.chat.id

    vip_info = (
        "Ödəniş - Online; Ödəmə Sistemi - M10; Aktiv deyil!\n"
        "1 aylıq - 2 manat; Üstünlükləri: Günlük 24 eşleşmə limiti, Sizi digər istifadəçilərdən ayıran Onay Rozeti, "
        "eşleşmədə istədiyiniz birinə sadəcə 1 dəfəyə məxsus mesaj göndərə bilərsiniz. "
        "Yəni eşleşdiyiniz hər istifadəçiyə 1 dəfəlik mesaj göndərə bilərsiniz."
    )

    bot.send_message(chat_id, vip_info)

# get_user_info fonksiyonunun içinde
def get_user_info(chat_id, usernamesend):
    sql = "SELECT username, age, region, info FROM userdb2 WHERE id = %s"
    val = (chat_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        username, age, region, info = result
        user_info = f"{username} - {age}, {region}\n{info}\n\n@{usernamesend}"
        return user_info
    else:
        return "İstifadəçi məlumatları tapılmadı."

def photo_send(chat_id): 
  sql = "SELECT foto1 FROM userdb2 WHERE id = %s"
  val = (chat_id,)
  cursor.execute(sql, val)
  result = cursor.fetchone()
  foto1 = result
  photogo = f"{foto1}"
  
@bot.message_handler(commands=['qeydiyyat'])
def save_user(message):
    chat_id = message.chat.id

    # Check if the user is already registered
    check_sql = "SELECT * FROM userdb2 WHERE id = %s"
    check_val = (chat_id,)
    cursor.execute(check_sql, check_val)
    result = cursor.fetchone()

    if result:
        username = result[1]
        bot.reply_to(message, "Qeydiyyatdan keçmisən :)")
    else:
      
        bot.reply_to(message, "İstifadəçi adınızı yazın.")
        bot.register_next_step_handler(message, save_username_step, chat_id)

def save_username_step(message, chat_id):
    username = message.text
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
    
    # Yaş aralığındaki düğmeleri ekleyin (10 ila 30)
    for age in range(10, 31):
        markup.add(types.KeyboardButton(str(age)))

    bot.reply_to(message, "Yaşınızı seçin:", reply_markup=markup)
    bot.register_next_step_handler(message, save_age_step, chat_id, username)

def save_age_step(message, chat_id, username):
    age = message.text

    # Yaşın geçerli bir sayı olup olmadığını kontrol edin
    if not age.isdigit() or not (10 <= int(age) <= 30):
        bot.reply_to(message, "Zəhmət olmasa 10 ila 30 arasında bir yaş seçin.")
        bot.register_next_step_handler(message, save_age_step, chat_id, username)
        return

    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(types.KeyboardButton("Kişi"), types.KeyboardButton("Qadın"))
    
    bot.reply_to(message, "Cinsiyyətinizi seçin", reply_markup=markup)
    bot.register_next_step_handler(message, save_gender_step, chat_id, username, age)

def save_gender_step(message, chat_id, username, age):
    gender = message.text.lower()
    if gender == "kişi":
        gender = "erkek"
    if gender == "qadın":
        gender = "kadin"

    if gender not in ["erkek", "kadin"]:
        bot.reply_to(message, "Zəhmət olmasa sadəcə butonlardan istifadə edərək cinsiyyətinizi yazın 😠")
        bot.register_next_step_handler(message, save_gender_step, chat_id, username, age)
        return

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    regions = ["Baku", "Həzi Aslanov", "Əhmədli", "28 may", "Nərimanov", "Xalqlar", "Nizami", "Nəsimi", "Sabunçu", "Səbail", "Xətai", "Xəzər"]
    
    for region in regions:
        markup.add(types.KeyboardButton(region))

    bot.reply_to(message, "Yaşadığınız bölgəni seçin:", reply_markup=markup)
    bot.register_next_step_handler(message, save_region_step, chat_id, username, age, gender)

def save_region_step(message, chat_id, username, age, gender):
    region = message.text
    bot.reply_to(message, "Özünüz haqqında qısa bir məlumat yazın(300 hərfi keçməyin!)")
    bot.register_next_step_handler(message, save_info_step, chat_id, username, age, gender, region)

def save_info_step(message, chat_id, username, age, gender, region):
    info = message.text
    if len(info) > 300:
        bot.reply_to(message, "300 hərfi keçmədən qısa özünüz haqqda məlumat yazın.")
        bot.register_next_step_handler(message, save_info_step, chat_id, username, age, gender, region)
        return

    likeing = 3  # Default value for likeing

    bot.reply_to(message, "Şəklinizi göndərin")
    bot.register_next_step_handler(message, save_photo_step, chat_id, username, age, gender, region, info, likeing)

def save_photo_step(message, chat_id, username, age, gender, region, info, likeing):
    if message.photo:
        photo = message.photo[-1].file_id

        # Insert user data into the 'userdb2' table
        sql = "INSERT INTO userdb2 (id, username, age, gender, region, info, foto1, likeing, history) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '0')"
        val = (chat_id, username, age, gender, region, info, photo, likeing)

        cursor.execute(sql, val)
        db.commit()

        bot.reply_to(message, f"İstifadəçi '{username}' TƏBRİKLƏR! Axır ki qeydiyyatdan keçdin. /start yazaraq başlaya bilərsən :)")

    else:
        bot.reply_to(message, "Zəhmət olmasa sadəcə şəkil göndərin 😡")
        bot.register_next_step_handler(message, save_photo_step, chat_id, username, age, gender, region, info, likeing)

def update_username_step(message, chat_id):
    bot.reply_to(message, "Yeni İstifadəçi adınızı yazın.")
    bot.register_next_step_handler(message, save_updated_username, chat_id)

def save_updated_username(message, chat_id):
    new_username = message.text
    update_sql = "UPDATE userdb2 SET username = %s WHERE id = %s"
    update_val = (new_username, chat_id)
    cursor.execute(update_sql, update_val)
    db.commit()
    bot.reply_to(message, "Uğurla güncəlləndi!")

def update_age_step(message, chat_id):
    bot.reply_to(message, "Yeni yaşınızı yazın.")
    bot.register_next_step_handler(message, save_updated_age, chat_id)

def save_updated_age(message, chat_id):
    new_age = message.text
    update_sql = "UPDATE userdb2 SET age = %s WHERE id = %s"
    update_val = (new_age, chat_id)
    cursor.execute(update_sql, update_val)
    db.commit()
    bot.reply_to(message, "Uğurla güncəlləndi! Daha cavan görünürsən 🤔")

def update_info_step(message, chat_id):
    bot.reply_to(message, "Özünüz haqqında yeni məlumatları yazın")
    bot.register_next_step_handler(message, save_updated_info, chat_id)

def save_updated_info(message, chat_id):
    new_info = message.text
    update_sql = "UPDATE userdb2 SET info = %s WHERE id = %s"
    update_val = (new_info, chat_id)
    cursor.execute(update_sql, update_val)
    db.commit()
    bot.reply_to(message, "Uğurla güncəlləndi!")

def update_photo_step(message, chat_id):
    bot.reply_to(message, "Yeni şəklinizi göndərin")
    bot.register_next_step_handler(message, save_updated_photo, chat_id)

def save_updated_photo(message, chat_id):
    if message.photo:
        new_photo = message.photo[-1].file_id

        update_sql = "UPDATE userdb2 SET foto1 = %s WHERE id = %s"
        update_val = (new_photo, chat_id)
        cursor.execute(update_sql, update_val)
        db.commit()

        bot.reply_to(message, "Uğurla güncəlləndi!.")
    else:
        bot.reply_to(message, "Axı dedim sənə! Sadəcə şəkil göndər😡")

def request_admin_message(message):
    chat_id = message.chat.id

    # Kullanıcıdan mesajı isteyin
    bot.reply_to(message, "Adminə göndərmək istədiyiniz mesajı yazın:")
    bot.register_next_step_handler(message, send_admin_message, chat_id)

# Admin mesajını alıp gönderen adım
def send_admin_message(message, user_chat_id):
    admin_chat_id = "5112613151"  # Adminin chat_id'sini buraya girin
    user_message = message.text

    # Kullanıcının chat_id'sini mesaja ekleyerek admin'e mesaj gönderin
    admin_message = f"Kullanıcı ({user_chat_id}):\n{user_message}"
    bot.send_message(admin_chat_id, admin_message)
    
    # Kullanıcıya mesajın gönderildiğini bildirin
    bot.reply_to(message, "Mesajınız göndərildi!")


@bot.message_handler(commands=['allmesaj'])
def initiate_admin_message_to_all_users(message):
    # Sadece adminin chat_id'siyle uyumlu mesajlar işlenir
    if message.chat.id == 5112613151:  # Adminin chat_id'sini buraya girin
        bot.reply_to(message, "Bütün istifadəçilərə mesaj göndərmək istədiyiniz mesajı yazın:")
        bot.register_next_step_handler(message, send_admin_message_to_all_users)
    else:
        bot.reply_to(message, "Bu komutu yalnızca admin kullanabilir.")

def send_admin_message_to_all_users(message):
    admin_message = message.text
    sql = "SELECT id FROM userdb2"
    cursor.execute(sql)
    user_ids = cursor.fetchall()

    for user_id in user_ids:
        try:
            user_id = user_id[0]
            bot.send_message(user_id, f"Admin mesajı:\n\n{admin_message}")
        except Exception as e:
            print(f"Hata oluştu: {e}")

    bot.reply_to(message, "Bütün istifadəçilərə mesaj göndərildi!")

@bot.message_handler(commands=['mesaj'])
def initiate_user_message(message):
    request_admin_message(message)

# Admin mesajı gönderme adımı
def send_admin_message_to_user(message, admin_chat_id, user_chat_id):
    user_message = message.text

    # Admin tarafından girilen mesajı kullanıcının chat_id'sine ekleyerek gönderin
    user_message_with_admin_info = f"Admindən mesajınız var!\n\n{user_message}"
    bot.send_message(user_chat_id, user_message_with_admin_info)

    # Admin'e mesajın gönderildiğini bildirin
    bot.send_message(admin_chat_id, "Mesajınız gönderildi!")

# Admin'in göndermek istediği mesajı alıp kullanıcı chat_id'sini soran adım
def request_user_chat_id(message):
    admin_chat_id = message.chat.id
    bot.reply_to(message, "Mesaj göndərmək istədiyiniz istifadəçinin chat ID'sini yazın:")
    bot.register_next_step_handler(message, request_user_message, admin_chat_id)

# Admin'in mesajını alıp kullanıcıya gönderen adım
def request_user_message(message, admin_chat_id):
    user_chat_id = message.text

    # Girilen chat_id'yi kontrol edin ve geçerliyse mesajı alın
    try:
        user_chat_id = int(user_chat_id)
        bot.reply_to(message, "Göndərmək istədiyiniz mesajı yazın:")
        bot.register_next_step_handler(message, send_admin_message_to_user, admin_chat_id, user_chat_id)
    except ValueError:
        bot.reply_to(message, "Yanlış chat ID. Xahiş edirəm düzgün bir chat ID yazın.")

@bot.message_handler(commands=['adminmesaj'])
def initiate_admin_message(message):
    # Sadece adminin chat_id'siyle uyumlu mesajlar işlenir
    if message.chat.id == 5112613151:  # Adminin chat_id'sini buraya girin
        request_user_chat_id(message)
    else:
        bot.reply_to(message, "Bu komutu yalnızca admin kullanabilir.")
      
@bot.message_handler(commands=['profil'])
def show_profile(message):
    chat_id = message.chat.id

    # Fetch user data from the 'userdb2' table
    sql = "SELECT username, age, region, info, foto1 FROM userdb2 WHERE id = %s"
    val = (chat_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()

    if result:
        username, age, region, info, foto1 = result
        bot.send_photo(chat_id, foto1, caption=f"{username} - {age}, {region}\n{info}")

        question_text = (
            "1. İstifadəçi adını dəyişdirmək\n"
            "2. Yaşı dəyişdirmək\n"
            "3. Məlumat dəyişdirmək\n"
            "4. Şəkli dəyişdirmək\n"
            "0. Çıxış"
        )

        # Create a keyboard with the options
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(types.KeyboardButton("1"), types.KeyboardButton("2"), types.KeyboardButton("3"), types.KeyboardButton("4"), types.KeyboardButton("0"))
        
        bot.reply_to(message, question_text, reply_markup=markup)
    else:
        bot.reply_to(message, "Əvvəlcə qeydiyyatdan keçməlisən. /qeydiyyat yazaraq qeydiyyatdan keç")

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    chat_id = message.chat.id
    user_input = message.text

    if user_input == '0':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        markup.add(types.KeyboardButton("/profil"), types.KeyboardButton("/match"), types.KeyboardButton("/mesaj"), types.KeyboardButton("/start"))
        bot.send_message(chat_id, "/start yazaraq məlumat al, və ya /match yazaraq eşleşməni başlat",reply_markup=markup)
    elif user_input == '1':
        bot.reply_to(message, "Yeni istifadəçi adınızı yazın.")
        bot.register_next_step_handler(message, save_updated_username, chat_id)
    elif user_input == '2':
        bot.reply_to(message, "Yeni yaşınızı yazın.")
        bot.register_next_step_handler(message, save_updated_age, chat_id)
    elif user_input == '3':
        bot.reply_to(message, "Yeni məlumat yazın")
        bot.register_next_step_handler(message, save_updated_info, chat_id)
    elif user_input == '4':
        update_photo_step(message, chat_id)


def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Hata oluştu: {e}")
            print("Kod durdu, 5 saniye sonra yeniden başlatılacak.")
            time.sleep(5)  # 5 saniye bekleyin ve yeniden başlatın

if __name__ == '__main__':
    bot.polling(none_stop=True)
