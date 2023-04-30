const modal_carro = document.getElementById("modal_carro");
if (modal_carro) {
	modal_carro.addEventListener("show.bs.modal", (event) => {
		const button = event.relatedTarget;
		if (button.getAttribute("data-bs-is-edicao")) {
			const id = button.getAttribute("data-bs-id");
			const modelo = button.getAttribute("data-bs-modelo");
			const marca = button.getAttribute("data-bs-marca");
			const placa = button.getAttribute("data-bs-placa");
			const descricao = button.getAttribute("data-bs-descricao");
			const descricao_imagem = button.getAttribute("data-bs-descricao_imagem");
			const url_imagem = button.getAttribute("data-bs-url_imagem");
			const capacidade_pessoas = button.getAttribute("data-bs-capacidade_pessoas");
			const custo_diario = button.getAttribute("data-bs-custo_diario");

			const modalTitle = modal_carro.querySelector(".modal-title");
			modalTitle.textContent = `Editando o carro ${modelo} - ${placa}`;

			modal_carro.querySelector('[name="id"]').value = id;
			modal_carro.querySelector('[name="modelo"]').value = modelo;
			modal_carro.querySelector('[name="marca"]').value = marca;
			modal_carro.querySelector('[name="placa"]').value = placa;
			modal_carro.querySelector('[name="descricao"]').value = descricao;
			modal_carro.querySelector('[name="descricao_imagem"]').value = descricao_imagem;
			modal_carro.querySelector('[name="url_imagem"]').value = url_imagem;
			modal_carro.querySelector('[name="capacidade_pessoas"]').value = capacidade_pessoas;
			modal_carro.querySelector('[name="custo_diario"]').value = custo_diario;
		} else {
			const modalTitle = modal_carro.querySelector(".modal-title");
			modalTitle.textContent = `Cadastrando novo carro`;
			const inputs = modal_carro.querySelectorAll(".modal-body input");
			inputs.forEach((input) => {
				input.value = "";
			});
		}
	});
}
