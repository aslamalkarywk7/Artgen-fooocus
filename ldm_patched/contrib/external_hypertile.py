# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 

#Taken from: https://github.com/tfernd/HyperTile/

# يقوم هذا الكود بدمج رقعة HyperTile في طبقات الانتباه في نموذج التعلم الآلي، ومن المرجح أن يتم استخدامها لمهام إنشاء الصور أو نماذج التعلم العميق الأخرى التي تعتمد على آليات الانتباه.

# المكونات الرئيسية:
# الواردات:

# math:عمليات الرياضيات القياسية.
# einops.rearrange:دالة ​​من einopsالمكتبة تستخدم لإعادة ترتيب أبعاد الموتر لنماذج PyTorch.
# torch.randint:يولد أعدادًا صحيحة عشوائية، مما يضمن الاتساق في اختيار المقسوم العشوائي أثناء إنشاء النموذج.
# random_divisorوظيفة:

# تقوم هذه الوظيفة بإنشاء قواسم لقيمة معينة واختيار أحدها عشوائيًا. وهي تضمن أن القاسم يناسب نطاقًا محددًا ( min_value) وتحد من عدد الخيارات الممكنة ( max_options).
# يتم استخدامه لتحديد كيفية تقسيم أبعاد الصورة المدخلة لعملية التبليط.
# HyperTileفصل:

# تقوم هذه الفئة بتصحيح نموذج باستخدام سلوك HyperTile ، والذي يتيح معالجة بيانات الإدخال (مثل الصور) في المربعات.
# تكوين الإدخال ( INPUT_TYPES) :
# tile_size:حجم البلاط الفردي (الافتراضي هو 256، الحد الأقصى هو 2048).
# swap_size:يتحكم في عدد المرات التي يتم فيها تبديل البلاط.
# max_depth:أقصى مستوى عمق يتم تطبيق البلاط عليه.
# scale_depth:قيمة منطقية لتحديد ما إذا كان يجب تطبيق التدرج بناءً على العمق.
# أنواع الإرجاع ( RETURN_TYPES) : تقوم الدالة بإرجاع "MODEL" معدّلاً.
# الفئة ( CATEGORY) : تشير إلى أن الفئة مرتبطة بتصحيحات النموذج.
# patchطريقة:

# تطبق هذه الطريقة آلية التبليط على النموذج.

# latent_tile_sizeيتم اشتقاقه من tile_size، مما يضمن أن البلاط لا يقل عن قيمة معينة.

# hypertile_in:

# هذه هي الوظيفة الأساسية التي تقوم بتقسيم موتر الإدخال ( ،، qمن طبقات الانتباه) إلى بلاطات أصغر استنادًا إلى قنوات النموذج وشكل الإدخال.kv
# تطبق الطريقة عملية التبليط عن طريق إعادة ترتيب أبعاد موتر الإدخال باستخدام einops.rearrange.
# يتم تنفيذ التبليط على الأبعاد ( hو w)، والتي يتم حسابها على أساس نسبة العرض إلى الارتفاع للموتر المدخل.
# يتم اختيار المقسوم بشكل عشوائي لتقسيم المدخلات إلى بلاطات ذات حجم (nh, nw).
# hypertile_out:

# بعد اكتمال عملية التبليط، تقوم هذه الوظيفة باستعادة شكل الموتر الأصلي عن طريق عكس عملية إعادة الترتيب المطبقة بواسطة hypertile_in.
# استنساخ النموذج وتصحيحه:

# تم استنساخ الكائن modelلتجنب الكتابة فوق النموذج الأصلي.
# تم تصحيح آلية الانتباه في النموذج المستنسخ باستخدام الدالتين hypertile_inو hypertile_out. تضمن هذه التصحيحات حدوث عملية التبليط أثناء خطوات الانتباه في النموذج.
# NODE_CLASS_MAPPINGS:

