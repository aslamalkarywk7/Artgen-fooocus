# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# يوفر مقتطف التعليمات البرمجية هذا تنفيذات لعقد معالجة الصور المختلفة في إطار عمل محتمل للتعلم الآلي أو معالجة الصور. فيما يلي تفصيل مفصل للتعليمات البرمجية ومكوناتها:

# 1. الواردات:
# ldm_patched.contrib.external:من المحتمل أن يحتوي على أدوات مساعدة خارجية أو ثوابت مستخدمة في إطار العمل.
# ldm_patched.utils.path_utils:يحتوي على وظائف مساعدة متعلقة بإدارة الملفات والمسارات.
# args:من ldm_patched.modules.args_parserالمحتمل أن يحتوي على تكوينات الوسيطة للإطار.
# PIL:مكتبة Python Imaging المستخدمة لمعالجة الصور.
# numpy:مكتبة للعمليات العددية في بايثون، تُستخدم هنا للتعامل مع صفائف الصور.
# json:للتعامل مع بيانات JSON، وتستخدم للبيانات الوصفية.
# os:للتفاعل مع نظام الملفات.
# 2. الفئات ووظائفها:
# ImageCropفصل:
# الغرض : اقتصاص صورة معينة بناءً على أبعاد وإحداثيات محددة.
# المدخلات :
# image:الصورة المراد اقتصاصها.
# width: heightأبعاد المنطقة المقطوعة.
# x: yإحداثيات البداية للقص.
# وظيفة :
# ضبط الإحداثيات xو yللتأكد من ملاءمتها لحدود الصورة.
# يقوم بقص الصورة باستخدام تقطيع مجموعة NumPy.
# RepeatImageBatchفصل:
# الغرض : تكرار الصورة عدة مرات على طول البعد الدفعي.
# المدخلات :
# image:الصورة المراد تكرارها.
# amount:عدد المرات التي يجب تكرار الصورة فيها.
# وظيفة :
# يستخدم طريقة NumPy repeatلإنشاء مجموعة من الصور المتكررة.
# SaveAnimatedWEBPفصل:
# الغرض : حفظ سلسلة من الصور كملف WEBP متحرك.
# المنشئ :
# يتم التهيئة باستخدام دليل الإخراج والتكوين.
# المدخلات :
# images:تسلسل الصور المراد حفظها.
# filename_prefix, fps, lossless, quality, method: معلمات لحفظ WEBP المتحرك.
# وظيفة :
# يقوم بتحويل الصور من التنسورات إلى صور PIL.
# إضافة البيانات الوصفية إذا لزم الأمر.
# يحفظ الصور كملف WEBP متحرك باستخدام saveطريقة PIL.
# يدعم إطارات متعددة وخيارات ضغط.
# SaveAnimatedPNGفصل:
# الغرض : حفظ سلسلة من الصور كملف PNG متحرك.
# المنشئ :
# يتم التهيئة باستخدام دليل الإخراج والتكوين.
# المدخلات :
# images:تسلسل الصور المراد حفظها.
# filename_prefix, fps, compress_level: معلمات لحفظ ملف PNG المتحرك.
# وظيفة :
# يقوم بتحويل الصور من التنسورات إلى صور PIL.
# إضافة البيانات الوصفية إذا لزم الأمر.
# يحفظ الصور كملف PNG متحرك باستخدام saveطريقة PIL.
# يدعم إطارات متعددة ومستويات ضغط.
# 3. NODE_CLASS_MAPPINGS:
# الغرض : ربط أسماء فئات العقد بتنفيذات الفئات الخاصة بها.
# الاستخدام : من المرجح استخدامه لإنشاء العقد الديناميكية أو معالجتها في واجهة رسومية أو قائمة على العقد.
# ملخص:
# ImageCrop : اقتصاص الصور استنادًا إلى الأبعاد والإحداثيات المحددة.
# RepeatImageBatch : يقوم بإنشاء مجموعة من الصور المتكررة.
# SaveAnimatedWEBP : يحفظ سلسلة من الصور كملف WEBP متحرك.
# SaveAnimatedPNG : يحفظ سلسلة من الصور كملف PNG متحرك.
# تم تصميم هذه الفئات لمهام معالجة الصور المختلفة، مثل القص والتجميع وحفظ تسلسلات الصور كملفات متحركة. وهي تتكامل مع إطار عمل يتعامل مع عمليات النموذج وبيانات الصور، على الأرجح في سياق تطبيقات التعلم الآلي أو إنشاء الصور.
import ldm_patched.contrib.external
import ldm_patched.utils.path_utils
from ldm_patched.modules.args_parser import args

