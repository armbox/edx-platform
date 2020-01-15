import * as $ from 'jquery';
import * as CourseDetailsModel from 'js/models/settings/course_details';
import * as MainView from 'js/views/settings/main';

'use strict';
export default function SettingsFactory(detailsUrl, showMinGradeWarning, showCertificateAvailableDate) {
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
};

export { SettingsFactory };
