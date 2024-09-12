# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# يحتوي الكود الذي قدمته على فئتين مصممتين للتعامل مع رفع مستوى الصورة باستخدام نماذج مدربة مسبقًا. فيما يلي نظرة عامة على وظائفهما وكيفية عملهما:

# نظرة عامة على الفصول الدراسية
# UpscaleModelLoaderفصل :

# الغرض : تحميل نموذج الترقية وإعداده للاستخدام.
# طُرق :
# INPUT_TYPES:
# يحدد أنواع الإدخال للعقدة. في هذه الحالة، يتوقع model_nameنوع الإدخال اسم ملف من قائمة النماذج المتطورة المتاحة.
# RETURN_TYPES:
# يحدد أن الطريقة تُرجع "UPSCALE_MODEL".
# FUNCTION:
# load_modelيشير إلى أنه سيتم استخدام الطريقة لهذه العقدة.
# CATEGORY:
# يصنف هذه العقدة تحت "loaders".
# load_model(self, model_name):
# يقوم بتحميل النموذج من المسار المحدد باستخدام الأدوات model_loadingالمساعدة utilsمن ldm_patched.
# يتولى تحميل قواميس الحالة ويضمن التوافق عن طريق استبدال بعض البادئات.
# إرجاع النموذج المحمّل.
# ImageUpscaleWithModelفصل :

# الغرض : تطبيق نموذج الارتقاء إلى مستوى أعلى على صورة.
# طُرق :
# INPUT_TYPES:
# يحدد أنواع الإدخال للعقدة. ويتطلب "UPSCALE_MODEL"و "IMAGE".
# RETURN_TYPES:
# يحدد أن الطريقة تُرجع "IMAGE".
# FUNCTION:
# upscaleيشير إلى أنه سيتم استخدام الطريقة لهذه العقدة.
# CATEGORY:
# يصنف هذه العقدة تحت "image/upscaling".
# upscale(self, upscale_model, image):
# نقل النموذج والصورة إلى الجهاز المناسب.
# يستخدم أسلوب التبليط للتعامل مع الصور الكبيرة عن طريق معالجتها في أجزاء أصغر لتجنب أخطاء نفاد الذاكرة.
# ضبط حجم البلاط بشكل ديناميكي ليتناسب مع قيود الذاكرة.
# يتم تطبيق نموذج الارتقاء إلى المستوى الأعلى على كل بلاطة من الصورة.
# إرجاع الصورة المُحسّنة بعد تثبيت قيم البكسل.
# الوظائف والمرافق الرئيسية:
# ldm_patched.utils.path_utils.get_filename_list("upscale_models"):

# استرداد قائمة بأسماء الملفات المتاحة لنماذج الترقية.
# ldm_patched.utils.path_utils.get_full_path("upscale_models", model_name):

# إنشاء المسار الكامل لملف النموذج بناءً على اسمه.
# ldm_patched.modules.utils.load_torch_file(model_path, safe_load=True):

# يقوم بتحميل ملف نموذج Torch، مما يضمن تحميله بأمان.
# model_loading.load_state_dict(sd):

# يقوم بتحميل قاموس الحالة إلى النموذج.
# model_management.get_torch_device():

# يقوم بإرجاع الجهاز (وحدة المعالجة المركزية أو وحدة معالجة الرسومات) الذي يجب إجراء العمليات الحسابية عليه.
# model_management.get_free_memory(device):

# إرجاع مقدار الذاكرة الحرة المتاحة على الجهاز المحدد.
# ldm_patched.modules.utils.tiled_scale(...):

# يقوم بتقسيم الصورة إلى مربعات للتعامل مع الصور الكبيرة وتقليل استخدام الذاكرة.
# ملخص
# UpscaleModelLoader:هذه الفئة مسؤولة عن تحميل نماذج الترقية من القرص وإعدادها للاستدلال.
# ImageUpscaleWithModel:تأخذ هذه الفئة صورة ونموذجًا محسّنًا، وتطبق النموذج على الصورة باستخدام نهج مبلط للتعامل مع قيود الذاكرة، وتعيد الصورة المحسّنة.
# يقوم القاموس NODE_CLASS_MAPPINGSبربط هذه الفئات بأسمائها الخاصة، مما يسمح باستخدامها في نظام قائم على العقد لمعالجة الصور. يعد هذا الإعداد مفيدًا لدمج تدفقات عمل رفع مستوى الصور المعقدة في البيئات المعيارية.
import os
from ldm_patched.pfn import model_loading
from ldm_patched.modules import model_management
import torch
import ldm_patched.modules.utils
import ldm_patched.utils.path_utils

class UpscaleModelLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model_name": (ldm_patched.utils.path_utils.get_filename_list("upscale_models"), ),
                             }}
    RETURN_TYPES = ("UPSCALE_MODEL",)
    FUNCTION = "load_model"

    CATEGORY = "loaders"

    def load_model(self, model_name):
        model_path = ldm_patched.utils.path_utils.get_full_path("upscale_models", model_name)
        sd = ldm_patched.modules.utils.load_torch_file(model_path, safe_load=True)
        if "module.layers.0.residual_group.blocks.0.norm1.weight" in sd:
            sd = ldm_patched.modules.utils.state_dict_prefix_replace(sd, {"module.":""})
        out = model_loading.load_state_dict(sd).eval()
        return (out, )


class ImageUpscaleWithModel:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "upscale_model": ("UPSCALE_MODEL",),
                              "image": ("IMAGE",),
                              }}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "upscale"

    CATEGORY = "image/upscaling"

    def upscale(self, upscale_model, image):
        device = model_management.get_torch_device()
        upscale_model.to(device)
        in_img = image.movedim(-1,-3).to(device)
        free_memory = model_management.get_free_memory(device)

        tile = 512
        overlap = 32

        oom = True
        while oom:
            try:
                steps = in_img.shape[0] * ldm_patched.modules.utils.get_tiled_scale_steps(in_img.shape[3], in_img.shape[2], tile_x=tile, tile_y=tile, overlap=overlap)
                pbar = ldm_patched.modules.utils.ProgressBar(steps)
                s = ldm_patched.modules.utils.tiled_scale(in_img, lambda a: upscale_model(a), tile_x=tile, tile_y=tile, overlap=overlap, upscale_amount=upscale_model.scale, pbar=pbar)
                oom = False
            except model_management.OOM_EXCEPTION as e:
                tile //= 2
                if tile < 128:
                    raise e

        upscale_model.cpu()
        s = torch.clamp(s.movedim(-3,-1), min=0, max=1.0)
        return (s,)

NODE_CLASS_MAPPINGS = {
    "UpscaleModelLoader": UpscaleModelLoader,
    "ImageUpscaleWithModel": ImageUpscaleWithModel
}