from PIL import Image
from PIL.PngImagePlugin import PngInfo

import numpy as np
import json
import os

MAX_RESOLUTION = ldm_patched.contrib.external.MAX_RESOLUTION

class ImageCrop:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "image": ("IMAGE",),
                              "width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                              "height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION, "step": 1}),
                              "x": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                              "y": ("INT", {"default": 0, "min": 0, "max": MAX_RESOLUTION, "step": 1}),
                              }}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "crop"

    CATEGORY = "image/transform"

    def crop(self, image, width, height, x, y):
        x = min(x, image.shape[2] - 1)
        y = min(y, image.shape[1] - 1)
        to_x = width + x
        to_y = height + y
        img = image[:,y:to_y, x:to_x, :]
        return (img,)

class RepeatImageBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "image": ("IMAGE",),
                              "amount": ("INT", {"default": 1, "min": 1, "max": 64}),
                              }}
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "repeat"

    CATEGORY = "image/batch"

    def repeat(self, image, amount):
        s = image.repeat((amount, 1,1,1))
        return (s,)

class SaveAnimatedWEBP:
    def __init__(self):
        self.output_dir = ldm_patched.utils.path_utils.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    methods = {"default": 4, "fastest": 0, "slowest": 6}
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ldm_patched"}),
                     "fps": ("FLOAT", {"default": 6.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                     "lossless": ("BOOLEAN", {"default": True}),
                     "quality": ("INT", {"default": 80, "min": 0, "max": 100}),
                     "method": (list(s.methods.keys()),),
                     # "num_frames": ("INT", {"default": 0, "min": 0, "max": 8192}),
                     },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image/animation"

    def save_images(self, images, fps, filename_prefix, lossless, quality, method, num_frames=0, prompt=None, extra_pnginfo=None):
        method = self.methods.get(method)
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = ldm_patched.utils.path_utils.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        pil_images = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            pil_images.append(img)

        metadata = pil_images[0].getexif()
        if not args.disable_server_info:
            if prompt is not None:
                metadata[0x0110] = "prompt:{}".format(json.dumps(prompt))
            if extra_pnginfo is not None:
                inital_exif = 0x010f
                for x in extra_pnginfo:
                    metadata[inital_exif] = "{}:{}".format(x, json.dumps(extra_pnginfo[x]))
                    inital_exif -= 1

        if num_frames == 0:
            num_frames = len(pil_images)

        c = len(pil_images)
        for i in range(0, c, num_frames):
            file = f"{filename}_{counter:05}_.webp"
            pil_images[i].save(os.path.join(full_output_folder, file), save_all=True, duration=int(1000.0/fps), append_images=pil_images[i + 1:i + num_frames], exif=metadata, lossless=lossless, quality=quality, method=method)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        animated = num_frames != 1
        return { "ui": { "images": results, "animated": (animated,) } }

class SaveAnimatedPNG:
    def __init__(self):
        self.output_dir = ldm_patched.utils.path_utils.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"images": ("IMAGE", ),
                     "filename_prefix": ("STRING", {"default": "ldm_patched"}),
                     "fps": ("FLOAT", {"default": 6.0, "min": 0.01, "max": 1000.0, "step": 0.01}),
                     "compress_level": ("INT", {"default": 4, "min": 0, "max": 9})
                     },
                "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image/animation"

    def save_images(self, images, fps, compress_level, filename_prefix="ldm_patched", prompt=None, extra_pnginfo=None):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = ldm_patched.utils.path_utils.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        pil_images = []
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            pil_images.append(img)

        metadata = None
        if not args.disable_server_info:
            metadata = PngInfo()
            if prompt is not None:
                metadata.add(b"ldm_patched", "prompt".encode("latin-1", "strict") + b"\0" + json.dumps(prompt).encode("latin-1", "strict"), after_idat=True)
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add(b"ldm_patched", x.encode("latin-1", "strict") + b"\0" + json.dumps(extra_pnginfo[x]).encode("latin-1", "strict"), after_idat=True)

        file = f"{filename}_{counter:05}_.png"
        pil_images[0].save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=compress_level, save_all=True, duration=int(1000.0/fps), append_images=pil_images[1:])
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })

        return { "ui": { "images": results, "animated": (True,)} }

NODE_CLASS_MAPPINGS = {
    "ImageCrop": ImageCrop,
    "RepeatImageBatch": RepeatImageBatch,
    "SaveAnimatedWEBP": SaveAnimatedWEBP,
    "SaveAnimatedPNG": SaveAnimatedPNG,
}
