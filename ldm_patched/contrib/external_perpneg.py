# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# الكود المقدم هو تنفيذ لـ Python يتعلق بنموذج التعلم الآلي، ومن المرجح أنه يستخدم لتوليد الصور أو بعض المهام الأخرى التي تتضمن نماذج التكييف والتنبؤ بالضوضاء والعينات. فيما يلي شرح موجز للكود:

# المكونات الرئيسية
# الواردات :

# يستورد الكود وحدات مثل torch(مكتبة PyTorch) والعديد من المكونات من ldm_patched.modulesمثل model_managementو sampleو samplersو و utils. يبدو أن هذه الوحدات تتعامل مع إدارة النماذج والعينات والأدوات المساعدة، ولكنها مُرقعة أو مخصصة لمهمة محددة.
# PerpNegفصل :

# يبدو أن هذه الفئة تنفذ تقنية تسمى "Perp-Neg" (ربما "Perpendicular Negative") لتعديل عملية تكييف النموذج.
# تحتوي الفئة على طريقة INPUT_TYPESتحدد المدخلات المطلوبة:
# model:النموذج الذي يتم تصحيحه.
# empty_conditioning:مدخلات التكييف، ربما تمثل سيناريو تكييف فارغ.
# neg_scale:قيمة فاصلة عائمة تتحكم في مقياس التكييف السلبي.
# RETURN_TYPESيحدد أن الدالة تقوم بإرجاع نموذج معدّل.
# تطبق الوظيفة patchالتحويل على النموذج من خلال تحديد مخصص cfg_functionيغير كيفية حساب النموذج لإزالة الضوضاء والتكييف.
# عملية التصحيح :

# تقوم الوظيفة patchبتعديل النموذج باستخدام نسخة من النموذج الأصلي.
# إنه يحدد عرفًا cfg_functionيتعامل مع التباين بين التنبؤات بالضوضاء الإيجابية ( cond_denoised) والسلبية ( ).uncond_denoised
# يحسب cfg_functionالمكون السالب العمودي للتكييف ويضبط الناتج النهائي بناءً على cond_scaleو neg_scale.
# يتم حساب النتيجة المشروطة النهائية عن طريق طرح التصحيح العمودي ( perp_neg) من التكييف الإيجابي ( pos)، وتعديله بناءً على المعطى neg_scale.
# يتم بعد ذلك تطبيق هذا التحويل مرة أخرى على النموذج باستخدام set_model_sampler_cfg_function.
# تعيينات فئة العقدة :

# تسجل القواميس والفئة باسم NODE_CLASS_MAPPINGSيمكن استخدامه في واجهة المستخدم (ComfyUI). يشير هذا إلى أن العقدة تُستخدم في نوع ما من الواجهة الرسومية لتكوين النماذج أو سير العمل.NODE_DISPLAY_NAME_MAPPINGSPerpNeg
# المفاهيم الرئيسية
# التنبؤ بالضوضاء : من المحتمل أن يكون جزءًا من عملية انتشار إزالة الضوضاء، حيث يقوم النموذج بإنشاء أو معالجة البيانات (مثل الصور) استنادًا إلى التنبؤات الخالية من الضوضاء تدريجيًا.
# التكييف : يشير إلى توجيه عملية إنشاء النموذج استنادًا إلى مدخلات أو قيود معينة (على سبيل المثال، مطالبات النص، والأنماط، وما إلى ذلك).
# سلبي عمودي : يشير المصطلح إلى أن النموذج يحاول مواجهة أو تعديل المكونات السلبية عن طريق إسقاط متجه عمودي في مساحة عالية الأبعاد لتحسين التكييف.
# import torch
import ldm_patched.modules.model_management
import ldm_patched.modules.sample
import ldm_patched.modules.samplers
import ldm_patched.modules.utils


class PerpNeg:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"model": ("MODEL", ),
                             "empty_conditioning": ("CONDITIONING", ),
                             "neg_scale": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 100.0}),
                            }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "_for_testing"

    def patch(self, model, empty_conditioning, neg_scale):
        m = model.clone()
        nocond = ldm_patched.modules.sample.convert_cond(empty_conditioning)

        def cfg_function(args):
            model = args["model"]
            noise_pred_pos = args["cond_denoised"]
            noise_pred_neg = args["uncond_denoised"]
            cond_scale = args["cond_scale"]
            x = args["input"]
            sigma = args["sigma"]
            model_options = args["model_options"]
            nocond_processed = ldm_patched.modules.samplers.encode_model_conds(model.extra_conds, nocond, x, x.device, "negative")

            (noise_pred_nocond, _) = ldm_patched.modules.samplers.calc_cond_uncond_batch(model, nocond_processed, None, x, sigma, model_options)

            pos = noise_pred_pos - noise_pred_nocond
            neg = noise_pred_neg - noise_pred_nocond
            perp = ((torch.mul(pos, neg).sum())/(torch.norm(neg)**2)) * neg
            perp_neg = perp * neg_scale
            cfg_result = noise_pred_nocond + cond_scale*(pos - perp_neg)
            cfg_result = x - cfg_result
            return cfg_result

        m.set_model_sampler_cfg_function(cfg_function)

        return (m, )


NODE_CLASS_MAPPINGS = {
    "PerpNeg": PerpNeg,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PerpNeg": "Perp-Neg",
}