# يقوم هذا القاموس بربط اسم الفصل "HyperTile"بالفصل HyperTileلسهولة الوصول إليه في النظام القائم على العقدة، ومن المرجح استخدامه لبناء النماذج أو خطوط الأنابيب في واجهة مستخدم رسومية.
# الوظائف:
# يقوم HyperTile بتقسيم موتر الإدخال لآلية الانتباه إلى مربعات أصغر، ومعالجتها بشكل فردي، وإعادة تجميعها. يمكن أن يكون هذا النهج مفيدًا للتعامل مع الصور الكبيرة أو البيانات ذات الأبعاد العالية.
# تسمح خيارات المقسوم العشوائي والقياس القائم على العمق باستراتيجيات تقسيم ديناميكية ومرنة تعتمد على تكوين النموذج وأبعاد الإدخال.
# يُعد هذا مفيدًا بشكل خاص في المجالات مثل إنشاء الصور والدقة الفائقة وتوليف الملمس العصبي حيث قد يكون التعامل مع الصور الكبيرة أمرًا صعبًا، كما يسمح التبليط بإجراء عمليات حسابية أكثر كفاءة.
import math
from einops import rearrange
# Use torch rng for consistency across generations
from torch import randint

def random_divisor(value: int, min_value: int, /, max_options: int = 1) -> int:
    min_value = min(min_value, value)

    # All big divisors of value (inclusive)
    divisors = [i for i in range(min_value, value + 1) if value % i == 0]

    ns = [value // i for i in divisors[:max_options]]  # has at least 1 element

    if len(ns) - 1 > 0:
        idx = randint(low=0, high=len(ns) - 1, size=(1,)).item()
    else:
        idx = 0

    return ns[idx]

class HyperTile:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                             "tile_size": ("INT", {"default": 256, "min": 1, "max": 2048}),
                             "swap_size": ("INT", {"default": 2, "min": 1, "max": 128}),
                             "max_depth": ("INT", {"default": 0, "min": 0, "max": 10}),
                             "scale_depth": ("BOOLEAN", {"default": False}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "model_patches"

    def patch(self, model, tile_size, swap_size, max_depth, scale_depth):
        model_channels = model.model.model_config.unet_config["model_channels"]

        latent_tile_size = max(32, tile_size) // 8
        self.temp = None

        def hypertile_in(q, k, v, extra_options):
            model_chans = q.shape[-2]
            orig_shape = extra_options['original_shape']
            apply_to = []
            for i in range(max_depth + 1):
                apply_to.append((orig_shape[-2] / (2 ** i)) * (orig_shape[-1] / (2 ** i)))

            if model_chans in apply_to:
                shape = extra_options["original_shape"]
                aspect_ratio = shape[-1] / shape[-2]

                hw = q.size(1)
                h, w = round(math.sqrt(hw * aspect_ratio)), round(math.sqrt(hw / aspect_ratio))

                factor = (2 ** apply_to.index(model_chans)) if scale_depth else 1
                nh = random_divisor(h, latent_tile_size * factor, swap_size)
                nw = random_divisor(w, latent_tile_size * factor, swap_size)

                if nh * nw > 1:
                    q = rearrange(q, "b (nh h nw w) c -> (b nh nw) (h w) c", h=h // nh, w=w // nw, nh=nh, nw=nw)
                    self.temp = (nh, nw, h, w)
                return q, k, v

            return q, k, v
        def hypertile_out(out, extra_options):
            if self.temp is not None:
                nh, nw, h, w = self.temp
                self.temp = None
                out = rearrange(out, "(b nh nw) hw c -> b nh nw hw c", nh=nh, nw=nw)
                out = rearrange(out, "b nh nw (h w) c -> b (nh h nw w) c", h=h // nh, w=w // nw)
            return out


        m = model.clone()
        m.set_model_attn1_patch(hypertile_in)
        m.set_model_attn1_output_patch(hypertile_out)
        return (m, )

NODE_CLASS_MAPPINGS = {
    "HyperTile": HyperTile,
}
