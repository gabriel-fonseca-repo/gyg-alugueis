$(document).ready(function () {
	$("#cpf").mask("000.000.000-00", { placeholder: "000.000.000-00" });
	$("[name='celular']").mask("(00) 90000-0000", {
		placeholder: "(__) 9____-____",
		clearIfNotMatch: true,
	});
});

function calcularTotalPagar() {
	const final_aluguel = document.getElementById("final_aluguel").value;
	const inicio_aluguel = document.getElementById("inicio_aluguel").value;
	if (final_aluguel && inicio_aluguel) {
		const dt_fim = new Date(final_aluguel);
		const dt_ini = new Date(inicio_aluguel);
		var difference = dt_fim.getTime() - dt_ini.getTime();
		var days = Math.ceil(difference / (1000 * 3600 * 24));
		console.log(days);
		if (days < 1) {
			return;
		}
		const valor = days * Number(document.getElementById("custo_diario").value);
		document.getElementById("total_pagar").value = new Intl.NumberFormat("pt-BR", {
			style: "currency",
			currency: "BRL",
		}).format(valor);
	}
}

function validarCPF(cpf) {
	cpf = cpf.replace(/[^\d]+/g, "");
	if (cpf == "") return null;
	if (cpf.length != 11 || cpf == "00000000000" || cpf == "11111111111" || cpf == "22222222222" || cpf == "33333333333" || cpf == "44444444444" || cpf == "55555555555" || cpf == "66666666666" || cpf == "77777777777" || cpf == "88888888888" || cpf == "99999999999") return null;
	add = 0;
	for (i = 0; i < 9; i++) add += parseInt(cpf.charAt(i)) * (10 - i);
	rev = 11 - (add % 11);
	if (rev == 10 || rev == 11) rev = 0;
	if (rev != parseInt(cpf.charAt(9))) return null;
	add = 0;
	for (i = 0; i < 10; i++) add += parseInt(cpf.charAt(i)) * (11 - i);
	rev = 11 - (add % 11);
	if (rev == 10 || rev == 11) rev = 0;
	if (rev != parseInt(cpf.charAt(10))) return null;
	return cpf;
}
