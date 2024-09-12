# https://github.com/comfyanonymous/ComfyUI/blob/master/nodes.py 
# هذا الكود فئتين، FreeUو FreeU_V2، وكلاهما مصممان لتعديل النماذج من خلال التصحيح. تتضمن الوظيفة الأساسية توسيع الطبقات المخفية لإخراج النموذج وتطبيق مرشح قائم على فورييه. فيما يلي ملخص للأجزاء الرئيسية:

# وظيفة مرشح فورييه
# Fourier_filter(x, threshold, scale):تطبق هذه الوظيفة تحويل فورييه على موتر x، وتعدل ترددات معينة باستخدام قناع، ثم تطبق تحويل فورييه عكسي لتصفية الموتر.
# FFT : تحويل فورييه الأمامي للانتقال إلى مجال التردد.
# القناع : يتم تطبيق القناع لضبط أجزاء معينة من طيف التردد.
# IFFT : تحويل فورييه العكسي للعودة إلى المجال المكاني.
# FreeUفصل
# تهدف هذه الفئة إلى تعديل الطبقات المخفية ( h) والطبقات المخفية المكانية ( hsp) للنموذج عن طريق تغيير حجمها وتصفيتها بناءً على شكلها والمعلمات المحددة ( b1، b2، s1، s2).
# الوظيفة الرئيسية :
# يتم تطبيق التدرج على قنوات محددة من h.
# المرشحات hspباستخدام Fourier_filterالوظيفة.
# يعالج مشكلات الأجهزة المحتملة التي torch.fftلا يتم دعمها، ويعود إلى وحدة المعالجة المركزية إذا لزم الأمر.
# FreeU_V2فصل
# هذه نسخة موسعة FreeUمع التطبيع الإضافي.
# تطبيع المتوسط ​​المخفي : تطبيع القيم المتوسطة المخفية hقبل تطبيق التدرج.
# الوظائف :
# يتم تطبيع الطبقات المخفية استنادًا إلى قيمها الدنيا/القصوى قبل التدرج.
# أما بقية الوظائف فهي مشابهة لـ FreeU، بما في ذلك مرشح فورييه وآلية الرجوع إلى وحدة المعالجة المركزية.
# الاستخدام والتعيينات
# يوفر الكود واجهة عقدة لهذه التصحيحات، مما يسمح باستخدامها في إطار عمل مثل ComfyUI للتلاعب بالنموذج.
# NODE_CLASS_MAPPINGS:ربط أسماء الفئات إلى FreeUو FreeU_V2، مما يجعلها متاحة كعقد في إطار العمل.
# يقوم الكود المقدم بتصحيح النماذج بشكل فعال من خلال تطبيق التدرج الديناميكي وتحويلات فورييه على مخرجات النموذج لتحسين المعالجة.
#code originally taken from: https://github.com/ChenyangSi/FreeU (under MIT License)

import torch


def Fourier_filter(x, threshold, scale):
    # FFT
    x_freq = torch.fft.fftn(x.float(), dim=(-2, -1))
    x_freq = torch.fft.fftshift(x_freq, dim=(-2, -1))

    B, C, H, W = x_freq.shape
    mask = torch.ones((B, C, H, W), device=x.device)

    crow, ccol = H // 2, W //2
    mask[..., crow - threshold:crow + threshold, ccol - threshold:ccol + threshold] = scale
    x_freq = x_freq * mask

    # IFFT
    x_freq = torch.fft.ifftshift(x_freq, dim=(-2, -1))
    x_filtered = torch.fft.ifftn(x_freq, dim=(-2, -1)).real

    return x_filtered.to(x.dtype)


class FreeU:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                             "b1": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "b2": ("FLOAT", {"default": 1.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s1": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s2": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "model_patches"

    def patch(self, model, b1, b2, s1, s2):
        model_channels = model.model.model_config.unet_config["model_channels"]
        scale_dict = {model_channels * 4: (b1, s1), model_channels * 2: (b2, s2)}
        on_cpu_devices = {}

        def output_block_patch(h, hsp, transformer_options):
            scale = scale_dict.get(h.shape[1], None)
            if scale is not None:
                h[:,:h.shape[1] // 2] = h[:,:h.shape[1] // 2] * scale[0]
                if hsp.device not in on_cpu_devices:
                    try:
                        hsp = Fourier_filter(hsp, threshold=1, scale=scale[1])
                    except:
                        print("Device", hsp.device, "does not support the torch.fft functions used in the FreeU node, switching to CPU.")
                        on_cpu_devices[hsp.device] = True
                        hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)
                else:
                    hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)

            return h, hsp

        m = model.clone()
        m.set_model_output_block_patch(output_block_patch)
        return (m, )

class FreeU_V2:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "model": ("MODEL",),
                             "b1": ("FLOAT", {"default": 1.3, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "b2": ("FLOAT", {"default": 1.4, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s1": ("FLOAT", {"default": 0.9, "min": 0.0, "max": 10.0, "step": 0.01}),
                             "s2": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                              }}
    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"

    CATEGORY = "model_patches"

    def patch(self, model, b1, b2, s1, s2):
        model_channels = model.model.model_config.unet_config["model_channels"]
        scale_dict = {model_channels * 4: (b1, s1), model_channels * 2: (b2, s2)}
        on_cpu_devices = {}

        def output_block_patch(h, hsp, transformer_options):
            scale = scale_dict.get(h.shape[1], None)
            if scale is not None:
                hidden_mean = h.mean(1).unsqueeze(1)
                B = hidden_mean.shape[0]
                hidden_max, _ = torch.max(hidden_mean.view(B, -1), dim=-1, keepdim=True)
                hidden_min, _ = torch.min(hidden_mean.view(B, -1), dim=-1, keepdim=True)
                hidden_mean = (hidden_mean - hidden_min.unsqueeze(2).unsqueeze(3)) / (hidden_max - hidden_min).unsqueeze(2).unsqueeze(3)

                h[:,:h.shape[1] // 2] = h[:,:h.shape[1] // 2] * ((scale[0] - 1 ) * hidden_mean + 1)

                if hsp.device not in on_cpu_devices:
                    try:
                        hsp = Fourier_filter(hsp, threshold=1, scale=scale[1])
                    except:
                        print("Device", hsp.device, "does not support the torch.fft functions used in the FreeU node, switching to CPU.")
                        on_cpu_devices[hsp.device] = True
                        hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)
                else:
                    hsp = Fourier_filter(hsp.cpu(), threshold=1, scale=scale[1]).to(hsp.device)

            return h, hsp

        m = model.clone()
        m.set_model_output_block_patch(output_block_patch)
        return (m, )

NODE_CLASS_MAPPINGS = {
    "FreeU": FreeU,
    "FreeU_V2": FreeU_V2,
}
