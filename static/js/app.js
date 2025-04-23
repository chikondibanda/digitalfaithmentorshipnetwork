
$(document).ready(function(){

	// Login

	$("#loginForm").on('submit', function (event) {
		event.preventDefault();

		// Collect data

		let formData = {
			email: $("#email").val(),
			password: $("#password").val()
		};

		collectData(formData);

		// Send data

		$.ajax({
			url: 'http://localhost:8080/login',
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(formData),

			success: function (response) {
				console.log("API response:", response);
				alert("Login credentials submitted successfully: " + response.message);
			},

			error: function(xhr, status, error){
				console.error('API error:', error);
				alert('Error submitting data: ' + error)
			}
		});
	});

		// Login

	$("#registerForm").on('submit', function (event) {
		event.preventDefault();

		// Collect data

		let formData = {
			firstname: $('#firstname').val(),
			lastname: $('#lastname').val(),
			username: $('#username').val(),
			email: $("#email").val(),
			phone: $("#phone").val(),
			password: $("#password").val()
		};

		collectData(formData);

		// Send data

		$.ajax({
			url: 'http://localhost:8080/register',
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(formData),

			success: function (response) {
				console.log("API response:", response);
				alert(response);
			},

			error: function(xhr, status, error){
				console.error('API error:', error);
				alert('Error submutting data: ' + error)
			}
		});
	});

	function collectData(data) {
		console.log("Data received" + JSON.stringify(data));
	}


});