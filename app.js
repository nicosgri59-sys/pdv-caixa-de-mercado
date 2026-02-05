const carrinho = document.getElementById("carrinho");
const resumo = document.getElementById("resumo");
const subtotalEl = document.getElementById("subtotal");
const descontosEl = document.getElementById("descontos");
const totalEl = document.getElementById("total");
const notaTotalEl = document.getElementById("nota-total");
const descontoInput = document.getElementById("desconto");
const recebidoInput = document.getElementById("recebido");
const trocoEl = document.getElementById("troco");
const dataEl = document.getElementById("data");

const itens = [];

const formatarMoeda = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(valor);

const atualizarResumo = () => {
  const subtotal = itens.reduce((acc, item) => acc + item.total, 0);
  const desconto = Number(descontoInput.value) || 0;
  const total = Math.max(subtotal - desconto, 0);
  const recebido = Number(recebidoInput.value) || 0;
  const troco = Math.max(recebido - total, 0);

  subtotalEl.textContent = formatarMoeda(subtotal);
  descontosEl.textContent = formatarMoeda(desconto);
  totalEl.textContent = formatarMoeda(total);
  notaTotalEl.textContent = formatarMoeda(total);
  trocoEl.textContent = formatarMoeda(troco);

  resumo.innerHTML = "";
  itens.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.quantidade}x ${item.nome} • ${formatarMoeda(item.total)}`;
    resumo.appendChild(li);
  });
};

const renderizarCarrinho = () => {
  carrinho.innerHTML = "";
  itens.forEach((item, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div>
        <strong>${item.nome}</strong><br />
        <small>${item.quantidade} x ${formatarMoeda(item.preco)}</small>
      </div>
      <span>${formatarMoeda(item.total)}</span>
      <button data-remove="${index}">Remover</button>
    `;
    carrinho.appendChild(li);
  });
  atualizarResumo();
};

const adicionarItem = (nome, preco, quantidade) => {
  const total = preco * quantidade;
  itens.push({ nome, preco, quantidade, total });
  renderizarCarrinho();
};

document.getElementById("produto-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const codigo = event.target.codigo.value.trim();
  const quantidade = Number(event.target.quantidade.value) || 1;
  if (!codigo) return;

  const preco = 4 + Math.random() * 20;
  adicionarItem(codigo, preco, quantidade);
  event.target.reset();
  event.target.quantidade.value = 1;
});

Array.from(document.querySelectorAll(".chips button")).forEach((button) => {
  button.addEventListener("click", () => {
    adicionarItem(button.dataset.produto, Number(button.dataset.preco), 1);
  });
});

carrinho.addEventListener("click", (event) => {
  if (event.target.matches("button[data-remove]")) {
    const index = Number(event.target.dataset.remove);
    itens.splice(index, 1);
    renderizarCarrinho();
  }
});

[descontoInput, recebidoInput].forEach((input) => {
  input.addEventListener("input", atualizarResumo);
});

document.getElementById("finalizar").addEventListener("click", () => {
  alert("Venda finalizada com sucesso!");
});

dataEl.textContent = new Date().toLocaleString("pt-BR");
renderizarCarrinho();
