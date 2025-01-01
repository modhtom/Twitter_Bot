from Helpers import TweetClient as client, Email as email
import datetime
import time
import traceback

last_sala_time = None
dua_index = 1
last_minute = None
Image_index = 0
first_tweet_in_the_day = True
sala_index = 1
sala = [
    "اللَّهُمَّ ‌صَلِّ ‌عَلَى ‌مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا صَلَّيْتَ عَلَى آلِ إِبْرَاهِيمَ، وَبَارِكْ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّدٍ كَمَا بَارَكْتَ عَلَى آلِ إِبْرَاهِيمَ ‌فِي ‌الْعَالَمِينَ ‌إِنَّكَ ‌حَمِيدٌ ‌مَجِيدٌ",
    "‌اللهُمَّ ‌صَلِّ ‌عَلَى ‌مُحَمَّدٍ ‌وَعَلَى ‌أَهْلِ ‌بَيْتِهِ، ‌وَعَلَى ‌أَزْوَاجِهِ وَذُرِّيَّتِهِ، كَمَا صَلَّيْتَ عَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ، وَبَارِكْ عَلَى مُحَمَّدٍ وَعَلَى أَهْلِ بَيْتِهِ، وَعَلَى أَزْوَاجِهِ وَذُرِّيَّتِهِ، كَمَا بَارَكْتَ عَلَى آلِ إِبْرَاهِيمَ إِنَّكَ حَمِيدٌ مَجِيدٌ",
    "‌اللهُمَّ ‌صَلِّ ‌عَلَى ‌مُحَمَّدٍ ‌النَّبِيِّ ‌الْأُمِّيِّ وَعَلَى آلِ مُحَمَّدٍ، كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ وَآلِ إِبْرَاهِيمَ، وَبَارِكْ عَلَى مُحَمَّدٍ النَّبِيِّ الْأُمِّيِّ، كَمَا بَارَكْتَ عَلَى إِبْرَاهِيمَ وَعَلَى آلِ إِبْرَاهِيمَ، إِنَّكَ حَمِيدٌ مَجِيدٌ"
    "اللَّهُمَّ ‌صَلِّ ‌عَلَى ‌مُحَمَّدٍ ‌عَبْدِكَ ‌وَرَسُولِكَ، كَمَا صَلَّيْتَ عَلَى إِبْرَاهِيمَ، وَبَارِكْ عَلَى مُحَمَّدٍ، وَعَلَى آلِ مُحَمَّدٍ، كَمَا باركت على إبراهيم وآل إبراهيم",
    "اللهم صل وسلم على سيدنا محمد صلاة تحل بها عقدتي، وتفرج بها كربتي، وتمحو بها خطيئتي، وتقضي بها حاجتي",
    "للَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَأَنْزِلْهُ الْمَنْزِلَ الْمُقَرَّبَ مِنْكَ يَوْمَ الْقِيَامَة.",
    "اللهم صلّ صلاة كاملة وسلّم سلاماً تاماً على سيدنا محمد النبي الأميّ الذي تنحل به العقد، وتنفرج به الكرب، وتُقضى به الحوائج، وتنال به الرغائب وحسن الخواتم، ويستسقى الغمام، وعلى آله وصحبه عدد كل معلوم لله.",
    "اللهم صل وسلم على سيدنا محمد وعلى آله، صلاة تكون لنا طريقاً لقربه، وتأكيداً لحبه، وباباً لجمعنا عليه، وهدية مقبولة بين يديه، وسلم وبارك كذلك أبداً، وارض عن آله وصحبه السعداء، واكسنا حُلل الرضا.",
    "اللهم صل وسلم على سيدنا محمد صلاة تهب لنا بها أكمل المراد وفوق المراد، في دار الدنيا ودار المعاد، وعلى آله وصحبه وبارك وسلم عدد ما علمت وزنة ماعلمت وملء ما علمت.",
    "اللهم صل على سيدنا محمد صلاة تنجينا بها من جميع الأهوال والآفات، وتقضي بها جميع الحاجات، وتطهرنا بها من جميع السيئات، وترفعنا بها عندك أعلى الدرجات، وتبلغنا بها أقصى الغايات من جميع الخيرات في الحياة وبعد الممات، وعلى آله وصحبه وسلم تسليماً كثيراً.",
    "اللهم صل على محمد عدد الرمل والحصى، في مستقر الأرضين شرقها وغربها وسهلها وجبالها، من يوم خلقت الدنيا إلى يوم القيامة، في كل يوم ألف مرة .",
    "اللهم صلّ على محمد وعلى آل محمد، كما صليت على إبراهيم وعلى آل إبراهيم، وبارك على محمد وعلى آل محمد، كما باركت على إبراهيم وعلى آل إبراهيم، إنك حميد مجيد.",
    "اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ وَعَلَى آلِ مُحَمَّد في الأَوَّلِينَ وَالآخِرِينَ، وَفِي الْمَلأِ الأَعْلَى إِلَى يَوْمِ الْدِّينِ.",
    "اللهم صل وسلم وبارك على سيدنا محمد وعلى آله وصحبه عدد ما في علم الله، صلاةً دائمة بدوام ملك الله.",
    "اللهم صل وسلم وبارك على سيدنا محمد وعلى آله وصحبه عدد كمال الله وكما يليق بكماله.",
    "اللهم صل وسلم وبارك على سيدنا محمد وعلى آله عدد حروف القرآن حرفاً حرفاً، وعدد كل حرف ألفاً ألفاً، وعدد صفوف الملائكة صفاً صفاً، وعدد كل صف ألفاً ألفاً، وعدد الرمال ذرة ذرة، وعدد ما أحاط به علمك، وجرى به قلمك، ونفذ به حكمك في برك وبحرك، وسائر خلقك.",
    "اللهم صلِّ وسلم على صاحب الخُلق العظيم والقدر الفخيم مَن أرسلته رحمة للعالمين سيدنا محمد وعلى آله وصحبه، وألحقنا بخُلقه وأدّبنا بأدبه، وأحيي فينا وفي أُمته هذه المعاني يا كريم.",
    "اللهم صل على سيدنا محمد النبي الأمي الحبيب العالي القدر العظيم الجاه، واغنني بفضلك عمن سواك، وعلى آله و صحبه وسلم، اللهم أعني على ذكرك وشكرك و حسن عبادتك، والطف بي فيما جرت به المقادير، و اغفر لي و لجميع المسلمين، وارحمني و إياهم برحمتك الواسعة في الدنيا والآخرة يا كريم يا رحيم",
    "الصلاة والسلام عليك يا حبيبي يا رسول الله، أنت المقدم في كل مقام، الصلاة والسلام عليك يا خيرة الله من خلقه أجمعين، الصلاة والسلام عليك وعلى آلك وأصحابك وأزواجك أجمعين، رب اغفر لي ولوالدي وارحمهما كما ربياني صغيراً.",
    "اللهم صَلِ عَلَى سَيِّدِنَا مُحَمَّدٍ أَصْلِ الأُصُول، نُورِ الْجَمَالِ، وَسِرِّ الْقَبُول، أَصْلِ الْكَمَالِ، وَبَابِ الْوُصُول، صلاةً تَدُومُ وَلا تَزُول، اللَّهُمَّ صَلِّ عَلَى سَيِّدِنَا مُحَمِّدٍ أَكْرَمِ نَبِيٍّ، وَأَعْظَمِ رَسُول مَنْ جَاهُهُ مَقْبُول، وَمُحِبُّهُ مَوْصُول، الْمُكَرَّمُ بِالصِّدْقِ فِي الْخُرُوجِ وَالدُّخُول، صلاةً تَشْفِي مِنَ الأَسْقَامِ وَالنُّحُول وَالأَمْرَاضِ وَالذُّبُول، وَنَنْجُو بِهَا يَوْمَ الْكَرْبِ الْعَظِيمِ مِنَ الذُّهُول، صلاةً تَشْمَلُ آلَ بَيْتِ الرَّسُول وَالأَزْوَاجَ وَالأَصْحَابَ، وَتَعُمُّ الْجَمِيعَ بِالْقَبُول، الشَّبَابَ فِيهِمْ وَالْكُهُول، وَسَلِّمْ عَلَيْهِ وَعَلَى آلِهِ وَأَصْحَابِه أجمعين، آمِين.",
    "اللَّهُمَّ صَلِّ علَى مُحَمَّدٍ وعلَى آلِ مُحَمَّدٍ، كما صَلَّيْتَ علَى إبْرَاهِيمَ، وعلَى آلِ إبْرَاهِيمَ، إنَّكَ حَمِيدٌ مَجِيدٌ، اللَّهُمَّ بَارِكْ علَى مُحَمَّدٍ وعلَى آلِ مُحَمَّدٍ، كما بَارَكْتَ علَى إبْرَاهِيمَ، وعلَى آلِ إبْرَاهِيمَ إنَّكَ حَمِيدٌ مَجِيدٌ",
]
dua = [
    "(رَبَّنَا إِنَّنَا آمَنَّا فَاغْفِرْ لَنَا ذُنُوبَنَا وَقِنَا عَذَابَ النَّارِ)",
    " (رَّبِّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِمَن دَخَلَ بَيْتِيَ مُؤْمِنًا وَلِلْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ)",
    "(رَبِّ إِنِّي ظَلَمْتُ نَفْسِي فَاغْفِرْ لِي)",
    "(رَبَّنَا لاَ تُؤَاخِذْنَا إِن نَّسِينَا أَوْ أَخْطَأْنَا رَبَّنَا وَلاَ تَحْمِلْ عَلَيْنَا إِصْرًا كَمَا حَمَلْتَهُ عَلَى الَّذِينَ مِن قَبْلِنَا رَبَّنَا وَلاَ تُحَمِّلْنَا مَا لاَ طَاقَةَ لَنَا بِهِ وَاعْفُ عَنَّا وَاغْفِرْ لَنَا وَارْحَمْنَآ أَنتَ مَوْلاَنَا فَانصُرْنَا عَلَى الْقَوْمِ الْكَافِرِينَ).",
    "(اللَّهُمَّ اغْفِرْ لي خَطِيئَتي وَجَهْلِي، وإسْرَافِي في أَمْرِي، وَما أَنْتَ أَعْلَمُ به مِنِّي، اللَّهُمَّ اغْفِرْ لي جِدِّي وَهَزْلِي، وَخَطَئِي وَعَمْدِي، وَكُلُّ ذلكَ عِندِي، اللَّهُمَّ اغْفِرْ لي ما قَدَّمْتُ وَما أَخَّرْتُ، وَما أَسْرَرْتُ وَما أَعْلَنْتُ، وَما أَنْتَ أَعْلَمُ به مِنِّي، أَنْتَ المُقَدِّمُ وَأَنْتَ المُؤَخِّرُ، وَأَنْتَ علَى كُلِّ شيءٍ قَدِيرٌ).",
    "اللهم في يوم الجمعة نسألك أن تغفر ذنوبنا جميعها، وأن تتقبّل منّا توبتنا، وأن تعفو عنّا وترحمنا.",
    " اللهم اغفر ذنوبي، واستر عيوبي، واعفُ عن خطاياي، وتجاوز عن تقصيري وإسرافي في أمري.",
    "اللهم إنّا نسألك الجنّة وما قرّب إليها من قولٍ أو عمل، ونعوذ بك من النار وما قرّب إليها من قولٍ أو عمل، وأكرمنا بمغفرتك وتفضّل علينا بعفوك يا عفوّ يا غفور يا ذا الفضل والإحسان.",
    "اللهم أنت ملاذنا، وأنت مولانا، وأنت العليم بحالنا، إن لم ترحمنا يا رب فمن يرحمنا، وإن لم تغفر لنا فمن يغفر لنا، جئناك يا ربّي منيبين تائبين خاضعين نرجو مغفرتك ونخشى عذابك، ونسألك ألّا تغيب شمس يوم الجمعة إلّا وقد غفرت لنا ذنوبنا جميعها وتجاوزت عن صغيرها وكبيرها يا أرحم الراحمين يا رب",
    "اللهم قِنا عذابك يوم تبعث عبادك، وارحمنا واغفر لنا وجازنا بفضلك وجودك ولا تجازنا بأعمالنا.",
]
The_virtue = "فيوم الجمعة هو أفضل الأيام بدليل قوله صلى الله عليه وسلم: خير يوم طلعت عليه الشمس يوم الجمعة؛ فيه خلق آدم, وفيه أدخل الجنة, وفيه أخرج منها, ولا تقوم الساعة إلا في يوم الجمعة. رواه مسلم في صحيحه.\
كما قال صلى الله عليه وسلم: إن من أفضل أيامكم يوم الجمعة؛ فيه خلق آدم, وفيه قبض, وفيه النفخة, وفيه الصعقة, فأكثروا علي من الصلاة فيه, فإن صلاتكم معروضة علي، قال: قالوا: يا رسول الله, وكيف تعرض صلاتنا عليك وقد أرمت؟ يقولون: بليت، فقال: إن الله عز وجل حرم على الأرض أجساد الأنبياء. رواه أبو داود والنسائي وابن ماجه وغيرهم وصححه الشيخ الألباني."
AlKahf_reminder = "فإن قراءة سورة الكهف ليلة الجمعة أو يومها مستحبة، قال في فيض القدير للمناوي: يندب قراءتها يوم الجمعة وكذا ليلتها كما نص عليه الشافعي، وقد أخرج الحاكم في المستدرك، والبيهقي في السنن عن أبي سعيد الخدري رضي الله تعالى عنه أن النبي صلى الله عليه وسلم قال: من قرأ سورة الكهف يوم الجمعة، أضاء له من النور ما بين الجمعتين.\
وفي رواية عند الحاكم أنه صلى الله عليه وسلم قال: من قرأ سورة الكهف كما أنزلت، كانت له نوراً يوم القيامة من مقامه إلى مكة، ومن قرأ عشر آياتٍ من آخرها ثم خرج الدجال لم يسلط عليه...\
وهذه الزيادة التي وردت في هذه الرواية أخرجها مسلم في صحيحه وأبو داود والترمذي في سننهما وأحمد في مسنده."


