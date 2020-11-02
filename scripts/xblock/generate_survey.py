#-*- coding:utf-8 -*-

import sys
import csv
import io
import json

surveys = {
    'block-v1:POSTECH+MCU101+M2001+type@survey+block@0431db968b21406897047422f830be17': {
        'questions': [[u'enjoy', {u'img': u'', u'img_alt': u'', u'label': u'Q1. \uac15\uc88c\ub294 4\ucc28 \uc0b0\uc5c5\ud601\uba85 \uad00\ub828 \ubd84\uc57c\uc758 \uc9c1\ubb34\ub2a5\ub825\uc744 \uc2b5\ub4dd\ud560 \uc218 \uc788\ub294 \ub0b4\uc6a9\uc73c\ub85c \uad6c\uc131\ub418\uc5c8\ub2e4.'}], [u'recommend', {u'img': u'', u'img_alt': u'', u'label': u'Q2. \uac15\uc88c\uc758 \ub0b4\uc6a9\uc740 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uad6c\uc131\ub418\uc5b4 \uc788\ub2e4.'}], [u'learn', {u'img': u'', u'img_alt': u'', u'label': u'Q3. \uad50\uc218\uc790\ub294 \uac15\uc88c \ub0b4\uc6a9\uc5d0 \ud544\uc694\ud55c \ucda9\ubd84\ud55c \uc804\ubb38\uc9c0\uc2dd\uc744 \uac16\uace0 \uc788\ub2e4.'}], [u'1590025054894', {u'img': u'', u'img_alt': u'', u'label': u'Q4. \uad50\uc218\uc790\ub294 \uac15\uc758 \ub0b4\uc6a9\uc744 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uc804\ub2ec\ud558\uc600\ub2e4.'}], [u'1590025060989', {u'img': u'', u'img_alt': u'', u'label': u'Q5. \uac15\uc88c\uc5d0\uc11c \uc81c\uacf5\ud558\ub294 \ud559\uc2b5 \ud65c\ub3d9\uacfc \uc790\ub8cc\ub294 \ud559\uc2b5\uc5d0 \ub9ce\uc740 \ub3c4\uc6c0\uc774 \ub418\uc5c8\ub2e4.'}], [u'1590025067173', {u'img': u'', u'img_alt': u'', u'label': u'Q6. \uc628\ub77c\uc778 \uc911\uc2ec\uc758 \uac15\uc88c \uc6b4\uc601\uc73c\ub85c \ud559\uc2b5\uc7a5\uc18c\uc640 \uc2dc\uac04 \uc120\ud0dd\uc5d0 \uc788\uc5b4 \ub9cc\uc871\uc2a4\ub7ec\uc6e0\ub2e4.'}], [u'1590025072334', {u'img': u'', u'img_alt': u'', u'label': u'Q7. \ub9e4\uce58\uc5c5 \uc0ac\uc774\ud2b8\ub294 \uad50\uc721\uae30\uad00\uc815\ubcf4 \ubc0f \uc778\uc99d\ud3c9\uac00 \uc77c\uc815 \ub4f1\uc744 \ud655\uc778\ud558\ub294\ub370 \uc720\uc6a9\ud558\uc600\ub2e4.'}], [u'1590025076919', {u'img': u'', u'img_alt': u'', u'label': u'Q8. \uac15\uc88c\ub97c \uc218\uac15\ud55c \ubcf8 \uc0ac\uc774\ud2b8\ub294 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \ud559\uc2b5\ud558\ub294\ub370 \ud3b8\ub9ac\ud558\uc600\ub2e4.'}], [u'1590025082661', {u'img': u'', u'img_alt': u'', u'label': u'Q9. \ud5a5\ud6c4 \ub9e4\uce58\uc5c5 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \uc2f6\ub2e4.'}], [u'1590025086933', {u'img': u'', u'img_alt': u'', u'label': u'Q10. \ub098\ub294 \uc774 \uac15\uc88c\ub97c \uce5c\uad6c\ub098 \ub3d9\ub8cc\ub4e4\uc5d0\uac8c \ucd94\ucc9c\ud558\uaca0\ub2e4.'}]],
        'answers': [[u'Y', u'\uc804\ud600 \uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'N', u'\uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'M', u'\ubcf4\ud1b5\uc774\ub2e4'], [u'1590025018613', u'\uadf8\ub807\ub2e4'], [u'1590025022925', u'\ub9e4\uc6b0 \uadf8\ub807\ub2e4']],
    },
    'block-v1:POSTECH+MCU102+M2001+type@survey+block@3d9623cf97f24dbb8eec0b2a644a349b': {
        'questions': [[u'enjoy', {u'img_alt': u'', u'img': u'', u'label': u'Q1. \uac15\uc88c\ub294 4\ucc28 \uc0b0\uc5c5\ud601\uba85 \uad00\ub828 \ubd84\uc57c\uc758 \uc9c1\ubb34\ub2a5\ub825\uc744 \uc2b5\ub4dd\ud560 \uc218 \uc788\ub294 \ub0b4\uc6a9\uc73c\ub85c \uad6c\uc131\ub418\uc5c8\ub2e4.'}], [u'recommend', {u'img_alt': u'', u'img': u'', u'label': u'Q2. \uac15\uc88c\uc758 \ub0b4\uc6a9\uc740 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uad6c\uc131\ub418\uc5b4 \uc788\ub2e4.'}], [u'learn', {u'img_alt': u'', u'img': u'', u'label': u'Q3. \uad50\uc218\uc790\ub294 \uac15\uc88c \ub0b4\uc6a9\uc5d0 \ud544\uc694\ud55c \ucda9\ubd84\ud55c \uc804\ubb38\uc9c0\uc2dd\uc744 \uac16\uace0 \uc788\ub2e4.'}], [u'1590025169070', {u'img_alt': u'', u'img': u'', u'label': u'Q4. \uad50\uc218\uc790\ub294 \uac15\uc758 \ub0b4\uc6a9\uc744 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uc804\ub2ec\ud558\uc600\ub2e4.'}], [u'1590025173374', {u'img_alt': u'', u'img': u'', u'label': u'Q5. \uac15\uc88c\uc5d0\uc11c \uc81c\uacf5\ud558\ub294 \ud559\uc2b5 \ud65c\ub3d9\uacfc \uc790\ub8cc\ub294 \ud559\uc2b5\uc5d0 \ub9ce\uc740 \ub3c4\uc6c0\uc774 \ub418\uc5c8\ub2e4.'}], [u'1590025179349', {u'img_alt': u'', u'img': u'', u'label': u'Q6. \uc628\ub77c\uc778 \uc911\uc2ec\uc758 \uac15\uc88c \uc6b4\uc601\uc73c\ub85c \ud559\uc2b5\uc7a5\uc18c\uc640 \uc2dc\uac04 \uc120\ud0dd\uc5d0 \uc788\uc5b4 \ub9cc\uc871\uc2a4\ub7ec\uc6e0\ub2e4.'}], [u'1590025184135', {u'img_alt': u'', u'img': u'', u'label': u'Q7. \ub9e4\uce58\uc5c5 \uc0ac\uc774\ud2b8\ub294 \uad50\uc721\uae30\uad00\uc815\ubcf4 \ubc0f \uc778\uc99d\ud3c9\uac00 \uc77c\uc815 \ub4f1\uc744 \ud655\uc778\ud558\ub294\ub370 \uc720\uc6a9\ud558\uc600\ub2e4.'}], [u'1590025188213', {u'img_alt': u'', u'img': u'', u'label': u'Q8. \uac15\uc88c\ub97c \uc218\uac15\ud55c \ubcf8 \uc0ac\uc774\ud2b8\ub294 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \ud559\uc2b5\ud558\ub294\ub370 \ud3b8\ub9ac\ud558\uc600\ub2e4.'}], [u'1590025192909', {u'img_alt': u'', u'img': u'', u'label': u'Q9. \ud5a5\ud6c4 \ub9e4\uce58\uc5c5 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \uc2f6\ub2e4.'}], [u'1590025197166', {u'img_alt': u'', u'img': u'', u'label': u'Q10. \ub098\ub294 \uc774 \uac15\uc88c\ub97c \uce5c\uad6c\ub098 \ub3d9\ub8cc\ub4e4\uc5d0\uac8c \ucd94\ucc9c\ud558\uaca0\ub2e4.'}]],
        'answers': [[u'Y', u'\uc804\ud600 \uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'N', u'\uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'M', u'\ubcf4\ud1b5\uc774\ub2e4'], [u'1590025144477', u'\uadf8\ub807\ub2e4'], [u'1590025148252', u'\ub9e4\uc6b0 \uadf8\ub807\ub2e4']],
    },
    'block-v1:POSTECH+MCU103+M2001+type@survey+block@ad71501a0c36468f928ee54c9e374498': {
        'questions': [[u'enjoy', {u'img': u'', u'img_alt': u'', u'label': u'Q1. \uac15\uc88c\ub294 4\ucc28 \uc0b0\uc5c5\ud601\uba85 \uad00\ub828 \ubd84\uc57c\uc758 \uc9c1\ubb34\ub2a5\ub825\uc744 \uc2b5\ub4dd\ud560 \uc218 \uc788\ub294 \ub0b4\uc6a9\uc73c\ub85c \uad6c\uc131\ub418\uc5c8\ub2e4.'}], [u'recommend', {u'img': u'', u'img_alt': u'', u'label': u'Q2. \uac15\uc88c\uc758 \ub0b4\uc6a9\uc740 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uad6c\uc131\ub418\uc5b4 \uc788\ub2e4.'}], [u'learn', {u'img': u'', u'img_alt': u'', u'label': u'Q3. \uad50\uc218\uc790\ub294 \uac15\uc88c \ub0b4\uc6a9\uc5d0 \ud544\uc694\ud55c \ucda9\ubd84\ud55c \uc804\ubb38\uc9c0\uc2dd\uc744 \uac16\uace0 \uc788\ub2e4.'}], [u'1590025263405', {u'img': u'', u'img_alt': u'', u'label': u'Q4. \uad50\uc218\uc790\ub294 \uac15\uc758 \ub0b4\uc6a9\uc744 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uc804\ub2ec\ud558\uc600\ub2e4.'}], [u'1590025267534', {u'img': u'', u'img_alt': u'', u'label': u'Q5. \uac15\uc88c\uc5d0\uc11c \uc81c\uacf5\ud558\ub294 \ud559\uc2b5 \ud65c\ub3d9\uacfc \uc790\ub8cc\ub294 \ud559\uc2b5\uc5d0 \ub9ce\uc740 \ub3c4\uc6c0\uc774 \ub418\uc5c8\ub2e4.'}], [u'1590025274196', {u'img': u'', u'img_alt': u'', u'label': u'Q6. \uc628\ub77c\uc778 \uc911\uc2ec\uc758 \uac15\uc88c \uc6b4\uc601\uc73c\ub85c \ud559\uc2b5\uc7a5\uc18c\uc640 \uc2dc\uac04 \uc120\ud0dd\uc5d0 \uc788\uc5b4 \ub9cc\uc871\uc2a4\ub7ec\uc6e0\ub2e4.'}], [u'1590025278420', {u'img': u'', u'img_alt': u'', u'label': u'Q7. \ub9e4\uce58\uc5c5 \uc0ac\uc774\ud2b8\ub294 \uad50\uc721\uae30\uad00\uc815\ubcf4 \ubc0f \uc778\uc99d\ud3c9\uac00 \uc77c\uc815 \ub4f1\uc744 \ud655\uc778\ud558\ub294\ub370 \uc720\uc6a9\ud558\uc600\ub2e4.'}], [u'1590025283669', {u'img': u'', u'img_alt': u'', u'label': u'Q8. \uac15\uc88c\ub97c \uc218\uac15\ud55c \ubcf8 \uc0ac\uc774\ud2b8\ub294 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \ud559\uc2b5\ud558\ub294\ub370 \ud3b8\ub9ac\ud558\uc600\ub2e4.'}], [u'1590025287366', {u'img': u'', u'img_alt': u'', u'label': u'Q9. \ud5a5\ud6c4 \ub9e4\uce58\uc5c5 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \uc2f6\ub2e4.'}], [u'1590025292991', {u'img': u'', u'img_alt': u'', u'label': u'Q10. \ub098\ub294 \uc774 \uac15\uc88c\ub97c \uce5c\uad6c\ub098 \ub3d9\ub8cc\ub4e4\uc5d0\uac8c \ucd94\ucc9c\ud558\uaca0\ub2e4.'}]],
        'answers': [[u'Y', u'\uc804\ud600 \uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'N', u'\uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'M', u'\ubcf4\ud1b5\uc774\ub2e4'], [u'1590025243174', u'\uadf8\ub807\ub2e4'], [u'1590025246727', u'\ub9e4\uc6b0 \uadf8\ub807\ub2e4']],
    },
    'block-v1:POSTECH+MCU104+M2001+type@survey+block@f7090e3a5abf475ab8285586d12a1a66': {
        'questions': [[u'enjoy', {u'img': u'', u'img_alt': u'', u'label': u'Q1. \uac15\uc88c\ub294 4\ucc28 \uc0b0\uc5c5\ud601\uba85 \uad00\ub828 \ubd84\uc57c\uc758 \uc9c1\ubb34\ub2a5\ub825\uc744 \uc2b5\ub4dd\ud560 \uc218 \uc788\ub294 \ub0b4\uc6a9\uc73c\ub85c \uad6c\uc131\ub418\uc5c8\ub2e4.'}], [u'recommend', {u'img': u'', u'img_alt': u'', u'label': u'Q2. \uac15\uc88c\uc758 \ub0b4\uc6a9\uc740 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uad6c\uc131\ub418\uc5b4 \uc788\ub2e4.'}], [u'learn', {u'img': u'', u'img_alt': u'', u'label': u'Q3. \uad50\uc218\uc790\ub294 \uac15\uc88c \ub0b4\uc6a9\uc5d0 \ud544\uc694\ud55c \ucda9\ubd84\ud55c \uc804\ubb38\uc9c0\uc2dd\uc744 \uac16\uace0 \uc788\ub2e4.'}], [u'1590025381390', {u'img': u'', u'img_alt': u'', u'label': u'Q4. \uad50\uc218\uc790\ub294 \uac15\uc758 \ub0b4\uc6a9\uc744 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uc804\ub2ec\ud558\uc600\ub2e4.'}], [u'1590025385982', {u'img': u'', u'img_alt': u'', u'label': u'Q5. \uac15\uc88c\uc5d0\uc11c \uc81c\uacf5\ud558\ub294 \ud559\uc2b5 \ud65c\ub3d9\uacfc \uc790\ub8cc\ub294 \ud559\uc2b5\uc5d0 \ub9ce\uc740 \ub3c4\uc6c0\uc774 \ub418\uc5c8\ub2e4.'}], [u'1590025390270', {u'img': u'', u'img_alt': u'', u'label': u'Q6. \uc628\ub77c\uc778 \uc911\uc2ec\uc758 \uac15\uc88c \uc6b4\uc601\uc73c\ub85c \ud559\uc2b5\uc7a5\uc18c\uc640 \uc2dc\uac04 \uc120\ud0dd\uc5d0 \uc788\uc5b4 \ub9cc\uc871\uc2a4\ub7ec\uc6e0\ub2e4.'}], [u'1590025395294', {u'img': u'', u'img_alt': u'', u'label': u'Q7. \ub9e4\uce58\uc5c5 \uc0ac\uc774\ud2b8\ub294 \uad50\uc721\uae30\uad00\uc815\ubcf4 \ubc0f \uc778\uc99d\ud3c9\uac00 \uc77c\uc815 \ub4f1\uc744 \ud655\uc778\ud558\ub294\ub370 \uc720\uc6a9\ud558\uc600\ub2e4.'}], [u'1590025400037', {u'img': u'', u'img_alt': u'', u'label': u'Q8. \uac15\uc88c\ub97c \uc218\uac15\ud55c \ubcf8 \uc0ac\uc774\ud2b8\ub294 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \ud559\uc2b5\ud558\ub294\ub370 \ud3b8\ub9ac\ud558\uc600\ub2e4.'}], [u'1590025404332', {u'img': u'', u'img_alt': u'', u'label': u'Q9. \ud5a5\ud6c4 \ub9e4\uce58\uc5c5 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \uc2f6\ub2e4.'}], [u'1590025408086', {u'img': u'', u'img_alt': u'', u'label': u'Q10. \ub098\ub294 \uc774 \uac15\uc88c\ub97c \uce5c\uad6c\ub098 \ub3d9\ub8cc\ub4e4\uc5d0\uac8c \ucd94\ucc9c\ud558\uaca0\ub2e4.'}]],
        'answers': [[u'Y', u'\uc804\ud600 \uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'N', u'\uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'M', u'\ubcf4\ud1b5\uc774\ub2e4'], [u'1590025358885', u'\uadf8\ub807\ub2e4'], [u'1590025362261', u'\ub9e4\uc6b0 \uadf8\ub807\ub2e4']],
    },
    'block-v1:POSTECH+MCU105+M2001+type@survey+block@7c0510b0f1d84c08874fd34fab500ef6': {
        'questions': [[u'enjoy', {u'img_alt': u'', u'img': u'', u'label': u'Q1. \uac15\uc88c\ub294 4\ucc28 \uc0b0\uc5c5\ud601\uba85 \uad00\ub828 \ubd84\uc57c\uc758 \uc9c1\ubb34\ub2a5\ub825\uc744 \uc2b5\ub4dd\ud560 \uc218 \uc788\ub294 \ub0b4\uc6a9\uc73c\ub85c \uad6c\uc131\ub418\uc5c8\ub2e4.'}], [u'recommend', {u'img_alt': u'', u'img': u'', u'label': u'Q2. \uac15\uc88c\uc758 \ub0b4\uc6a9\uc740 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uad6c\uc131\ub418\uc5b4 \uc788\ub2e4.'}], [u'learn', {u'img_alt': u'', u'img': u'', u'label': u'Q3. \uad50\uc218\uc790\ub294 \uac15\uc88c \ub0b4\uc6a9\uc5d0 \ud544\uc694\ud55c \ucda9\ubd84\ud55c \uc804\ubb38\uc9c0\uc2dd\uc744 \uac16\uace0 \uc788\ub2e4.'}], [u'1590025472102', {u'img_alt': u'', u'img': u'', u'label': u'Q4. \uad50\uc218\uc790\ub294 \uac15\uc758 \ub0b4\uc6a9\uc744 \uc774\ud574\ud558\uae30 \uc27d\uac8c \uc804\ub2ec\ud558\uc600\ub2e4.'}], [u'1590025480086', {u'img_alt': u'', u'img': u'', u'label': u'Q5. \uac15\uc88c\uc5d0\uc11c \uc81c\uacf5\ud558\ub294 \ud559\uc2b5 \ud65c\ub3d9\uacfc \uc790\ub8cc\ub294 \ud559\uc2b5\uc5d0 \ub9ce\uc740 \ub3c4\uc6c0\uc774 \ub418\uc5c8\ub2e4.'}], [u'1590025486541', {u'img_alt': u'', u'img': u'', u'label': u'Q6. \uc628\ub77c\uc778 \uc911\uc2ec\uc758 \uac15\uc88c \uc6b4\uc601\uc73c\ub85c \ud559\uc2b5\uc7a5\uc18c\uc640 \uc2dc\uac04 \uc120\ud0dd\uc5d0 \uc788\uc5b4 \ub9cc\uc871\uc2a4\ub7ec\uc6e0\ub2e4.'}], [u'1590025493740', {u'img_alt': u'', u'img': u'', u'label': u'Q7. \ub9e4\uce58\uc5c5 \uc0ac\uc774\ud2b8\ub294 \uad50\uc721\uae30\uad00\uc815\ubcf4 \ubc0f \uc778\uc99d\ud3c9\uac00 \uc77c\uc815 \ub4f1\uc744 \ud655\uc778\ud558\ub294\ub370 \uc720\uc6a9\ud558\uc600\ub2e4.'}], [u'1590025498108', {u'img_alt': u'', u'img': u'', u'label': u'Q8. \uac15\uc88c\ub97c \uc218\uac15\ud55c \ubcf8 \uc0ac\uc774\ud2b8\ub294 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \ud559\uc2b5\ud558\ub294\ub370 \ud3b8\ub9ac\ud558\uc600\ub2e4.'}], [u'1590025502180', {u'img_alt': u'', u'img': u'', u'label': u'Q9. \ud5a5\ud6c4 \ub9e4\uce58\uc5c5 \uac15\uc88c\ub97c \uc218\uac15\ud558\uace0 \uc2f6\ub2e4.'}], [u'1590025506310', {u'img_alt': u'', u'img': u'', u'label': u'Q10. \ub098\ub294 \uc774 \uac15\uc88c\ub97c \uce5c\uad6c\ub098 \ub3d9\ub8cc\ub4e4\uc5d0\uac8c \ucd94\ucc9c\ud558\uaca0\ub2e4.'}]],
        'answers': [[u'Y', u'\uc804\ud600 \uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'N', u'\uadf8\ub807\uc9c0 \uc54a\ub2e4'], [u'M', u'\ubcf4\ud1b5\uc774\ub2e4'], [u'1590025452236', u'\uadf8\ub807\ub2e4'], [u'1590025455612', u'\ub9e4\uc6b0 \uadf8\ub807\ub2e4']]
    }
}

def generate_survey_report(filename):
    fr = io.open(filename, 'rt', encoding='utf-8')
    fw = io.open('new_' + filename, 'wt', encoding='utf-8')
    rd = csv.reader(fr)
    wr = csv.writer(fw)

    num = 0
    for line in rd:
        if num == 0:
            col_answer = line.index('답변')
            col_question = line.index('질문')
            col_key = line.index('block_key')
            col_state = line.index('state')
            wr.writerow(line)
        else:
            block_key = line[col_key]
            survey = surveys.get(block_key)
            state = json.loads(line[col_state])

            if survey:
                answers = {
                    key: value
                    for key, value in survey.get('answers')
                }
                questions = {
                    key: value.get('label')
                    for key, value in survey.get('questions')
                }
                state_answers = state.get('choices')
                line[col_question] = [label for label in questions.values()]
                if state_answers:
                    line[col_answer] = [answers.get(state_answers.get(key)) for key in questions.keys()]

            wr.writerow(line)
        num += 1

    fr.close()
    fw.close()
    print("%d rows is written in %s" % (num, 'new_' + filename))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Generate survey report from instructor's report csv file.")
        print("  Usage: %s <input.csv>" % sys.argv[0])
        print("")
        sys.exit(0)

    generate_survey_report(sys.argv[1])
