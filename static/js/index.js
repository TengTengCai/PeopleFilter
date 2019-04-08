$(document).ready(function() {
    var table = $('#example').DataTable( {
        "ajax": "/people/person_time/",
        "columns": [
            { "data": "id" },
            { "data": "name" },
            { "data": "id_num" },
            { "data": "sex" },
            { "data": "birthday" },
            { "data": "age" },
        ]
    } );
    $('#age_from').on('submit', function (e) {
        e.preventDefault()
    });
    table.on('xhr.dt', function (e, settings, json, xhr ) {
        if (json.in_total !== undefined){
            var min_age = $('#input_min_age').val();
            var max_age = $('#input_max_age').val();
            var html_str = '年龄在'+min_age+'-'+max_age+'岁占'+json.in_total*100
                +'% 其他占'+(1-json.in_total)*100+'%';
            $('#total_p').html(html_str)
        }
        // console.log(json.in_total)
    });

    // table.ajax.url( 'newData.json' ).load();
    $('#query_current').on('click', function (e) {
        e.preventDefault();
        var upload_time = $('#select_uploda_time').val();
        var current_time = $('#input_current_time').val();
        var sex = $('#select_sex').val();
        console.log(current_time);
        table.ajax.url('/people/person_time/' +
            '?upload_time='+upload_time+
            '&current_time='+current_time+
            '&sex='+sex).load();
    });

    $('#query_age').on('click', function (e) {
        e.preventDefault();
        var upload_time = $('#select_uploda_time').val();
        var min_age = $('#input_min_age').val();
        var max_age = $('#input_max_age').val();
        var current_time = $('#input_current_time').val();
        var sex = $('#select_sex').val();
        console.log(min_age,max_age);
        if (parseInt(min_age) < parseInt(max_age)){
            table.ajax.url('/people/person_age/' +
                '?upload_time='+upload_time+
                '&min_age='+min_age+
                '&max_age='+max_age+
                '&sex='+sex+
                '&current_time='+current_time).load();
        } else {
            alert('输入有误，最小年龄不得大于最大年龄')
        }
    });
    $('#button_output').on('click', function (e) {
        e.preventDefault();
        window.open('/people/download/');
    });
    L2Dwidget.on('*', (name) => {
        console.log('%c EVENT ' + '%c -> ' + name, 'background: #222; color: yellow', 'background: #fff; color: #000')
        }).init({
            dialog: {
                enable: true,
                hitokoto: true
            }
        });
} );
