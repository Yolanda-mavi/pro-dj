function message_error(obj){
    var html = "<ul style='text-align: left;'>"

    Object.entries(obj).forEach(([key, value]) => {
        html +="<li>"+key+":"+ value+"</li> "
      //console.log(`${clave}: ${valor}`);
    });
    html +="</ul>"
     alert(html);
}