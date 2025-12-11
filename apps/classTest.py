import marimo

__generated_with = "0.18.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    # Definition der Klassen
    class Rechteck:
        def __init__(self, x=0, y=0, breite="2 cm", höhe="2 cm", farbe="white"):
            self.x = x
            self.y = y
            self.Breite = breite
            self.Höhe = höhe
            self.Füllfarbe = farbe
            self.Linienstärke = "1 mm"

        def bewegen(self, richtung: str):
            distanz = 20
            if richtung == "LINKS": self.x -= distanz
            elif richtung == "RECHTS": self.x += distanz
            elif richtung == "OBEN": self.y -= distanz
            elif richtung == "UNTEN": self.y += distanz

        def anmalen(self, neue_farbe: str):
            self.Füllfarbe = neue_farbe

        def _scale(self, factor):
            def scale_val(s):
                try: return f"{float(str(s).split(' ')[0]) * factor:.1f} px"
                except: return s
            self.Breite = scale_val(self.Breite)
            self.Höhe = scale_val(self.Höhe)

        def vergrößern(self):
            self._scale(1.1)

        def verkleinern(self):
            self._scale(1/1.1)

    class Kreis:
        def __init__(self, x=0, y=0, radius="1.5 cm", farbe="white"):
            self.x = x
            self.y = y
            self.Radius = radius
            self.Füllfarbe = farbe
            self.Linienstärke = "1 mm"

        def bewegen(self, richtung: str):
            distanz = 20
            if richtung == "LINKS": self.x -= distanz
            elif richtung == "RECHTS": self.x += distanz
            elif richtung == "OBEN": self.y -= distanz
            elif richtung == "UNTEN": self.y += distanz

        def anmalen(self, neue_farbe: str):
            self.Füllfarbe = neue_farbe

        def _scale(self, factor):
            def scale_val(s):
                try: return f"{float(str(s).split(' ')[0]) * factor:.1f} px"
                except: return s
            self.Radius = scale_val(self.Radius)

        def vergrößern(self):
            self._scale(1.1)

        def verkleinern(self):
            self._scale(1/1.1)

    # State
    initial_objects = {
        "Tisch": Rechteck(x=50, y=50, breite="120 px", höhe="80 px", farbe="#e0e0e0"),
        "Schrank": Rechteck(x=200, y=50, breite="60 px", höhe="150 px", farbe="#8d6e63"),
        "Stuhl1": Kreis(x=110, y=140, radius="20 px", farbe="#bcaaa4"),
        "Stuhl2": Kreis(x=110, y=10, radius="20 px", farbe="#bcaaa4"),
        "Pflanze": Kreis(x=350, y=300, radius="25 px", farbe="#a5d6a7")
    }

    get_objects, set_objects = mo.state(initial_objects)
    get_log, set_log = mo.state(["Willkommen!"])
    get_selection, set_selection = mo.state(list(initial_objects.keys())[0] if initial_objects else "(keine)")
    return (
        Kreis,
        Rechteck,
        get_log,
        get_objects,
        get_selection,
        set_log,
        set_objects,
        set_selection,
    )


@app.cell
def _(get_objects, get_selection, mo, set_selection):
    # Selectors Cell (Re-runs when objects change)
    obj_names = sorted(list(get_objects().keys()))
    current_sel = get_selection()

    # Validierung: Falls selektiertes Objekt gelöscht wurde, nimm das erste verfügbare
    if current_sel not in obj_names and obj_names:
        current_sel = obj_names[0]
        # Wir müssen hier nicht set_selection aufrufen, das Value-Argument reicht für das UI

    obj_selector = mo.ui.dropdown(
        options=obj_names if obj_names else ["(keine)"],
        value=current_sel if current_sel in obj_names else (obj_names[0] if obj_names else "(keine)"),
        label="Objekt",
        on_change=set_selection # Update state on manual change
    )

    # Class Selector for creation
    class_select = mo.ui.dropdown(options=["Rechteck", "Kreis"], value="Rechteck", label="Klasse")
    return class_select, obj_selector


