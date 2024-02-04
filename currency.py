import flet as ft
import requests


class ExchangeApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        url = 'https://api.exchangerate-api.com/v4/latest/RUB'
        self.currency_data = requests.get(url).json()['rates']

    def build(self):
        self.amount = ft.TextField(value="100", width=275)
        self.currencies = ft.Column()
        currencies = ["BYN", "EUR", "KZT", "RUB", "UAH", "USD", "BRL", "TRY", "PLN"]

        for currency in currencies:
            self.currencies.controls.append(Currency(currency))
        return ft.Column(
            controls=[
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.amount,
                        ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=self.refresh),
                    ],
                ),
                self.currencies,
            ],
        )

    def refresh(self, e):
        for currency in self.currencies.controls:
            currency.currency_input.value = round(
                self.currency_data[currency.currency_name] * int(self.amount.value), 2
            )
            currency.update()
        self.update()


class Currency(ft.UserControl):
    def __init__(self, currency_name):
        super().__init__()
        self.currency_name = currency_name

    def copy(self, e):
        get_text = self.currency_input.value
        self.page.set_clipboard(get_text)
        self.update()

    def build(self):
        self.currency_name_field = ft.Text(value=self.currency_name, text_align=ft.TextAlign.RIGHT, width=100)
        self.currency_input = ft.TextField(value='0', text_align=ft.TextAlign.RIGHT, width=100)
        self.copy_button = ft.IconButton(icon=ft.icons.CONTENT_COPY, on_click=self.copy)
        self.display_view = ft.Row(
            controls=[
                self.currency_name_field,
                self.currency_input,
                self.copy_button
            ],
        )
        return self.display_view


def main(page: ft.Page):
    page.title = "Exchange App"
    page.window_width = 400
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    exchange = ExchangeApp()

    page.add(exchange)


ft.app(target=main)
