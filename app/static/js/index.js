// index.js

// EVENT LISTENERS
document.getElementById("selectpicker").addEventListener("change",getContactInfo)


// FUNCTIONS
function getContactInfo() {
    var e = document.getElementById("selectpicker");
    var option = e.options[e.selectedIndex];
    
    //var attrs = option.attributes;
    
    villageID = $('option:selected', this).attr("data-member");
    
    var dataToSend = {
        villageID: villageID
    };
    fetch(`${window.origin}/getMemberContactInfo`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(dataToSend),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
    .then(function (response) {
        if (response.status != 200) {
            console.log(`Response status was not 200: ${response.status}`);
            return ;
        }
        response.json().then(function (data) {
            // Was the member found in the lightspeed database?
            if (data.hasOwnProperty('msg')){
                modalAlert('ERROR',data.msg)
                return
            }
            // Populate form
            document.getElementById('memberName').innerHTML = data.memberName
            document.getElementById('villageID').innerHTML = data.memberID
            document.getElementById('homePhone').innerHTML = data.homePhone
            document.getElementById('mobilePhone').innerHTML = data.mobilePhone
            document.getElementById('eMail').innerHTML = data.eMail   
        })
    })
}



function modalAlert(title,msg) {
	document.getElementById("modalTitle").innerHTML = title
	document.getElementById("modalBody").innerHTML= msg
	$('#myModalMsg').modal('show')
}

function closeModal() {
	$('#myModalMsg').modal('hide')
}

// END OF FUNCTIONS
