import * as $ from 'jquery';
import * as CourseDetailsModel from 'js/models/settings/course_details';
import * as MainView from 'js/views/settings/main';
import 'froala-editor';

'use strict';
export default function SettingsFactory(detailsUrl, showMinGradeWarning, showCertificateAvailableDate, froalaEditorKey) {
    var model;
    // highlighting labels when fields are focused in
    $('form :input')
        .focus(function() {
            $('label[for="' + this.id + '"]').addClass('is-focused');
        })
        .blur(function() {
            $('label').removeClass('is-focused');
        });

    model = new CourseDetailsModel();
    model.urlRoot = detailsUrl;
    model.showCertificateAvailableDate = showCertificateAvailableDate;
    model.fetch({
        success: function(model) {
            var editor = new MainView({
                el: $('.settings-details'),
                model: model,
                showMinGradeWarning: showMinGradeWarning
            });
            editor.render();
        },
        reset: true
    });

    /* 모든 강의 소개 페이지를 변환했으니 이제는 필요없어 일단 제거.
    $.FroalaEditor.DefineIcon('convertOverview', {NAME: 'edit'});
    $.FroalaEditor.RegisterCommand('convertOverview', {
      title: '강의개요 변환',
      focus: false,
      undo: true,
      refreshAfterCallback: true,
      callback: function () {
        var classes = [ '.about', '.content_list', '.content_header', '.course-staff' ],
            converted = false,
            newline = '<p><br></p>',
            block;

        for (cl of classes) {
          block = $(cl);
          if (block.length > 0) {
            var inner = block[0].innerHTML;
            if (cl !== '.content_header' && cl !== '.course-staff') {
              inner += newline;
            }
            block.replaceWith(inner);
            converted = true;
          }
        }
        block = $('.teacher');
        if (block.length > 0) {
          $(newline).insertAfter('.teacher');
          converted = true;
        }

        if (converted) {
          this.undo.saveStep();
          this.events.focus();
        }
      }
    })
    */
   $.FroalaEditor.DefineIcon('dropdownStaff', {NAME: 'cog'});
   $.FroalaEditor.RegisterCommand('dropdownStaff', {
     title: 'Staff options',
     type: 'dropdown',
     focus: false,
     undo: false,
     refreshAfterCallback: true,
     options: {
       'init': '강의개요 초기화',
       'add': '운영진 추가',
       'remove': '운영진 삭제'
     },
     callback: function (cmd, val) {
       var node = document.getSelection().anchorNode;
       var selected = (node.nodeType === 3) ? node.parentNode : node;
       var teacher = $(selected).closest('.teacher');
       if (val === 'add') {
         if (teacher.length > 0) {
           $(document.getElementById('teacher-template').innerHTML).insertAfter(teacher);
         } else {
           this.html.insert($('#teacher-template').html())
         }
       } else if (val === 'remove' && teacher.length > 0) {
         // remove staff
         teacher.remove();
       } else if (val === 'init') {
         this.html.set(document.getElementById('course-overview-template').innerHTML);
       }
       this.undo.saveStep();
       this.events.focus();
     },
   });
   $('#course-overview').froalaEditor({
     key: froalaEditorKey,
     imageStyles: {
       'rounded-circle': 'Circle',
       'fr-rounded': 'Rounded',
       'fr-bordered': 'Bordered',
       'fr-shadow': 'Shadow',
     },
     toolbarButtons: [
       'fullscreen', 'bold', 'italic', 'underline', 'strikeThrough', 'subscript', 'superscript', '|',
       'fontFamily', 'fontSize', 'color', 'inlineClass', 'inlineStyle', 'paragraphStyle', 'lineHeight', '|', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'outdent', 'indent', 'quote', '|',
       'insertLink', 'insertImage', 'insertTable', '|',
       'emoticons', 'fontAwesome', 'specialCharacters', 'insertHR', 'selectAll', 'clearFormatting', '|',
       'help', 'html', '|',
       'undo', 'redo', '|',
       'dropdownStaff', // 일단 제거: 'convertOverview',
     ],
   });
};

export {SettingsFactory}
