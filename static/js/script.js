document.addEventListener("DOMContentLoaded", function () {
	const alerts = document.querySelectorAll(".alert");

	alerts.forEach(function (alert) {
		window.setTimeout(function () {
			alert.style.transition = "opacity 0.4s ease";
			alert.style.opacity = "0";

			window.setTimeout(function () {
				alert.remove();
			}, 450);
		}, 3500);
	});
});
