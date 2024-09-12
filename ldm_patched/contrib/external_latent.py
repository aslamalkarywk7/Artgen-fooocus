# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# 
# يوفر هذا الكود تنفيذات لعدة فئات عقدية تقوم بعمليات مختلفة على التمثيلات الكامنة في إطار الشبكة العصبية. من المحتمل أن تُستخدم هذه العمليات في سياق معالجة الصور أو الإشارات ضمن خط أنابيب التعلم الآلي. فيما يلي تفصيل لكل مكون:

# 1. الواردات:
# ldm_patched.modules.utils:من المفترض أن تحتوي هذه الوحدة على وظائف مفيدة، مثل رفع مستوى الموتر الكامن وتكراره.
# torch:مكتبة PyTorch، تُستخدم لعمليات الموتر والحسابات.
# 2. الوظائف:
# reshape_latent_to(target_shape, latent):
# الغرض : إعادة تشكيل الموتر الكامن ليتناسب مع شكل الهدف.
# تفاصيل :
# latentإذا لم يتطابق الشكل target_shape، فسيتم تغيير الحجم latentإلى الارتفاع والعرض المستهدفين باستخدام الاستيفاء الخطي الثنائي.
# ثم يكرر الموتر الكامن ليتناسب مع حجم الدفعة للشكل المستهدف.
# 3. الفصول الدراسية:
# LatentAddفصل:
# الغرض : إضافة عنصرين كامنين للموتر على أساس كل عنصر.
# المدخلات :
# samples1: samples2الموترات الكامنة التي سيتم إضافتها.
# وظيفة :
# إعادة تشكيلها samples2لتتناسب مع شكل samples1.
# يحسب مجموع samples1و samples2.
# LatentSubtractفصل:
# الغرض : طرح موتر كامن واحد من عنصر آخر.
# المدخلات :
# samples1, samples2: يتم طرح المتجهات الكامنة حيث samples2من samples1.
# وظيفة :
# إعادة تشكيلها samples2لتتناسب مع شكل samples1.
# يحسب الفرق بين samples1و samples2.
# LatentMultiplyفصل:
# الغرض : ضرب موتر كامن بمضاعف قياسي.
# المدخلات :
# samples:الموتر الكامن الذي يجب ضربه.
# multiplier:القيمة القياسية التي يتم بها ضرب الموتر الكامن.
# وظيفة :
# يضرب samplesبـ multiplier.
# LatentInterpolateفصل:
# الغرض : تنفيذ الاستيفاء بين اثنين من الموترات الكامنة.
# المدخلات :
# samples1: samples2الموترات الكامنة التي يجب الاستيفاء بينها.
# ratio:نسبة الاستيفاء بين samples1و samples2.
# وظيفة :
# تطبيع samples1و samples2.
# يحسب الاستيفاء المرجح بينهما بناءً على ratio.
# إعادة قياس النتيجة للحفاظ على الحجم الأصلي.
# LatentBatchفصل:
# الغرض : ربط اثنين من الموترات الكامنة على طول بُعد الدفعة.
# المدخلات :
# samples1: samples2الموترات الكامنة التي سيتم تجميعها في دفعات.
# وظيفة :
# يمكن ترقيتها samples2إذا لزم الأمر لتتناسب مع شكل samples1.
# يتسلسل samples1على samples2طول أبعاد الدفعة.
# يجمع مؤشرات الدفعة من كلا الموترين.
# LatentBatchSeedBehaviorفصل:
# الغرض : إدارة سلوك مؤشرات الدفعة للموترات الكامنة بناءً على سلوك البذرة.
# المدخلات :
# samples:الموتر الكامن مع مؤشرات الدفعة الاختيارية.
# seed_behavior:يحدد كيفية التعامل مع مؤشرات الدفعة (عشوائية أو ثابتة).
# وظيفة :
# إذا seed_behaviorكان "عشوائيًا"، فإنه يقوم بإزالة مؤشرات الدفعة.
# إذا seed_behaviorتم "إصلاحه"، فسيتم تعيين جميع مؤشرات الدفعة إلى قيمة ثابتة استنادًا إلى المؤشر الأول.
# 4. NODE_CLASS_MAPPINGS:
# الغرض : ربط أسماء فئات العقد بالتطبيقات المقابلة لها.
# الاستخدام : يستخدم للإشارة إلى العقد وإنشائها بشكل ديناميكي استنادًا إلى أسماء فئاتها، مما يسهل إطار معالجة قائم على العقد ومرن.
# ملخص:
# LatentAdd : يضيف اثنين من المتجهين الكامنين.
# LatentSubtract : يطرح موتر كامن واحد من آخر.
# LatentMultiply : ضرب موتر كامن بمقياس قياسي.
# LatentInterpolate : يقوم بالتدخل بين اثنين من المتجهين الكامنين.
# LatentBatch : يقوم بربط المتجهات الكامنة على طول بُعد الدفعة.
# LatentBatchSeedBehavior : إدارة سلوك مؤشر الدفعة استنادًا إلى إعدادات البذرة.
# توفر هذه الفئات عمليات أساسية للتلاعب ومعالجة التمثيلات الكامنة في بيئة الشبكة العصبية، مما يسهل المهام مثل الجمع بين الميزات الكامنة وتوسيعها واستيفائها.
import ldm_patched.modules.utils
import torch

