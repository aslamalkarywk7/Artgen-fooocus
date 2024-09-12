# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# 
# يوفر هذا الكود آلية تصحيح لنموذج التعلم العميق الذي يعدل كيفية تعامل كتل الإدخال والإخراج مع التخفيض والزيادة أثناء تشغيل النموذج. فيما يلي تفصيل موجز للمكونات الأساسية:

# المكونات الأساسية:
# فئة PatchModelAddDownscale :

# تتيح هذه الفئة تطبيق طرق التخفيض والترقية المخصصة على نموذج أثناء كتل محددة في بنية النموذج.
# ويقدم العديد من المعايير للمرونة، بما في ذلك:
# block_number : كتلة النموذج التي يحدث فيها التخفيض.
# downscale_factor : العامل الذي سيتم من خلاله تقليص حجم المدخلات.
# start_percent / end_percent : قم بتحديد النسبة المئوية لخطوات وقت النموذج التي سيحدث فيها التخفيض.
# downscale_after_skip : يحدد ما إذا كان يجب أن يحدث تخفيض الحجم بعد اتصال التخطي أو قبله.
# downscale_method / upscale_method : الطرق المستخدمة للتوسع (تتضمن الخيارات bicubic وbilinear وما إلى ذلك).
# الوظائف :

# input_block_patch : يتم تطبيقه على كتل الإدخال في النموذج. يتحقق مما إذا كانت الكتلة الحالية ضمن النطاق المحدد (بناءً على قيم سيجما) ويقيس موتر الإدخال إذا لزم الأمر.
# output_block_patch : يتم تطبيقه على كتل الإخراج. وهذا يضمن إعادة تكبير حجم موتر الإخراج إلى حجمه الأصلي بعد تطبيق أي تخفيض في الحجم.
# تصحيح النموذج :

# تقوم الفئة بتصحيح النموذج باستخدام m.set_model_input_block_patchأو m.set_model_input_block_patch_after_skipاعتمادًا على ما إذا كان المستخدم يريد حدوث التخفيض بعد اتصال التخطي.
# ويقوم أيضًا بتصحيح إخراج النموذج باستخدام m.set_model_output_block_patch.
# مثال على الاستخدام:
# يتيح هذا للمطورين تعديل السلوك الداخلي للنماذج لأداء عمليات التخفيض/الزيادة أثناء التدريب أو الاستدلال. يمكن استخدام آلية التصحيح بالتزامن مع مهام مثل إنشاء الصور، حيث قد يؤثر تغيير الدقة في أجزاء مختلفة من النموذج على السرعة أو استخدام الذاكرة.

# قم NODE_CLASS_MAPPINGSبتعيين NODE_DISPLAY_NAME_MAPPINGSالفئة إلى النظام لسهولة الرجوع إليها في بيئة واجهة المستخدم أو سطر الأوامر.
import torch
import ldm_patched.modules.utils

class PatchModelAddDownscale:
    upscale_methods = ["bicubic", "nearest-exact", "bilinear", "area", "bislerp"]
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "block_number": ("INT", {"default": 3, "min": 1, "max": 32, "step": 1}),
                              "downscale_factor": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 9.0, "step": 0.001}),
                              "start_percent": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.001}),
                              "end_percent": ("FLOAT", {"default": 0.35, "min": 0.0, "max": 1.0, "step": 0.001}),
                              "downscale_after_skip": ("BOOLEAN", {"default": True}),
                              "downscale_method": (s.upscale_methods,),
                              "upscale_method": (s.upscale_methods,),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "_for_testing"

    def patch(self, model, block_number, downscale_factor, start_percent, end_percent, downscale_after_skip, downscale_method, upscale_method):
        sigma_start = model.model.model_sampling.percent_to_sigma(start_percent)
        sigma_end = model.model.model_sampling.percent_to_sigma(end_percent)

        def input_block_patch(h, transformer_options):
            if transformer_options["block"][1] == block_number:
                sigma = transformer_options["sigmas"][0].item()
                if sigma <= sigma_start and sigma >= sigma_end:
                    h = ldm_patched.modules.utils.common_upscale(h, round(h.shape[-1] * (1.0 / downscale_factor)), round(h.shape[-2] * (1.0 / downscale_factor)), downscale_method, "disabled")
            return h

        def output_block_patch(h, hsp, transformer_options):
            if h.shape[2] != hsp.shape[2]:
                h = ldm_patched.modules.utils.common_upscale(h, hsp.shape[-1], hsp.shape[-2], upscale_method, "disabled")
            return h, hsp

        m = model.clone()
        if downscale_after_skip:
            m.set_model_input_block_patch_after_skip(input_block_patch)
        else:
            m.set_model_input_block_patch(input_block_patch)
        m.set_model_output_block_patch(output_block_patch)
        return (m, )

NODE_CLASS_MAPPINGS = {
    "PatchModelAddDownscale": PatchModelAddDownscale,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # Sampling
    "PatchModelAddDownscale": "PatchModelAddDownscale (Kohya Deep Shrink)",
}
