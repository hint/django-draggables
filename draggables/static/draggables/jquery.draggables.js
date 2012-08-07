// body-class .change-list
// body-class .change-form

(function ($) {

    var exceptions = {
        UnsupportedMode: 1,
        NotImplemented: 2
    };

    var settings = {};

    var methods = {
        idListToSelector: function (ids) {
            return '#' + ids.join(', #');
        },

        changedCallbackChangeform: function (event, ui) {
            var elements;
            elements = $(methods.idListToSelector($(this).sortable('toArray')));
            for (var e = 0; e < elements.length; e++) {
                $('input.draggableAutoField', elements[e]).val(e+1);
                //console.log($('input.draggableAutoField', elements[e]), e+1);
            }
        },

        changedCallbackChangelist: function (event, ui) {
            $.post(
                './save_positions/',
                $(this).sortable('serialize'),
                function (data, textStatus, jqXHR) {
                    var timestamp = Math.round(new Date().getTime() / 1000);
                    $('<ul class="messagelist" id="draggables-' + timestamp + '" style="display: none;"><li class="info">' + gettext('New order saved successfully!') + '</li></ul>').insertAfter('.breadcrumbs').slideDown();
                    window.setTimeout(function () {
                        $('#draggables-' + timestamp).slideUp();
                    }, 3000);
                }
            );
        },

        getChangedCallback: function (mode) {
            if (mode == 'change-list') {
                return methods.changedCallbackChangelist;
            }
            if (mode == 'change-form') {
                return methods.changedCallbackChangeform;
            }
        },

        /**
         * This function should return string CSS selector
         * in order for serialization methods to work.
         *
         * @param wrapper
         * @param mode
         * @todo wrapper can be an array, support that!
         * 
         */
        getSortables: function (wrapper, mode) {
            var ids, unfiltered;
            if (mode == 'change-form') {
                unfiltered = $('tr, div.inline-related', wrapper);
                ids = [];
                for (var u = 0; u < unfiltered.length; u++) {
                    if($('.delete input', unfiltered[u]).length > 0) {
                        ids.push($(unfiltered[u]).attr('id'));
                    }
                }
                return methods.idListToSelector(ids);
            }
            if (mode == 'change-list') {
                return 'tr';
            }
        },

        changeListAppendIds: function (wrapper) {
            var rows, id;
            rows = $(methods.getSortables(wrapper, 'change-list'));
            for (var r = 0; r < rows.length; r++) {
                id = parseInt($('a:first', rows[r]).attr('href'));
                $(rows[r]).attr('id', 'order_' + id); // might not be standard - compliant
            }
        },

        getMode: function () {
            var mode;
            if ($('body.change-list').length > 0) {
                mode = 'change-list';
            } else if ($('body.change-form').length > 0) {
                mode = 'change-form';
            } else {
                throw exceptions.UnsupportedMode;
            }
            return mode;
        },

        getSortablesWrapper: function (mode) {
            var wrapper;
            if (mode == 'change-list') {
                wrapper = $('#result_list tbody');
            }
            if (mode == 'change-form') {
                // tabular inline
                if ($('.change-form .tabular').length > 0) {
                    wrapper = $('.change-form .tabular tbody');
                // otherwise considered stacked, since stacked has no
                // specific class in django admin
                } else {
                    wrapper = $('.inline-group');
                }
            }
            return wrapper;
        },

        makeSortables: function (mode) {
            var callback, items, wrapper;

            wrapper = methods.getSortablesWrapper(mode);
            callback = methods.getChangedCallback(mode);
            items = methods.getSortables(wrapper, mode);

            wrapper.sortable({
                axis: 'y',
                forcePlaceholderSize: 'true',
                items: items,
                update: callback
            });
            $(items).css('cursor', 'move');

            if (mode == 'change-list') {
                methods.changeListAppendIds(wrapper);
            }
        },

        init: function (options) {
            var mode;

            if (options) {
                $.extend(settings, options);
            }

            try {
                mode = methods.getMode();
                methods.makeSortables(mode);
            } catch (error) {
            }

            return this;
        }
    };

    $.fn.Draggables = function (method) {
        if (methods[method]) {
            return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return methods.init.apply(this, arguments);
        } else {
            $.error('Method ' + method + ' does not exist on django.jQuery.Draggables');
        }
    };

}(django.jQuery));

django.jQuery(function () {
    django.jQuery('body').Draggables();
});
