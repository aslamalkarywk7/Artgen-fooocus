# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
#  فئات مصممة لتحميل النماذج، وتكييف الصور، وتطبيق الإرشادات على نماذج الفيديو، وخاصة لخط الأنابيب الذي يتعامل مع معالجة الصور إلى الفيديو وإدارة نقاط التفتيش. فيما يلي نظرة عامة على كل فئة ووظائفها:

# نظرة عامة على الفصول الدراسية
# ImageOnlyCheckpointLoaderفصل :

# الغرض : تحميل نقاط تفتيش النموذج لمهام تحويل الصورة إلى فيديو.
# طُرق :
# INPUT_TYPES:
# يتوقع ckpt_nameوجود اسم ملف نقطة تفتيش من القائمة المتاحة.
# RETURN_TYPES:
# إرجاع مجموعة مكونة من "MODEL"، "CLIP_VISION"، و "VAE"(Variational Autoencoder).
# FUNCTION:
# يتم استدعاء الطريقة load_checkpointلتحميل نقطة التفتيش.
# CATEGORY:
# مصنفة تحت "loaders/video_models".
# load_checkpoint(self, ckpt_name):
# يقوم بتحميل نقطة التفتيش المحددة من القرص ويعيد النموذج المحمل، وVAE، ومكونات الرؤية CLIP.
# SVD_img2vid_Conditioningفصل :

# الغرض : ترميز معلومات التكييف لتوليد الصور إلى مقاطع فيديو باستخدام تضمينات الصور.
# طُرق :
# INPUT_TYPES:
# يتطلب مدخلات مثل clip_vision، init_image، vae، العرض، الارتفاع، إطارات الفيديو، ومعلمات أخرى.
# RETURN_TYPES:
# إرجاع "CONDITIONING"، "CONDITIONING"، "LATENT"والموترات.
# FUNCTION:
# يقوم بتشفير البيانات المتعلقة بالصور والفيديو من خلال encodeالطريقة.
# CATEGORY:
# مصنفة تحت "conditioning/video_models".
# encode(self, clip_vision, init_image, vae, width, height, video_frames, motion_bucket_id, fps, augmentation_level):
# يقوم بتشفير الصورة الأولية باستخدام رؤية CLIP وVAE، ويطبق الترقية، ويتعامل مع معالجة الصورة الكامنة.
# يضيف تعزيز الضوضاء الاختياري ويعيد التكييف الإيجابي والسلبي والموتر الكامن لتوليد الفيديو.
# VideoLinearCFGGuidanceفصل :

# الغرض : تطبيق التوجيه أثناء إنشاء الفيديو عن طريق قياس التوجيه الخالي من المصنف (CFG) بشكل خطي.
# طُرق :
# INPUT_TYPES:
# يتوقع نموذجًا و min_cfg(مقياس إرشادي خالٍ من التصنيف على الأقل).
# RETURN_TYPES:
# إرجاع النسخة المعدلة "MODEL".
# FUNCTION:
# يستخدم patchالوظيفة لتعديل وظيفة CFG للنموذج.
# CATEGORY:
# مصنفة تحت "sampling/video_models".
# patch(self, model, min_cfg):
# يقوم بتصحيح النموذج من خلال تطبيق دالة القياس الخطي لـ CFG بين min_cfgومقياس CFG الحالي للنموذج.
# إرجاع النموذج المرقّع.
# ImageOnlyCheckpointSaveفصل :

# الغرض : حفظ نقاط تفتيش النموذج لمهام تحويل الصورة إلى فيديو.
# طُرق :
# INPUT_TYPES:
# يتوقع وجود model, clip_vision, vae, وبادئة اسم الملف لحفظ نقطة التفتيش.
# FUNCTION:
# استخدم saveالوظيفة from ldm_patched.contrib.external_model_mergingلحفظ نقطة التفتيش.
# CATEGORY:
# مصنفة تحت "_for_testing".
# save(self, model, clip_vision, vae, filename_prefix, prompt=None, extra_pnginfo=None):
# يحفظ النموذج الحالي ورؤية CLIP وحالة VAE في ملف نقطة تفتيش.
# ملخص المفاهيم الرئيسية:
# معالجة الصورة إلى فيديو (img2vid) :

# يركز هذا الخط على تحويل الصور الثابتة إلى مقاطع فيديو من خلال معالجة الصور وإنشاء إطارات فيديو استنادًا إلى البيانات المشفرة. يستخدم النظام نماذج رؤية CLIP لاستخراج تضمينات الصور وVAE لمعالجة المساحة الكامنة.
# نقطة تفتيش التحميل والحفظ :

# تقوم الفئة ImageOnlyCheckpointLoaderبتحميل نقاط التفتيش لمكونات النموذج المطلوبة لمعالجة الصور إلى الفيديو.
# تعتبر الفئة ImageOnlyCheckpointSaveمسؤولة عن حفظ حالة النموذج، بما في ذلك البيانات المتعلقة بالصور والفيديو.
# إرشادات VideoLinearCFG :

# تطبق هذه الفئة التدرج الخطي للتوجيه الخالي من المصنف أثناء إنشاء الفيديو، مما يساعد في تعديل تأثير إشارات التكييف أثناء عملية التوليد.
# البلاط والتكييف :

