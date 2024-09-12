# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# كود Python المقدم فئتين، CLIPTextEncodeSDXLRefinerو CLIPTextEncodeSDXL، والتي تتعامل مع ترميز النص لنماذج CLIP. تم تصميم هذه المشفرات لنموذج Stable Diffusion XL (SDXL)، على وجه التحديد في إطار يتضمن تكييف النص والنتائج الجمالية لتوليد الصور.

# فيما يلي ملخص لكيفية عمل الكود:

# نظرة عامة على الفصول الدراسية:
# CLIPTextEncodeSDXLRefiner:

# تقوم هذه الفئة بترميز النص باستخدام نموذج CLIP وإرجاع معلومات التكييف، بما في ذلك النتيجة الجمالية ( ascore)، وأبعاد الصورة ( widthو height)، والمخرجات المجمعة من نموذج CLIP.
# المدخلات:
# ascore:قيمة فاصلة عائمة تمثل النتيجة الجمالية.
# width: heightأبعاد الصورة.
# text:إدخال النص المراد تقسيمه وترميزه.
# clip:مثال لنموذج CLIP.
# المخرجات:
# مجموعة تحتوي على الرموز المشفرة ( cond) والسياق الإضافي (الإخراج المجمع، النتيجة الجمالية، الأبعاد).
# CLIPTextEncodeSDXL:

# مشابه لـ CLIPTextEncodeSDXLRefiner، ولكن مع وظائف إضافية، بما في ذلك القدرة على تحديد رموز منفصلة للسياقات العالمية ( text_g) والمحلية ( text_l)، وأبعاد اقتصاص الصورة، وأبعاد الصورة المستهدفة.
# المدخلات:
# width: heightأبعاد الصورة.
# crop_w, crop_h: أبعاد القطع للصورة.
# target_width, target_height: أبعاد الهدف للصورة.
# text_g:نص السياق العالمي.
# text_l:نص السياق المحلي.
# clip:مثال لنموذج CLIP.
# المخرجات:
# مشابه لـ CLIPTextEncodeSDXLRefiner، ولكنه يتضمن أيضًا أبعاد المحصول والهدف.
# الأساليب الرئيسية:
# INPUT_TYPES: يحدد المدخلات المطلوبة لكل فئة. ويتضمن ذلك معلمات مختلفة مثل النص والأبعاد وإعدادات النموذج.
# encode: الوظيفة الأساسية حيث يتم تقسيم النص المدخل ومعالجته من خلال نموذج CLIP لتوليد رموز مشفرة ( cond) وبيانات وصفية أخرى (الإخراج المجمع والأبعاد وما إلى ذلك).
# تسجيل العقدة:
# في أسفل البرنامج النصي، يتم تسجيل الفئتين في NODE_CLASS_MAPPINGSالقاموس، مما يسمح باستخدامهما كعقد في رسم بياني أو نموذج حسابي أكبر.

# التطبيقات:
# يبدو أن هذا البرنامج النصي هو جزء من خط أنابيب لإنشاء الصور أو تحسينها استنادًا إلى مطالبات النص باستخدام نموذج مثل CLIP في سياق الانتشار المستقر.
import torch
from ldm_patched.contrib.external import MAX_RESOLUTION

class CLIPTextEncodeSDXLRefiner:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "ascore": ("FLOAT", {"default": 6.0, "min": 0.0, "max": 1000.0, "step": 0.01}),
            "width": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "height": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "text": ("STRING", {"multiline": True}), "clip": ("CLIP", ),
            }}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "advanced/conditioning"

    def encode(self, clip, ascore, width, height, text):
        tokens = clip.tokenize(text)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled, "aesthetic_score": ascore, "width": width,"height": height}]], )

class CLIPTextEncodeSDXL:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "width": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "height": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "crop_w": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION}),
            "crop_h": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION}),
            "target_width": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "target_height": ("INT", {"default": 1024.0, "min": 0, "max": MAX_RESOLUTION}),
            "text_g": ("STRING", {"multiline": True, "default": "CLIP_G"}), "clip": ("CLIP", ),
            "text_l": ("STRING", {"multiline": True, "default": "CLIP_L"}), "clip": ("CLIP", ),
            }}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "advanced/conditioning"

    def encode(self, clip, width, height, crop_w, crop_h, target_width, target_height, text_g, text_l):
        tokens = clip.tokenize(text_g)
        tokens["l"] = clip.tokenize(text_l)["l"]
        if len(tokens["l"]) != len(tokens["g"]):
            empty = clip.tokenize("")
            while len(tokens["l"]) < len(tokens["g"]):
                tokens["l"] += empty["l"]
            while len(tokens["l"]) > len(tokens["g"]):
                tokens["g"] += empty["g"]
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
        return ([[cond, {"pooled_output": pooled, "width": width, "height": height, "crop_w": crop_w, "crop_h": crop_h, "target_width": target_width, "target_height": target_height}]], )

NODE_CLASS_MAPPINGS = {
    "CLIPTextEncodeSDXLRefiner": CLIPTextEncodeSDXLRefiner,
    "CLIPTextEncodeSDXL": CLIPTextEncodeSDXL,
}
