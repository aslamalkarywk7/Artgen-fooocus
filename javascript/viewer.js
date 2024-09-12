/* تحديد ارتفاع العرض: يحدد قيمة ابتدائية لارتفاع عنصر العرض.

تحديث شبكة العناصر: يحسب عدد الأعمدة في شبكة عرض الصور بناءً على حجم العنصر ويقوم بتحديث الشبكة.

تحديث الشبكة بتأخير: يقوم بتحديث الشبكة بشكل متكرر مع تأخيرات مختلفة لضمان تحديث العرض بشكل مستمر.

تحديث حجم العناصر عند تغيير حجم النافذة: يعدل ارتفاع عناصر معينة بناءً على حجم نافذة المتصفح ويحدث الشبكة.

التمرير إلى أعلى الصفحة: يمرر الصفحة إلى أعلى بعد فترة زمنية محددة.

التمرير إلى أسفل الصفحة: يمرر الصفحة إلى أسفل حتى يظهر عنصر معين في أسفل الصفحة.

استماع لتغييرات حجم النافذة: يستمع لتغيرات حجم النافذة ويقوم بتحديث العناصر عند تغيير الحجم.

تشغيل الوظائف بعد تحميل واجهة المستخدم: ينفذ وظائف معينة بعد تحميل واجهة المستخدم، مثل تحديث الشبكة وتنسيق العناصر.

تحديث قيم عناصر الإدخال عند فقدان التركيز: يقوم بتحديث النصوص في منطقة معينة وإرسال حدث لتحديث الواجهة.

تنسيق بعض عناصر الواجهة: يعدل محتوى وتنسيق بعض العناصر بعد تحميل واجهة المستخدم، مثل استبدال الرموز وتحريك عناصر الإدخال. */
window.main_viewer_height = 512;

function refresh_grid() {
    let gridContainer = document.querySelector('#final_gallery .grid-container');
    let final_gallery = document.getElementById('final_gallery');

    if (gridContainer) if (final_gallery) {
        let rect = final_gallery.getBoundingClientRect();
        let cols = Math.ceil((rect.width - 16.0) / rect.height);
        if (cols < 2) cols = 2;
        gridContainer.style.setProperty('--grid-cols', cols);
    }
}

function refresh_grid_delayed() {
    refresh_grid();
    setTimeout(refresh_grid, 100);
    setTimeout(refresh_grid, 500);
    setTimeout(refresh_grid, 1000);
}

function resized() {
    let windowHeight = window.innerHeight - 260;
    let elements = document.getElementsByClassName('main_view');

    if (windowHeight > 745) windowHeight = 745;

    for (let i = 0; i < elements.length; i++) {
        elements[i].style.height = windowHeight + 'px';
    }

    window.main_viewer_height = windowHeight;

    refresh_grid();
}

function viewer_to_top(delay = 100) {
    setTimeout(() => window.scrollTo({top: 0, behavior: 'smooth'}), delay);
}

function viewer_to_bottom(delay = 100) {
    let element = document.getElementById('positive_prompt');
    let yPos = window.main_viewer_height;

    if (element) {
        yPos = element.getBoundingClientRect().top + window.scrollY;
    }

    setTimeout(() => window.scrollTo({top: yPos - 8, behavior: 'smooth'}), delay);
}

window.addEventListener('resize', (e) => {
    resized();
});

onUiLoaded(async () => {
    resized();
});

function on_style_selection_blur() {
    let target = document.querySelector("#gradio_receiver_style_selections textarea");
    target.value = "on_style_selection_blur " + Math.random();
    let e = new Event("input", {bubbles: true})
    Object.defineProperty(e, "target", {value: target})
    target.dispatchEvent(e);
}

onUiLoaded(async () => {
    let spans = document.querySelectorAll('.aspect_ratios span');

    spans.forEach(function (span) {
        span.innerHTML = span.innerHTML.replace(/&lt;/g, '<').replace(/&gt;/g, '>');
    });

    document.querySelector('.style_selections').addEventListener('focusout', function (event) {
        setTimeout(() => {
            if (!this.contains(document.activeElement)) {
                on_style_selection_blur();
            }
        }, 200);
    });

    let inputs = document.querySelectorAll('.lora_weight input[type="range"]');

    inputs.forEach(function (input) {
        input.style.marginTop = '12px';
    });
});
