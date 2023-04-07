function addEvLisCampos() {
	const evts = ["invalid", "input"];

	const nomeInput = document.getElementById("nome");
	const emailInput = document.getElementById("email");
	const pswdInput = document.getElementById("pswd");

	evts.forEach((e) => {
		nomeInput.addEventListener(e, () => {
			invMsg(nomeInput, "Preencha seu nome.");
		});
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
