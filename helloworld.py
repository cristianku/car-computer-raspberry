from piui import DemoPiUi
ui = DemoPiUi()
page = ui.new_ui_page(title="Hello")
title = page.add_textbox("Hello, world!")