@app.cell
def _(class_select, mo):
    # Creation Inputs Cell (Re-runs when class selection changes)
    selected_class = class_select.value

    # Define inputs conditionally
    input_width = mo.ui.text(value="80 px", label="Breite")
    input_height = mo.ui.text(value="80 px", label="Höhe")
    input_radius = mo.ui.text(value="40 px", label="Radius")
    new_name_input = mo.ui.text(label="Name", value="")

    if selected_class == "Rechteck":
        dim_inputs = mo.hstack([input_width, input_height])
    else:
        dim_inputs = input_radius
    return (
        dim_inputs,
        input_height,
        input_radius,
        input_width,
        new_name_input,
        selected_class,
    )


@app.cell
def _(
    Kreis,
    Rechteck,
    class_select,
    dim_inputs,
    get_log,
    get_objects,
    input_height,
    input_radius,
    input_width,
    mo,
    new_name_input,
    obj_selector,
    selected_class,
    set_log,
    set_objects,
    set_selection,
):
    # Logic & Actions Cell

    def append_log(msg):
        l = get_log()
        l.append(msg)
        set_log(list(l))

    def create_object(_):
        name = new_name_input.value
        cls_name = class_select.value
        if not name: return

        objs = get_objects()
        if name in objs: return

        import random
        rx, ry = random.randint(50, 400), random.randint(50, 300)

        if cls_name == "Rechteck":
            new_obj = Rechteck(x=rx, y=ry, breite=input_width.value, höhe=input_height.value, farbe="white")
        else:
            new_obj = Kreis(x=rx, y=ry, radius=input_radius.value, farbe="white")

        objs[name] = new_obj
        set_objects(dict(objs))
        set_selection(name) # Automatisch neu erstelltes Objekt auswählen
        append_log(f"{name} = {cls_name}() erstellt.")

    create_btn = mo.ui.button(label="Erstellen", on_click=create_object)

    def delete_selected(_):
        name = obj_selector.value
        if name == "(keine)": return
        objs = get_objects()
        if name in objs:
            del objs[name]
            set_objects(dict(objs))
            # Selektion wird im nächsten Render der Dropdown-Zelle korrigiert
            append_log(f"del {name}")

    delete_btn = mo.ui.button(label="🗑️ Löschen", on_click=delete_selected)

    def move(direction):
        name = obj_selector.value
        if name == "(keine)": return
        objs = get_objects()
        if name in objs:
            objs[name].bewegen(direction)
            set_objects(dict(objs))
            append_log(f"{name}.bewegen('{direction}')")

    def paint(color_name, hex_code):
        name = obj_selector.value
        if name == "(keine)": return
        objs = get_objects()
        if name in objs:
            objs[name].anmalen(hex_code)
            set_objects(dict(objs))
            append_log(f"{name}.anmalen('{color_name}')")

    btn_l = mo.ui.button(label="⬅️", on_click=lambda _: move("LINKS"))
    btn_r = mo.ui.button(label="➡️", on_click=lambda _: move("RECHTS"))
    btn_u = mo.ui.button(label="⬆️", on_click=lambda _: move("OBEN"))
    btn_d = mo.ui.button(label="⬇️", on_click=lambda _: move("UNTEN"))

    btn_scale_up = mo.ui.button(label="➕ vergrößern()", on_click=lambda _: scale(1.1, "vergrößern"))
    btn_scale_down = mo.ui.button(label="➖ verkleinern()", on_click=lambda _: scale(1/1.1, "verkleinern"))

    def scale(factor, name_log):
        name = obj_selector.value
        if name == "(keine)": return
        objs = get_objects()
        if name in objs:
            if name_log == "vergrößern":
                objs[name].vergrößern()
            else:
                objs[name].verkleinern()
            set_objects(dict(objs))
            append_log(f"{name}.{name_log}()")

    colors = [
        ("🔴 Rot", "#ff9999"), 
        ("🟢 Grün", "#99ff99"), 
        ("🔵 Blau", "#99ccff"), 
        ("🟡 Gelb", "#ffff99"), 
        ("🟣 Lila", "#e6ccff"),
        ("🟤 Braun", "#8d6e63")
    ]
    color_btns = [mo.ui.button(label=n, on_click=lambda _, c=c, n=n: paint(n, c)) for n, c in colors]

    # Layouts

    # Intro / Help Text
    intro_text = mo.md("""
    ## 🎓 Objekte und Klassen

    In der Informatik modellieren wir Ausschnitte der echten Welt. Wir unterscheiden dabei zwischen dem **Bauplan (Klasse)** und dem **konkreten Ding (Objekt)**.

    ### 1. Natur 🐕
    *   **Klasse `Hund`:** Der allgemeine Bauplan. Jeder Hund hat einen *Namen* und eine *Rasse* und kann *bellen*.
    *   **Objekt `Bello`:** Ein konkreter Dackel. Er hat den Namen "Bello" und bellt gerade jetzt.

    ### 2. Technik 🚲
    *   **Klasse `Fahrzeug`:** Definiert, dass Fahrzeuge *Räder* haben und *motorisiert* sein können.
    *   **Objekt `meinFahrrad`:** Ein konkretes Fahrzeug mit *2 Rädern* und *ohne Motor*.

    ### 3. Grafikobjekte 🎨
    Hier ist die Klasse `RECHTECK` der Bauplan. Das Objekt `Tisch` ist das konkrete Rechteck, das du siehst.

    ### Fachbegriffe im Vergleich
    | Begriff | Erklärung | Natur | Technik | Grafik |
    | :--- | :--- | :--- | :--- | :--- |
    | **Klasse** | Der Bauplan | `Hund` | `Fahrzeug` | `Rechteck` |
    | **Objekt** | Konkretes Ding | `Bello` | `meinFahrrad` | `Tisch` |
    | **Attribut** | Eigenschaft | `Rasse` | `RäderZahl` | `Füllfarbe` |
    | **Wert** | Zustand | `"Dackel"` | `2` | `"#e0e0e0"` |
    | **Methode** | Fähigkeit | `bellen()` | `fahren()` | `anmalen(...)` |

    ### Die Punktnotation
    Wir steuern Objekte mit der Schreibweise `Objektname.Anweisung`:
    *   `Bello.bellen()`
    *   `meinFahrrad.fahren()`
    *   `Tisch.anmalen("rot")`

    ---
    **Aufgaben:** 
    1. **Analysieren:** Prüfe die **Objektkarten**. 
    2. **Modellieren:** Erstelle neue Objekte. 
    3. **Gestalten:** Verändere sie mit den Buttons!
    """)

    # 1. Creation Panel (Moved to top area)
    # We wrap the content in a styled div manually because vstack doesn't accept style
    creation_content = mo.vstack([
        mo.md("#### Neues Objekt"),
        mo.hstack([new_name_input, class_select], gap=2),
        mo.md(f"*Eigenschaften für {selected_class}:*"),
        dim_inputs,
        mo.hstack([create_btn], justify="start")
    ])

    creation_panel = mo.Html(f"""
    <div style="border: 1px solid #ccc; padding: 10px; border-radius: 8px; background: #f8f8f8; display: inline-block; min-width: 250px;">
        {creation_content}
    </div>
    """)

    # 2. Control Panel (Bottom area)
    control_panel = mo.vstack([
        mo.md("**Objektwahl**"),
        mo.hstack([obj_selector, delete_btn], justify="start"),
        mo.md("**Methoden**"),
        mo.md("_bewegen(...)_"),
        mo.vstack([
            mo.hstack([btn_u], justify="center"), 
            mo.hstack([btn_l, btn_d, btn_r], justify="center")
        ], align="center"),
        mo.md("_anmalen(...)_"),
        mo.hstack(color_btns, wrap=True, justify="start"),
        mo.hstack([btn_scale_up, btn_scale_down], justify="start")
    ], align="start")
    return control_panel, creation_panel, intro_text


