//signup.html
function imgPreview(fileDom){
    //判断是否支持FileReader
    if (window.FileReader) {
        var reader = new FileReader();
    } else {
        alert("您的设备不支持图片预览功能，如需该功能请升级您的设备！");
    }

    //获取文件
    var file = fileDom.files[0];
    var imageType = /^image\//;
    //是否是图片
    if (!imageType.test(file.type)) {
        alert("请选择图片！");
        return;
    }
    //读取完成,FileReader.onload()文件读取完后触发
    reader.onload = function(e) {
        //获取图片dom
        var img = document.getElementById("preview");
        //图片路径设置为读取的图片
        img.src = e.target.result;
    };
    //读取文件，然后触发onload
    reader.readAsDataURL(file);
}

//home.html

function edit(id) {
    var num = id.split('_')[1];
    var str = "#out_" + num + " input";
    $(str).removeAttr('readonly');
    $(str).addClass('editable');
    var str2 = "#out_" + num + " textarea";
    $(str2).removeAttr('readonly');
    $(str2).addClass('editable');

    document.getElementById("ctype_"+num).disabled=false;
    document.getElementById("cgender_"+num).disabled=false;
    $('#ctype_'+num).removeClass('displaynone');
    $('#type_input_'+num).addClass('displaynone');

    str_out = "#out_"+num;
    $(str_out).animate({ height: "391px" }, 200, "swing", function () {
        $("#cedit_" + num).addClass('displaynone');
        $("#out_"+num+" .buttonselect").removeClass('displaynone')
    });

    var num = id.split('_')[1];
    var str = "#ctype_" + num +" option:selected";
    var value = $(str).val();
    var str2 = "#newtype_input_"+num;
    if (value == "new" & $(str2).hasClass('displaynone')) {
        $(str2).removeClass('displaynone');
    } else {
        $(str2).addClass('displaynone');
    }
}

function cancel(id) {
    var num = id.split('_')[1];
    var str = "#out_" + num + " input";
    $(str).attr('readonly', 'readonly');
    $(str).removeClass('editable');
    var str2 = "#out_" + num + " textarea";
    $(str2).attr('readonly', 'readonly');
    $(str2).removeClass('editable');

    document.getElementById("ctype_"+num).disabled=true;
    document.getElementById("cgender_"+num).disabled=true;
    $('#ctype_'+num).addClass('displaynone');
    $('#type_input_'+num).removeClass('displaynone');

    if($('#newtype_input_'+num).hasClass('displaynone')==false){
        $('#newtype_input_'+num).addClass('displaynone')
    }

    str_out = "#out_"+num;
    $(str_out).animate({ height: "361px" }, 200, "swing", function () {
        $("#cedit_" + num).removeClass('displaynone');
        $("#out_"+num+" .buttonselect").addClass('displaynone')

    });
}

function add_contact() {
    $('#add_contact').addClass('displaynone');
    $('#add_contact_form').removeClass('displaynone');
}
function addtype() {
    var value = $('#type_select option:selected').val();
    if (value == "new") {
        $('#newtype_input').removeClass('displaynone');
    } else {
        $('#newtype_input').addClass('displaynone');
    }
}

function addtype_id(id) {
    var num = id.split('_')[1];
    var str = "#ctype_" + num +" option:selected";
    var value = $(str).val();
    var str2 = "#newtype_input_"+num;
    if (value == "new") {
        $(str2).removeClass('displaynone');
    } else {
        $(str2).addClass('displaynone');
    }
}



