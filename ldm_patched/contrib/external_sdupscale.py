# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# يحدد الكود المقدم فئة SD_4XUpscale_Conditioningتُستخدم لرفع مستوى الصور باستخدام التكييف في إعداد نموذج الانتشار. وفيما يلي نظرة عامة على كيفية عملها:

# المكونات الرئيسية:
# تعريف الفصل :

# SD_4XUpscale_Conditioning:فئة مصممة للتعامل مع رفع مستوى الصورة وتكييفها لنماذج الانتشار.
# INPUT_TYPESطريقة :

# يحدد أنواع المدخلات التي تتوقعها الفئة:
# images:الصور المدخلة التي سيتم تحسينها.
# positive:قائمة بيانات التكييف الإيجابية.
# negative:قائمة بيانات التكييف السلبية.
# scale_ratio:العامل الذي يتم من خلاله رفع مستوى الصور.
# noise_augmentation:كمية الضوضاء التي يجب إضافتها أثناء العملية.
# encodeطريقة :

# الغرض : التعامل مع ترميز الصور باستخدام التكييف وزيادة الضوضاء.
# حدود :
# images:الصور الأصلية المراد معالجتها.
# positiveو negative: مدخلات التكييف.
# scale_ratio:النسبة التي سيتم بها تكبير الصور.
# noise_augmentation:كمية الضوضاء المضافة إلى الصور.
# عملية :
# يحسب العرض والارتفاع الجديدين للصورة المُكبرة.
# يقوم بترقية الصور باستخدام common_upscale، وهي وظيفة مساعدة من المفترض أنها تم تعريفها في مكان آخر.
# إنشاء نسخ من بيانات التكييف الإيجابية والسلبية، وضبطها باستخدام الصورة المحسنة ومعلمات الضوضاء.
# يقوم بتهيئة موتر كامن باستخدام الأصفار لتمثيل البيانات المعالجة.
# الإرجاع :
# بيانات التكييف الإيجابية والسلبية المعدلة.
# موتر كامن بقيم صفرية، يمثل العينات التي تمت معالجتها.
# NODE_CLASS_MAPPINGS:

# يقوم بربط اسم فئة العقدة "SD_4XUpscale_Conditioning"بالفئة الفعلية SD_4XUpscale_Conditioning.
# الغرض والاستخدام:
# الغرض : تُستخدم هذه الفئة لتحسين جودة الصور وإعدادها للاستخدام في نموذج الانتشار من خلال دمج بيانات التكييف وإضافة الضوضاء. ويمكن استخدامها في مهام إنشاء الصور أو تحسينها حيث يلعب التكييف دورًا.

# الاستخدام :

# في نماذج الانتشار : تُعد هذه الفئة مفيدة لإنشاء صور عالية الدقة من مدخلات منخفضة الدقة عن طريق تطبيق التكييف والضوضاء.
# في النظام القائم على العقد : سيتم استخدام الفصل كعقدة في النظام القائم على العقد لمعالجة الصور في سير عمل التعلم الآلي، وخاصة تلك التي تنطوي على نماذج الانتشار أو تقنيات إنشاء الصور الأخرى.
# ملخص:
# SD_4XUpscale_Conditioningتم تصميمه لتحسين جودة الصور مع دمج بيانات التكييف وزيادة الضوضاء. فهو يقوم بإعداد الصور وتكييفها لمزيد من المعالجة، عادةً في سياق نماذج الانتشار المستخدمة في المهام التوليدية.
import torch
import ldm_patched.contrib.external
import ldm_patched.modules.utils

class SD_4XUpscale_Conditioning:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "images": ("IMAGE",),
                              "positive": ("CONDITIONING",),
                              "negative": ("CONDITIONING",),
                              "scale_ratio": ("FLOAT", {"default": 4.0, "min": 0.0, "max": 10.0, "step": 0.01}),
                              "noise_augmentation": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                             }}
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "LATENT")
    RETURN_NAMES = ("positive", "negative", "latent")

    FUNCTION = "encode"

    CATEGORY = "conditioning/upscale_diffusion"

    def encode(self, images, positive, negative, scale_ratio, noise_augmentation):
        width = max(1, round(images.shape[-2] * scale_ratio))
        height = max(1, round(images.shape[-3] * scale_ratio))

        pixels = ldm_patched.modules.utils.common_upscale((images.movedim(-1,1) * 2.0) - 1.0, width // 4, height // 4, "bilinear", "center")

        out_cp = []
        out_cn = []

        for t in positive:
            n = [t[0], t[1].copy()]
            n[1]['concat_image'] = pixels
            n[1]['noise_augmentation'] = noise_augmentation
            out_cp.append(n)

        for t in negative:
            n = [t[0], t[1].copy()]
            n[1]['concat_image'] = pixels
            n[1]['noise_augmentation'] = noise_augmentation
            out_cn.append(n)

        latent = torch.zeros([images.shape[0], 4, height // 4, width // 4])
        return (out_cp, out_cn, {"samples":latent})

NODE_CLASS_MAPPINGS = {
    "SD_4XUpscale_Conditioning": SD_4XUpscale_Conditioning,
}
