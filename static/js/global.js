showLoadingDialog();

function showLoadingDialog() {
	const loadingDialog = document.getElementById("loading");
	loadingDialog.showModal();
}

function hideLoadingDialog() {
	const loadingDialog = document.getElementById("loading");
	loadingDialog.close(null);
}

function red(endpoint) {
	window.location.href = endpoint;
}

function invMsg(element, msg) {
	if (!element.value) {
		element.setCustomValidity(msg);
	} else {
		element.setCustomValidity("");
	}
}

function valEmail(email) {
	if (email.value == "") {
		email.setCustomValidity("Preencha o email.");
	} else if (email.validity.typeMismatch) {
		email.setCustomValidity("Preencha um email válido.");
	} else {
		email.setCustomValidity("");
	}
	return true;
}

function formatarDinheiro(valor) {
	return new Intl.NumberFormat("pt-BR", {
		style: "currency",
		currency: "BRL",
	}).format(valor);
}
