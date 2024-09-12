# https://github.com/sail-sg/EditAnything/blob/main/sam2groundingdino_edit.py
# يستخدم مقتطف التعليمات البرمجية المقدم صورة ( cat.webp)، ويحولها إلى مصفوفة NumPy، ويطبق قناع التجزئة باستخدام generate_mask_from_image. من المحتمل أن تستخدم هذه العملية نهج SAM (نموذج التجزئة لأي شيء)، حيث تجمع بين الخيارات المحددة في الفصل SAMOptionsلإنشاء أقنعة حول مناطق الاهتمام (على سبيل المثال، عين القط في هذه الحالة). ثم يتم عرض القناع الناتج باستخدام PIL.Image.

# المكونات الرئيسية:
# تحميل الصورة ومعالجتها مسبقًا :

# يتم تحميل الصورة من ملف ( cat.webp) باستخدام PIL.Image.
# يتم تحويل الصورة إلى مصفوفة NumPy ( image) للمعالجة باستخدام وظيفة إنشاء القناع.
# خيارات SAM :

# يحدد هذا الهيكل معلمات مختلفة لتوليد القناع:
# dino_prompt:يحدد المنطقة أو الكائن محل الاهتمام ("العين" في هذه الحالة).
# dino_box_threshold:يتحكم في عتبة الثقة لمربعات التحديد.
# dino_text_threshold:يحدد حدًا للكشف عن المنطقة المستندة إلى النص.
# dino_erode_or_dilate:ضبط القناع (يؤدي إلى تآكل النتيجة أو توسيعها).
# max_detections:يحدد عدد المناطق التي سيتم اكتشافها (2 في هذه الحالة).
# model_type:اختر نموذج التجزئة (على سبيل المثال، نموذج ViT).
# إنشاء القناع :

# تأخذ الوظيفة generate_mask_from_imageصورة الإدخال وتطبق خيارات SAM لإنتاج قناع تقسيم. يحدد القناع المنطقة المقابلة للمطالبة (هنا، يركز على "عين" القطة).
# قناع العرض :

# يتم تحويل القناع الناتج مرة أخرى إلى صورة PIL وعرضها باستخدام merged_masks_img.show().
# ملحوظات:
# من المرجح أن تكون الوظيفة generate_mask_from_imageجزءًا من وحدة إضافية تسمى inpaint_maskالتي تستخدم نهجًا يعتمد على SAM لتجزئة أو اكتشاف مناطق معينة من الاهتمام استنادًا إلى المطالبة المقدمة ( dino_prompt).

# يجب عليك التأكد من:

# التبعيات : تأكد من تثبيت جميع التبعيات المطلوبة، مثل PIL، numpyوالوحدة النمطية extras.inpaint_mask، والتي قد تعتمد على مكتبات أخرى مثل PyTorch.
# إعداد النموذج : يجب تنزيل نموذج SAM ( vit_b) أو النماذج الأخرى بشكل صحيح وإعدادها لكي يعمل إنشاء القناع بشكل صحيح.
# الإخراج:
# النتيجة المتوقعة هي صورة بنفس حجم الصورة الأصلية، حيث يتم إخفاء مناطق معينة (مثل عين القطة) وفقًا للمطالبة. سيتم بعد ذلك عرض القناع.
import numpy as np
from PIL import Image

from extras.inpaint_mask import SAMOptions, generate_mask_from_image

original_image = Image.open('cat.webp')
image = np.array(original_image, dtype=np.uint8)

sam_options = SAMOptions(
    dino_prompt='eye',
    dino_box_threshold=0.3,
    dino_text_threshold=0.25,
    dino_erode_or_dilate=0,
    dino_debug=False,
    max_detections=2,
    model_type='vit_b'
)

mask_image, _, _, _ = generate_mask_from_image(image, sam_options=sam_options)

merged_masks_img = Image.fromarray(mask_image)
merged_masks_img.show()
