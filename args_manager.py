
# يقوم البرنامج النصي الذي شاركته بتكوين محلل وسيطات سطر الأوامر باستخدام argparseوحدة Python. يبدو أنك تقوم بدمج هذه التكوينات في تطبيق، ربما لأداة مثل Fooocus، والتي تُستخدم لإدارة نماذج التعلم الآلي أو لأغراض مماثلة.

# فيما يلي تفصيل سريع لما يفعله كل قسم:

# إضافة الحجج :

# --share:إضافة القدرة على المشاركة عبر Gradio.
# --preset:يسمح بتطبيق إعداد مسبق محدد لواجهة المستخدم.
# --disable-preset-selection:تعطيل خيار تحديد إعداد مسبق في واجهة المستخدم.
# --language:تعيين ملف ترجمة لغة محددة.
# --disable-offload-from-vram:إجبار النماذج على البقاء في VRAM، وهو أمر مفيد لإعدادات أجهزة معينة مثل تلك الموجودة على جهاز Mac.
# --theme:يسمح بالتبديل بين السمات الفاتحة والداكنة.
# --disable-image-log:يمنع كتابة الصور/السجلات إلى مجلد.
# --disable-analytics:تعطيل إرسال التحليلات.
# --disable-metadata:يمنع حفظ البيانات الوصفية للصور المُولدة.
# --disable-preset-download:إيقاف تنزيل النماذج المحددة مسبقًا.
# --disable-enhance-output-sorting:يمنع فرز الصور النهائية في المعرض.
# --enable-auto-describe-image:يصف الصور تلقائيًا عندما لا يتم تقديم أي مطالبة.
# --always-download-new-model:إجبار على تنزيل أحدث الموديلات.
# --rebuild-hash-cache:إعادة بناء ذاكرة التخزين المؤقت للنموذج/LoRA باستخدام عدد محدد من الخيوط.
# الإعدادات الافتراضية :

# disable_cuda_malloc=True:يضبط تخصيص ذاكرة CUDA على الوضع المعطل بشكل افتراضي.
# in_browser=True:يتم تشغيل التطبيق في المتصفح بشكل افتراضي.
# port=None:لم يتم تحديد منفذ افتراضي.
# تحليل الحجج :

# يتم تحليل الحجج باستخدام args_parser.parser.parse_args().
# المنطق الشرطي :

# إذا disable_analyticsتم تعيينه، فإنه يقوم بتعيين متغير بيئي لإيقاف تشغيل التحليلات.
# ضبط ما إذا كان يجب تشغيل التطبيق في متصفح استنادًا إلى الوسيطة.
# يتأكد من إلغاء تحميل النماذج من VRAM ما لم يتم تعطيلها صراحةً.
# هذا الإعداد مرن للغاية ويبدو أنه مصمم لتكوين واجهة مستخدم أو تطبيق للتعلم الآلي.
import ldm_patched.modules.args_parser as args_parser

args_parser.parser.add_argument("--share", action='store_true', help="Set whether to share on Gradio.")

args_parser.parser.add_argument("--preset", type=str, default=None, help="Apply specified UI preset.")
args_parser.parser.add_argument("--disable-preset-selection", action='store_true',
                                help="Disables preset selection in Gradio.")

args_parser.parser.add_argument("--language", type=str, default='default',
                                help="Translate UI using json files in [language] folder. "
                                  "For example, [--language example] will use [language/example.json] for translation.")

# For example, https://github.com/lllyasviel/Fooocus/issues/849
args_parser.parser.add_argument("--disable-offload-from-vram", action="store_true",
                                help="Force loading models to vram when the unload can be avoided. "
                                  "Some Mac users may need this.")

args_parser.parser.add_argument("--theme", type=str, help="launches the UI with light or dark theme", default=None)
args_parser.parser.add_argument("--disable-image-log", action='store_true',
                                help="Prevent writing images and logs to the outputs folder.")

args_parser.parser.add_argument("--disable-analytics", action='store_true',
                                help="Disables analytics for Gradio.")

args_parser.parser.add_argument("--disable-metadata", action='store_true',
                                help="Disables saving metadata to images.")

args_parser.parser.add_argument("--disable-preset-download", action='store_true',
                                help="Disables downloading models for presets", default=False)

args_parser.parser.add_argument("--disable-enhance-output-sorting", action='store_true',
                                help="Disables enhance output sorting for final image gallery.")

args_parser.parser.add_argument("--enable-auto-describe-image", action='store_true',
                                help="Enables automatic description of uov and enhance image when prompt is empty", default=False)

args_parser.parser.add_argument("--always-download-new-model", action='store_true',
                                help="Always download newer models", default=False)

args_parser.parser.add_argument("--rebuild-hash-cache", help="Generates missing model and LoRA hashes.",
                                type=int, nargs="?", metavar="CPU_NUM_THREADS", const=-1)

args_parser.parser.set_defaults(
    disable_cuda_malloc=True,
    in_browser=True,
    port=None
)

args_parser.args = args_parser.parser.parse_args()

# (Disable by default because of issues like https://github.com/lllyasviel/Fooocus/issues/724)
args_parser.args.always_offload_from_vram = not args_parser.args.disable_offload_from_vram

if args_parser.args.disable_analytics:
    import os
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

if args_parser.args.disable_in_browser:
    args_parser.args.in_browser = False

args = args_parser.args