def reshape_latent_to(target_shape, latent):
    if latent.shape[1:] != target_shape[1:]:
        latent = ldm_patched.modules.utils.common_upscale(latent, target_shape[3], target_shape[2], "bilinear", "center")
    return ldm_patched.modules.utils.repeat_to_batch_size(latent, target_shape[0])


class LatentAdd:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples1": ("LATENT",), "samples2": ("LATENT",)}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "op"

    CATEGORY = "latent/advanced"

    def op(self, samples1, samples2):
        samples_out = samples1.copy()

        s1 = samples1["samples"]
        s2 = samples2["samples"]

        s2 = reshape_latent_to(s1.shape, s2)
        samples_out["samples"] = s1 + s2
        return (samples_out,)

class LatentSubtract:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples1": ("LATENT",), "samples2": ("LATENT",)}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "op"

    CATEGORY = "latent/advanced"

    def op(self, samples1, samples2):
        samples_out = samples1.copy()

        s1 = samples1["samples"]
        s2 = samples2["samples"]

        s2 = reshape_latent_to(s1.shape, s2)
        samples_out["samples"] = s1 - s2
        return (samples_out,)

class LatentMultiply:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples": ("LATENT",),
                              "multiplier": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.01}),
                             }}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "op"

    CATEGORY = "latent/advanced"

    def op(self, samples, multiplier):
        samples_out = samples.copy()

        s1 = samples["samples"]
        samples_out["samples"] = s1 * multiplier
        return (samples_out,)

class LatentInterpolate:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples1": ("LATENT",),
                              "samples2": ("LATENT",),
                              "ratio": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                              }}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "op"

    CATEGORY = "latent/advanced"

    def op(self, samples1, samples2, ratio):
        samples_out = samples1.copy()

        s1 = samples1["samples"]
        s2 = samples2["samples"]

        s2 = reshape_latent_to(s1.shape, s2)

        m1 = torch.linalg.vector_norm(s1, dim=(1))
        m2 = torch.linalg.vector_norm(s2, dim=(1))

        s1 = torch.nan_to_num(s1 / m1)
        s2 = torch.nan_to_num(s2 / m2)

        t = (s1 * ratio + s2 * (1.0 - ratio))
        mt = torch.linalg.vector_norm(t, dim=(1))
        st = torch.nan_to_num(t / mt)

        samples_out["samples"] = st * (m1 * ratio + m2 * (1.0 - ratio))
        return (samples_out,)

class LatentBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples1": ("LATENT",), "samples2": ("LATENT",)}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "batch"

    CATEGORY = "latent/batch"

    def batch(self, samples1, samples2):
        samples_out = samples1.copy()
        s1 = samples1["samples"]
        s2 = samples2["samples"]

        if s1.shape[1:] != s2.shape[1:]:
            s2 = ldm_patched.modules.utils.common_upscale(s2, s1.shape[3], s1.shape[2], "bilinear", "center")
        s = torch.cat((s1, s2), dim=0)
        samples_out["samples"] = s
        samples_out["batch_index"] = samples1.get("batch_index", [x for x in range(0, s1.shape[0])]) + samples2.get("batch_index", [x for x in range(0, s2.shape[0])])
        return (samples_out,)

class LatentBatchSeedBehavior:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "samples": ("LATENT",),
                              "seed_behavior": (["random", "fixed"],),}}

    RETURN_TYPES = ("LATENT",)
    FUNCTION = "op"

    CATEGORY = "latent/advanced"

    def op(self, samples, seed_behavior):
        samples_out = samples.copy()
        latent = samples["samples"]
        if seed_behavior == "random":
            if 'batch_index' in samples_out:
                samples_out.pop('batch_index')
        elif seed_behavior == "fixed":
            batch_number = samples_out.get("batch_index", [0])[0]
            samples_out["batch_index"] = [batch_number] * latent.shape[0]

        return (samples_out,)

NODE_CLASS_MAPPINGS = {
    "LatentAdd": LatentAdd,
    "LatentSubtract": LatentSubtract,
    "LatentMultiply": LatentMultiply,
    "LatentInterpolate": LatentInterpolate,
    "LatentBatch": LatentBatch,
    "LatentBatchSeedBehavior": LatentBatchSeedBehavior,
}
