/*
يستخدم لترجمة محتوى صفحة الويب بناءً على بيانات الترجمة المتاحة (Localization). هنا ملخص لما يقوم به الكود:

الملخص:
التأكد من توفر الترجمة:

يتم التحقق مما إذا كانت هناك بيانات للترجمة (window.localization) ووجود محتوى في تلك البيانات باستخدام دالة hasLocalization().
معالجة عقد النصوص (Text Nodes):

يتم استخدام textNodesUnder() للحصول على جميع النصوص في شجرة الـ DOM.
يتم التحقق مما إذا كانت النصوص قابلة للترجمة باستخدام canBeTranslated() التي تستثني عناصر مثل <script>, <style>, <textarea>, والأرقام.
ترجمة النصوص:

getTranslation() تستخدم للبحث عن الترجمة في بيانات localization بناءً على النص الأصلي.
إذا تم العثور على الترجمة، يتم استبدال النص الأصلي بها في صفحة الويب.
معالجة النصوص والعناوين والعناصر النائبة (Placeholders):

processTextNode() تقوم بمعالجة النصوص فقط، بينما processNode() تتعامل مع النصوص، عناوين العناصر، والعناصر النائبة.
إذا كان هناك نص قابل للترجمة، يتم استبداله في صفحة الويب ويتم تخزين النص الأصلي في سمة data-original-text.
التحديثات التلقائية:

عندما يتم تحميل عناصر جديدة إلى الصفحة (مثلًا عند التحديثات الديناميكية)، يتم تطبيق الترجمة تلقائيًا عبر مراقبة التغييرات في شجرة DOM باستخدام MutationObserver.
محاذاة النصوص من اليمين لليسار (RTL):

إذا كانت اللغة المستخدمة هي لغة تكتب من اليمين إلى اليسار (مثل العربية أو العبرية)، يتم تطبيق القواعد المناسبة لذلك عبر CSS.
كيفية الاستخدام:
الكود يعمل على ترجمة صفحة الويب ديناميكيًا بناءً على محتويات كائن localization الذي يحتوي على الترجمات.
يتم تطبيق الترجمة على العناوين (title)، العناصر النائبة (placeholder)، والنصوص داخل الصفحة.
يعتمد هذا النظام على تكامل مكتبة Gradio لمعالجة المحتوى الديناميكي.
*/
var re_num = /^[.\d]+$/;

var original_lines = {};
var translated_lines = {};

function hasLocalization() {
    return window.localization && Object.keys(window.localization).length > 0;
}

function textNodesUnder(el) {
    var n, a = [], walk = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
    while ((n = walk.nextNode())) a.push(n);
    return a;
}

function canBeTranslated(node, text) {
    if (!text) return false;
    if (!node.parentElement) return false;
    var parentType = node.parentElement.nodeName;
    if (parentType == 'SCRIPT' || parentType == 'STYLE' || parentType == 'TEXTAREA') return false;
    if (re_num.test(text)) return false;
    return true;
}

function getTranslation(text) {
    if (!text) return undefined;

    if (translated_lines[text] === undefined) {
        original_lines[text] = 1;
    }

    var tl = localization[text];
    if (tl !== undefined) {
        translated_lines[tl] = 1;
    }

    return tl;
}

function processTextNode(node) {
    var text = node.textContent.trim();

    if (!canBeTranslated(node, text)) return;

    var tl = getTranslation(text);
    if (tl !== undefined) {
        node.textContent = tl;
        if (text && node.parentElement) {
          node.parentElement.setAttribute("data-original-text", text);
        }
    }
}

function processNode(node) {
    if (node.nodeType == 3) {
        processTextNode(node);
        return;
    }

    if (node.title) {
        let tl = getTranslation(node.title);
        if (tl !== undefined) {
            node.title = tl;
        }
    }

    if (node.placeholder) {
        let tl = getTranslation(node.placeholder);
        if (tl !== undefined) {
            node.placeholder = tl;
        }
    }

    textNodesUnder(node).forEach(function(node) {
        processTextNode(node);
    });
}

function refresh_style_localization() {
    processNode(document.querySelector('.style_selections'));
}

function refresh_aspect_ratios_label(value) {
    label = document.querySelector('#aspect_ratios_accordion div span');
    translation = getTranslation("Aspect Ratios");
    if (typeof translation == "undefined") {
        translation = "Aspect Ratios";
    }
    label.textContent = translation + " " + htmlDecode(value);
}

function localizeWholePage() {
    processNode(gradioApp());

    function elem(comp) {
        var elem_id = comp.props.elem_id ? comp.props.elem_id : "component-" + comp.id;
        return gradioApp().getElementById(elem_id);
    }

    for (var comp of window.gradio_config.components) {
        if (comp.props.webui_tooltip) {
            let e = elem(comp);

            let tl = e ? getTranslation(e.title) : undefined;
            if (tl !== undefined) {
                e.title = tl;
            }
        }
        if (comp.props.placeholder) {
            let e = elem(comp);
            let textbox = e ? e.querySelector('[placeholder]') : null;

            let tl = textbox ? getTranslation(textbox.placeholder) : undefined;
            if (tl !== undefined) {
                textbox.placeholder = tl;
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    if (!hasLocalization()) {
        return;
    }

    onUiUpdate(function(m) {
        m.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                processNode(node);
            });
        });
    });

    localizeWholePage();

    if (localization.rtl) { // if the language is from right to left,
        (new MutationObserver((mutations, observer) => { // wait for the style to load
            mutations.forEach(mutation => {
                mutation.addedNodes.forEach(node => {
                    if (node.tagName === 'STYLE') {
                        observer.disconnect();

                        for (const x of node.sheet.rules) { // find all rtl media rules
                            if (Array.from(x.media || []).includes('rtl')) {
                                x.media.appendMedium('all'); // enable them
                            }
                        }
                    }
                });
            });
        })).observe(gradioApp(), {childList: true});
    }
});
