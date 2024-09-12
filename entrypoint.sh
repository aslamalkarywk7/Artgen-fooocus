#!/bin/bash

ORIGINALDIR=/content/app
# استخدم DATADIR المحدد مسبقًا إذا كان محددًا
[[ x"${DATADIR}" == "x" ]] && DATADIR=/content/data

# إنشاء دليل دائم من الدليل الأصلي
function mklink () {
	mkdir -p $DATADIR/$1
	ln -s $DATADIR/$1 $ORIGINALDIR
}

# نسخ الملفات القديمة من استيراد الدليل
function import () {
	(test -d /import/$1 && cd /import/$1 && cp -Rpn . $DATADIR/$1/)
}

cd $ORIGINALDIR

# النماذج
mklink models
# نسخ الملفات الأصلية
(cd $ORIGINALDIR/models.org && cp -Rpn . $ORIGINALDIR/models/)
# استيراد الملفات القديمة
import models

# المخرجات
mklink outputs
# استيراد الملفات القديمة
import outputs

# بدء التطبيق
python launch.py $*
