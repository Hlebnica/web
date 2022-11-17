let buttonLoginDisabled = false;
let buttonEmailDisabled = false;
let buttonPasswordDisabled = false;

function btnDisabled(){ 
	return buttonEmailDisabled || buttonLoginDisabled || buttonPasswordDisabled;
}

$("#id_login").change(function(){
	let login =  $(this).val();
	$.ajax({
		type: "POST",
		headers: {'X-CSRFToken': csrf},
		url: "check_login/", 
		data: {"login": login },
		dataType: "json",
		success: function(data) {
			if (data.login_exists){
				if (!(document.body.contains(document.getElementById("exists")))){
					document.getElementById("btn submit").disabled = true;
					buttonLoginDisabled = true;
					regform.insertAdjacentHTML("afterbegin", "<p id='exists'>Login exists</p>");
				}
			}
			else {
				p = document.getElementById("exists");
				if (p)
					p.remove()
				buttonLoginDisabled = false;
				if (document.getElementById("btn submit").disabled && !btnDisabled())
					document.getElementById("btn submit").disabled = false;
			}
		}
	});
	return false;
});

$("#id_email").change(function(){
	let email = $(this).val();
	$.ajax({
		type: "POST",
		headers: {'X-CSRFToken': csrf},
		url: "check_email/", 
		data: {"email": email },
		dataType: "json",
		success: function(data) {
			if (data.email_correct){
				p = document.getElementById("correct");
				if (p)
					p.remove()
				buttonEmailDisabled = false;
				if (document.getElementById("btn submit").disabled && !btnDisabled())
					document.getElementById("btn submit").disabled = false;
			}
			else {
				if (!(document.body.contains(document.getElementById("correct")))){
					document.getElementById("btn submit").disabled = true;
					buttonEmailDisabled = true;
					regform.insertAdjacentHTML("afterbegin", "<p id='correct'>Email is incorrect</p>");
				}
			}
		}
	});
	return false;
});
$("#id_password").change(function(){
	let password = $(this).val();
	$.ajax({
		type: "POST",
		headers: {'X-CSRFToken': csrf},
		url: "check_password/", 
		data: {"password": password },
		dataType: "json",
		success: function(data) {
			if (data.password_correct){
				p = document.getElementById("password");
				if (p)
					p.remove()
				buttonPasswordDisabled = false;
				if (document.getElementById("btn submit").disabled && !btnDisabled())
					document.getElementById("btn submit").disabled = false;
			}
			else {
				if (!(document.body.contains(document.getElementById("password")))){
					document.getElementById("btn submit").disabled = true;
					buttonPasswordDisabled = true;
					regform.insertAdjacentHTML("afterbegin", "<p id='password'>Password need to be more than 6 symbols.</p>");
				}
			}
		}
	});
	return false;
});