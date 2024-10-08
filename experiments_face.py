# يؤدي هذا البرنامج النصي عملية اقتصاص الوجه باستخدام OpenCV لتحميل صورة ( lena.png)، ثم يعالجها باستخدام crop_imageوظيفة مخصصة من extras.face_cropالوحدة النمطية، ثم يحفظ الصورة المقصوصة الناتجة بتنسيق lena_result.png.

# تقسيم الكود:
# جاري تحميل الصورة ( cv2.imread) :

# img = cv2.imread('lena.png'):يقوم هذا السطر بتحميل الصورة lena.pngمن دليل العمل إلى imgالمتغير. يقوم OpenCV بتحميل الصورة بتنسيق BGR افتراضيًا.
# قص الوجه ( crop_image) :

# result = cropper.crop_image(img):يستخدم هذا السطر crop_imageالوظيفة من extras.face_cropالوحدة النمطية. ومن المتوقع أن تقوم هذه الوظيفة باكتشاف الوجه داخل الصورة وقصه. يتم تخزين الصورة المقصوصة في المتغير result.
# حفظ النتيجة ( cv2.imwrite) :

# cv2.imwrite('lena_result.png', result):يحفظ هذا السطر الصورة المقطوعة كما هي lena_result.pngفي دليل العمل.
# نقاط يجب مراعاتها:
# كشف الوجه :

# تأكد من تنفيذ crop_imageالوظيفة extras.face_cropبشكل صحيح لاكتشاف الوجه والقص.
# من المحتمل أن تستخدم الوظيفة إما نموذج اكتشاف الوجه المدرب مسبقًا أو خوارزميات مثل Haar Cascades أو Dlib أو طريقة تعتمد على التعلم العميق لاكتشاف الوجوه في الصورة.
# مسارات الملفات :

# 'lena.png'يفترض مسار الملف أن lena.pngالصورة موجودة في دليل العمل الحالي. إذا كانت الصورة موجودة في مكان آخر، فتأكد من توفير مسار الملف الصحيح.
# حدود اكتشاف الوجه :

# إذا لم يتم اكتشاف الوجه بشكل صحيح، crop_imageفقد تعيد الوظيفة الصورة الأصلية، أو قد تعيد نتيجة فارغة أو مقطوعة بشكل غير صحيح. تأكد من أن الصورة تحتوي على وجه واضح ومرئي.
# التوفير :

# تقوم الوظيفة cv2.imwriteبحفظ النتيجة بنفس التنسيق (BGR) الذي تمت معالجتها به، وبالتالي يظل تنسيق اللون متسقًا.
# مثال على التدفق المتوقع:
# حمولة lena.png.
# اكتشف الوجه واقتصاصه من الصورة باستخدام الوظيفة crop_image.
# احفظ الصورة المقصوصة باسم lena_result.png.
# استكشاف الأخطاء وإصلاحها:
# إذا lena_result.pngلم يتم الحفظ بشكل صحيح، فتأكد من أن crop_imageالأمر يعمل كما هو متوقع.
# تأكد من lena.pngوجود الملف في الدليل الصحيح أو قم بتحديث المسار وفقًا لذلك.
# اختبر وظيفة الاقتصاص باستخدام صور مختلفة للتأكد من سلوكها.


import cv2
import extras.face_crop as cropper


img = cv2.imread('lena.png')
result = cropper.crop_image(img)
cv2.imwrite('lena_result.png', result)