@app.cell
def _(
    Kreis,
    Rechteck,
    control_panel,
    creation_panel,
    get_log,
    get_objects,
    intro_text,
    mo,
    obj_selector,
):
    # Visualization Only
    objects_for_display = get_objects()
    selected_name = obj_selector.value if obj_selector.value != "(keine)" else None
    log_entries = get_log()

    def render_class_card(cls):
        class_name = cls.__name__.upper()
        dummy = cls()
        attributes = [k for k in dummy.__dict__.keys() if not k.startswith("_")]
        methods = [k for k in cls.__dict__.keys() if not k.startswith("_") and callable(getattr(cls, k))]

        attr_html = "".join([f"<div style='font-family: monospace;'>{a}</div>" for a in attributes])
        meth_html = "".join([f"<div style='font-family: monospace;'>{m}(...)</div>" for m in methods])

        return mo.Html(f"""
        <div style='border: 2px solid #333; background-color: #f0f0f0; width: 220px; padding: 10px; margin: 5px; font-family: sans-serif; box-shadow: 3px 3px 5px rgba(0,0,0,0.1);'>
            <div style='font-weight: bold; text-align: center; border-bottom: 1px solid #999; margin-bottom: 5px; padding-bottom: 5px;'>{class_name}</div>
            <div style='text-align: left;'>{attr_html}</div>
            <div style='border-top: 1px solid #999; margin-top: 5px; padding-top: 5px; text-align: left;'>{meth_html}</div>
        </div>""")

    def render_canvas(objects, selected):
        def parse_val(s):
            s = str(s).lower().replace(",", ".")
            if "cm" in s: return float(s.replace("cm", "").strip()) * 30
            if "px" in s: return float(s.replace("px", "").strip())
            try: return float(s)
            except: return 40

        svg_elements = ""
        for name, obj in objects.items():
            is_kreis = hasattr(obj, "Radius")
            fill = getattr(obj, "Füllfarbe", "white")
            stroke_w = "4" if name == selected else "2"
            x, y = obj.x, obj.y

            if is_kreis:
                r = parse_val(getattr(obj, "Radius", "20 px"))
                svg_elements += f'<g transform="translate({x},{y})"><circle r="{r}" fill="{fill}" stroke="black" stroke-width="{stroke_w}"/><text x="0" y="0" font-family="sans-serif" font-size="12" text-anchor="middle" alignment-baseline="middle" fill="#333">{name}</text></g>'
            else:
                w = parse_val(getattr(obj, "Breite", "50 px"))
                h = parse_val(getattr(obj, "Höhe", "50 px"))
                svg_elements += f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" fill="{fill}" stroke="black" stroke-width="{stroke_w}" rx="5" ry="5"/><text x="{w/2}" y="{h/2}" font-family="sans-serif" font-size="12" text-anchor="middle" alignment-baseline="middle" fill="#333">{name}</text></g>'

        return mo.Html(f"""
        <svg width="500" height="400" style="border: 2px solid #333; background-color: #fafafa; border-radius: 4px;">
            <defs><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ddd" stroke-width="1"/></pattern></defs>
            <rect width="100%" height="100%" fill="url(#grid)"/>
            {svg_elements}
        </svg>""")

    # Object cards
    object_cards = []
    for name, obj in sorted(objects_for_display.items()):
        cls_name = type(obj).__name__.upper()
        attrs = obj.__dict__
        attr_lines = "<br>".join([f"<code>{k}</code> = <code>{v}</code>" for k, v in attrs.items()])
        border_w = "4px" if name == selected_name else "2px"

        card_html = mo.Html(f"""
        <div style="border: {border_w} solid #0066cc; border-radius: 12px; background-color: #e6f2ff; padding: 10px; min-width: 180px; margin: 5px;">
            <div style="font-weight: bold; text-align: center; color: #0066cc;">{name}: {cls_name}</div>
            <div style="font-size: 0.85em; margin-top: 5px;">{attr_lines}</div>
        </div>""")
        object_cards.append(card_html)

    # Sections

    # Top Section: Classes involved
    # Top Section: Classes involved and Creation
    class_cards = mo.hstack([render_class_card(Rechteck), render_class_card(Kreis)], justify="start")
    top_section = mo.hstack([class_cards, creation_panel], justify="start", align="start", gap=2)

    instance_layout = mo.hstack(object_cards, wrap=True, justify="start") if object_cards else mo.md("*Keine Objekte*")

    log_content = "\n".join(log_entries)
    log_view = mo.Html(f"""
    <div style="min-width: 220px; max-height: 200px; display: flex; flex-direction: column;">
        <b>Protokoll</b>
        <div style="background: #333; color: #0f0; font-family: monospace; padding: 8px; border-radius: 4px; overflow-y: auto; flex: 1; white-space: pre-wrap; font-size: 0.85em;">{log_content}</div>
    </div>""")

    playground_upper = mo.hstack([
        render_canvas(objects_for_display, selected_name),
        control_panel
    ], align="start", gap=2, widths=[2, 1])

    mo.vstack([
        mo.md("# 🏫 Interaktive Lernumgebung: Objektorientierte Modellierung"),
        intro_text,
        mo.md("### 1. Klassen (Baupläne)"),
        top_section,
        mo.md("### 2. Objekte (Instanzen)"),
        instance_layout,
        mo.md("---"),
        mo.md("### 3. Arbeitsfläche & Methoden"),
        playground_upper,
        log_view
    ], gap=1)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
