function setPressedButton(event) {
    document.getElementById('pressed_button').value = event.currentTarget.value;
}

function addEvLisCampos() {
	const evts = ["invalid", "input"];

	const emailInput = document.getElementById("email");
	const pswdInput = document.getElementById("pswd");

	evts.forEach((e) => {
		pswdInput.addEventListener(e, () => {
			invMsg(pswdInput, "Preencha a senha.");
		});
		emailInput.addEventListener(e, () => {
			valEmail(emailInput);
		});
	});
}

document.addEventListener("DOMContentLoaded", () => {
	addEvLisCampos();
});
