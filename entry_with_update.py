# تم تصميم هذا البرنامج النصي لأتمتة عملية جلب التحديثات من مستودع Git البعيد، والتحقق من حالة الفرع الحالي، وتنفيذ إجراء مناسب بناءً على حالة المستودع. يستخدم البرنامج النصي المكتبة pygit2للتفاعل مع مستودع Git برمجيًا، مما يجعله جزءًا من نظام تحديث تلقائي.

# الخطوات الرئيسية موضحة:
# إعداد بيئة البرنامج النصي :

# يبدأ البرنامج النصي بتحديد الدليل الجذر للبرنامج النصي ( root = os.path.dirname(os.path.abspath(__file__)))، وإضافته إلى sys.path، وتغيير دليل العمل إلى هذا الجذر ( os.chdir(root)).
# يضمن هذا أن يتمكن البرنامج النصي من العثور على الوحدات النمطية أو الملفات واستيرادها بشكل صحيح بالنسبة لموقعه الخاص.
# تهيئة وجلب البيانات من Git Remote :

# يتم استخدام المكتبة pygit2للتفاعل مع Git:
# يقوم بتعطيل التحقق من ملكية Git pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)، ومن المرجح أن يتجاوز بعض عمليات التحقق من الملكية.
# تم تهيئة المستودع ( repo = pygit2.Repository(...))، وتم استرجاع الفرع الحالي.
# يقوم بجلب التحديثات من الجهاز البعيد (عادةً origin)، مما يضمن أن الفرع المحلي على علم بأحدث التغييرات على الجهاز البعيد.
# تحديد حالة الفرع :

# يتحقق البرنامج النصي مما إذا كان الفرع المحلي محدثًا، وما إذا كان بإمكانه تنفيذ دمج سريع للأمام، أو ما إذا كانت التغييرات المحلية بحاجة إلى الدمج يدويًا:
# محدث : إذا كان الفرع المحلي متزامنًا بالفعل مع الفرع البعيد، فسيتم طباعة "محدث بالفعل".
# دمج التقديم السريع : إذا كان الجهاز البعيد يحتوي على تغييرات جديدة ولكن لا يوجد تعارضات، فإنه يقوم بالتقديم السريع للفرع المحلي ليتطابق مع الفرع البعيد.
# مطلوب دمج يدوي : إذا انحرف الفرع المحلي عن الفرع البعيد، يتوقف البرنامج النصي ويبلغ المستخدم أنه قد يحتاج إلى حل تعارضات الدمج يدويًا.
# معالجة الأخطاء :

# يتم التقاط أي أخطاء أثناء العملية بواسطة try-exceptكتلة، ويتم طباعة رسالة "فشل التحديث" مع تفاصيل الخطأ.
# الاستيراد النهائي :

# بعد معالجة عمليات Git، يقوم البرنامج النصي بالاستيراد من launchالوحدة النمطية ( from launch import *). وهذا يعني أن البرنامج النصي يستمر في تشغيل المهام الأخرى المحددة في launchالوحدة النمطية بعد تحديث المستودع.
# حالات الاستخدام الممكنة:
# نظام التحديث الآلي : يمكن استخدام البرنامج النصي في تطبيق حيث تكون التحديثات التلقائية من مستودع بعيد ضرورية. فهو يقوم بالبحث عن التحديثات والتحقق منها والتقدم السريع إذا أمكن، مما يقلل الحاجة إلى التدخل اليدوي.
# خطوط أنابيب CI/CD : يمكن أن تكون جزءًا من خط أنابيب التكامل المستمر أو النشر حيث يلزم تحديث الكود بشكل متكرر.
# التحسينات والاقتراحات:
# الإخراج المفصل :

# قد يكون من المفيد إضافة تسجيل أكثر تفصيلاً (على سبيل المثال، printالبيانات) لكل خطوة، حتى يتمكن المستخدم من تتبع ما يحدث أثناء التنفيذ.
# التعامل مع عمليات الدمج غير السريعة :

# يتوقف البرنامج النصي حاليًا إذا كان هناك حاجة إلى دمج غير سريع التقديم. يمكنك توسيع هذا لتنفيذ دمج تلقائي، أو محاولة حل النزاع، أو إخطار المستخدم بشكل أكثر وضوحًا بشأن الحاجة إلى التدخل اليدوي.
# التحقق من صحة الفروع :

# تأكد من وجود الفرع محليًا وعن بُعد قبل محاولة إجراء العمليات، حيث أن الفروع المفقودة قد تؤدي إلى إثارة الاستثناءات.
# الفشل الرشيق :

# بدلاً من التوقف عند استثناء ما، فكر في تقديم إرشادات أو خيارات للحل اليدوي (على سبيل المثال، طباعة خطوات محددة لحل المشكلة).
import os
import sys


root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)


try:
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    branch_name = repo.head.shorthand

    remote_name = 'origin'
    remote = repo.remotes[remote_name]

    remote.fetch()

    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Did you modify any file?")
except Exception as e:
    print('Update failed.')
    print(str(e))

print('Update succeeded.')
from launch import *
