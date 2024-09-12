/* 
مخصص لتعديل وتحسين النصوص المدخلة داخل حقل إدخال من نوع textarea، حيث يحتوي على العديد من الوظائف التي تتعامل مع الأحداث المتعلقة بالمفاتيح وتعديل النصوص بشكل ديناميكي.

شرح لأجزاء الكود:
دالة updateInput(target):

هذه الدالة تقوم بإطلاق حدث input بشكل برمجي على العنصر الهدف (target)، مما يتيح تحديث حالة الإدخال (مثل النصوص المدخلة) دون تدخل المستخدم بشكل مباشر.
دالة keyupEditAttention(event):

هذه الدالة هي المسؤولة عن التعامل مع حدث keydown (الضغط على المفاتيح) داخل حقول الإدخال التي تحتوي على النصوص (مثل textarea).
الدالة تفحص إذا تم الضغط على مفاتيح التحكم مثل ctrl أو meta (الموجودة في أجهزة الماك)، وإذا كان المفتاح المضغوط هو السهم للأعلى أو للأسفل.
إذا كان السهم للأعلى أو للأسفل، فإنه يضبط ويعدل "وزن" النصوص المدخلة داخل علامات معينة مثل الأقواس () أو الأقواس الزاويّة < >.
كما أن هناك وظيفة لاختيار الكلمة الحالية أو النص داخل الأقواس لضبط وزن معين لهذا الجزء من النص بناءً على السهم المضغوط (لزيادة أو تقليل الوزن).
الدوال المساعدة داخل keyupEditAttention:

selectCurrentParenthesisBlock: تحدد النص الموجود داخل الأقواس (سواءً كانت () أو < >) وتقوم بتحديده.

selectCurrentWord: إذا لم يكن هناك أي أقواس حول المؤشر، فإن هذه الدالة تقوم بتحديد الكلمة الحالية التي يقف عندها المؤشر.

يتم تعديل النصوص بإضافة أو إزالة الوزن بناءً على ما إذا تم ضغط السهم لأعلى أو لأسفل.

إضافة المستمع addEventListener:

يتم استخدام مستمع لحدث keydown، بحيث يتم استدعاء الدالة keyupEditAttention عند الضغط على أي مفتاح داخل المستند، مما يسمح بتعديل النصوص ديناميكيًا بناءً على تفاعل المستخدم.
الاستخدام:
هذا الكود قد يكون مفيدًا في بيئات تحرير النصوص التي تتطلب تعديل أوزان النصوص أو القيم المحاطة بأقواس معينة (مثل تحرير نصوص باستخدام الذكاء الاصطناعي أو تخصيص إعدادات معينة للنصوص).
مثال عملي:
في محرر نصوص يستخدم لإنشاء محتوى أو بيانات مهيكلة، قد يحتاج المستخدم لضبط أوزان كلمات أو عبارات معينة داخل النص. باستخدام هذا الكود، يمكن للمستخدم التنقل بين النصوص وضبط هذه الأوزان بسهولة عن طريق الضغط على مفاتيح السهم للأعلى أو السهم للأسفل.
*/
function updateInput(target) {
    let e = new Event("input", {bubbles: true});
    Object.defineProperty(e, "target", {value: target});
    target.dispatchEvent(e);
}