def fri():
    global sala, dua, last_sala_time, sala_index, dua_index, last_minute, first_tweet_in_the_day, AlKahf_reminder, Image_index, The_virtue

    bot = client.TwitterBot()
    try:
        if first_tweet_in_the_day:
            bot.tweet(The_virtue)
            time.sleep(60 * 5)
            bot.i_tweet(
                "https://imgs.search.brave.com/dK5drzycq-jQ7f41UmtYRoLtI1LYKgDaC4Va9lxGAPA/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5lbHptYW5uZXdz/LmNvbS9pbWcvMTkv/MTEvMTUvMTU4NjUw/NDE0OTcyNzUxMDUu/cG5n"
            )
            time.sleep(60 * 5)
            bot.tweet(AlKahf_reminder)
            first_tweet_in_the_day = False
    except Exception as e:
        print(e)
        email.send(f"Error sending in fri function :\n{e}")


def friday_sala_dua():
    global sala, dua, last_sala_time, sala_index, dua_index, last_minute, first_tweet_in_the_day, AlKahf_reminder, Image_index, The_virtue
    try:
        bot = client.TwitterBot()
        now = datetime.datetime.now()
        while now.hour != 20:
            if last_sala_time is None or (now - last_sala_time).seconds >= 7200:
                bot.tweet(sala[sala_index])
                last_sala_time = now
                sala_index = (sala_index + 1) % len(sala)

            time.sleep(60)

        if last_minute is None or now.minute > last_minute:
            bot.tweet(dua[dua_index])
            last_minute = now.minute
            dua_index = (dua_index + 1) % len(dua)

            time.sleep(60 * 60 * 2)
    except Exception as e:
        error_message = (
            f"An error occurred while tweeting friday_sala_dua.\n"
            f"sala_index: {sala_index}, dua_index: {dua_index}\n"
            f"Error Type: {type(e).__name__}\n"
            f"Error Message: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        print(error_message)
        email.send(error_message)