# artgen على Docker

تعتمد صورة docker على NVIDIA CUDA 12.4 وPyTorch 2.1، راجع
للحصول على التفاصيل.

المتطلبات

- جهاز كمبيوتر بمواصفات جيدة بما يكفي لتشغيل artgen، وبرامج تشغيل Nvidia الخاصة
- Docker أو Docker Compose أو Podman
البدء السريع[Dockerfile](Dockerfile) and [requirements_docker.txt](requirements_docker.txt) artgen على Docker

تعتمد صورة docker على NVIDIA CUDA 12.4 وPyTorch 2.1، راجع
للحصول على التفاصيل.

المتطلبات

- جهاز كمبيوتر بمواصفات جيدة بما يكفي لتشغيل artgen، وبرامج تشغيل Nvidia الخاصة
- Docker أو Docker Compose أو Podman
البدء السريع

## artgen على Docker

تعتمد صورة docker على NVIDIA CUDA 12.4 وPyTorch 2.1، راجع
للحصول على التفاصيل.

المتطلبات

- جهاز كمبيوتر بمواصفات جيدة بما يكفي لتشغيل artgen، وبرامج تشغيل Nvidia الخاصة
- Docker أو Docker Compose أو Podman
البدء السريع

## artgen على Docker

تعتمد صورة docker على NVIDIA CUDA 12.4 وPyTorch 2.1، راجع
للحصول على التفاصيل.

المتطلبات

- جهاز كمبيوتر بمواصفات جيدة بما يكفي لتشغيل artgen، وبرامج تشغيل Nvidia الخاصة
- Docker أو Docker Compose أو Podman
البدء السريع