# يستخدم النظام التبليط للتعامل بكفاءة مع الصور ومقاطع الفيديو الكبيرة، ويمكن إضافة زيادة الضوضاء إلى تضمينات الصور لتحسين تنوع الفيديو.
# تعيينات العقد:
# NODE_CLASS_MAPPINGS:يقوم هذا القاموس بربط أسماء الفئات بتنفيذات العقد الخاصة بها لاستخدامها في واجهة تعتمد على العقد.
# NODE_DISPLAY_NAME_MAPPINGS:يوفر أسماء قابلة للقراءة من قبل الإنسان لعقد معينة، مثل "Image Only Checkpoint Loader (img2vid model)".
# يركز هذا الخط الأنبوبي بشكل أساسي على إنشاء الفيديو باستخدام التكييف القائم على الصور والتعامل الفعال مع الذاكرة من خلال التبليط وإدارة نقاط التفتيش.
# import ldm_patched.contrib.external
import torch
import ldm_patched.modules.utils
import ldm_patched.modules.sd
import ldm_patched.utils.path_utils
import ldm_patched.contrib.external_model_merging


class ImageOnlyCheckpointLoader:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "ckpt_name": (ldm_patched.utils.path_utils.get_filename_list("checkpoints"), ),
                             }}
    RETURN_TYPES = ("MODEL", "CLIP_VISION", "VAE")
    FUNCTION = "load_checkpoint"

    CATEGORY = "loaders/video_models"

    def load_checkpoint(self, ckpt_name, output_vae=True, output_clip=True):
        ckpt_path = ldm_patched.utils.path_utils.get_full_path("checkpoints", ckpt_name)
        out = ldm_patched.modules.sd.load_checkpoint_guess_config(ckpt_path, output_vae=True, output_clip=False, output_clipvision=True, embedding_directory=ldm_patched.utils.path_utils.get_folder_paths("embeddings"))
        return (out[0], out[3], out[2])


class SVD_img2vid_Conditioning:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "clip_vision": ("CLIP_VISION",),
                              "init_image": ("IMAGE",),
                              "vae": ("VAE",),
                              "width": ("INT", {"default": 1024, "min": 16, "max": ldm_patched.contrib.external.MAX_RESOLUTION, "step": 8}),
                              "height": ("INT", {"default": 576, "min": 16, "max": ldm_patched.contrib.external.MAX_RESOLUTION, "step": 8}),
                              "video_frames": ("INT", {"default": 14, "min": 1, "max": 4096}),
                              "motion_bucket_id": ("INT", {"default": 127, "min": 1, "max": 1023}),
                              "fps": ("INT", {"default": 6, "min": 1, "max": 1024}),
                              "augmentation_level": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 10.0, "step": 0.01})
                             }}
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING", "LATENT")
    RETURN_NAMES = ("positive", "negative", "latent")

    FUNCTION = "encode"

    CATEGORY = "conditioning/video_models"

    def encode(self, clip_vision, init_image, vae, width, height, video_frames, motion_bucket_id, fps, augmentation_level):
        output = clip_vision.encode_image(init_image)
        pooled = output.image_embeds.unsqueeze(0)
        pixels = ldm_patched.modules.utils.common_upscale(init_image.movedim(-1,1), width, height, "bilinear", "center").movedim(1,-1)
        encode_pixels = pixels[:,:,:,:3]
        if augmentation_level > 0:
            encode_pixels += torch.randn_like(pixels) * augmentation_level
        t = vae.encode(encode_pixels)
        positive = [[pooled, {"motion_bucket_id": motion_bucket_id, "fps": fps, "augmentation_level": augmentation_level, "concat_latent_image": t}]]
        negative = [[torch.zeros_like(pooled), {"motion_bucket_id": motion_bucket_id, "fps": fps, "augmentation_level": augmentation_level, "concat_latent_image": torch.zeros_like(t)}]]
        latent = torch.zeros([video_frames, 4, height // 8, width // 8])
        return (positive, negative, {"samples":latent})

class VideoLinearCFGGuidance:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "min_cfg": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 100.0, "step":0.5, "round": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "sampling/video_models"

    def patch(self, model, min_cfg):
        def linear_cfg(args):
            cond = args["cond"]
            uncond = args["uncond"]
            cond_scale = args["cond_scale"]

            scale = torch.linspace(min_cfg, cond_scale, cond.shape[0], device=cond.device).reshape((cond.shape[0], 1, 1, 1))
            return uncond + scale * (cond - uncond)

        m = model.clone()
        m.set_model_sampler_cfg_function(linear_cfg)
        return (m, )

class ImageOnlyCheckpointSave(ldm_patched.contrib.external_model_merging.CheckpointSave):
    CATEGORY = "_for_testing"

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                              "clip_vision": ("CLIP_VISION",),
                              "vae": ("VAE",),
                              "filename_prefix": ("STRING", {"default": "checkpoints/ldm_patched"}),},
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},}

    def save(self, model, clip_vision, vae, filename_prefix, prompt=None, extra_pnginfo=None):
        ldm_patched.contrib.external_model_merging.save_checkpoint(model, clip_vision=clip_vision, vae=vae, filename_prefix=filename_prefix, output_dir=self.output_dir, prompt=prompt, extra_pnginfo=extra_pnginfo)
        return {}

NODE_CLASS_MAPPINGS = {
    "ImageOnlyCheckpointLoader": ImageOnlyCheckpointLoader,
    "SVD_img2vid_Conditioning": SVD_img2vid_Conditioning,
    "VideoLinearCFGGuidance": VideoLinearCFGGuidance,
    "ImageOnlyCheckpointSave": ImageOnlyCheckpointSave,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOnlyCheckpointLoader": "Image Only Checkpoint Loader (img2vid model)",
}
