import flet as ft
import ipaddress


def main(pagina: ft.Page):
    pagina.title = "Calculadora de Sub-rede IP"
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.padding = 20
    pagina.scroll = "adaptive"

    def alternar_tema(e):
        if pagina.theme_mode == ft.ThemeMode.LIGHT:
            pagina.theme_mode = ft.ThemeMode.DARK
            botao_tema.icon = ft.Icons.WB_SUNNY_OUTLINED
        else:
            pagina.theme_mode = ft.ThemeMode.LIGHT
            botao_tema.icon = ft.Icons.NIGHTLIGHT_OUTLINED
        pagina.update()

    def calcular_subrede(e):
        try:
            endereco_ip = campo_ip.value.strip()
            mascara = campo_mascara.value.replace("/", "").strip()

            if not endereco_ip:
                raise ValueError("Por favor, insira um endereço IP válido.")

            rede = ipaddress.ip_network(f"{endereco_ip}/{mascara}", strict=False)

            primeiro_host_ip = rede.network_address + 1
            ultimo_host_ip = rede.broadcast_address - 1
            hosts_validos = rede.num_addresses - 2 if rede.prefixlen < 31 else 0

            texto_rede.value = f"Endereço de Rede: {rede.network_address}"
            texto_primeiro_host.value = f"Primeiro Endereço Válido: {primeiro_host_ip}"
            texto_ultimo_host.value = f"Último Endereço Válido: {ultimo_host_ip}"
            texto_broadcast.value = f"Endereço de Broadcast: {rede.broadcast_address}"
            texto_qtd_hosts.value = f"Quantidade de Hosts Possíveis: {hosts_validos}"

            lista_subredes.controls.clear()
            novo_prefixo = min(rede.prefixlen + 2, 30)
            subredes = list(rede.subnets(new_prefix=novo_prefixo))
            lista_subredes.controls.append(ft.Text(f"Sub-redes /{novo_prefixo}:"))
            for subrede in subredes:
                lista_subredes.controls.append(ft.Text(str(subrede)))

            pagina.snack_bar = ft.SnackBar(ft.Text("Cálculo realizado com sucesso!"), open=True)
            pagina.update()

        except Exception as ex:
            pagina.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(ex)}"), open=True)
            pagina.update()

    def copiar_resultados(e):
        resultados = "\n".join(
            [
                texto_rede.value,
                texto_primeiro_host.value,
                texto_ultimo_host.value,
                texto_broadcast.value,
                texto_qtd_hosts.value,
            ]
        )
        pagina.set_clipboard(resultados)
        pagina.snack_bar = ft.SnackBar(
            ft.Text("Resultados copiados para a área de transferência!"), open=True
        )
        pagina.update()

    def limpar_campos(e):
        campo_ip.value = ""
        campo_mascara.value = "/24"
        texto_rede.value = ""
        texto_primeiro_host.value = ""
        texto_ultimo_host.value = ""
        texto_broadcast.value = ""
        texto_qtd_hosts.value = ""
        lista_subredes.controls.clear()
        pagina.update()

    campo_ip = ft.TextField(
        label="Endereço IP",
        hint_text="Ex.: 192.168.10.0",
        width=300,
        autofocus=True,
    )

    campo_mascara = ft.Dropdown(
        label="Máscara de Sub-rede",
        options=[ft.dropdown.Option(f"/{i}") for i in range(8, 31)],
        value="/24",
        width=150,
    )

    botao_calcular = ft.ElevatedButton(
        "Calcular", icon=ft.Icons.CALCULATE, on_click=calcular_subrede
    )
    botao_limpar = ft.OutlinedButton(
        "Limpar", icon=ft.Icons.CLEAR, on_click=limpar_campos
    )
    botao_copiar = ft.FilledTonalButton(
        "Copiar Resultados", icon=ft.Icons.COPY, on_click=copiar_resultados
    )
    botao_tema = ft.IconButton(
        icon=ft.Icons.NIGHTLIGHT_OUTLINED,
        tooltip="Alternar Tema",
        on_click=alternar_tema,
    )

    texto_rede = ft.Text("", selectable=True)
    texto_primeiro_host = ft.Text("", selectable=True)
    texto_ultimo_host = ft.Text("", selectable=True)
    texto_broadcast = ft.Text("", selectable=True)
    texto_qtd_hosts = ft.Text("", selectable=True)

    lista_subredes = ft.Column(spacing=5)

    cartao_resultados = ft.Container(
        content=ft.Column(
            [
                texto_rede,
                texto_primeiro_host,
                texto_ultimo_host,
                texto_broadcast,
                texto_qtd_hosts,
            ],
            spacing=5,
        ),
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.BLUE,
    )

    pagina.add(
        ft.Row(
            [campo_ip, campo_mascara, botao_tema],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        ft.Row(
            [botao_calcular, botao_limpar, botao_copiar],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        ft.Divider(),
        cartao_resultados,
        ft.Divider(),
        ft.Text("Sub-redes Geradas:", weight=ft.FontWeight.BOLD),
        lista_subredes,
    )


ft.app(target=main, view=ft.WEB_BROWSER)