**مزيد من المعلومات في [notes](#notes).**

### التشغيل باستخدام Docker Compose

1. استنساخ هذا المستودع
2. تشغيل حاوية Docker باستخدام `docker compose up`.

### التشغيل باستخدام Docker

```sh
docker run -p 7865:7865 -v artgen-data:/content/data -it \
--gpus all \
-e CMDARGS=--listen \
-e DATADIR=/content/data \
-e config_path=/content/data/config.txt \
-e config_example_path=/content/data/config_modification_tutorial.txt \
-e path_checkpoints=/content/data/models/checkpoints/ \
-e path_loras=/content/data/models/loras/ \
-e path_embeddings=/content/data/models/embeddings/ \
-e path_vae_approx=/content/data/models/vae_approx/ \
-e path_upscale_models=/content/data/models/upscale_models/ \
-e path_inpaint=/content/data/models/inpaint/ \
-e path_controlnet=/content/data/models/controlnet/ \
-e path_clip_vision=/content/data/models/clip_vision/ \
-e path_artgen_expansion=/content/data/models/prompt_expansion/artgen_expansion/ \
-e path_outputs=/content/app/outputs/ \
ghcr.io/lllyasviel/artgen
```
### التشغيل باستخدام Podman

```sh
podman run -p 7865:7865 -v artgen-data:/content/data -it \
--security-opt=no-new-privileges --cap-drop=ALL --security-opt label=type:nvidia_container_t --device=nvidia.com/gpu=all \
-e CMDARGS=--listen \
-e DATADIR=/content/data \
-e config_path=/content/data/config.txt \
-e config_example_path=/content/data/config_modification_tutorial.txt \
-e path_checkpoints=/content/data/models/checkpoints/ \
-e path_loras=/content/data/models/loras/ \
-e path_embeddings=/content/data/models/embeddings/ \
-e path_vae_approx=/content/data/models/vae_approx/ \
-e path_upscale_models=/content/data/models/upscale_models/ \
-e path_inpaint=/content/data/models/inpaint/ \
-e path_controlnet=/content/data/models/controlnet/ \
-e path_clip_vision=/content/data/models/clip_vision/ \
-e path_artgen_expansion=/content/data/models/prompt_expansion/artgen_expansion/ \
-e path_outputs=/content/app/outputs/ \
ghcr.io/lllyasviel/artgen
```

عندما ترى الرسالةe  `Use the app with http://0.0.0.0:7865/` في وحدة التحكم، يمكنك الوصول إلى عنوان URL في متصفحك.

Your models and outputs are stored in the `artgen-data` المجلد، والذي يتم تخزينه فيه، وفقًا لنظام التشغيل `/var/lib/docker/volumes/` (or `~/.local/share/containers/storage/volumes/` عند استخدام `podman`).

## بناء الحاوية محليًا

استنساخ المستودع أولاً، وفتح محطة طرفية في المجلد.

البناء باستخدام `docker`:
```sh
docker build . -t artgen
```

Build with `podman`:
```sh
podman build . -t artgen
```

## التفاصيل

### تحديث الحاوية يدويًا (`docker compose`)

عند استخدامك `docker compose up` بشكل مستمر، لا يتم تحديث الحاوية إلى أحدث إصدار من artgen تلقائيًا.
Run `git pull` before executing `docker compose build --no-cache` لبناء صورة بأحدث إصدار من artgen.
يمكنك بعد ذلك البدء باستخدام `docker compose up`

### استيراد النماذج والمخرجات

إذا كنت تريد استيراد الملفات من مجلد النماذج أو المخرجات، فيمكنك إضافة عمليات التثبيت التالية في [docker-compose.yml](docker-compose.yml) أو الطريقة المفضلة لديك لتشغيل الحاوية:
```
#- ./models:/import/models   # بمجرد استيراد الملفات، لن تحتاج إلى التثبيت مرة أخرى.
#- ./outputs:/import/outputs  # بمجرد استيراد الملفات، لن تحتاج إلى التثبيت مرة أخرى.
```
بعد تشغيل الحاوية، سيتم نسخ ملفاتك إلى `/content/data/models` and `/content/data/outputs`
نظرًا لأن `/content/data` مجلد وحدة تخزين دائمة، فستظل ملفاتك مستمرة حتى عند إعادة تشغيل الحاوية بدون عمليات التثبيت المذكورة أعلاه.


### المسارات داخل الحاوية

|Path|Details|
|-|-|
|/content/app|The application stored folder|
|/content/app/models.org|Original 'models' folder.<br> Files are copied to the '/content/app/models' which is symlinked to '/content/data/models' every time the container boots. (Existing files will not be overwritten.) |
|/content/data|Persistent volume mount point|
|/content/data/models|The folder is symlinked to '/content/app/models'|
|/content/data/outputs|The folder is symlinked to '/content/app/outputs'|

### البيئات

يمكنك تغيير `config.txt` المعلمات باستخدام متغيرات البيئة.
**أولوية استخدام البيئات أعلى من القيم المحددة في `config.txt`، وسيتم حفظها في `config_modification_tutorial.txt`**

البيئات المحددة في Docker. يتم استخدامها بواسطة 'entrypoint.sh'
|Environment|Details|
|-|-|
|DATADIR|'/content/data' location.|
|CMDARGS|Arguments for [entry_with_update.py](entry_with_update.py) which is called by [entrypoint.sh](entrypoint.sh)|
|config_path|'config.txt' location|
|config_example_path|'config_modification_tutorial.txt' location|
|HF_MIRROR| huggingface mirror site domain| 

يمكنك أيضًا استخدام نفس أسماء وقيم مفاتيح json الموضحة في
كبيئات.
راجع الأمثلة في'config_modification_tutorial.txt' يمكنك أيضًا استخدام نفس أسماء وقيم مفاتيح json الموضحة في
كبيئات.
راجع الأمثلة في[docker-compose.yml](docker-compose.yml)

## ملاحظات

- يرجى الاحتفاظ بـ "path_outputs" ضمن "/content/app". وإلا، فقد تتلقى خطأً عند فتح سجل التاريخ.
- لا يزال Docker على Mac/Windows يعاني من مشكلات في شكل بطء الوصول إلى وحدة التخزين عند استخدام وحدات تخزين "bind mount". يرجى الرجوع إلى[this article](https://docs.docker.com/storage/volumes/#use-a-volume-with-docker-compose) لعدم استخدام "bind mount".
- لا يتم دعم واجهة MPS الخلفية (Metal Performance Shaders، Apple Silicon M1/M2/إلخ) في Docker حتى الآن، راجع https://github.com/pytorch/pytorch/issues/81224
- يمكنك أيضًا استخدام `docker compose up -d` لبدء تشغيل الحاوية منفصلة والاتصال بالسجلات باستخدام `docker compose logs -f`. بهذه الطريقة، يمكنك أيضًا إغلاق المحطة الطرفية والحفاظ على تشغيل الحاوية.