function keyupEditAttention(event) {
    let target = event.originalTarget || event.composedPath()[0];
    if (!target.matches("*:is([id*='_prompt'], .prompt) textarea")) return;
    if (!(event.metaKey || event.ctrlKey)) return;

    let isPlus = event.key == "ArrowUp";
    let isMinus = event.key == "ArrowDown";
    if (!isPlus && !isMinus) return;

    let selectionStart = target.selectionStart;
    let selectionEnd = target.selectionEnd;
    let text = target.value;

    function selectCurrentParenthesisBlock(OPEN, CLOSE) {
        if (selectionStart !== selectionEnd) return false;

        // Find opening parenthesis around current cursor
        const before = text.substring(0, selectionStart);
        let beforeParen = before.lastIndexOf(OPEN);
        if (beforeParen == -1) return false;
        let beforeParenClose = before.lastIndexOf(CLOSE);
        while (beforeParenClose !== -1 && beforeParenClose > beforeParen) {
            beforeParen = before.lastIndexOf(OPEN, beforeParen - 1);
            beforeParenClose = before.lastIndexOf(CLOSE, beforeParenClose - 1);
        }

        // Find closing parenthesis around current cursor
        const after = text.substring(selectionStart);
        let afterParen = after.indexOf(CLOSE);
        if (afterParen == -1) return false;
        let afterParenOpen = after.indexOf(OPEN);
        while (afterParenOpen !== -1 && afterParen > afterParenOpen) {
            afterParen = after.indexOf(CLOSE, afterParen + 1);
            afterParenOpen = after.indexOf(OPEN, afterParenOpen + 1);
        }
        if (beforeParen === -1 || afterParen === -1) return false;

        // Set the selection to the text between the parenthesis
        const parenContent = text.substring(beforeParen + 1, selectionStart + afterParen);
        const lastColon = parenContent.lastIndexOf(":");
        selectionStart = beforeParen + 1;
        selectionEnd = selectionStart + lastColon;
        target.setSelectionRange(selectionStart, selectionEnd);
        return true;
    }

    function selectCurrentWord() {
        if (selectionStart !== selectionEnd) return false;
        const delimiters = ".,\\/!?%^*;:{}=`~() \r\n\t";

        // seek backward until to find beggining
        while (!delimiters.includes(text[selectionStart - 1]) && selectionStart > 0) {
            selectionStart--;
        }

        // seek forward to find end
        while (!delimiters.includes(text[selectionEnd]) && selectionEnd < text.length) {
            selectionEnd++;
        }

        target.setSelectionRange(selectionStart, selectionEnd);
        return true;
    }

    // If the user hasn't selected anything, let's select their current parenthesis block or word
    if (!selectCurrentParenthesisBlock('<', '>') && !selectCurrentParenthesisBlock('(', ')')) {
        selectCurrentWord();
    }

    event.preventDefault();

    var closeCharacter = ')';
    var delta = 0.1;

    if (selectionStart > 0 && text[selectionStart - 1] == '<') {
        closeCharacter = '>';
        delta = 0.05;
    } else if (selectionStart == 0 || text[selectionStart - 1] != "(") {

        // do not include spaces at the end
        while (selectionEnd > selectionStart && text[selectionEnd - 1] == ' ') {
            selectionEnd -= 1;
        }
        if (selectionStart == selectionEnd) {
            return;
        }

        text = text.slice(0, selectionStart) + "(" + text.slice(selectionStart, selectionEnd) + ":1.0)" + text.slice(selectionEnd);

        selectionStart += 1;
        selectionEnd += 1;
    }

    var end = text.slice(selectionEnd + 1).indexOf(closeCharacter) + 1;
    var weight = parseFloat(text.slice(selectionEnd + 1, selectionEnd + 1 + end));
    if (isNaN(weight)) return;

    weight += isPlus ? delta : -delta;
    weight = parseFloat(weight.toPrecision(12));
    if (String(weight).length == 1) weight += ".0";

    if (closeCharacter == ')' && weight == 1) {
        var endParenPos = text.substring(selectionEnd).indexOf(')');
        text = text.slice(0, selectionStart - 1) + text.slice(selectionStart, selectionEnd) + text.slice(selectionEnd + endParenPos + 1);
        selectionStart--;
        selectionEnd--;
    } else {
        text = text.slice(0, selectionEnd + 1) + weight + text.slice(selectionEnd + end);
    }

    target.focus();
    target.value = text;
    target.selectionStart = selectionStart;
    target.selectionEnd = selectionEnd;

    updateInput(target);

}

addEventListener('keydown', (event) => {
    keyupEditAttention(event);
});
